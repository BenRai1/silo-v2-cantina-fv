// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ShareDebtToken} from "silo-core/contracts/utils/ShareDebtToken.sol";
import {IShareToken} from "silo-core/contracts/interfaces/IShareToken.sol";
import {ShareTokenLib} from "silo-core/contracts/lib/ShareTokenLib.sol";

contract ShareDebtToken0 is ShareDebtToken { //@audit fixed version for issue #1

    
    function getTransferWithChecks() external view returns (bool) {
        IShareToken.ShareTokenStorage storage $ = ShareTokenLib.getShareTokenStorage();
        return $.transferWithChecks;
    }


    function _spendReceiverAllowance(address owner, address spender, uint256 value) internal virtual {
    uint256 currentReceiverAllowance = _receiveAllowance(owner, spender);
    if (currentReceiverAllowance!= type(uint256).max) {
        if (currentReceiverAllowance < value) {
            revert ERC20InsufficientAllowance(spender, currentReceiverAllowance, value);
        }
            unchecked {
                _setReceiveApproval(owner, spender, currentReceiverAllowance - value);
            }
        }
    }

    function mint(address _owner, address _spender, uint256 _amount) external virtual override onlySilo {
    if (_owner != _spender) _spendReceiverAllowance(_owner, _spender, _amount);
        _mint(_owner, _amount);
    }

}
