// SPDX-License-Identifier: MIT
pragma solidity 0.6.12;

interface ILendingPoolAddressesProvider {
    function getLendingPool() external view returns (address);

    function getAddress(bytes32 id) external view returns (address);
}
