// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/**
 * @title Simple Vault for Bug Injection Testing
 * @notice This is a target contract for the sanad-mutator-poc.
 * The goal is to see if we can automatically remove the onlyOwner 
 * modifier via AST pruning.
 */
contract Vault {
    address public owner;
    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // TARGET: The mutator script will try to remove the 'onlyOwner' 
    // modifier from this specific function.
    function withdraw() public onlyOwner {
        uint256 amount = address(this).balance;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    receive() external payable {}
}
