methods {
    function Silo._accrueInterest()
        internal
        returns (uint256) => accrueInterest_noStateChange();

    function Silo._accrueInterestForAsset(address _interestRateModel, uint256 _daoFee, uint256 _deployerFee)
        internal
        returns (uint256) => accrueInterestForAsset_noStateChange(_interestRateModel, _daoFee, _deployerFee);

    function _.getCompoundInterestRate(address, uint256) external => getCompoundInterestRate_noStateChange() expect void;
}

function accrueInterest_noStateChange() returns uint256 {
    uint256 anyInterest;

    return (anyInterest);
}

function accrueInterestForAsset_noStateChange(address _interestRateModel, uint256 _daoFee, uint256 _deployerFee)
    returns uint256
{
    uint256 anyInterest;
    return anyInterest;
}

function getCompoundInterestRate_noStateChange() {}
