# Solidity



```solidity
pragma solidity ^0.4.21;

contract Coin {
    address public minter;
    mapping (address => uint) public balances;

    event Sent(address from, address to, uint amount);

    // when we create a contract, we call this.
    function Coin() public {
        minter = msg.sender;
    }

    // receiver and amount are from Calldata
    function mint(address receiver, uint amount) public {
        if (msg.sender != minter) return;
        balances[receiver] += amount;
    }

    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Sent(msg.sender, receiver, amount);
    }
}
```

1. When each smart contract is created, it will rely on a smart contract account.

2. Each smart contract account has a storage, which is a KV database. Minter and balances in the instance will enter it, and there is no clear maximum capacity limit for storage.

3. Every call to a smart contract function is equivalent to a transaction, and the transaction needs to be recorded in the block. The Ethereum blockchain can only produce one block at a time. This ensures orderliness.

4. Essentially any node can execute the function, which is concurrent. But only one execution result is recognized.

5. As long as it is a variable stored in storage, it can be obtained directly without executing the contract function.

6. Read-only Calldata changes the state of storage, which is the nature of most functions.

7. The payable function modifier enables Solidity contracts to accept payment in ether

8. When an error is reported in the middle of the execution of the function of the smart contract, the function state will automatically roll back to the state before the function execution to ensure that the state of the contract will not be modified to an invalid or inconsistent state.



### Global Variables

There are many predefined global variables in Solidity, here are some common ones:

1. msg.sender - contains the address of the caller of the current function, used to verify the identity of the caller.
2. msg.value - Contains the amount of ether sent by the caller of the current function for receiving ether in the smart contract.
3. now - the timestamp of the current block (in seconds), which can be used to get the current time in the smart contract.
4. block.timestamp - the timestamp (in seconds) of the current block, same as the now variable.
5. block.number - the block number of the current block.
6. address(this) - the address of the current smart contract, used to refer to itself in the smart contract.
7. tx.origin - Contains the sender address of the transaction, not the address of the calling contract. Normally, tx.origin should not be used to authenticate the caller.
8. gasleft() - contains how much gas is left in the current transaction, which can be used to determine the gas usage of the current transaction in the smart contract.

These global variables provide a convenient way to obtain various information in smart contracts, and can be used to write various types of smart contracts. However, they need to be used with care to avoid security holes and misbehavior.





### USDT



```solidity
/**
 *Submitted for verification at Etherscan.io on 2017-11-28
*/

pragma solidity ^0.4.17;
```

The pragma instructs to use a specific version of Solidity. ^0.4.17 means to use 0.4.17 and all latest versions that are upwardly compatible with that version, such as 0.4.18, 0.4.19, etc. If you declare a version with the "^" symbol, the compiler will automatically select the latest version that is upwardly compatible with the current Solidity compiler version for compilation.

```solidity
/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        // assert(b > 0); // Solidity automatically throws when dividing by 0
        uint256 c = a / b;
        // assert(a == b * c + a % b); // There is no case in which this doesn't hold
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
```



- `library`: Indicates that this is a Solidity library (library), used to implement reusable code modules, be careful using other people's libraries.
- `internal`: Indicates that this function can only be called inside the current contract or its inherited contracts, and cannot be called from outside the contract.
- `pure`: Indicates that this function will not modify the state of the contract, and will not access the storage variables of the contract, nor will it interact with other contracts.
- `returns`: indicates that this function will return one or more values.
- `assert`: Indicates that if the function execution fails, an exception will be thrown (that is, the assertion failed) to terminate the program execution.





```solidity
/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
    address public owner;

    /**
      * @dev The Ownable constructor sets the original `owner` of the contract to the sender
      * account.
      */
    function Ownable() public {
        owner = msg.sender;
    }

    /**
      * @dev Throws if called by any account other than the owner.
      */
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    /**
    * @dev Allows the current owner to transfer control of the contract to a newOwner.
    * @param newOwner The address to transfer ownership to.
    */
    function transferOwnership(address newOwner) public onlyOwner {
        if (newOwner != address(0)) {
            owner = newOwner;
        }
    }

}

/**
 * @title Pausable
 * @dev Base contract which allows children to implement an emergency stop mechanism.
 */
contract Pausable is Ownable {
  event Pause();
  event Unpause();

  bool public paused = false;


  /**
   * @dev Modifier to make a function callable only when the contract is not paused.
   */
  modifier whenNotPaused() {
    require(!paused);
    _;
  }

  /**
   * @dev Modifier to make a function callable only when the contract is paused.
   */
  modifier whenPaused() {
    require(paused);
    _;
  }

  /**
   * @dev called by the owner to pause, triggers stopped state
   */
  function pause() onlyOwner whenNotPaused public {
    paused = true;
    Pause();
  }

  /**
   * @dev called by the owner to unpause, returns to normal state
   */
  function unpause() onlyOwner whenPaused public {
    paused = false;
    Unpause();
  }
}
```

- `modifier` is used to define a reusable modifier function. A modifier is a special function that can be used to modify the behavior of a function, it can be added to the function definition to perform some logic checks or modifications on the function before or after the function is executed. Using modifiers can simplify your code, improve code readability, and reduce repetitive logic in your code.
- `event` is a special type in Solidity used to trigger notifications inside smart contracts. Events are a lightweight communication mechanism for making notifications within smart contracts and providing data to external applications. An application can listen to events and perform some actions when the event is triggered. Events are often used to record important activities and state changes in smart contracts so that applications can respond to these changes.
- `public` is a function access modifier in Solidity. Functions declared with the public keyword can be called by anyone, including addresses inside and outside the contract. State variables declared public can be read by anyone inside or outside the contract. It should be noted that public functions may affect the state of the contract, so security and logical correctness need to be carefully considered when writing public functions.
- The underscore `_` is often used as a placeholder to denote the position of a function or modifier parameter. In the function or modifier definition, the position of the underscore `_` will be replaced by the actual parameter. For example, here's a simple example using underscores:
- Require is an exception handling mechanism, which is used to check whether certain conditions are met during function execution. If the conditions are not met, the function execution is terminated and all states during the execution process are restored to the state before the function call. `
- The is keyword is used to indicate inheritance





```solidity

/**
 * @title ERC20Basic
 * @dev Simpler version of ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20Basic {
    uint public _totalSupply;
    function totalSupply() public constant returns (uint);
    function balanceOf(address who) public constant returns (uint);
    function transfer(address to, uint value) public;
    event Transfer(address indexed from, address indexed to, uint value);
}

/**
 * @title ERC20 interface
 * @dev see https://github.com/ethereum/EIPs/issues/20
 */
contract ERC20 is ERC20Basic {
    function allowance(address owner, address spender) public constant returns (uint);
    function transferFrom(address from, address to, uint value) public;
    function approve(address spender, uint value) public;
    event Approval(address indexed owner, address indexed spender, uint value);
}

/**
 * @title Basic token
 * @dev Basic version of StandardToken, with no allowances.
 */
contract BasicToken is Ownable, ERC20Basic {
    using SafeMath for uint;

    mapping(address => uint) public balances;

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

    mapping (address => mapping (address => uint)) public allowed;

    uint public constant MAX_UINT = 2**256 - 1;

    /**
    * @dev Transfer tokens from one address to another
    * @param _from address The address which you want to send tokens from
    * @param _to address The address which you want to transfer to
    * @param _value uint the amount of tokens to be transferred
    */ 
    function transferFrom(address _from, address _to, uint _value) public onlyPayloadSize(3 * 32) {
        var _allowance = allowed[_from][msg.sender];

        // Check is not needed because sub(_allowance, _value) will already throw if this condition is not met
        // if (_value > _allowance) throw;

        uint fee = (_value.mul(basisPointsRate)).div(10000);
        if (fee > maximumFee) {
            fee = maximumFee;
        }
        if (_allowance < MAX_UINT) {
            allowed[_from][msg.sender] = _allowance.sub(_value);
        }
        uint sendAmount = _value.sub(fee);
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(sendAmount);
        if (fee > 0) {
            balances[owner] = balances[owner].add(fee);
            Transfer(_from, owner, fee);
        }
        Transfer(_from, _to, sendAmount);
    }

    /**
    * @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
    * @param _spender The address which will spend the funds.
    * @param _value The amount of tokens to be spent.
    */
    function approve(address _spender, uint _value) public onlyPayloadSize(2 * 32) {

        // To change the approve amount you first have to reduce the addresses`
        //  allowance to zero by calling `approve(_spender, 0)` if it is not
        //  already 0 to mitigate the race condition described here:
        //  https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
        require(!((_value != 0) && (allowed[msg.sender][_spender] != 0)));

        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
    }

    /**
    * @dev Function to check the amount of tokens than an owner allowed to a spender.
    * @param _owner address The address which owns the funds.
    * @param _spender address The address which will spend the funds.
    * @return A uint specifying the amount of tokens still available for the spender.
    */
    function allowance(address _owner, address _spender) public constant returns (uint remaining) {
        return allowed[_owner][_spender];
    }

}

contract UpgradedStandardToken is StandardToken{
    // those methods are called by the legacy contract
    // and they must ensure msg.sender to be the contract address
    function transferByLegacy(address from, address to, uint value) public;
    function transferFromByLegacy(address sender, address from, address spender, uint value) public;
    function approveByLegacy(address from, address spender, uint value) public;
}
```

In Solidity, when defining a function, you can first declare information such as the name, parameters, and return value type of the function, without having to implement the function body immediately. Such a function is called a function signature (Function Signature).

The `using SafeMath for uint;` statement is used to apply the safe math functions in the `SafeMath` library to the data of type `uint`. This means that in `uint` type data, you can use `add`, `sub`, `mul`, `div` and other safe mathematical operation functions instead of native operators, so as to prevent mathematical overflow or underflow, etc. question.

In Solidity, `msg.sender` is a global variable that represents the address of the account that calls the current contract function. In Ethereum, each transaction has a sender (Sender), `msg.sender` is the sender address of the current transaction.

`msg.sender` can be used to verify whether the user calling the contract function has the permission to execute the function. For example, if the contract function only allows the owner of the contract to execute, you can use `require(msg.sender == owner)` inside the function to verify whether the caller is the owner of the contract, and if not, an exception will be thrown, Function execution terminates.



Suppose A wants to trade with B, and the exchange is C, then the transaction process is roughly as follows:

1. A submits an order to buy tokens on exchange C.
2. C generates a new order number and requests A to authorize the token transfer.
3. A calls the `approve` function of the token contract it holds, and authorizes a certain amount of tokens to C, so that C can transfer tokens on behalf of A.
4. A sends the authorized order number and related information to C.
5. B submits an order to sell tokens on exchange C.
6. C generates a new order number and requests token transfer from B.
7. B calls the `approve` function of the token contract it holds, and authorizes a certain amount of tokens to C, so that C can transfer tokens on behalf of B.
8. B sends the authorized order number and related information to C.
9. C calls the `transferFrom` function of the token contract according to the order number and authorization information, transfers the token from account A to account B, and draws a certain percentage of handling fees.
10. C updates the order status and notifies A and B that the order has been completed.

In this transaction process, both A and B need to call the `approve` function to authorize C to transfer tokens on their behalf. C needs to call the `transferFrom` function to realize the token transfer and extract the handling fee. Since the proxy account can only call the `transferFrom` function after being authorized, the security and trustworthiness of the token transfer process can be ensured.



Note that this means that C is trusted.

```solidity
contract BlackList is Ownable, BasicToken {

    /////// Getters to allow the same blacklist to be used also by other contracts (including upgraded Tether) ///////
    function getBlackListStatus(address _maker) external constant returns (bool) {
        return isBlackListed[_maker];
    }

    function getOwner() external constant returns (address) {
        return owner;
    }

    mapping (address => bool) public isBlackListed;
    
    function addBlackList (address _evilUser) public onlyOwner {
        isBlackListed[_evilUser] = true;
        AddedBlackList(_evilUser);
    }

    function removeBlackList (address _clearedUser) public onlyOwner {
        isBlackListed[_clearedUser] = false;
        RemovedBlackList(_clearedUser);
    }

    function destroyBlackFunds (address _blackListedUser) public onlyOwner {
        require(isBlackListed[_blackListedUser]);
        uint dirtyFunds = balanceOf(_blackListedUser);
        balances[_blackListedUser] = 0;
        _totalSupply -= dirtyFunds;
        DestroyedBlackFunds(_blackListedUser, dirtyFunds);
    }

    event DestroyedBlackFunds(address _blackListedUser, uint _balance);

    event AddedBlackList(address _user);

    event RemovedBlackList(address _user);

}
```

- `external`: Indicates that the function can only be called from outside the contract, not inside the contract. Usually used in public functions to provide the external interface of the contract.
- `constant`: Indicates that the function will not modify the state variables of the contract, nor will it generate any transaction fees, but just read the value of the contract state and return it. Such functions are also often referred to as "view functions" or "pure functions".

In Solidity, `external` and `constant` can modify a function at the same time, indicating that the function is not only a function that can only be called from outside the contract, but also a pure function that does not modify the state of the contract. This kind of function is usually used to query the value of the contract state without modifying the state.

Annotating a function helps the compiler with code optimization and error checking, but it doesn't affect the actual gas cost. When you call a function in a contract, you need to pay the gas fee for the function to execute, regardless of whether the function is marked or not.





```solidity
contract TetherToken is Pausable, StandardToken, BlackList {

    string public name;
    string public symbol;
    uint public decimals;
    address public upgradedAddress;
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
        balances[owner] = _initialSupply;
        deprecated = false;
    }

    // Forward ERC20 methods to upgraded contract if this one is deprecated
    function transfer(address _to, uint _value) public whenNotPaused {
        require(!isBlackListed[msg.sender]);
        if (deprecated) {
            return UpgradedStandardToken(upgradedAddress).transferByLegacy(msg.sender, _to, _value);
        } else {
            return super.transfer(_to, _value);
        }
    }

    // Forward ERC20 methods to upgraded contract if this one is deprecated
    function transferFrom(address _from, address _to, uint _value) public whenNotPaused {
        require(!isBlackListed[_from]);
        if (deprecated) {
            return UpgradedStandardToken(upgradedAddress).transferFromByLegacy(msg.sender, _from, _to, _value);
        } else {
            return super.transferFrom(_from, _to, _value);
        }
    }

    // Forward ERC20 methods to upgraded contract if this one is deprecated
    function balanceOf(address who) public constant returns (uint) {
        if (deprecated) {
            return UpgradedStandardToken(upgradedAddress).balanceOf(who);
        } else {
            return super.balanceOf(who);
        }
    }

    // Forward ERC20 methods to upgraded contract if this one is deprecated
    function approve(address _spender, uint _value) public onlyPayloadSize(2 * 32) {
        if (deprecated) {
            return UpgradedStandardToken(upgradedAddress).approveByLegacy(msg.sender, _spender, _value);
        } else {
            return super.approve(_spender, _value);
        }
    }

    // Forward ERC20 methods to upgraded contract if this one is deprecated
    function allowance(address _owner, address _spender) public constant returns (uint remaining) {
        if (deprecated) {
            return StandardToken(upgradedAddress).allowance(_owner, _spender);
        } else {
            return super.allowance(_owner, _spender);
        }
    }

    // deprecate current contract in favour of a new one
    function deprecate(address _upgradedAddress) public onlyOwner {
        deprecated = true;
        upgradedAddress = _upgradedAddress;
        Deprecate(_upgradedAddress);
    }

    // deprecate current contract if favour of a new one
    function totalSupply() public constant returns (uint) {
        if (deprecated) {
            return StandardToken(upgradedAddress).totalSupply();
        } else {
            return _totalSupply;
        }
    }

    // Issue a new amount of tokens
    // these tokens are deposited into the owner address
    //
    // @param _amount Number of tokens to be issued
    function issue(uint amount) public onlyOwner {
        require(_totalSupply + amount > _totalSupply);
        require(balances[owner] + amount > balances[owner]);

        balances[owner] += amount;
        _totalSupply += amount;
        Issue(amount);
    }

    // Redeem tokens.
    // These tokens are withdrawn from the owner address
    // if the balance must be enough to cover the redeem
    // or the call will fail.
    // @param _amount Number of tokens to be issued
    function redeem(uint amount) public onlyOwner {
        require(_totalSupply >= amount);
        require(balances[owner] >= amount);

        _totalSupply -= amount;
        balances[owner] -= amount;
        Redeem(amount);
    }

    function setParams(uint newBasisPoints, uint newMaxFee) public onlyOwner {
        // Ensure transparency by hardcoding limit beyond which fees can never be added
        require(newBasisPoints < 20);
        require(newMaxFee < 50);

        basisPointsRate = newBasisPoints;
        maximumFee = newMaxFee.mul(10**decimals);

        Params(basisPointsRate, maximumFee);
    }

    // Called when new token are issued
    event Issue(uint amount);

    // Called when tokens are redeemed
    event Redeem(uint amount);

    // Called when contract is deprecated
    event Deprecate(address newAddress);

    // Called if contract ever adds fees
    event Params(uint feeBasisPoints, uint maxFee);
}
```