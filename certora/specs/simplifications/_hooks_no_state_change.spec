methods {

    function _.synchronizeHooks(uint24,uint24) external 
            => synchronizeHooks__noStateChange() expect void;
    function _.hookReceiverConfig(address) external 
            => hookReceiverConfig__noStateChange() expect void;
    function _.reentrancyGuardEntered() external 
            => reentrancyGuardEntered__noStateChange() expect void;

   

}

function synchronizeHooks__noStateChange() {
   // no state change but needed to avoid DEVAULT HAVOC
}

function hookReceiverConfig__noStateChange() {
   // no state change but needed to avoid DEVAULT HAVOC
}

function reentrancyGuardEntered__noStateChange() {
   // no state change but needed to avoid DEVAULT HAVOC
}