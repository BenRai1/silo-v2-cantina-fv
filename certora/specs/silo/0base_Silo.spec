/////////////////// METHODS START ///////////////////////
methods{
   function _.totalSupply() external envfree; 
   function _.balanceOf(address user) external envfree; 
   function _.allowance(address owner, address spender) external envfree;
   function _.silo() external envfree;
   function silo1.totalAssetsHarness() external returns (uint256, uint256, uint256)envfree;
   function borrowerCollateralSiloHarness(address) external returns (address) envfree;
   function ltvBelowMaxLtvHarness(address) external returns (bool) envfree;
   function shareDebtToken0.receiveAllowance(address,address) external returns (uint256) envfree;
   function shareDebtToken1.receiveAllowance(address,address) external returns (uint256) envfree;
}
//add all view functions to methodes and make them envfree

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////
   definition HARNESS_METHODS(method f) returns bool = 
      f.selector == sig:getSiloDataInterestRateTimestamp().selector ||
      f.selector == sig:getSiloDataDaoAndDeployerRevenue().selector ||
      f.selector == sig:getFlashloanFee0().selector ||
      f.selector == sig:reentrancyGuardEntered().selector ||
      f.selector == sig:getDaoFee().selector ||
      f.selector == sig:getDeployerFee().selector ||
      f.selector == sig:getLTV(address).selector ||
      f.selector == sig:getAssetsDataForLtvCalculations(address).selector ||
      f.selector == sig:getTransferWithChecks().selector ||
      f.selector == sig:getSiloFromStorage().selector ||
      f.selector == sig:totalAssetsHarness().selector ||
      f.selector == sig:borrowerCollateralSiloHarness(address).selector ||
      f.selector == sig:ltvBelowMaxLtvHarness(address).selector;









// definition HARNESS_VIEW_METHODS(method f) returns bool 
//    = HARNESS_METHODS(f) || f.isView;"
  //  f.selector == sig:evcCompatibleAsset().selector
  //  || f.selector == sig:isKnownNonOwnerAccountHarness(address).selector"
//creat a definiton which holds all view
//use definitions for cluster of functions
///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////

////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
