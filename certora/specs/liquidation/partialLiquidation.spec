import "../setup/CompleteSiloSetup.spec";
import "../silo/unresolved.spec";
import "../simplifications/Oracle_quote_one_UNSAFE.spec";
import "../simplifications/SiloMathLib_SAFE.spec";
import "../simplifications/Silo_noAccrueInterest_simplification_UNSAFE.spec"; //accrueInterest does not change state
import "../simplifications/_Oracle_call_before_quote_UNSAFE.spec"; //to avoide DEFAUL HAVOC for oracle calls
// import "../simplifications/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
// import "../simplifications/_hooks_no_state_change.spec"; //calls to hooks do not change state


//------------------------------- DEFENITION AND METHODS START ---------------------------------- //i: in video 13:42

    methods {
        // ---- `envfree` ----------------------------------------------------------
        function _.repay(uint256,address) external => DISPATCHER(true);
        function _.forwardTransferFromNoChecks(address,address,uint256) external => DISPATCHER(true);
        // function _.previewRedeem(uint256,ISilo.CollateralType) external => DISPATCHER(true);
        function _.redeem(uint256,address,address,ISilo.CollateralType) external => DISPATCHER(true);

        function _.balanceOf(address) external envfree;

        //nothing should happen
        // function _.turnOnReentrancyProtection() external => nothingHappens() expect void;
        // function _.turnOffReentrancyProtection() external => nothingHappens()  expect void;
        // function _.accrueInterest() external => nothingHappens() expect void;
        //@audit-issue commented out
        // function _.previewRedeem(uint256,ISilo.CollateralType) external => nothingHappensReturnValue() expect uint256; //@audit-issue not sure if not used somewhere else
        // function _.callSolvencyOracleBeforeQuote() internal => nothingHappens() expect void;
        // function _.splitReceiveCollateralToLiquidate(uint256 _collateralToLiquidate, uint256 _borrowerProtectedAssets) internal => splitReceiveCollateralToLiquidate(_collateralToLiquidate) expect (uint256, uint256);        
    }

    //setup: collateral silo is silo0, debt silo is silo1, user has no protected collateral, only normal collateral
    function setupFewerPaths(env e, address borrower) returns (address, address){
        //collateral silo is silo0
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(collateralSilo == silo0);
        //only normal collateral
        address protectedShateToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        require(protectedShateToken.balanceOf(e, borrower) == 0);
        //debt silo is silo1
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        require(debtSilo == silo1);

        //oracles not set => no quote
        address silo0MaxLTVOracle = siloConfig.getConfig(e, silo0).maxLtvOracle;
        require(silo0MaxLTVOracle == 0);
        address silo0SolvencyOracle = siloConfig.getConfig(e, silo0).solvencyOracle;
        require(silo0SolvencyOracle == 0);
        address silo1MaxLTVOracle = siloConfig.getConfig(e, silo1).maxLtvOracle;
        require(silo1MaxLTVOracle == 0);
        address silo1SolvencyOracle = siloConfig.getConfig(e, silo1).solvencyOracle;
        require(silo1SolvencyOracle == 0);

        //callBeforeQuote = false => no calls
        bool silo0CallBeforeQuote = siloConfig.getConfig(e, silo0).callBeforeQuote;
        require(!silo0CallBeforeQuote);
        bool silo1CallBeforeQuote = siloConfig.getConfig(e, silo1).callBeforeQuote;
        require(!silo1CallBeforeQuote);

        totalSuppliesMoreThanBalance(borrower);

        //assets and shares are 1 to 1 for silo0
        address protectedShareTokenSilo0 = siloConfig.getConfig(e, silo0).protectedShareToken;
        address debtShareTokenSilo0 = siloConfig.getConfig(e, silo0).debtShareToken;
        uint256 protectedShareTokenSilo0TotalSupply = protectedShareTokenSilo0.totalSupply(e);
        uint256 collateralShareTokenSilo0TotalSupply = silo0.totalSupply(e);
        uint256 debtShareTokenSilo0TotalSupply = debtShareTokenSilo0.totalSupply(e);
        uint256 protectedAssetsSilo0;
        uint256 collateralAssetsSilo0;
        uint256 debtAssetsSilo0;
        (_, _, protectedAssetsSilo0, collateralAssetsSilo0, debtAssetsSilo0) = silo0.getSiloStorage(e);
        require protectedShareTokenSilo0TotalSupply == protectedAssetsSilo0;
        require collateralShareTokenSilo0TotalSupply == collateralAssetsSilo0;
        require debtShareTokenSilo0TotalSupply == debtAssetsSilo0;

        //assets and shares are 1 to 1 for silo1
        address protectedShareTokenSilo1 = siloConfig.getConfig(e, silo1).protectedShareToken;
        address debtShareTokenSilo1 = siloConfig.getConfig(e, silo1).debtShareToken;
        uint256 protectedShareTokenSilo1TotalSupply = protectedShareTokenSilo1.totalSupply(e);
        uint256 collateralShareTokenSilo1TotalSupply = silo1.totalSupply(e);
        uint256 debtShareTokenSilo1TotalSupply = debtShareTokenSilo1.totalSupply(e);
        uint256 protectedAssetsSilo1;
        uint256 collateralAssetsSilo1;
        uint256 debtAssetsSilo1;
        (_, _, protectedAssetsSilo1, collateralAssetsSilo1, debtAssetsSilo1) = silo1.getSiloStorage(e);
        require protectedShareTokenSilo1TotalSupply == protectedAssetsSilo1;
        require collateralShareTokenSilo1TotalSupply == collateralAssetsSilo1;
        require debtShareTokenSilo1TotalSupply == debtAssetsSilo1;

        //hooksBefore == 0 and hooksAfter == 0 => hooks are not called
        uint256 hooksBeforeSilo0 = silo0.hooksBeforeHarness(e);
        require hooksBeforeSilo0 == 0;
        uint256 hooksAfterSilo0 = silo0.hooksAfterHarness(e);
        require hooksAfterSilo0 == 0;
        uint256 hooksBeforeSilo1 = silo1.hooksBeforeHarness(e);
        require hooksBeforeSilo1 == 0;
        uint256 hooksAfterSilo1 = silo1.hooksAfterHarness(e);
        require hooksAfterSilo1 == 0;

        return (collateralSilo, debtSilo);
    }
  

    definition ignoredMethod(method f) returns bool =
        f.selector == sig:PartialLiquidationHarness.initialize(address, bytes).selector;

//------------------------------- DEFENITION AND METHODS END ----------------------------------

//------------------------FUNCTIONS START------------------------

    function nothingHappens(){
    }
    
    function nothingHappensReturnValue() returns uint256{
        return 0;
    }

    function splitReceiveCollateralToLiquidate(uint256 _collateralToLiquidate) returns (uint256, uint256) {
        //split collateral to liquidate
        //return values
        return (_collateralToLiquidate, 0);
    }



    //inital setup for liquidations (silos different, users different)
    function setupLiquidationRules(env e, address borrower) {
        nonSceneAddressRequirements(e.msg.sender);
        nonSceneAddressRequirements(borrower);
        require(borrower != e.msg.sender);

        //debt silo not collateral silo
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(debtSilo != collateralSilo);
    }

    //ensure the borrower has only protected shares, no normal collateral shares
    function borrowerHasOnlyProtectedShares(env e, address borrower) {
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        require(collateralSilo.balanceOf(e, borrower) == 0);

    }

//------------------------FUNCTIONS END------------------------


//------------------------------- RULES TEST START ----------------------------------

    // -------------------------------- ISSUE --------------------

    // ---------------------------------reverts	
    
    // 	liquidationCall() reverts if _borrower has no debtShares
    rule revertIfBorrowerHasNoDebtAssets(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        require collateralAsset == token0; //@audit-issue added to reduce runtime
        address debtAsset;
        require debtAsset == token1; //@audit-issue added to reduce runtime
        address borrower;
        uint256 maxDebtToCover;
        require maxDebtToCover != 0; //@audit-issue added to reduce runtime
        bool receiveSToken;
        setupFewerPaths(e, borrower);

        //setup
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address debtShareToken = siloConfig.getConfig(e, debtSilo).debtShareToken;
        require debtShareToken.balanceOf(e, borrower) == 0;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted becasue borrower does not have debtShares
        assert lastReverted;        
    }
    
    // 	liquidationCall() reverts if liquidty of collateralSilo is 0 and user only has collateralShare and _receiveSToken == false
    rule revertIfCollateralSiloLiquidityIsZero(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        address protectedShareToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        require collateralSilo.getLiquidity(e) == 0;
        require protectedShareToken.balanceOf(e, borrower) == 0;
        require !receiveSToken;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted
        assert lastReverted;        
    }
    
    // ---------------------------------borrower	
    
    // 	liquidationCall() collateralShares (protected) of borrower decrease (//@audit-issue is false since function works if collateralAssets are 0)
    rule borrowerCollateralShareDecrease(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        borrowerHasOnlyProtectedShares(e, borrower);

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        address protectedShareToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        uint256 balanceOfProtectedSharesBefore = protectedShareToken.balanceOf(e, borrower);

        //function call
        liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 balanceOfProtectedSharesAfter = protectedShareToken.balanceOf(e, borrower);

        //asserts
        assert balanceOfProtectedSharesAfter < balanceOfProtectedSharesBefore;   
    }
    
    // 	liquidationCall() debtShares of borrower decrease
    rule borrowerDebtSharesDecrease(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);

        //values before
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address debtShareToken = siloConfig.getConfig(e, debtSilo).debtShareToken;
        uint256 balanceDebtSharesBefore = debtShareToken.balanceOf(e, borrower);

        //function call
        liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 balanceDebtSharesAfter = debtShareToken.balanceOf(e, borrower);

        //asserts
        assert balanceDebtSharesAfter < balanceDebtSharesBefore;   
    }
    
    // 	liquidationCall() after liquidation, if borrower still has protectedShares, the amount of collateralShare did not change
    rule protectedCollateralIsLiquidatedFirst(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        address protectedShareToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        uint256 balanceOfProtectedSharesBefore = protectedShareToken.balanceOf(e, borrower);
        uint256 balanceCollateralSharesBefore = collateralSilo.balanceOf(e, borrower);

        //function call
        liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 balanceOfProtectedSharesAfter = protectedShareToken.balanceOf(e, borrower);
        uint256 balanceCollateralSharesAfter = collateralSilo.balanceOf(e, borrower);

        //asserts
        assert balanceOfProtectedSharesAfter > 0 => balanceCollateralSharesAfter == balanceCollateralSharesBefore;   
    }
    
    // ---------------------------------other user	
    
    // 	liquidationCall() no balances for other user changes if user is not msg.sender, _borrower or silo
    rule balanceOfOtherUserDoesNotChange(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        address otherUser;
        nonSceneAddressRequirements(otherUser);
        threeUsersNotEqual(e.msg.sender, borrower, otherUser);

        //values before
        uint256 balanceCollateralShares0Before = silo0.balanceOf(e, otherUser);
        uint256 balanceOfProtectedShares0Before = shareProtectedCollateralToken0.balanceOf(e, otherUser);
        uint256 balanceDebtShares0Before = shareDebtToken0.balanceOf(e, otherUser);
        uint256 balanceToken0Before = token0.balanceOf(e, otherUser);
        uint256 balanceCollateralShares1Before = silo1.balanceOf(e, otherUser);
        uint256 balanceOfProtectedShares1Before = shareProtectedCollateralToken1.balanceOf(e, otherUser);
        uint256 balanceDebtShares1Before = shareDebtToken1.balanceOf(e, otherUser);
        uint256 balanceToken1Before = token1.balanceOf(e, otherUser);

        //function call
        liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceCollateralShares0After = silo0.balanceOf(e, otherUser);
        uint256 balanceOfProtectedShares0After = shareProtectedCollateralToken0.balanceOf(e, otherUser);
        uint256 balanceDebtShares0After = shareDebtToken0.balanceOf(e, otherUser);
        uint256 balanceToken0After = token0.balanceOf(e, otherUser);
        uint256 balanceCollateralShares1After = silo1.balanceOf(e, otherUser);
        uint256 balanceOfProtectedShares1After = shareProtectedCollateralToken1.balanceOf(e, otherUser);
        uint256 balanceDebtShares1After = shareDebtToken1.balanceOf(e, otherUser);
        uint256 balanceToken1After = token1.balanceOf(e, otherUser);

        //asserts
        assert balanceCollateralShares0Before == balanceCollateralShares0After;
        assert balanceOfProtectedShares0Before == balanceOfProtectedShares0After;
        assert balanceDebtShares0Before == balanceDebtShares0After;
        assert balanceToken0Before == balanceToken0After;
        assert balanceCollateralShares1Before == balanceCollateralShares1After;
        assert balanceOfProtectedShares1Before == balanceOfProtectedShares1After;
        assert balanceDebtShares1Before == balanceDebtShares1After;
        assert balanceToken1Before == balanceToken1After;
    }        
    
    // ---------------------------------msg.sender	
    
    // 	liquidationCall() _receiveSToken == false => balance collateralToken for msg.sender increases by withdrawCollateral
    rule balanceCollateralTokenForMsgSenderIncreasesByWithdrawCollateral(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        address msgSender = e.msg.sender;

        //setup
        setupLiquidationRules(e, borrower);
        require !receiveSToken;

        //values before
        uint256 balanceCollateralTokenBefore = collateralAsset.balanceOf(e, msgSender);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceCollateralTokenAfter = collateralAsset.balanceOf(e, msgSender);

        //asserts
        assert balanceCollateralTokenAfter == balanceCollateralTokenBefore + withdrawCollateral;
    }
    
    // 	liquidationCall() _receiveSToken == false => collateralShare of msg.sender do not change
    rule collateralShareOfMsgSenderDoesNotChange(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        address msgSender = e.msg.sender;

        //setup
        require !receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 balanceCollateralSharesBefore = collateralSilo.balanceOf(e, msgSender);
        address protectedShareToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        uint256 balanceOfProtectedSharesBefore = protectedShareToken.balanceOf(e, msgSender);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceCollateralSharesAfter = collateralSilo.balanceOf(e, msgSender);
        uint256 balanceOfProtectedSharesAfter = protectedShareToken.balanceOf(e, msgSender);

        //asserts
        assert balanceCollateralSharesAfter == balanceCollateralSharesBefore;
        assert balanceOfProtectedSharesAfter == balanceOfProtectedSharesBefore;
    }
    
    // 	liquidationCall() _receiveSToken == true => msg.sender balances of collateralShares increase (sum of both)
    rule msgSenderBalancesOfCollateralSharesIncreaseSumOfBoth(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        address msgSender = e.msg.sender;

        //setup
        setupLiquidationRules(e, borrower);
        borrowerHasOnlyProtectedShares(e, borrower);
        require receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 balanceCollateralSharesBefore = collateralSilo.balanceOf(e, msgSender);
        address protectedShareToken = siloConfig.getConfig(e, collateralSilo).protectedShareToken;
        uint256 balanceOfProtectedSharesBefore = protectedShareToken.balanceOf(e, msgSender);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceCollateralSharesAfter = collateralSilo.balanceOf(e, msgSender);
        uint256 balanceOfProtectedSharesAfter = protectedShareToken.balanceOf(e, msgSender);

        //asserts
        assert balanceCollateralSharesAfter == balanceCollateralSharesBefore;
        assert balanceOfProtectedSharesAfter > balanceOfProtectedSharesBefore;
    }
    
    // 	liquidationCall() _debtAsset balance of msg.sender decreases by repayDebtAssets 
    rule debtAssetBalanceOfMsgSenderDecreasesByRepayDebtAssets(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        address msgSender = e.msg.sender;

        //setup
        setupLiquidationRules(e, borrower);


        //values before
        uint256 balanceDebtAssetBefore = debtAsset.balanceOf(e, msgSender);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceDebtAssetAfter = debtAsset.balanceOf(e, msgSender);

        //asserts
        assert balanceDebtAssetAfter == balanceDebtAssetBefore - repayDebtAssets;
    }

    // --------------------------------- debtSilo	
    
    // 	liquidationCall() debtAssets in debtSilo are reduced by "repayDebtAssets"
    rule debtAssetsInDebtSiloAreReducedByRepayDebtAssets(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);

        //values before
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        uint256 debtAssetBefore;
        (_, _, _, _, debtAssetBefore) = debtSilo.getSiloStorage(e);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 debtAssetAfter;
        (_, _, _, _, debtAssetAfter) = debtSilo.getSiloStorage(e);

        //asserts
        assert debtAssetAfter == debtAssetBefore - repayDebtAssets;
    }
    
    // 	liquidationCall() _debtAsset(underlyingToken) balance of silo increases by repayDebtAssets
    rule debtTokenBalanceOfSiloIncreasesByRepayDebtAssets(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        setupLiquidationRules(e, borrower);

        //setup

        //values before
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        uint256 balanceUnderlyingTokenBefore = debtAsset.balanceOf(e, debtSilo);

        //function call
        uint256 withdrawCollateral; 
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);    

        //values after
        uint256 balanceUnderlyingTokenAfter = debtAsset.balanceOf(e, debtSilo);

        //asserts
        assert balanceUnderlyingTokenAfter == balanceUnderlyingTokenBefore + repayDebtAssets;
    }

    // --------------------------------- colateralSilo	
    
    // 	liquidationCall() _receiveSToken == false => balance collateralToken for collateralSilo decreases by withdrawCollateral
    rule balanceCollateralTokenForCollateralSiloDecreasesByWithdrawCollateral(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        setupLiquidationRules(e, borrower);
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        require !receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 balanceCollateralTokenBefore = collateralAsset.balanceOf(e, collateralSilo);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 balanceCollateralTokenAfter = collateralAsset.balanceOf(e, collateralSilo);

        //asserts
        assert balanceCollateralTokenAfter == balanceCollateralTokenBefore - withdrawCollateral;
    }
    
    // 	liquidationCall() _receiveSToken == false => collateralAssets for collateralSilo decreases by withdrawCollateral
    rule collateralAssetsForCollateralSiloDecreaseByWithdrawCollateral(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        borrowerHasOnlyProtectedShares(e, borrower);
        require !receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 protectedAssetsBefore;
        (_, _, protectedAssetsBefore, _, _) = collateralSilo.getSiloStorage(e);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 protectedAssetsAfter;
        (_, _, protectedAssetsAfter, _, _) = collateralSilo.getSiloStorage(e);

        //asserts
        assert protectedAssetsAfter == protectedAssetsBefore - withdrawCollateral;
    }

    // 	liquidationCall() _receiveSToken == true => no balance of collateralAsset changes
    rule collateralAssetsSiloDoNotChange(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        
        //setup
        setupLiquidationRules(e, borrower);
        borrowerHasOnlyProtectedShares(e, borrower);
        require receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 protectedAssetsBefore;
        uint256 collateralAssetsBefore;
        (_, _, protectedAssetsBefore, collateralAssetsBefore, _) = collateralSilo.getSiloStorage(e);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 protectedAssetsAfter;
        uint256 collateralAssetsAfter;
        (_, _, protectedAssetsAfter, collateralAssetsAfter, _) = collateralSilo.getSiloStorage(e);

        //asserts
        assert collateralAssetsAfter == collateralAssetsBefore;
        assert protectedAssetsAfter == protectedAssetsBefore;
    }
    
    
    // 	liquidationCall() _receiveSToken == true => collateralAssets of collateralSilo stays the same
    rule noBalanceOfCollateralAssetChanges(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        borrowerHasOnlyProtectedShares(e, borrower);
        require receiveSToken;

        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        uint256 balanceCollateralTokenBefore = collateralAsset.balanceOf(e, collateralSilo);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 balanceCollateralTokenAfter = collateralAsset.balanceOf(e, collateralSilo);

        //asserts
        assert balanceCollateralTokenAfter == balanceCollateralTokenBefore;
    }
    
    // --------------------------------- general	
    
    //using the result of maxLiquidation to call liquidationCall should never revert
    // liquidationCall() msg.sender never pays more than _maxDebtToConvert
    rule msgSenderNeverPaysMoreThanMaxDebtToConvert(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);

        //values before
        uint256 senderBalanceToken0Before = token0.balanceOf(e.msg.sender);

        //function call
        liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 senderBalanceToken0After = token0.balanceOf(e.msg.sender);

        //asserts
        assert senderBalanceToken0After >= senderBalanceToken0Before - maxDebtToCover;
    }
    // liquidationCall() revert if borrower solvent
    rule revertIfBorrowerSolvent(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        require silo0.isSolvent(e, borrower);

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //call reverted
        assert lastReverted;
    }

    // liquidationCall() only specific values in the debt silo change //@audit can be split if it times out
    rule onlySpecificValuesInDebtSiloChange(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        
        //values before
        address debtSilo = siloConfig.getDebtSilo(e, borrower);

        address protectedTokenDebtSilo;
        uint256 protectedAssetsDebtSiloBefore;
        (protectedTokenDebtSilo, protectedAssetsDebtSiloBefore) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Protected);
        
        address collateralTokenDebtSilo;
        uint256 collateralAssetsDebtSiloBefore;
        (collateralTokenDebtSilo, collateralAssetsDebtSiloBefore) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Collateral);
        
        address debtShareTokenDebtSilo;
        uint256 debtAssetsDebtSiloBefore;
        (debtShareTokenDebtSilo, debtAssetsDebtSiloBefore) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Debt);
        
        address underlyingTokenDebtSilo = siloConfig.getConfig(e, debtSilo).token;
        uint256 balanceUnderlyingTokenBefore = underlyingTokenDebtSilo.balanceOf(e, debtSilo);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 protectedAssetsDebtSiloAfter;
        (_, protectedAssetsDebtSiloAfter) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Protected);
        uint256 collateralAssetsDebtSiloAfter;
        (_, collateralAssetsDebtSiloAfter) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Collateral);
        uint256 debtAssetsDebtSiloAfter;
        (_, debtAssetsDebtSiloAfter) = debtSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Debt);
        uint256 balanceUnderlyingTokenAfter = underlyingTokenDebtSilo.balanceOf(e, debtSilo);

        //asserts
        assert protectedAssetsDebtSiloAfter == protectedAssetsDebtSiloBefore;
        assert collateralAssetsDebtSiloAfter == collateralAssetsDebtSiloBefore;
        assert debtAssetsDebtSiloAfter == debtAssetsDebtSiloBefore - repayDebtAssets;
        assert balanceUnderlyingTokenAfter == balanceUnderlyingTokenBefore + repayDebtAssets;
    }

    // liquidationCall() only specific values in the collateral silo change //@audit can be split if it times out
    rule onlySpecificValuesInCollateralSiloChange(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        setupLiquidationRules(e, borrower);
        
        //values before
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);

        address protectedTokencollateralSilo;
        uint256 protectedAssetscollateralSiloBefore;
        (protectedTokencollateralSilo, protectedAssetscollateralSiloBefore) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Protected);
        
        address collateralTokencollateralSilo;
        uint256 collateralAssetscollateralSiloBefore;
        (collateralTokencollateralSilo, collateralAssetscollateralSiloBefore) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Collateral);
        
        address debtShareTokencollateralSilo;
        uint256 debtAssetscollateralSiloBefore;
        (debtShareTokencollateralSilo, debtAssetscollateralSiloBefore) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Debt);
        
        address underlyingTokencollateralSilo = siloConfig.getConfig(e, collateralSilo).token;
        uint256 balanceUnderlyingTokenBefore = underlyingTokencollateralSilo.balanceOf(e, collateralSilo);

        //function call
        uint256 withdrawCollateral;
        uint256 repayDebtAssets;
        (withdrawCollateral, repayDebtAssets) = liquidationCall(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);

        //values after
        uint256 protectedAssetscollateralSiloAfter;
        (_, protectedAssetscollateralSiloAfter) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Protected);
        uint256 collateralAssetscollateralSiloAfter;
        (_, collateralAssetscollateralSiloAfter) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Collateral);
        uint256 debtAssetscollateralSiloAfter;
        (_, debtAssetscollateralSiloAfter) = collateralSilo.getTokenAndAssetsDataHarness(e, ISilo.AssetType.Debt);
        uint256 balanceUnderlyingTokenAfter = underlyingTokencollateralSilo.balanceOf(e, collateralSilo);

        //asserts
        assert protectedAssetscollateralSiloAfter <= protectedAssetscollateralSiloBefore;
        assert collateralAssetscollateralSiloAfter <= collateralAssetscollateralSiloBefore;
        assert debtAssetscollateralSiloAfter == debtAssetscollateralSiloBefore;
        assert balanceUnderlyingTokenAfter <= balanceUnderlyingTokenBefore;
    }




    // //@audit-issue ganaue berechnungen der Werte fehlen




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

    // 	liquidationCall() reverts if _maxDebtToConvert == 0
    rule revertIfMaxDebtToConvertIsZero(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        require maxDebtToCover == 0;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted
        assert lastReverted;        
    }
    
    // 	liquidationCall() reverts if debtSilo of borrower == 0
    rule revertIfDebtSiloIsZero(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;
        require siloConfig.getDebtSilo(e, borrower) == 0;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted
        assert lastReverted;        
    }
    
    // 	liquidationCall() reverts if _collateralAsset is not the asset of the collateralSilo
    rule revertIfCollateralAssetIsNotTheAssetOfCollateralSilo(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        address collateralSilo = siloConfig.borrowerCollateralSilo(e, borrower);
        address underlyingToken = siloConfig.getConfig(e, collateralSilo).token;
        require underlyingToken != collateralAsset;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted
        assert lastReverted;        
    }
    
    // 	liquidationCall() reverts if the _debtAsset is not the asset in the debtSilo
    rule revertIfDebtAssetIsNotTheAssetInDebtSilo(env e){
        configForEightTokensSetupRequirements();
        address collateralAsset;
        address debtAsset;
        address borrower;
        uint256 maxDebtToCover;
        bool receiveSToken;

        //setup
        address debtSilo = siloConfig.getDebtSilo(e, borrower);
        address underlyingToken = siloConfig.getConfig(e, debtSilo).token;
        require underlyingToken != debtAsset;

        //function call
        liquidationCall@withrevert(e, collateralAsset, debtAsset, borrower, maxDebtToCover, receiveSToken);
        
        //call reverted
        assert lastReverted;        
    }
    
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


