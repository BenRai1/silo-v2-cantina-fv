import "../setup/CompleteSiloSetup.spec";
import "./0base_Silo.spec";
import "../simplifications/Silo_noAccrueInterest_simplification_UNSAFE.spec";
// import "../simplifications/_Oracle_call_before_quote_UNSAFE.spec"; //i: summarizes before the call to beforeQuote
import "../simplifications/Oracle_quote_one_UNSAFE.spec";
import "../simplifications/_flashloan_no_state_changes.spec";
import "../simplifications/SiloMathLib_SAFE.spec";
import "../simplifications/Silo_noAccrueInterest_simplification_UNSAFE.spec"; //accrueInterest does not change state
// import "../simplifications/_Oracle_call_before_quote_UNSAFE.spec"; //to avoide DEFAUL HAVOC for oracle calls
// import "../simplifications/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
// import "../simplifications/_hooks_no_state_change.spec"; //calls to hooks do not change state

//---------------------- METHODES, FUNCTIONS, GHOSTS START----------------------
    methods{

    function _.beforeQuote(address) external => beforeQuote__noStateChange(calledContract) expect void;
    }

    //number of calls to the oracle
    persistent ghost mapping(address => mathint) callCountBeforeQuote{
        //all runs starts with the value 0
        init_state axiom forall address a. callCountBeforeQuote[a] == 0;
        // init_state axiom forall uint256 p. tracked_weight(p) == 0;
    }

    //oracle calls
    function beforeQuote__noStateChange(address _calledContract) {
        callCountBeforeQuote[_calledContract] = callCountBeforeQuote[_calledContract] + 1;
    }

    //setup for the maxLtvOracles
    function maxLtvOracleRulesSetup(env e, address otherOracle) {
        address silo0MaxLtvOracle = siloConfig.getConfig(e, silo0).maxLtvOracle;
        address silo1MaxLtvOracle = siloConfig.getConfig(e, silo1).maxLtvOracle;
        //oracle addresses are different
        require(silo0MaxLtvOracle != silo1MaxLtvOracle);
        require(silo0MaxLtvOracle != otherOracle);
        require(silo1MaxLtvOracle != otherOracle);
    }

    //setup for the solvencyOracles
    function solvencyOracleRulesSetup(env e, address otherOracle) {
        address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
        address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;
        //oracle addresses are different
        require(silo0SolvencyOracle != silo1SolvencyOracle);
        require(silo0SolvencyOracle != otherOracle);
        require(silo1SolvencyOracle != otherOracle);
    }

    function allOraclesDifferent(env e, address otherOracle) {
        address silo0MaxLtvOracle = siloConfig.getConfig(e, silo0).maxLtvOracle;
        address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
        address silo1MaxLtvOracle = siloConfig.getConfig(e, silo1).maxLtvOracle;
        address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;

        //oracle addresses are different
        require(silo0MaxLtvOracle != silo0SolvencyOracle);
        require(silo0MaxLtvOracle != silo1MaxLtvOracle);
        require(silo0MaxLtvOracle != silo1SolvencyOracle);
        require(silo0MaxLtvOracle != otherOracle);
        require(silo0SolvencyOracle != silo1MaxLtvOracle);
        require(silo0SolvencyOracle != silo1SolvencyOracle);
        require(silo0SolvencyOracle != otherOracle);
        require(silo1MaxLtvOracle != silo1SolvencyOracle);
        require(silo1MaxLtvOracle != otherOracle);
        require(silo1SolvencyOracle != otherOracle);
    }
//---------------------- METHODES, FUNCTIONS, GHOSTS END----------------------


//------------------------------- RULES TEST START ----------------------------------

    //-----------------maxLtvOracle callBeforeQuote -----------------
        // onlySpecific functions should call the maxLTVOracle beforeQuote
        rule onlySpecificFunctionsCallMaxLtvOracleBeforeCall (env e, method f, calldataarg args) 
            filtered {f-> 
                !f.isView && 
                !HARNESS_METHODS(f) && 
                f.selector != sig:decimals().selector &&
                f.selector != sig:flashLoan(address,address,uint256,bytes).selector
        } {
            address silo0MaxLtvOracle = siloConfig.getConfig(e, silo0).maxLtvOracle;
            address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
            address silo1MaxLtvOracle = siloConfig.getConfig(e, silo1).maxLtvOracle;
            address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;
            address otherOracle;

            //setup
            allOraclesDifferent(e, otherOracle);

            //valus before
            mathint silo0MaxLtvOracleCountBefore = callCountBeforeQuote[silo0MaxLtvOracle];
            mathint silo0SolvencyOracleCountBefore = callCountBeforeQuote[silo0SolvencyOracle];

            //function call
            f(e, args);

            //values after
            mathint silo0MaxLtvOracleCountAfter = callCountBeforeQuote[silo0MaxLtvOracle];
            mathint silo0SolvencyOracleCountAfter = callCountBeforeQuote[silo0SolvencyOracle];

            //only specific functions should call the maxLTVOracle
            assert (silo0MaxLtvOracleCountAfter > silo0MaxLtvOracleCountBefore || silo0SolvencyOracleCountAfter > silo0SolvencyOracleCountBefore => 
                        f.selector == sig:borrow(uint256,address,address).selector ||
                        f.selector == sig:borrowSameAsset(uint256,address,address).selector ||
                        f.selector == sig:borrowShares(uint256,address,address).selector
                    );
        }

    //------------------- solvancyOracle callBeforeQuote -----------------
        // onlySpecific functions should call the solvancyOracle beforeQuote
        rule onlySpecificFunctionsCallSolvalcyOracleBeforeQuote(env e, method f, calldataarg args) 
            filtered {f-> 
                !HARNESS_METHODS(f) && 
                f.selector != sig:decimals().selector &&
                f.selector != sig:flashLoan(address,address,uint256,bytes).selector
                } {
            address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
            address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;
            address otherOracle;

            //setup
            allOraclesDifferent(e, otherOracle);

            //valus before
            mathint silo0SolvencyOracleCountBefore = callCountBeforeQuote[silo0SolvencyOracle];
            mathint silo1SolvencyOracleCountBefore = callCountBeforeQuote[silo1SolvencyOracle];

            //function call
            f(e, args);

            //values after
            mathint silo0SolvencyOracleCountAfter = callCountBeforeQuote[silo0SolvencyOracle];
            mathint silo1SolvencyOracleCountAfter = callCountBeforeQuote[silo1SolvencyOracle];

            //only specific functions should call the solvancyOracle
            assert (silo0SolvencyOracleCountAfter > silo0SolvencyOracleCountBefore || silo1SolvencyOracleCountAfter > silo1SolvencyOracleCountBefore => 
                        f.selector == sig:redeem(uint256,address,address).selector ||
                        f.selector == sig:redeem(uint256,address,address, ISilo.CollateralType).selector ||
                        f.selector == sig:withdraw(uint256,address,address).selector ||
                        f.selector == sig:withdraw(uint256,address,address, ISilo.CollateralType).selector ||
                        f.selector == sig:transitionCollateral(uint256,address,ISilo.CollateralType).selector ||
                        f.selector == sig:switchCollateralToThisSilo().selector ||
                        f.selector == sig:transfer(address,uint256).selector ||
                        f.selector == sig:transferFrom(address,address,uint256).selector ||
                        f.selector == sig:mint(uint256,address).selector ||
                        f.selector == sig:mint(address,address,uint256).selector ||
                        // f.selector == sig:borrowShares(uint256,address,address).selector ||
                        // f.selector == sig:borrow(uint256,address,address).selector ||
                        f.selector == sig:burn(address,address,uint256).selector

                    );
        }


        rule onlySolvencyOraclesCalledBeforeQuote(env e) {
            uint256 assets;
            address receiver;
            address owner;
            address otherOracle;
            address debtSilo = siloConfig.getDebtSilo(e, owner);
            address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
            require(collateralSilo == silo0);

            address debtSiloSolvencyOracle = siloConfig.getConfig(e, debtSilo).solvencyOracle;
            address collateralSiloSolvencyOracle = siloConfig.getConfig(e, collateralSilo).solvencyOracle;
            bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
            bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
            require(debtSiloSolvencyOracle != 0 && collateralSiloSolvencyOracle != 0);
            require(debtSiloCallBeforeQuote == true && collateralSiloCallBeforeQuote == true);
            
            //setup
            solvencyOracleRulesSetup(e, otherOracle);

            //values before
            mathint debtSiloSolvencyOracleCountBefore = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint collateralSiloSolvencyOracleCountBefore = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];

            //function call
            withdraw(e, assets, receiver, owner);

            //values after
            mathint debtSiloSolvencyOracleCountAfter = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint collateralSiloSolvencyOracleCountAfter = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

            //only the solvancyOracles are called once before the quote
            assert (debtSiloSolvencyOracleCountAfter == debtSiloSolvencyOracleCountBefore + 1);
            assert (collateralSiloSolvencyOracleCountAfter == collateralSiloSolvencyOracleCountBefore + 1);
            assert (otherOracleCountAfter == otherOracleCountBefore);
        }

        // withdraw() if solvancyOracle != 0 && _config.callBeforeQuote == true for debtSilo, no oracle is called before the quote (only collateralSilo is checked)
        rule onlySolvencyOracleDebtSiloCalledBeforeQuote(env e) {
            uint256 assets;
            address receiver;
            address owner;
            address otherOracle;
            address debtSilo = siloConfig.getDebtSilo(e, owner);
            address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
            require(collateralSilo == silo0);
            require(debtSilo != collateralSilo);

            address debtSiloSolvencyOracle = siloConfig.getConfig(e, debtSilo).solvencyOracle;
            address collateralSiloSolvencyOracle = siloConfig.getConfig(e, collateralSilo).solvencyOracle;
            bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
            bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
            require(debtSiloSolvencyOracle != 0 && collateralSiloSolvencyOracle == 0);
            require(debtSiloCallBeforeQuote == true && collateralSiloCallBeforeQuote == false);
            
            //setup
            solvencyOracleRulesSetup(e, otherOracle);

            //values before
            mathint debtSiloSolvencyOracleCountBefore = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint collateralSiloSolvencyOracleCountBefore = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];


            //function call
            withdraw(e, assets, receiver, owner);

            //values after
            mathint debtSiloSolvencyOracleCountAfter = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint collateralSiloSolvencyOracleCountAfter = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

            //only the solvancyOracles are called once before the quote
            assert (debtSiloSolvencyOracleCountAfter == debtSiloSolvencyOracleCountBefore +1);
            assert (collateralSiloSolvencyOracleCountAfter == collateralSiloSolvencyOracleCountBefore);
            assert (otherOracleCountAfter == otherOracleCountBefore);
        }


        // withdraw() if solvancyOracle != 0 && _config.callBeforeQuote == true for collateralSilo, only the solvancyOracle of collateralSilo is called once before the quote
        rule onlySolvencyOracleCollateralSiloCalledBeforeQuote(env e) {
            uint256 assets;
            address receiver;
            address owner;
            address otherOracle;
            address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
            address debtSilo = siloConfig.getDebtSilo(e, owner);
            require(collateralSilo == silo0);
            require(collateralSilo != debtSilo);

            address collateralSiloSolvencyOracle = siloConfig.getConfig(e, collateralSilo).solvencyOracle;
            address debtSiloSolvencyOracle = siloConfig.getConfig(e, debtSilo).solvencyOracle;
            bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
            bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
            require(collateralSiloSolvencyOracle != 0 && debtSiloSolvencyOracle == 0);
            require(collateralSiloCallBeforeQuote == true && debtSiloCallBeforeQuote == false);

            //setup
            solvencyOracleRulesSetup(e, otherOracle);

            //values before
            mathint collateralSiloSolvencyOracleCountBefore = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint debtSiloSolvencyOracleCountBefore = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];

            //function call
            withdraw(e, assets, receiver, owner);

            //values after
            mathint collateralSiloSolvencyOracleCountAfter = callCountBeforeQuote[collateralSiloSolvencyOracle];
            mathint debtSiloSolvencyOracleCountAfter = callCountBeforeQuote[debtSiloSolvencyOracle];
            mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

            //only the solvancyOracles are called once before the quote
            assert (collateralSiloSolvencyOracleCountAfter == collateralSiloSolvencyOracleCountBefore + 1);
            assert (debtSiloSolvencyOracleCountAfter == debtSiloSolvencyOracleCountBefore);
            assert (otherOracleCountAfter == otherOracleCountBefore);
        }
        


    //---------- maxLtvOracle quote -----------------
        //only specific functions should call quote //@audit testrun to see which functions call quote //@audit-issue why are the oracles never called?
        rule onlySpecificFunctionsCallQuote(env e, method f, calldataarg args) filtered{f-> !HARNESS_METHODS(f)} {
            address silo0MaxLtvOracle = siloConfig.getConfig(e, silo0).maxLtvOracle;
            address silo1MaxLtvOracle = siloConfig.getConfig(e, silo1).maxLtvOracle;
            address otherOracle;

            //setup
            maxLtvOracleRulesSetup(e, otherOracle);

            //values before
            mathint silo0MaxLtvOracleCountBefore = callCountQuote[silo0MaxLtvOracle];
            mathint silo1MaxLtvOracleCountBefore = callCountQuote[silo1MaxLtvOracle];

            //function call
            f(e, args);

            //values after
            mathint silo0MaxLtvOracleCountAfter = callCountQuote[silo0MaxLtvOracle];
            mathint silo1MaxLtvOracleCountAfter = callCountQuote[silo1MaxLtvOracle];

            //only specific functions should call quote
            assert (silo0MaxLtvOracleCountAfter > silo0MaxLtvOracleCountBefore || silo1MaxLtvOracleCountAfter > silo1MaxLtvOracleCountBefore => 
                        f.selector != sig:decimals().selector
                    );
        }

    //----------------- solvancyOracle quote
    //only specific functions should call quote //@audit testrun to see which functions call quote
        rule onlySpecificFunctionsCallQuoteSolvancyOracle(env e, method f, calldataarg args) filtered{f-> !HARNESS_METHODS(f)} {
            address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
            address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;
            address otherOracle;

            //setup
            solvencyOracleRulesSetup(e, otherOracle);

            //values before
            mathint silo0SolvencyOracleCountBefore = callCountQuote[silo0SolvencyOracle];
            mathint silo1SolvencyOracleCountBefore = callCountQuote[silo1SolvencyOracle];

            //function call
            f(e, args);

            //values after
            mathint silo0SolvencyOracleCountAfter = callCountQuote[silo0SolvencyOracle];
            mathint silo1SolvencyOracleCountAfter = callCountQuote[silo1SolvencyOracle];

            //@audit-issue is it even possible to call the quote function?
            satisfy silo0SolvencyOracleCountBefore != silo0SolvencyOracleCountAfter;

        //     //only specific functions should call quote
        //     assert (silo0SolvencyOracleCountAfter > silo0SolvencyOracleCountBefore || silo1SolvencyOracleCountAfter > silo1SolvencyOracleCountBefore => 
        //                 f.selector != sig:decimals().selector
        //             );
        }


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------




    //withdwar() if collateralSilo != silo0 no oracle is called before the quote
    rule noCallBeforeIfCollateralSiloNotSilo0(env e){
        uint256 assets;
        address receiver;
        address owner;
        address anyOracle;
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
        require(collateralSilo != silo0);

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        withdraw(e, assets, receiver, owner);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }

    // withdraw() if  _config.solvencyOracle == address(0) no oracle is called before the quote
    rule noCallBeforeIfSolvencyOracles0(env e){
        uint256 assets;
        address receiver;
        address owner;
        address anyOracle;
        address debtSilo = siloConfig.getDebtSilo(e, owner);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
        require(debtSilo != collateralSilo);

        address debtSiloSolvencyOracle = siloConfig.getConfig(e, debtSilo).solvencyOracle;
        address collateralSiloSolvencyOracle = siloConfig.getConfig(e, collateralSilo).solvencyOracle;
        require(debtSiloSolvencyOracle == 0);
        require(collateralSiloSolvencyOracle == 0);

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        withdraw(e, assets, receiver, owner);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }

    // withdraw() if callBeforeQuote == false no oracle is called before the quote
    rule noCallBeforeQuoteIfFalseSolvancyOracle(env e) {
        uint256 assets;
        address receiver;
        address owner;
        address anyOracle;
        address debtSilo = siloConfig.getDebtSilo(e, owner);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, owner);
        require(debtSilo != collateralSilo);

        bool callBeforeQuoteDebtSilo = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
        bool callBeforeQuoteCollateralSilo = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
        require(callBeforeQuoteDebtSilo == false);
        require(callBeforeQuoteCollateralSilo == false);

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        withdraw(e, assets, receiver, owner);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }

    // borrow() if  _config.maxLtvOracle == address(0) no oracle is called before the quote
    rule noCallBeforeIfOracles0(env e){
        uint256 assets;
        address receiver;
        address borrower;
        address anyOracle;
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);

        address debtSiloMaxLtvOracle = siloConfig.getConfig(e, debtSilo).maxLtvOracle;
        address collateralSiloMaxLtvOracle = siloConfig.getConfig(e, collateralSilo).maxLtvOracle;
        require(debtSiloMaxLtvOracle == 0);
        require(collateralSiloMaxLtvOracle == 0);

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        borrow(e, assets, receiver, borrower);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }

    // borrow() if maxLtvOracle != 0 && _config.callBeforeQuote == true for collateralSilo, only the maxLtvOracle of collateralSilo is called once before the quote
    rule onlyCollateralSiloMaxLtvOracleCalledBeforeQuote(env e) {
        uint256 assets;
        address receiver;
        address borrower;
        address otherOracle;
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);

        address debtSiloMaxLtvOracle = siloConfig.getConfig(e, debtSilo).maxLtvOracle;
        address collateralSiloMaxLtvOracle = siloConfig.getConfig(e, collateralSilo).maxLtvOracle;
        bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
        bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
        require(debtSiloMaxLtvOracle == 0 && collateralSiloMaxLtvOracle != 0);
        require(debtSiloCallBeforeQuote == false && collateralSiloCallBeforeQuote == true);
        
        //setup
        maxLtvOracleRulesSetup(e, otherOracle);

        //values before
        mathint debtSiloMaxLtvOracleCountBefore = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountBefore = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];

        //function call
        borrow(e, assets, receiver, borrower);

        //values after
        mathint debtSiloMaxLtvOracleCountAfter = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountAfter = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

        //only the maxLtvOracles are called once before the quote
        assert (debtSiloMaxLtvOracleCountAfter == debtSiloMaxLtvOracleCountBefore);
        assert (collateralSiloMaxLtvOracleCountAfter == collateralSiloMaxLtvOracleCountBefore + 1);
        assert (otherOracleCountAfter == otherOracleCountBefore);
    }

    // borrow() if maxLtvOracle != 0 && _config.callBeforeQuote == true, only the maxLtvOracles are called once before the quote
    rule onlyMaxLtvOraclesCalledBeforeQuote(env e) {
        uint256 assets;
        address receiver;
        address borrower;
        address otherOracle;
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);

        address debtSiloMaxLtvOracle = siloConfig.getConfig(e, debtSilo).maxLtvOracle;
        address collateralSiloMaxLtvOracle = siloConfig.getConfig(e, collateralSilo).maxLtvOracle;
        bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
        bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
        require(debtSiloMaxLtvOracle != 0 && collateralSiloMaxLtvOracle != 0);
        require(debtSiloCallBeforeQuote == true && collateralSiloCallBeforeQuote == true);
        
        //setup
        maxLtvOracleRulesSetup(e, otherOracle);

        //values before
        mathint debtSiloMaxLtvOracleCountBefore = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountBefore = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];

        //function call
        borrow(e, assets, receiver, borrower);

        //values after
        mathint debtSiloMaxLtvOracleCountAfter = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountAfter = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

        //only the maxLtvOracles are called once before the quote
        assert (debtSiloMaxLtvOracleCountAfter == debtSiloMaxLtvOracleCountBefore + 1);
        assert (collateralSiloMaxLtvOracleCountAfter == collateralSiloMaxLtvOracleCountBefore + 1);
        assert (otherOracleCountAfter == otherOracleCountBefore);
    }

    // borrow() if maxLtvOracle != 0 && _config.callBeforeQuote == true for debtSilo, only the maxLtvOracle of debtSilo is called once before the quote
    rule onlyDebtSiloMaxLtvOracleCalledBeforeQuote(env e) {
        uint256 assets;
        address receiver;
        address borrower;
        address otherOracle;
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);

        address debtSiloMaxLtvOracle = siloConfig.getConfig(e, debtSilo).maxLtvOracle;
        address collateralSiloMaxLtvOracle = siloConfig.getConfig(e, collateralSilo).maxLtvOracle;
        bool debtSiloCallBeforeQuote = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
        bool collateralSiloCallBeforeQuote = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
        require(debtSiloMaxLtvOracle != 0 && collateralSiloMaxLtvOracle == 0);
        require(debtSiloCallBeforeQuote == true && collateralSiloCallBeforeQuote == false);
        
        //setup
        maxLtvOracleRulesSetup(e, otherOracle);

        //values before
        mathint debtSiloMaxLtvOracleCountBefore = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountBefore = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountBefore = callCountBeforeQuote[otherOracle];

        //function call
        borrow(e, assets, receiver, borrower);

        //values after
        mathint debtSiloMaxLtvOracleCountAfter = callCountBeforeQuote[debtSiloMaxLtvOracle];
        mathint collateralSiloMaxLtvOracleCountAfter = callCountBeforeQuote[collateralSiloMaxLtvOracle];
        mathint otherOracleCountAfter = callCountBeforeQuote[otherOracle];

        //only the maxLtvOracles are called once before the quote
        assert (debtSiloMaxLtvOracleCountAfter == debtSiloMaxLtvOracleCountBefore + 1);
        assert (collateralSiloMaxLtvOracleCountAfter == collateralSiloMaxLtvOracleCountBefore);
        assert (otherOracleCountAfter == otherOracleCountBefore);
    }

    //borrowSameAsset() no oracle is called before quote
    rule noOracleCalledBeforeQuote(env e) {
        uint256 assets;
        address receiver;
        address borrower;
        address anyOracle;

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        borrowSameAsset(e, assets, receiver, borrower);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }
    
    // borrow() if callBeforeQuote == false no oracle is called before the quote
    rule noCallBeforeQuoteIfFalse(env e) {
        uint256 assets;
        address receiver;
        address borrower;
        address anyOracle;
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);

        bool callBeforeQuoteDebtSilo = siloConfig.getConfig(e, debtSilo).callBeforeQuote;
        bool callBeforeQuoteCollateralSilo = siloConfig.getConfig(e, collateralSilo).callBeforeQuote;
        require(callBeforeQuoteDebtSilo == false);
        require(callBeforeQuoteCollateralSilo == false);

        //values before
        mathint countBefore = callCountBeforeQuote[anyOracle];

        //function call
        borrow(e, assets, receiver, borrower);

        //values after
        mathint countAfter = callCountBeforeQuote[anyOracle];

        //no oracle is called before the quote
        assert (countAfter == countBefore);
    }
//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
