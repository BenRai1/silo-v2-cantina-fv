import "../setup/CompleteSiloSetup.spec";
import "../silo/unresolved.spec";
import "../simplifications/Oracle_quote_one_UNSAFE.spec";
import "../simplifications/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
import "../simplifications/SiloMathLib_SAFE.spec";

//------------------------------- DEFENITION AND METHODS START ---------------------------------- //i: in video 16:19

    methods {
        // ---- `envfree` ----------------------------------------------------------
        function _.balanceOf(address) external envfree;
        
    }

    definition ignoredMethod(method f) returns bool =
        f.selector == sig:PartialLiquidationHarness.initialize(address, bytes).selector;

//------------------------------- DEFENITION AND METHODS END ----------------------------------


//------------------------------- RULES TEST START ----------------------------------

    
    //no debt, no liquidation
    rule noDebtNoLiquidation(env e){
        address _collateralAsset;
        address _debtAsset;
        address _borrower;
        uint256 _maxDebtToCover;
        bool _receiveSToken;

        uint256 balanceDebtAssetBorrower = _debtAsset.balanceOf(e, _borrower);

        storage init = lastStorage;
        liquidationCall@withrevert(e, _collateralAsset, _debtAsset, _borrower, _maxDebtToCover, _receiveSToken);
        storage final = lastStorage;
        assert init == final;
    }

    //using the result of maxLiquidation to call liquidationCall should never revert
   



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------
    //initialize can only be called once RULE NOT VACOUSE https://prover.certora.com/output/8418/5677faa6a12d45b7a42cc6064571f0e5/?anonymousKey=7fceae5238ed59b1eb873b2495eaad3107096e77
    rule initializeCanOnlyBeCalledOnce(env e, address _siloConfig, bytes data){
        initialize(e, _siloConfig, data);
        initialize@withrevert(e, _siloConfig, data);
        assert lastReverted;
    }

    //after initialize, siloConfig is not address0 RULE NOT VACOUSE
    rule siloConfigIsNotZero(env e, address _siloConfig, bytes data){
        initialize(e, _siloConfig, data);
        address siloAddress = siloConfig(e);
        assert siloAddress != 0;
    }

    //once set, siloConfig can not be changed RULE NOT VACOUSE
    rule siloConfigCanNotBeChanged(env e, address _siloConfig, bytes data, method f, calldataarg args){
        initialize(e, _siloConfig, data);
        address siloAddressBefore = siloConfig(e);
        f(e, args);
        address siloAddressAfter = siloConfig(e);
        assert siloAddressBefore == siloAddressAfter;
    }

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    //hookReceiverConfig() always returns (0,0)
    rule hookReceiverConfigAlwaysReturnsZero(env e, address _address){
        uint24 hooksBefore;
        uint24 hooksAfter;
        (hooksBefore, hooksAfter) = hookReceiverConfig(e, _address);
        assert hooksBefore == 0;
        assert hooksAfter == 0;
    }

    //calling beforeAction and afterAction should never revert
    rule beforeAfterActionNeverReverts(env e, address _address, uint256 number, bytes data){
        require(e.msg.value == 0);
        
        beforeAction@withrevert(e, _address, number, data);
        assert(!lastReverted, "beforeAction reverted");
        
        afterAction@withrevert(e, _address, number, data);
        assert(!lastReverted, "afterAction reverted");
    }

    //calling beforeAction and afterAction does not change any state
    rule beforeAfterActionDoesNotChangeState(env e, address _address, uint256 number, bytes data){
        storage initial = lastStorage;
        beforeAction@withrevert(e, _address, number, data);
        afterAction@withrevert(e, _address, number, data);
        storage final = lastStorage;
        assert initial == final;
    }

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


