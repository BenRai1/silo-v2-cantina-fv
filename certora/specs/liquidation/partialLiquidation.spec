import "../setup/CompleteSiloSetup.spec";
import "../silo/unresolved.spec";
import "../simplifications/Oracle_quote_one_UNSAFE.spec";
import "../simplifications/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
import "../simplifications/SiloMathLib_SAFE.spec";

//------------------------------- DEFENITION AND METHODS START ----------------------------------

    methods {
        
    }

    definition ignoredMethod(method f) returns bool =
        f.selector == sig:PartialLiquidationHarness.initialize(address, bytes).selector;

//------------------------------- DEFENITION AND METHODS END ----------------------------------


//------------------------------- RULES TEST START ----------------------------------

    //calling beforeAction and afterAction does not change any state
    //calling beforeAction and afterAction should never revert
    //initialize can only be called once
    //once set, siloConfig can not be changed
    //hookReceiverConfig() always returns (0,0)
    //no debt, no liquidation
    //silo0/1 can never be debt and collateral at the same time
    //silo0 and silo1 can never be the same
    //different tokens can never be the same address (Protected, Debt, Collateral)

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


    rule doesntAlwaysRevert(method f, env e)
        filtered { f -> !ignoredMethod(f) }
    {
        SafeAssumptionsEnv_withInvariants(e);
        calldataarg args;
        f(e, args);
        satisfy true;
    }

    rule maxLiquidationNeverReverts(env e, address user)
    {
        address colSiloBefore = siloConfig(e).borrowerCollateralSilo(e, user);
        require colSiloBefore == silo0 || colSiloBefore == silo1 || colSiloBefore == 0;
        SafeAssumptions_withInvariants(e, user);
        uint256 collateralToLiquidate; uint256 debtToRepay; bool sTokenRequired;
        collateralToLiquidate, debtToRepay, sTokenRequired = maxLiquidation@withrevert(e, user);
        assert !lastReverted;
    }

//-------------------------------OLD RULES END----------------------------------


