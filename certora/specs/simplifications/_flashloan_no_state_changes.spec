methods {

    function _.onFlashLoan(address, address, uint256, uint192, bytes) external 
            => onFlashLoan__noStateChange() expect void;

   

}

function onFlashLoan__noStateChange() {
   // no state change but needed to avoid DEVAULT HAVOC
}