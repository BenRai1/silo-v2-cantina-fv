import "../setup/CompleteSiloSetup.spec";
import "./0base_Silo.spec";
import "../simplifications/_Oracle_call_before_quote_UNSAFE.spec";
import "../simplifications/Oracle_quote_one_UNSAFE.spec";
import "../simplifications/_flashloan_no_state_changes.spec";

//------------------------------- RULES TEST START ----------------------------------
    // maxDeposit():using the results from maxDeposit() to call deposit() should be possible (satisfy not revert)
    // maxMint():using the results from maxMint() to call mint() should be possible (satisfy not revert)
    // maxWithdraw():using the results from maxWithdraw() to call withdraw() should be possible (satisfy not revert)
    // maxRedeem():using the results from maxRedeem() to call redeem() should be possible (satisfy not revert)
    // maxWithdraw(protected):using the results from maxWithdraw(protected) to call withdraw(protected) should be possible (satisfy not revert)
    // maxRedeem(protected):using the results from maxRedeem(protected) to call redeem(protected) should be possible (satisfy not revert)
    // maxBorrow():using the results from maxBorrow() to call borrow() should be possible (satisfy not revert)
    // maxBorrowShares():using the results from maxBorrowShares() to call borrowShares() should be possible (satisfy not revert)
    // maxBorrowSameAsset():using the results from maxBorrowSameAsset() to call borrowSameAsset() should be possible (satisfy not revert)
    // maxRepay():using the results from maxRepay() to call repay() should be possible (satisfy not revert)
    // maxRepayShares():using the results from maxRepayShares() to call repayShares() should be possible (satisfy not revert)
    // maxFlashLoan():using the results from maxFlashLoan() to call flashLoan() should be possible (satisfy not revert)



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
