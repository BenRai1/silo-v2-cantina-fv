/* Verifies the protocol allows anyone user access 
 * This setup is for a single silo - `Silo0`
 */

import "../setup/single_silo_tokens_requirements.spec";
import "../setup/summaries/silo0_summaries.spec";
import "../setup/summaries/siloconfig_dispatchers.spec";
import "../setup/summaries/config_for_one_in_cvl.spec";
import "../setup/summaries/safe-approximations.spec";
import "./0base_Silo.spec";

methods {
    // ---- `SiloConfig` -------------------------------------------------------
    // `envfree`
    function SiloConfig.accrueInterestForSilo(address) external envfree;
    function SiloConfig.getCollateralShareTokenAndAsset(
        address,
        ISilo.CollateralType
    ) external returns (address, address) envfree;

    // ---- `IInterestRateModel` -----------------------------------------------
    // Since `getCompoundInterestRateAndUpdate` is not *pure*, this is not strictly sound.
    function _.getCompoundInterestRateAndUpdate(
        uint256 _collateralAssets,
        uint256 _debtAssets,
        uint256 _interestRateTimestamp
    ) external =>  CVLGetCompoundInterestRate(
        _collateralAssets,
        _debtAssets,
        _interestRateTimestamp
    ) expect (uint256);
    
    // TODO: Is this sound?
    function _.getCompoundInterestRate(
        address _silo,
        uint256 _blockTimestamp
    ) external => CVLGetCompoundInterestRateForSilo(_silo, _blockTimestamp) expect (uint256);

    // ---- `ISiloOracle` ------------------------------------------------------
    // NOTE: Since `beforeQuote` is not a view function, strictly speaking this is unsound.
    function _.beforeQuote(address) external => NONDET DELETE;
}

// ---- Functions and ghosts START ---------------------------------------------------

    ghost mapping(uint256 => mapping(uint256 => mapping(uint256 => uint256))) interestGhost;

    // @title An arbitrary (pure) function for the interest rate
    function CVLGetCompoundInterestRate(
        uint256 _collateralAssets,
        uint256 _debtAssets,
        uint256 _interestRateTimestamp
    ) returns uint256 {
        return interestGhost[_collateralAssets][_debtAssets][_interestRateTimestamp];
    }


    ghost mapping(address => mapping(uint256 => uint256)) interestGhostSilo;

    // @title An arbitrary (pure) function for the interest rate 
    function CVLGetCompoundInterestRateForSilo(
        address _silo,
        uint256 _blockTimestamp
    ) returns uint256 {
        return interestGhostSilo[_silo][_blockTimestamp];
    }


    // @title Require that the second env has at least as much allowance and balance as first
    function requireSecondEnvAtLeastAsFirst(env e1, env e2) {
        /// At least as much allowance as first `env`
        require (
            token0.allowance(e2, e2.msg.sender, silo0) >=
            token0.allowance(e1, e1.msg.sender, silo0)
        );
        /// At least as much balance as first `env`
        require token0.balanceOf(e2, e2.msg.sender) >= token0.balanceOf(e1, e1.msg.sender);
    }

// ---- Functions and ghosts END ---------------------------------------------------

//------------------------------- RULES TEST START ----------------------------------





    //only specific functions can change the ballance of a user
    rule onlySpecificFunctionsCanChangeBalanceOfUser(env e, method f, calldataarg args) filtered{f-> !f.isView} {
        address user;
        uint256 balanceBefore = silo0.balanceOf(user);

        f(e, args);

        uint256 balanceAfter = silo0.balanceOf(user);

        assert(balanceBefore != balanceAfter =>
                f.selector == sig:burn(address,address,uint256).selector || 
                f.selector == sig:withdraw(uint256,address,address).selector ||
                f.selector == sig:redeem(uint256,address,address).selector ||
                f.selector == sig:deposit(uint256,address).selector ||
                f.selector == sig:mint(uint256,address).selector ||
                f.selector == sig:mint(address,address,uint256).selector ||
                f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector || 
                f.selector == sig:deposit(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:mint(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:transitionCollateral(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector || 
                f.selector == sig:transfer(address,uint256).selector || 
                f.selector == sig:transferFrom(address,address,uint256).selector || 
                f.selector == sig:forwardTransferFromNoChecks(address,address,uint256).selector || 
                f.selector == sig:callOnBehalfOfSilo(address,uint256,ISilo.CallType,bytes).selector
        );
    }

    //only user or address with allowance can redeem shares
    rule onlyUserOrAllowanceCanRedeemOrWithdrawShares(env e, ) filtered{f-> 
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector        
    } {
        address amountAsset;
        address owner;
        uint256 allowanceMsgSender = Silo0.allowance(owner, e.msg.sender);
        uint256 sharesBefore = silo0.balanceOf(owner);

        redeem(e, asset, receiver, owner)
        

        f(e, args);

        uint256 sharesAfter = silo0.balanceOf(user);
        uint256 redeemedShares = sharesBefore - sharesAfter;

        assert(sharesBefore != sharesAfter => e.msg.sender == user || allowanceMsgSender >= redeemedShares);
    }
        
    //balacenOfAndTotalSupply returns the right values
    rule balanceOfAndTotalSupplyWorks(env e) {
        address user;
        uint256 balance = silo0.balanceOf(user);
        uint256 totalSupply = silo0.totalSupply();

        uint256 balanceResult;
        uint256 totalSupplyResult;
        (balanceResult, totalSupplyResult) = silo0.balanceOfAndTotalSupply(e,user);

        assert balance == balanceResult && totalSupply == totalSupplyResult;
    }

    //callOnBehalfOfSilo can only be called by hookReceiver



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    //only Silo can call mint and burn
    rule onlySiloCanCallMintAndBurn(env e, method f, calldataarg args) filtered{f->
        f.selector == sig:mint(address,address,uint256).selector || 
        f.selector == sig:burn(address,address,uint256).selector} {
        
        f(e, args);

        assert e.msg.sender == getSiloFromStorage(e);
    }

    //only specific functions can change the total supply
    rule onlySpecificFunctionsCanChangeTotalSupply(env e, method f, calldataarg args) filtered{f-> !f.isView} {
        uint256 totalSupplyBefore = silo0.totalSupply();

        f(e, args);

        uint256 totalSupplyAfter = silo0.totalSupply();

        assert(totalSupplyBefore != totalSupplyAfter => 
                f.selector == sig:burn(address,address,uint256).selector || 
                f.selector == sig:withdraw(uint256,address,address).selector ||
                f.selector == sig:redeem(uint256,address,address).selector ||
                f.selector == sig:deposit(uint256,address).selector ||
                f.selector == sig:mint(uint256,address).selector ||
                f.selector == sig:mint(address,address,uint256).selector ||
                f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector || 
                f.selector == sig:deposit(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:mint(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:transitionCollateral(uint256,address,ISilo.CollateralType).selector ||
                f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector || 
                f.selector == sig:callOnBehalfOfSilo(address,uint256,ISilo.CallType,bytes).selector 
        );
    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

//-------------------------------OLD RULES START----------------------------------



    // ---- Rules ------------------------------------------------------------------

    /// @title For testing the setup
    rule sanityWithSetup_borrow() {
        calldataarg args;
        env e; 
        configForEightTokensSetupRequirements();
        nonSceneAddressRequirements(e.msg.sender);
        silosTimestampSetupRequirements(e);
        silo0.borrow(e, args);
        satisfy true;
    }

    /// @title If a user may deposit some amount, any other user also may
    /// @property user-access
    rule RA_anyone_may_deposit(env e1, env e2, address recipient, uint256 amount) {
        /// Assuming same context (time and value).
        require e1.block.timestamp == e2.block.timestamp;
        require e1.msg.value == e2.msg.value;

        // Block time-stamp >= interest rate time-stamp
        silosTimestampSetupRequirements(e1);
        silosTimestampSetupRequirements(e2);

        // Conditions necessary that `e2` will not revert if `e1` did not
        requireSecondEnvAtLeastAsFirst(e1, e2);

        storage initState = lastStorage;
        deposit(e1, amount, recipient);
        deposit@withrevert(e2, amount, recipient) at initState;

        assert e2.msg.sender != 0 => !lastReverted;
    }

    /// @title If one user can repay some borrower's debt, any other user also can
    /// @property user-access
    rule RA_anyone_may_repay(env e1, env e2, uint256 amount, address borrower) {
        /// Assuming same context (time and value).
        require e1.block.timestamp == e2.block.timestamp;
        require e1.msg.value == e2.msg.value;

        // Block time-stamp >= interest rate time-stamp
        silosTimestampSetupRequirements(e1);
        silosTimestampSetupRequirements(e2);

        // Conditions necessary that `e2` will not revert if `e1` did not
        requireSecondEnvAtLeastAsFirst(e1, e2);

        storage initState = lastStorage;
        repay(e1, amount, borrower);
        repay@withrevert(e2, amount, borrower) at initState;

        assert e2.msg.sender != 0 => !lastReverted;
    }


    /// @title The deposit recipient is not discriminated
    /// @property user-access
    rule RA_deposit_recipient_is_not_restricted(address user1, address user2, uint256 amount) {
        env e;

        storage initState = lastStorage;
        deposit(e, amount, user1);
        deposit@withrevert(e, amount, user2) at initState;

        assert user2 !=0 => !lastReverted;
    }

    /// @title The repay action of a borrower is not discriminated (by shares)
    /// @property user-access
    rule RA_repay_borrower_is_not_restricted_by_shares(
        address borrower1,
        address borrower2,
        uint256 amount
    ) {
        env e;
        require borrower2 != 0;

        // Get the borrowers debts
        uint256 debt1 = shareDebtToken0.balanceOf(e, borrower1);
        uint256 debt2 = shareDebtToken0.balanceOf(e, borrower2);
        require debt2 >= debt1;

        storage initState = lastStorage;
        repay(e, amount, borrower1);
        repay@withrevert(e, amount, borrower2) at initState;


        // The repaid amount is less than the borrower's debt, hence the operation must succeed.
        assert !lastReverted;
    }
//-------------------------------OLD RULES END----------------------------------





