/* Rules concerning withdraw and redeem  */

import "../setup/CompleteSiloSetup.spec";
import "./0base_Silo.spec";
import "../simplifications/Silo_noAccrueInterest_simplification_UNSAFE.spec";
import "../simplifications/_Oracle_call_before_quote_UNSAFE.spec";


//------------------------------- RULES TEST START ----------------------------------

    // withdraw() does not change any shares for other user or receiver
    rule withdrawDoesNotChangeSharesOfOthers(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;
        address otherUser;
        require(owner != otherUser);
        require(owner != receiver);

        //shares of other user and receiver before withdraw
        uint256 debtSharesOtherUserBefore = shareDebtToken0.balanceOf(otherUser);
        uint256 collateralSharesOtherUserBefore = silo0.balanceOf(otherUser);
        uint256 protectedSharesOtherUserBefore = shareProtectedCollateralToken0.balanceOf(otherUser);
        uint256 debtSharesReceiverBefore = shareDebtToken0.balanceOf(receiver);
        uint256 collateralSharesReceiverBefore = silo0.balanceOf(receiver);
        uint256 protectedSharesReceiverBefore = shareProtectedCollateralToken0.balanceOf(receiver);

        //withdraw
        withdraw(e, assets, receiver, owner);

        //shares of other user and receiver after withdraw
        uint256 debtSharesOtherUserAfter = shareDebtToken0.balanceOf(otherUser);
        uint256 collateralSharesOtherUserAfter = silo0.balanceOf(otherUser);
        uint256 protectedSharesOtherUserAfter = shareProtectedCollateralToken0.balanceOf(otherUser);
        uint256 debtSharesReceiverAfter = shareDebtToken0.balanceOf(receiver);
        uint256 collateralSharesReceiverAfter = silo0.balanceOf(receiver);
        uint256 protectedSharesReceiverAfter = shareProtectedCollateralToken0.balanceOf(receiver);

        //shares of other user and receiver did not change
        assert debtSharesOtherUserBefore == debtSharesOtherUserAfter;
        assert collateralSharesOtherUserBefore == collateralSharesOtherUserAfter;
        assert protectedSharesOtherUserBefore == protectedSharesOtherUserAfter;
        assert debtSharesReceiverBefore == debtSharesReceiverAfter;
        assert collateralSharesReceiverBefore == collateralSharesReceiverAfter;
        assert protectedSharesReceiverBefore == protectedSharesReceiverAfter;
    }

    // withdraw() does not change totalSupply or balance for borrower for debt and protectedCollateral shares
    rule withdrawDoesNotChangeDebtOrProtectedShares(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //totalSupply and balance of owner before withdraw
        uint256 debtSharesTotalBalanceBefore = shareDebtToken0.totalSupply();
        uint256 protectedSharesTotalBalanceBefore = shareProtectedCollateralToken0.totalSupply();
        uint256 debtSharesBalanceOwnerBefore = shareDebtToken0.balanceOf(owner);
        uint256 protectedSharesBalanceOwnerBefore = shareProtectedCollateralToken0.balanceOf(owner);

        //withdraw
        withdraw(e, assets, receiver, owner);

        //totalSupply and balance of owner after withdraw
        uint256 debtSharesTotalBalanceAfter = shareDebtToken0.totalSupply();
        uint256 protectedSharesTotalBalanceAfter = shareProtectedCollateralToken0.totalSupply();
        uint256 debtSharesBalanceOwnerAfter = shareDebtToken0.balanceOf(owner);
        uint256 protectedSharesBalanceOwnerAfter = shareProtectedCollateralToken0.balanceOf(owner);

        //totalSupply and balance of owner did not change
        assert debtSharesTotalBalanceBefore == debtSharesTotalBalanceAfter;
        assert protectedSharesTotalBalanceBefore == protectedSharesTotalBalanceAfter;
        assert debtSharesBalanceOwnerBefore == debtSharesBalanceOwnerAfter;
        assert protectedSharesBalanceOwnerBefore == protectedSharesBalanceOwnerAfter;
    }

    // withdraw() always decreases collateralShares for owner
    rule withdrawDecreasesCollateralSharesForOwner(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //collateralShares of owner before withdraw
        uint256 collateralSharesBalanceOwnerBefore = silo0.balanceOf(owner);

        //withdraw
        withdraw(e, assets, receiver, owner);

        //collateralShares of owner after withdraw
        uint256 collateralSharesBalanceOwnerAfter = silo0.balanceOf(owner);

        //collateralShares of owner decreased
        assert collateralSharesBalanceOwnerBefore > collateralSharesBalanceOwnerAfter;
    }


    // withdraw() decreases totalSupply of collateral shares by dif for owner
    rule withdrawReducesTotalSupplyOfCollateralShares(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //totalSupply of collateral shares before withdraw
        uint256 collateralSharesTotalSupplyBefore = silo0.totalSupply();
        uint256 collateralSharesBalanceOwnerBefore = silo0.balanceOf(owner);
        require(collateralSharesTotalSupplyBefore >= collateralSharesBalanceOwnerBefore);

        //withdraw
        uint256 burnedShares = withdraw(e, assets, receiver, owner);

        //totalSupply of collateral shares after withdraw
        uint256 collateralSharesTotalSupplyAfter = silo0.totalSupply();
        uint256 collateralSharesBalanceOwnerAfter = silo0.balanceOf(owner);

        //totalSupply of collateral shares decreased by dif
        assert collateralSharesTotalSupplyBefore == collateralSharesTotalSupplyAfter + collateralSharesBalanceOwnerAfter - collateralSharesBalanceOwnerBefore;
    }

    // withdraw() increases underlyingToken for receiver by assets, decreases the balance of silo accordingly and does not change for owner or receiver
    rule withdrawIncreasesUnderlyingTokenForReceiver(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        nonSceneAddressRequirements(receiver);
        address owner;
        nonSceneAddressRequirements(owner);
        address otherUser;
        nonSceneAddressRequirements(otherUser);
        require(owner != receiver);
        require(otherUser != receiver);

        //underlyingToken balances before 
        uint256 underlyingTokenBalanceReceiverBefore = token0.balanceOf(receiver);
        uint256 underlyingTokenBalanceOwnerBefore = token0.balanceOf(owner);
        uint256 underlyingTokenBalanceOtherUserBefore = token0.balanceOf(otherUser);
        uint256 underlyingTokenBalanceSiloBefore = token0.balanceOf(silo0);

        //withdraw
        withdraw(e, assets, receiver, owner);

        //underlyingToken balances after
        uint256 underlyingTokenBalanceReceiverAfter = token0.balanceOf(receiver);
        uint256 underlyingTokenBalanceOwnerAfter = token0.balanceOf(owner);
        uint256 underlyingTokenBalanceOtherUserAfter = token0.balanceOf(otherUser);
        uint256 underlyingTokenBalanceSiloAfter = token0.balanceOf(silo0);

        //underlyingToken of receiver increased by assets
        assert underlyingTokenBalanceReceiverAfter == underlyingTokenBalanceReceiverBefore + assets;
        //underlyingToken of owner did not change
        assert underlyingTokenBalanceOwnerBefore == underlyingTokenBalanceOwnerAfter;
        //underlyingToken of other user did not change
        assert underlyingTokenBalanceOtherUserBefore == underlyingTokenBalanceOtherUserAfter;
        //underlyingToken of silo decreased by assets
        assert underlyingTokenBalanceSiloAfter == underlyingTokenBalanceSiloBefore - assets;
    }

    // withdraw() decreases collateralAssets by assets, debtAssets and protectedCollateralAssets stay the same
    rule withdrawDecreasesCollateralAssets(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        // assets before withdraw
        uint256 collateralAssetsBefore;
        uint256 protectedCollateralAssetsBefore;
        uint256 debtAssetsBefore;
        (protectedCollateralAssetsBefore, collateralAssetsBefore, debtAssetsBefore) = silo0.totalAssetsHarness(e);

        //withdraw
        withdraw(e, assets, receiver, owner);

        // assets after withdraw
        uint256 collateralAssetsAfter;
        uint256 protectedCollateralAssetsAfter;
        uint256 debtAssetsAfter;
        (protectedCollateralAssetsAfter, collateralAssetsAfter, debtAssetsAfter) = silo0.totalAssetsHarness(e);

        //collateralAssets decreased by assets
        assert collateralAssetsAfter == collateralAssetsBefore - assets;
        //protectedCollateralAssets did not change
        assert protectedCollateralAssetsBefore == protectedCollateralAssetsAfter;
        //debtAssets did not change
        assert debtAssetsBefore == debtAssetsAfter;
    }

    // withdraw() is the same as withdraw(collateralAssets)
    rule withdrawIsTheSameAsWithdrawCollateralAssets(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        storage init = lastStorage;
        
        //withdraw
        withdraw(e, assets, receiver, owner);

        storage afterWithdraw = lastStorage;

        withdraw(e, assets, receiver, owner, ISilo.CollateralType.Collateral) at init;

        storage afterWithdrawCollateral = lastStorage;

        assert afterWithdraw == afterWithdrawCollateral;
    }

    // withdraw() can not withdraw more than liquidity
    rule withdrawCanNotWithdrawMoreThanLiquidity(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        uint256 liquidity = silo0.getLiquidity();

        //withdraw
        withdraw@withRevert(e, assets, receiver, owner);

        //reverted if assest > liquidity
        assert assets > liquidity => lastReverted;
    }

    // withdraw() after call, owner is solvent
    rule withdrawOwnerIsSolventAfterCall(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //withdraw
        withdraw(e, assets, receiver, owner);

        //owner is solvent
        assert silo0.isSolvent(owner);
    }

    // withdraw() and redeem can only be called by owner or allowance
    rule onlyUserOrAllowanceCanRedeemOrWithdrawShares(env e, method f, calldataarg args) filtered{f-> 
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector        
    } {
        address amountAsset;
        address owner;
        uint256 allowanceMsgSender = silo0.allowance(e, owner, e.msg.sender);
        uint256 sharesBefore = silo0.balanceOf(owner);        

        f(e, args);

        uint256 sharesAfter = silo0.balanceOf(owner);
        mathint redeemedShares = sharesBefore - sharesAfter;

        assert(sharesBefore != sharesAfter => e.msg.sender == owner || allowanceMsgSender >= redeemedShares);
    }

    // withdraw( protected) does not change any shares for other user or receiver
    rule withdrawProtectedDoesNotChangeSharesOfOthers(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;
        address otherUser;
        require(owner != otherUser);
        require(owner != receiver);

        //shares of other user and receiver before withdraw
        uint256 debtSharesOtherUserBefore = shareDebtToken0.balanceOf(otherUser);
        uint256 collateralSharesOtherUserBefore = silo0.balanceOf(otherUser);
        uint256 protectedSharesOtherUserBefore = shareProtectedCollateralToken0.balanceOf(otherUser);
        uint256 debtSharesReceiverBefore = shareDebtToken0.balanceOf(receiver);
        uint256 collateralSharesReceiverBefore = silo0.balanceOf(receiver);
        uint256 protectedSharesReceiverBefore = shareProtectedCollateralToken0.balanceOf(receiver);

        //withdraw
        withdraw(e, assets, receiver, owner, ISilo.CollateralType.Protected);

        //shares of other user and receiver after withdraw
        uint256 debtSharesOtherUserAfter = shareDebtToken0.balanceOf(otherUser);
        uint256 collateralSharesOtherUserAfter = silo0.balanceOf(otherUser);
        uint256 protectedSharesOtherUserAfter = shareProtectedCollateralToken0.balanceOf(otherUser);
        uint256 debtSharesReceiverAfter = shareDebtToken0.balanceOf(receiver);
        uint256 collateralSharesReceiverAfter = silo0.balanceOf(receiver);
        uint256 protectedSharesReceiverAfter = shareProtectedCollateralToken0.balanceOf(receiver);

        //shares of other user and receiver did not change
        assert debtSharesOtherUserBefore == debtSharesOtherUserAfter;
        assert collateralSharesOtherUserBefore == collateralSharesOtherUserAfter;
        assert protectedSharesOtherUserBefore == protectedSharesOtherUserAfter;
        assert debtSharesReceiverBefore == debtSharesReceiverAfter;
        assert collateralSharesReceiverBefore == collateralSharesReceiverAfter;
        assert protectedSharesReceiverBefore == protectedSharesReceiverAfter;
    }

    // withdraw( protected) does not change totalSupply or balance for borrower for debt and Collateral shares
    rule withdrawDoesNotChangeDebtOrCollateralShares(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //totalSupply and balance of owner before withdraw
        uint256 debtSharesTotalBalanceBefore = shareDebtToken0.totalSupply();
        uint256 collateralSharesTotalBalanceBefore = silo0.totalSupply();
        uint256 debtSharesBalanceOwnerBefore = shareDebtToken0.balanceOf(owner);
        uint256 collateralSharesBalanceOwnerBefore = silo0.balanceOf(owner);

        //withdraw
        withdraw(e, assets, receiver, owner);

        //totalSupply and balance of owner after withdraw
        uint256 debtSharesTotalBalanceAfter = shareDebtToken0.totalSupply();
        uint256 collateralSharesTotalBalanceAfter = silo0.totalSupply();
        uint256 debtSharesBalanceOwnerAfter = shareDebtToken0.balanceOf(owner);
        uint256 collateralSharesBalanceOwnerAfter = silo0.balanceOf(owner);

        //totalSupply and balance of owner did not change
        assert debtSharesTotalBalanceBefore == debtSharesTotalBalanceAfter;
        assert collateralSharesTotalBalanceBefore == collateralSharesTotalBalanceAfter;
        assert debtSharesBalanceOwnerBefore == debtSharesBalanceOwnerAfter;
        assert collateralSharesBalanceOwnerBefore == collateralSharesBalanceOwnerAfter;
    }

    // withdraw( protected) decreases totalSupply of protected shares by dif for owner
    rule withdrawReducesTotalSupplyOfProtectedShares(env e){
        configForEightTokensSetupRequirements();
        uint256 assets;
        address receiver;
        address owner;

        //totalSupply of protected shares before withdraw
        uint256 protectedSharesTotalSupplyBefore = shareProtectedCollateralToken0.totalSupply();
        uint256 protectedSharesBalanceOwnerBefore = shareProtectedCollateralToken0.balanceOf(owner);
        require(protectedSharesTotalSupplyBefore >= protectedSharesBalanceOwnerBefore);

        //withdraw
        withdraw(e, assets, receiver, owner, ISilo.CollateralType.Protected);

        //totalSupply of protected shares after withdraw
        uint256 protectedSharesTotalSupplyAfter = shareProtectedCollateralToken0.totalSupply();
        uint256 protectedSharesBalanceOwnerAfter = shareProtectedCollateralToken0.balanceOf(owner);

        //totalSupply of protected shares decreased by dif
        assert protectedSharesTotalSupplyBefore == protectedSharesTotalSupplyAfter + protectedSharesBalanceOwnerAfter - protectedSharesBalanceOwnerBefore;
    }

    // withdraw( protected) always decreases protectedShares for owner
    // withdraw( protected) increases underlyingToken for receiver by assets, decreases the balance of silo accordingly and does not change for owner or receiver
    // withdraw( protected) decreases protectedAssets by assets, debtAssets and CollateralAssets stay the same
    // withdraw( protected) should never revert because of to little liquidity
    // withdraw( protected) after call, owner is solvent
    // withdraw( protected) with other type then protected or collateral reverts
    // * `withdraw()` should never revert if liquidity for a user and a silo is sufficient even if oracle reverts
    // * result of `maxWithdraw()` should never be more than liquidity of the Silo
    // * result of `maxWithdraw()` used as input to withdraw() should never revert
    // * if user has no debt and liquidity is available, shareToken.balanceOf(user) used as input to redeem(), assets from redeem() should be equal to maxWithdraw()
    // * result of `previewWithdraw()` should be equal to result of `withdraw()`





//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

//-------------------------------OLD RULES START----------------------------------

//-------------------------------OLD RULES END----------------------------------
