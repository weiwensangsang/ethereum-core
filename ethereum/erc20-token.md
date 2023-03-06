# ERC 20

Let us try to build a homogeneous token!

A homogeneous token (ERC-20) is a token created on the Ethereum (Ethereum) blockchain. Each token is exactly the same on the blockchain and has the same value and attributes. For example, if you buy 10 ERC-20 tokens, the tokens are the same, there is no difference.

Non-homogeneous tokens (NFTs) are different. Each NFT is unique, unique, and has unique attributes and values. For example, a piece of digital artwork could be an NFT that has a unique design, time of creation, and artist information, attributes that set it apart from other NFTs or tokens.

As another example, a real estate developer could use NFTs to represent their real estate projects. Each NFT represents a unique real estate unit with unique attributes such as location, floor area, style, design and selling price.

In conclusion, fungible tokens are fungible and indistinguishable, while non-fungible tokens are unique, each with its own value and attributes.

**In fact, before the launch of NFT, all tokens are homogeneous.**



```go
contract ERC20Interface {

    string public constant name = "Token Name";
    string public constant symbol = "SYM";
    uint8 public constant decimals = 18;  // 18 is the most common number of decimal places

    function totalSupply() public constant returns (uint);
    function balanceOf(address tokenOwner) public constant returns (uint balance);
    function allowance(address tokenOwner, address spender) public constant returns (uint remaining);
    function transfer(address to, uint tokens) public returns (bool success);
    function approve(address spender, uint tokens) public returns (bool success);
    function transferFrom(address from, address to, uint tokens) public returns (bool success);

    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
```



Let us see how Tether (USDT) built  by smart contract.



### Tether(USDT)

Form this url https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7#code

By the way, smart contracts themselves cannot be changed - once deployed to the blockchain, they are immutable.
But there can be one or more smart contracts running together, some of which can act as "backends". In this way, we can upgrade the interaction mode between these smart contracts. Here, upgrading a smart contract does not mean modifying the code of a deployed smart contract, but replacing one of the smart contracts with another. We do this in such a way that (in most cases) the end user doesn't have to change how they interact with the dApp.

So the real upgrading of smart contracts is a process in which new smart contracts replace old smart contracts. When the new smart contract is used, the old smart contract will be "abandoned" on the chain, because the old contract is immutable.



USDT needs to have the following functions

1. Functions of transfer, balance inquiry and authorized consumption under ERC20 requirements
2. Token emergency suspension and restart
3. Token User Blacklist
4. The contract is conveniently upgraded and can be adapted to non-ERC20 protocol tokens
5. Token manager authority transfer

```solidity
/**
 *Submitted for verification at Etherscan.io on 2017-11-28
*/

pragma solidity ^0.4.17;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
    ...
}

/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
    address public owner;

    ...

    /**
    * @dev Allows the current owner to transfer control of the contract to a newOwner.
    * @param newOwner The address to transfer ownership to.
    */
    function transferOwnership(address newOwner) public onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner; // give this contract to another account
        }
    }

}

/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20Basic {
    ...;
}

/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20 is ERC20Basic {
   ...;
}

/**
 * @title Basic token
 * @dev Basic version of StandardToken, with no allowances.
 */
contract BasicToken is Ownable, ERC20Basic {
    using SafeMath for uint;

    mapping(address => uint) public balances; // This is balacne Db

    // additional variables for use if transaction fees ever became necessary
    uint public basisPointsRate = 0;
    uint public maximumFee = 0;

    /**
    * @dev Fix for the ERC20 short address attack.
    */
    modifier onlyPayloadSize(uint size) {
        require(!(msg.data.length < size + 4));
        _;
    }

    /**
    * @dev transfer token for a specified address
    * @param _to The address to transfer to.
    * @param _value The amount to be transferred.
    */
    function transfer(address _to, uint _value) public onlyPayloadSize(2 * 32) {
        uint fee = (_value.mul(basisPointsRate)).div(10000);
        if (fee > maximumFee) {
            fee = maximumFee;
        }
        uint sendAmount = _value.sub(fee);
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(sendAmount);
        if (fee > 0) {
            balances[owner] = balances[owner].add(fee);
            Transfer(msg.sender, owner, fee);
        }
        Transfer(msg.sender, _to, sendAmount);
    }

    /**
    * @dev Gets the balance of the specified address.
    * @param _owner The address to query the the balance of.
    * @return An uint representing the amount owned by the passed address.
    */
    function balanceOf(address _owner) public constant returns (uint balance) {
        return balances[_owner];
    }

}

/**
 * @title Standard ERC20 token
 *
 * @dev Implementation of the basic standard token.
 * @dev https://github.com/ethereum/EIPs/issues/20
 * @dev Based oncode by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
 */
contract StandardToken is BasicToken, ERC20 {
   ...
}

...

contract TetherToken is Pausable, StandardToken, BlackList {

    string public name;
    string public symbol;
    uint public decimals;
    address public upgradedAddress; // We use this to update Smart Contract
    bool public deprecated;

    //  The contract can be initialized with a number of tokens
    //  All the tokens are deposited to the owner address
    //
    // @param _balance Initial supply of the contract
    // @param _name Token Name
    // @param _symbol Token symbol
    // @param _decimals Token decimals
    function TetherToken(uint _initialSupply, string _name, string _symbol, uint _decimals) public {
        _totalSupply = _initialSupply;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        balances[owner] = _initialSupply; // Owner Get All Token!
        deprecated = false;
    }

    ...
}
```



Tether claims that it will strictly abide by the 1:1 reserve guarantee. For every USDT token issued, its bank account will have 1 dollar of funds as a guarantee.

We can see that Tether's smart contract has no constraints on its promises. And the smart contract of Tether currency can also be upgraded.
In theory, the owner of Tether can withdraw any amount of USDT from its account to exchange for US dollars, and it will not be discovered by anyone.

But we believe he won't. Because Tether has a noble and admirable moral bottom line. **Even if Tether does not have transparent financial audits and closed audits, it has never responded positively to everyone's doubts. .**