/* Rules concerning deposit and mint  */

import "../setup/CompleteSiloSetup.spec";
import "./0base_Silo.spec";

//------------------------------- RULES TEST START ----------------------------------



// `borrow()` should decrease Silo balance by exactly `_assets`
rule borrowDecreasesSiloBalanceExactlyByAssets(env e) {
    configForEightTokensSetupRequirements();
    uint256 assets;
    address receiver;
    nonSceneAddressRequirements(receiver);
    address borrower;

    uint256 balanceToken0Before = token0.balanceOf(silo0);

    silo0.borrow(e, assets, receiver, borrower);

    uint256 balanceToken0After = token0.balanceOf(silo0);

    assert balanceToken0After == balanceToken0Before - assets;
}

//`borrow()` should increase balance of the receiver by assets
rule borrowIncreasesReceiverBalanceExactlyByAssets(env e) {
    configForEightTokensSetupRequirements();
    uint256 assets;
    address receiver;
    address borrower;
    nonSceneAddressRequirements(receiver);
    totalSuppliesMoreThanBalances(receiver, silo0);

    uint256 balanceReceiverBefore = token0.balanceOf(receiver);

    silo0.borrow(e, assets, receiver, borrower);

    uint256 balanceReceiverAfter = token0.balanceOf(receiver);

    assert balanceReceiverAfter == balanceReceiverBefore + assets;
}




//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
