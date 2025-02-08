// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {PartialLiquidation} from "silo-core/contracts/utils/hook-receivers/liquidation/PartialLiquidation.sol";
import {PartialLiquidationLib} from "silo-core/contracts/utils/hook-receivers/liquidation/lib/PartialLiquidationLib.sol";
import {PartialLiquidationExecLib} from "silo-core/contracts/utils/hook-receivers/liquidation/lib/PartialLiquidationExecLib.sol";
import {SiloSolvencyLib} from "silo-core/contracts/lib/SiloSolvencyLib.sol";
import {RevertLib} from "silo-core/contracts/lib/RevertLib.sol";
import {ISiloConfig} from "silo-core/contracts/interfaces/ISiloConfig.sol";
import {ISilo} from "silo-core/contracts/interfaces/ISilo.sol";
import {IERC20} from "openzeppelin5/interfaces/IERC20.sol";
import {SafeERC20} from "openzeppelin5/token/ERC20/utils/SafeERC20.sol";

import {IShareToken} from "silo-core/contracts/interfaces/IShareToken.sol";
import {IPartialLiquidation} from "silo-core/contracts/interfaces/IPartialLiquidation.sol";
import {IHookReceiver} from "silo-core/contracts/interfaces/IHookReceiver.sol";

import {SiloMathLib} from "silo-core/contracts/lib/SiloMathLib.sol";
import {Hook} from "silo-core/contracts/lib/Hook.sol";
import {Rounding} from "silo-core/contracts/lib/Rounding.sol";
import {CallBeforeQuoteLib} from "silo-core/contracts/lib/CallBeforeQuoteLib.sol";



contract PartialLiquidationHarness is PartialLiquidation {

    function estimateMaxRepayValueHarness(
        uint256 _totalBorrowerDebtValue, 
        uint256 _totalBorrowerCollateralValue,
        uint256 _ltvAfterLiquidation, //i: liquidationTargetLtv from collateralConfig
        uint256 _liquidationFee 
    ) external view returns (uint256) {
        return PartialLiquidationLib.estimateMaxRepayValue(_totalBorrowerDebtValue, _totalBorrowerCollateralValue, _ltvAfterLiquidation, _liquidationFee);
    }

    function valueToAssetsByRatioHarness(
        uint256 _value, //i: debtToRepay in USD
        uint256 _totalAssets, //i: _borrowerDebtValue in USD (TOTAL)
        uint256 _totalValue //i: _borrowerDebtAssets (TOTAL)
    ) external view returns (uint256) {
        return PartialLiquidationLib.valueToAssetsByRatio(_value, _totalAssets, _totalValue);
    }
   
    function calculateCollateralToLiquidateHarness(uint256 _maxDebtToCover, uint256 _sumOfCollateral, uint256 _liquidationFee) public pure returns (uint256 toLiquidate){
        return PartialLiquidationLib.calculateCollateralToLiquidate(_maxDebtToCover, _sumOfCollateral, _liquidationFee);
    }

    function liquidationPreviewHarness(
        uint256 _ltvBefore,
        uint256 _sumOfCollateralAssets,
        uint256 _sumOfCollateralValue,
        uint256 _borrowerDebtAssets,
        uint256 _borrowerDebtValue,
        PartialLiquidationLib.LiquidationPreviewParams memory _params
    )
    public
    pure
    returns (uint256 collateralToLiquidate, uint256 debtToRepay, uint256 ltvAfter){
        return PartialLiquidationLib.liquidationPreview(_ltvBefore, _sumOfCollateralAssets, _sumOfCollateralValue, _borrowerDebtAssets, _borrowerDebtValue, _params);
    }

    function calculateLtvAfterHarness(
        uint256 _sumOfCollateralValue,
        uint256 _totalDebtValue,
        uint256 _collateralValueToLiquidate,
        uint256 _debtValueToCover
    )
        public pure returns (uint256 ltvAfter)
    {
        if (_sumOfCollateralValue <= _collateralValueToLiquidate || _totalDebtValue <= _debtValueToCover) {
            return 0;
        }

        ltvAfter = (_totalDebtValue - _debtValueToCover) * 1e18;
        ltvAfter = ceilDiv(ltvAfter, _sumOfCollateralValue - _collateralValueToLiquidate);
    }

    function ceilDiv(uint256 a, uint256 b) internal pure returns (uint256) {
    require (b != 0);

    unchecked {
        return a == 0 ? 0 : (a - 1) / b + 1;
    }
    }

    function liquidationPreviewExecHarness(
        SiloSolvencyLib.LtvData memory _ltvData,
        PartialLiquidationLib.LiquidationPreviewParams memory _params
    )
        public
        view
        returns (uint256 collateralToLiquidate, uint256 debtToRepay, bytes4 customError)
    {
        return PartialLiquidationExecLib.liquidationPreview(_ltvData, _params);
    }

    function splitReceiveCollateralToLiquidateHarness(uint256 _collateralToLiquidate, uint256 _borrowerProtectedAssets) public pure
    returns (uint256 withdrawAssetsFromCollateral, uint256 withdrawAssetsFromProtected){
        return PartialLiquidationLib.splitReceiveCollateralToLiquidate(_collateralToLiquidate, _borrowerProtectedAssets);
    }

    function _fetchConfigsHarness(
        ISiloConfig _siloConfigCached,
        address _collateralAsset,
        address _debtAsset,
        address _borrower
    )
        public
        virtual
    returns (
        ISiloConfig.ConfigData memory collateralConfig,
        ISiloConfig.ConfigData memory debtConfig
    ){
        return _fetchConfigs(_siloConfigCached, _collateralAsset, _debtAsset, _borrower);
    }

    function _callShareTokenForwardTransferNoChecksHarness(
        address _silo,
        address _borrower,
        address _receiver,
        uint256 _withdrawAssets,
        address _shareToken,
        ISilo.AssetType _assetType
    ) public virtual returns (uint256 shares) {
        return _callShareTokenForwardTransferNoChecks(_silo, _borrower, _receiver, _withdrawAssets, _shareToken, _assetType);
    }

    function getExactLiquidationAmountsHarness(
        ISiloConfig.ConfigData memory _collateralConfig,
        ISiloConfig.ConfigData memory _debtConfig, address _user,
        uint256 _maxDebtToCover,
        uint256 _liquidationFee
    )
        external
        view
        returns (
            uint256 withdrawAssetsFromCollateral,
            uint256 withdrawAssetsFromProtected,
            uint256 repayDebtAssets,
            bytes4 customError
        )
    {
        return PartialLiquidationExecLib.getExactLiquidationAmounts(_collateralConfig, _debtConfig, _user, _maxDebtToCover, _liquidationFee);
    }


     function liquidationCall( // solhint-disable-line function-max-lines, code-complexity
        address _collateralAsset,
        address _debtAsset,
        address _borrower,
        uint256 _maxDebtToCover,
        bool _receiveSToken,
        bool _repayBadDebt
    )
        external
        virtual
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        ISiloConfig siloConfigCached = siloConfig;

        require(address(siloConfigCached) != address(0), EmptySiloConfig());
        require(_maxDebtToCover != 0, NoDebtToCover());

        siloConfigCached.turnOnReentrancyProtection();

        (
            ISiloConfig.ConfigData memory collateralConfig,
            ISiloConfig.ConfigData memory debtConfig
        ) = _fetchConfigs(siloConfigCached, _collateralAsset, _debtAsset, _borrower);

        LiquidationCallParams memory params;

        (
            params.withdrawAssetsFromCollateral, params.withdrawAssetsFromProtected, repayDebtAssets, params.customError
        ) = PartialLiquidationExecLib.getExactLiquidationAmounts(
            collateralConfig,
            debtConfig,
            _borrower,
            _maxDebtToCover,
            collateralConfig.liquidationFee
        );

        RevertLib.revertIfError(params.customError);

        // revert if no bad debt should be payed
        if (!_repayBadDebt) {
            require(params.withdrawAssetsFromCollateral + params.withdrawAssetsFromProtected > 0, "Bad Debt");
        }
        // we do not allow dust so full liquidation is required //i: can not be used to prevent liquidations because total repay is always possible
        require(repayDebtAssets <= _maxDebtToCover, FullLiquidationRequired());

        IERC20(debtConfig.token).safeTransferFrom(msg.sender, address(this), repayDebtAssets); //i: debt token used both times, becasue first is moving it to this contract, 2nd: increase allowance for the silo to be able to call repay
        IERC20(debtConfig.token).safeIncreaseAllowance(debtConfig.silo, repayDebtAssets);

        address shareTokenReceiver = _receiveSToken ? msg.sender : address(this);

        params.collateralShares = _callShareTokenForwardTransferNoChecks(
            collateralConfig.silo,
            _borrower,
            shareTokenReceiver,
            params.withdrawAssetsFromCollateral,
            collateralConfig.collateralShareToken,
            ISilo.AssetType.Collateral
        );

        params.protectedShares = _callShareTokenForwardTransferNoChecks(
            collateralConfig.silo,
            _borrower,
            shareTokenReceiver,
            params.withdrawAssetsFromProtected,
            collateralConfig.protectedShareToken,
            ISilo.AssetType.Protected
        );

        siloConfigCached.turnOffReentrancyProtection();

        ISilo(debtConfig.silo).repay(repayDebtAssets, _borrower);

        if (_receiveSToken) {
            if (params.collateralShares != 0) {
                withdrawCollateral = ISilo(collateralConfig.silo).previewRedeem(
                    params.collateralShares,
                    ISilo.CollateralType.Collateral
                );
            }

            if (params.protectedShares != 0) {
                unchecked {
                    // protected and collateral values were split from total collateral to withdraw,
                    // so we will not overflow when we sum them back, especially that on redeem, we rounding down
                    withdrawCollateral += ISilo(collateralConfig.silo).previewRedeem(
                        params.protectedShares,
                        ISilo.CollateralType.Protected
                    );
                }
            }
        } else {
            // in case of liquidation redeem, hook transfers sTokens to itself and it has no debt
            // so solvency will not be checked in silo on redeem action

            // if share token offset is more than 0, positive number of shares can generate 0 assets
            // so there is a need to check assets before we withdraw collateral/protected

            if (params.collateralShares != 0) {
                withdrawCollateral = ISilo(collateralConfig.silo).redeem({
                    _shares: params.collateralShares,
                    _receiver: msg.sender,
                    _owner: address(this),
                    _collateralType: ISilo.CollateralType.Collateral
                });
            }

            if (params.protectedShares != 0) {
                unchecked {
                    // protected and collateral values were split from total collateral to withdraw,
                    // so we will not overflow when we sum them back, especially that on redeem, we rounding down
                    withdrawCollateral += ISilo(collateralConfig.silo).redeem({
                        _shares: params.protectedShares,
                        _receiver: msg.sender,
                        _owner: address(this),
                        _collateralType: ISilo.CollateralType.Protected
                    });
                }
            }
        }

        emit LiquidationCall(
            msg.sender,
            debtConfig.silo,
            _borrower,
            repayDebtAssets,
            withdrawCollateral,
            _receiveSToken
        );
    }




    



}