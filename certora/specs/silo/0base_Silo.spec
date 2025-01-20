/////////////////// METHODS START ///////////////////////
methods{
   function _.totalSupply() external envfree; 
   function _.balanceOf(address user) external envfree; 
   function _.allowance(address owner, address spender) external envfree;
   function _.silo() external envfree;
}
//add all view functions to methodes and make them envfree

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////
// definition HARNESS_VIEW_METHODS(method f) returns bool 
//    = HARNESS_METHODS(f) || f.isView;"
   //definition HARNESS_METHODS(method f) returns bool = 
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
