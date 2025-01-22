/* Rules concerning two silos  */

import "../setup/CompleteSiloSetup.spec";
import "./0base_Silo.spec";

//------------------------------- RULES TEST START ----------------------------------

//calls to silo0 do not change balances of silo1 tokens
rule callsToSilo0DoNotChangeBalancesOfSilo1Tokens(env e, method f, calldataarg args) filtered{f -> !f.isView} {
    configForEightTokensSetupRequirements();
    address user;

    //supply silo1 tokens before
    uint256 totalSupplyCollateralToken1Before = silo1.totalSupply();
    uint256 totalSupplyShareProtectedCollateralToken1Before = shareProtectedCollateralToken1.totalSupply();
    uint256 totalSupplyShareDebtToken1Before = shareDebtToken1.totalSupply();

    //balance of user for silo1 tokens before
    uint256 balanceUserCollateralToken1Before = silo1.balanceOf(user);
    uint256 balanceUserShareProtectedCollateralToken1Before = shareProtectedCollateralToken1.balanceOf(user);
    uint256 balanceUserShareDebtToken1Before = shareDebtToken1.balanceOf(user);

    //assets silo1 before

    uint256 collateralAssetsSilo1Before;
    uint256 protectedCollateralAssetsSilo1Before;
    uint256 debtAssetsSilo1Before;
    (protectedCollateralAssetsSilo1Before, collateralAssetsSilo1Before, debtAssetsSilo1Before) = silo1.totalAssetsHarness();

    //call randome function in silo0
    f(e, args);

    //supply silo1 tokens after
    uint256 totalSupplyCollateralToken1After = silo1.totalSupply();
    uint256 totalSupplyShareProtectedCollateralToken1After = shareProtectedCollateralToken1.totalSupply();
    uint256 totalSupplyShareDebtToken1After = shareDebtToken1.totalSupply();

    //balance of user for silo1 tokens after
    uint256 balanceUserCollateralToken1After = silo1.balanceOf(user);
    uint256 balanceUserShareProtectedCollateralToken1After = shareProtectedCollateralToken1.balanceOf(user);
    uint256 balanceUserShareDebtToken1After = shareDebtToken1.balanceOf(user);

    //assets silo1 after
    uint256 collateralAssetsSilo1After;
    uint256 protectedCollateralAssetsSilo1After;
    uint256 debtAssetsSilo1After;
    (protectedCollateralAssetsSilo1After, collateralAssetsSilo1After, debtAssetsSilo1After) = silo1.totalAssetsHarness();

    //total supplies did not change
    assert totalSupplyCollateralToken1Before == totalSupplyCollateralToken1After;
    assert totalSupplyShareProtectedCollateralToken1Before == totalSupplyShareProtectedCollateralToken1After;
    assert totalSupplyShareDebtToken1Before == totalSupplyShareDebtToken1After;

    //balances of user did not change
    assert balanceUserCollateralToken1Before == balanceUserCollateralToken1After;
    assert balanceUserShareProtectedCollateralToken1Before == balanceUserShareProtectedCollateralToken1After;
    assert balanceUserShareDebtToken1Before == balanceUserShareDebtToken1After;

    //assets did not change
    assert collateralAssetsSilo1Before == collateralAssetsSilo1After;
    assert protectedCollateralAssetsSilo1Before == protectedCollateralAssetsSilo1After;
    assert debtAssetsSilo1Before == debtAssetsSilo1After;
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

//-------------------------------OLD RULES START----------------------------------

//-------------------------------OLD RULES END----------------------------------
