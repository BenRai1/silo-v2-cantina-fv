//------------------------------------ SETUP START --------------------------------------

    methods {
        function _.accrueInterestForConfig(address, uint256, uint256) external => accrueInterestForSiloCVL(calledContract) expect void;
    }

    function accrueInterestForSiloCVL(address silo) {
        accrueInterestCalled[silo] = accrueInterestCalled[silo] + 1;
    }


    ghost mapping (address => mathint) accrueInterestCalled;

    function debtSiloAndCollateralSiloAreDifferent(env e, address borrower) {
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo[borrower];
        require debtSilo != collateralSilo || debtSilo == 0 && collateralSilo == 0;
        require debtSilo == silo0 || collateralSilo == silo1 || debtSilo == 0;
        require collateralSilo == silo0 || collateralSilo == silo1 || collateralSilo == 0;
    }

//------------------------------------ SETUP END --------------------------------------
// accrueInterestForSilo() calls accrueInterest for the provided silo //@audit-issue Multiple summaries for all external functions with the signature accrueInterestForConfig(address, uint256, uint256)
    rule accrueInterestForSiloCallsAccrueInterestForProvidedSilo(env e) {
        address silo;

        address silo0;
        address silo1;
        (silo0, silo1) = siloConfig.getSilos(e);

        //values before
        mathint callsSilo0 = accrueInterestCalled[silo0];
        mathint callsSilo1 = accrueInterestCalled[silo1];

        //function call
        siloConfig.accrueInterestForSilo(e, silo);

        //values after
        mathint callsSilo0After = accrueInterestCalled[silo0];
        mathint callsSilo1After = accrueInterestCalled[silo1];

        //assert
        assert silo == silo0 => callsSilo0After == callsSilo0 + 1 && callsSilo1After == callsSilo1;
        assert silo == silo1 => callsSilo1After == callsSilo1 + 1 && callsSilo0After == callsSilo0;
    }


     // accrueInterestForBothSilos() calls accrueInterest for both silos //@audit-issue Multiple summaries for all external functions with the signature accrueInterestForConfig(address, uint256, uint256)