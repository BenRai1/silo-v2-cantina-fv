// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "openzeppelin5/token/ERC20/IERC20.sol";

import {ISilo} from "silo-core/contracts/interfaces/ISilo.sol";
import {ISiloConfig} from "silo-core/contracts/interfaces/ISiloConfig.sol";
import {IPartialLiquidation} from "silo-core/contracts/interfaces/IPartialLiquidation.sol";
import {SiloLensLib} from "silo-core/contracts/lib/SiloLensLib.sol";
import {MintableToken} from "../../_common/MintableToken.sol";
import {SiloLittleHelper} from "../../_common/SiloLittleHelper.sol";
import {SiloConfigOverride} from "../../_common/fixtures/SiloFixture.sol";
import {SiloFixtureWithVeSilo as SiloFixture} from "../../_common/fixtures/SiloFixtureWithVeSilo.sol";

contract RawLiquidityAndProtectedCollateralTest is SiloLittleHelper, Test {
    using SiloLensLib for ISilo;

    ISiloConfig internal _siloConfig;

    function setUp() public {
        SiloFixture siloFixture = new SiloFixture();
        SiloConfigOverride memory configOverride;

        token0 = new MintableToken(18);
        token1 = new MintableToken(18);

        configOverride.token0 = address(token0);
        configOverride.token1 = address(token1);

        address hook;
        (_siloConfig, silo0, silo1,,, hook) = siloFixture.deploy_local(configOverride);
        partialLiquidation = IPartialLiquidation(hook);
    }


//--------------------- OWN TESTS START-----------------------

   // FOUNDRY_PROFILE=core-test forge test -vvv --ffi --mt testLiquidatingBadDebtIssue
    function testLiquidatingBadDebtIssue() public { 

        address borrower = makeAddr("borrower");
        address lpProvider = makeAddr("lpProvider");
        address liquidator1 = makeAddr("liquidator1");
        address liquidator2 = makeAddr("liquidator2");

        uint256 depositAmount = 1000;

        //deposit 1000 for borrower in silo0
        _deposit(silo0, token0, borrower, depositAmount, ISilo.CollateralType.Collateral);

        //deposit 1000 for lpProvider in silo1
        _deposit(silo1, token1, lpProvider, depositAmount, ISilo.CollateralType.Collateral);

        vm.warp(block.timestamp + 30 days);

        //borrow 750 from silo1
        uint256 borrowAmount = 750; // maxLtv = 75%

        //borrower borrows 750 from silo1
        vm.prank(borrower);
        silo1.borrow(borrowAmount, borrower, borrower);

        vm.warp(block.timestamp + 365 days);
        silo0.accrueInterest();

        //liquidator1: setup for liquidation
        token1.mint(liquidator1, depositAmount); 
        vm.prank(liquidator1);
        token1.approve(address(partialLiquidation), depositAmount);

        //liquidator2: setup for liquidation
        token1.mint(liquidator2, depositAmount);
        vm.prank(liquidator2);
        token1.approve(address(partialLiquidation), depositAmount);

        //values liquidator2 before liquidation
        uint256 debtAssetsLiquidator2Before = token1.balanceOf(liquidator2);
        uint256 collateralAssetsLiquidator2Before = token0.balanceOf(liquidator2);
        emit log ("\nBalances liquidator2 before liquidation");
        emit log_named_uint("debtAssetsLiquidator2Before", debtAssetsLiquidator2Before);
        emit log_named_uint("collateralAssetsLiquidator2Before", collateralAssetsLiquidator2Before);

        
        //liquidator1: liquidate the borrower for all his assets
        vm.prank(liquidator1);
        partialLiquidation.liquidationCall(
            address(token0), address(token1), borrower, depositAmount, false /* receive share tokens */
        );


        //liquidator2: make a second call to liquidate the borrower (_receiveShareTokens = false)
        vm.prank(liquidator2);
        partialLiquidation.liquidationCall(
            address(token0), address(token1), borrower, depositAmount, false /* receive share tokens */
        );

        //values after liquidation
        uint256 debtAssetsLiquidator2After = token1.balanceOf(liquidator2);
        uint256 collateralAssetsLiquidator2After = token0.balanceOf(liquidator2);
        emit log ("\nBalances liquidator2 after liquidation");
        emit log_named_uint("debtAssetsLiquidator2After", debtAssetsLiquidator2After);
        emit log_named_uint("collateralAssetsLiquidator2After", collateralAssetsLiquidator2After);

        //assert for liquidator2: the debtAsset is reduced but the collateralAsset is not increased
        assertEq(collateralAssetsLiquidator2Before, collateralAssetsLiquidator2After, "collateralAssetsLiquidator2Before == collateralAssetsLiquidator2After");
        assertLt(debtAssetsLiquidator2After, debtAssetsLiquidator2Before , "debtAssetsLiquidator2After < debtAssetsLiquidator2Before");
    }


    // FOUNDRY_PROFILE=core-test forge test -vvv --ffi --mt testDoesNotPreventDust
    function testDoesNotPreventDust() public { 
        uint256 dust = 0.9 * 10**18; // 0.9 value

        address borrower = makeAddr("borrower");

        uint256 depositAmount = 1 * 10**18;

        //deposit 1 for borrower in silo0
        _deposit(silo0, token0, borrower, depositAmount, ISilo.CollateralType.Collateral);

        //deposit 1 in silo1
        _deposit(silo1, token1, address(this), depositAmount, ISilo.CollateralType.Collateral);

        vm.warp(block.timestamp + 30 days);

        //borrow 0,750 from silo1
        uint256 borrowAmount = 0.750 * 10** 18; // maxLtv = 75%

        //borrower borrows 0.750 from silo1
        vm.prank(borrower);
        silo1.borrow(borrowAmount, borrower, borrower);

        _printSiloStats("\nValues after borrow 750 (Silo0)", silo0, token0);


        vm.warp(block.timestamp + 131 days);
        silo0.accrueInterest();

        //debtAssets of borrower before liquidation
        _printSiloStats("\nValues after accrue interest(Silo0)", silo0, token0);
        (address protectedShareToken, address collateralShareToken, address debtShareToken) = _siloConfig.getShareTokens(address(silo1));
        uint256 debtSharesBorrowerBefore = IERC20(debtShareToken).balanceOf(borrower);
        uint256 debtAssetsBorrowerBefore = silo1.convertToAssets(debtSharesBorrowerBefore, ISilo.AssetType.Debt);

        // setup for liquidation
        token1.mint(address(this), debtAssetsBorrowerBefore); //(address(this) is the liquidator)
        token1.approve(address(partialLiquidation), debtAssetsBorrowerBefore);

        uint256 assetsToLiquidate = 890 * debtAssetsBorrowerBefore / 1000; // 89% of the debt
        
        //liquidate 89% of the borrower´s debt
        partialLiquidation.liquidationCall(
            address(token0), address(token1), borrower, assetsToLiquidate, false /* receive share tokens */
        );

        //debtAssets of borrower after liquidation
        _printSiloStats("\nValues after liquidation 89% of the debt (Silo0)", silo0, token0);
        uint256 debtSharesBorrowerAfter = IERC20(debtShareToken).balanceOf(borrower);
        uint256 debtAssetsBorrowerAfter = silo1.convertToAssets(debtSharesBorrowerAfter, ISilo.AssetType.Debt);
        emit log("dust");
        emit log_named_uint("",dust);
        emit log("debtAssetsBorrowerAfter:");
        emit log_named_uint("",debtAssetsBorrowerAfter);
        assertLt(debtAssetsBorrowerAfter, dust, "debtAssetsBorrower < dust");
    }

    // FOUNDRY_PROFILE=core-test forge test -vvv --ffi --mt testPreventsValidLiquidation
    function testPreventsValidLiquidation() public { 
        uint256 dust = 0.9 * 10**18; // 0.9 value

        address borrower = makeAddr("borrower");

        uint256 depositAmount = 1000 * 10**18;

        //deposit 1000 for borrower in silo0
        _deposit(silo0, token0, borrower, depositAmount, ISilo.CollateralType.Collateral);

        //deposit 1000 in silo1
        _deposit(silo1, token1, address(this), depositAmount, ISilo.CollateralType.Collateral);

        vm.warp(block.timestamp + 30 days);

        //borrow 750 from silo1
        uint256 borrowAmount = 750 * 10** 18; // maxLtv = 75%

        //borrower borrows 750 from silo1
        vm.prank(borrower);
        silo1.borrow(borrowAmount, borrower, borrower);

        _printSiloStats("\nValues after borrow 750 (Silo0)", silo0, token0);


        vm.warp(block.timestamp + 39 days);
        silo0.accrueInterest();
     
        // debtAssets of borrower before liquidation
        _printSiloStats("\nValues after accrue interest(Silo0)", silo0, token0);
        (, , address debtShareToken) = _siloConfig.getShareTokens(address(silo1));
        uint256 debtSharesBorrowerBefore = IERC20(debtShareToken).balanceOf(borrower);
        uint256 debtAssetsBorrowerBefore = silo1.convertToAssets(debtSharesBorrowerBefore, ISilo.AssetType.Debt);
        emit log_named_uint("debtAssetsBorrowerBefore (in 1e17)",debtAssetsBorrowerBefore/1e17);

        //liquidator1: setup for liquidation
        token1.mint(address(this), debtAssetsBorrowerBefore); //(address(this) is the liquidator)
        token1.approve(address(partialLiquidation), debtAssetsBorrowerBefore);

        uint256 assetsToLiquidate = 910 * debtAssetsBorrowerBefore / 1000; // 91% of the debt
        emit log_named_uint("assetsToLiquidate (in 1e17)",assetsToLiquidate/1e17);
        
        //try to liquidate 95% of the borrower´s debt
        vm.expectRevert();
        partialLiquidation.liquidationCall(
            address(token0), address(token1), borrower, assetsToLiquidate, false /* receive share tokens */
        );

        //potential debtAssets of borrower after liquidation
        uint256 potentialDebtAssetsBorrowerAfter = debtAssetsBorrowerBefore - assetsToLiquidate;
        emit log_named_uint("dust (in 1e17)",dust/1e17);
        emit log_named_uint("Potential DebtAssetsBorrower after liquidation (in 1e17)",potentialDebtAssetsBorrowerAfter/1e17);
        assertGt(potentialDebtAssetsBorrowerAfter, dust, "potentialDebtAssetsBorrowerAfter > dust");
    }




//---------------------- OWN TEST END ------------------




    // FOUNDRY_PROFILE=core-test forge test -vvv --ffi --mt testLiquidityAndProtectedAssets
    function testLiquidityAndProtectedAssets() public {
        address user0 = makeAddr("user0");
        address user1 = makeAddr("user1");
        address depositorProtected = makeAddr("depositProtected");

        uint256 depositAmount = 1000;

        _deposit(silo0, token0, user0, depositAmount, ISilo.CollateralType.Collateral);
        _printSiloStats("\nStep1 deposit collateral 1000 (Silo0)", silo0, token0);

        // for borrow
        _deposit(silo1, token1, user1, depositAmount, ISilo.CollateralType.Collateral);

        vm.warp(block.timestamp + 30 days);

        uint256 borrowAmount = 750; // maxLtv = 75%
        vm.prank(user1);
        silo0.borrow(borrowAmount, user1, user1);
        _printSiloStats("\nStep2 borrow 750 (Silo0)", silo0, token0);

        vm.prank(user0);
        silo1.borrow(borrowAmount, user0, user0);

        vm.warp(block.timestamp + 30 days);

        _deposit(silo0, token0, depositorProtected, depositAmount, ISilo.CollateralType.Protected);
        _printSiloStats("\nStep3 deposit protected 1000 (Silo0)", silo0, token0);

        vm.warp(block.timestamp + 365 days);
        silo0.accrueInterest();
        _printSiloStats("\nStep4 accrueInterest in 365 days (Silo0)", silo0, token0);

        silo0.withdrawFees();
        _printSiloStats("\nStep5 withdraw fees (Silo0)", silo0, token0);

        // liquidation
        (uint256 collateralToLiquidate, uint256 debtToRepay, bool sTokenRequired) = partialLiquidation.maxLiquidation(user0);

        assertGt(collateralToLiquidate, 0, "expect collateralToLiquidate");
        assertTrue(sTokenRequired, "sTokenRequired required because NotEnoughLiquidity");

        token1.mint(address(this), debtToRepay); // address(this) is liquidator
        token1.approve(address(partialLiquidation), debtToRepay);

        vm.expectRevert(ISilo.NotEnoughLiquidity.selector);
        partialLiquidation.liquidationCall(
            address(token0), address(token1), user0, debtToRepay, false /* receive share tokens */
        );

        // If there is not liquidity in the silo, the liquidator can receive share tokens

        (,address collateralShareToken,) = _siloConfig.getShareTokens(address(silo0));

        assertEq(IERC20(collateralShareToken).balanceOf(address(this)), 0, "expect 0 balance");

        partialLiquidation.liquidationCall(
            address(token0), address(token1), user0, debtToRepay, true /* receive share tokens */
        );

        assertGt(IERC20(collateralShareToken).balanceOf(address(this)), 0, "expect balance");
    }

    function _printSiloStats(string memory _step, ISilo _silo, MintableToken _token) internal {
        emit log(_step);

        (uint256 collateralAssets, uint256 protectedAssets) = _silo.getCollateralAndProtectedTotalsStorage();
        uint256 debtAssets = _silo.getDebtAssets();
        (uint192 daoAndDeployerRevenue,,,,) = _silo.getSiloStorage();
        uint256 liquidity = _silo.getRawLiquidity();

        emit log_named_uint("collateralAssets", collateralAssets);
        emit log_named_uint("protectedAssets", protectedAssets);
        emit log_named_uint("debtAssets", debtAssets);
        emit log_named_uint("daoAndDeployerRevenue", daoAndDeployerRevenue);
        emit log_named_uint("liquidity", liquidity);
        emit log_named_uint("silo balance", _token.balanceOf(address(_silo)));
    }

    function _deposit(
        ISilo _silo,
        MintableToken _token,
        address _depositorAddr,
        uint256 _amount,
        ISilo.CollateralType _collateralType
    ) internal {
        _token.mint(_depositorAddr, _amount);

        vm.prank(_depositorAddr);
        _token.approve(address(_silo), _amount);

        vm.prank(_depositorAddr);
        _silo.deposit(_amount, _depositorAddr, _collateralType);
    }
}
