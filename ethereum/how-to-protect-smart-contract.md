## How to Protect a Smart Contract?

Ethereum and other complex blockchain projects are in their early stages and are highly experimental. Therefore, as new bugs and security vulnerabilities are discovered, new functions are continuously developed, and the security threats it faces are also constantly changing. This article is just the beginning for developers writing secure smart contracts.

Developing smart contracts requires a new engineering mindset, which is different from the development of our previous projects. Because the cost of making mistakes is huge, and it is difficult to patch as easily as traditional software. Like programming hardware directly or developing financial services software, there are bigger challenges than web development and mobile development. Therefore, it is not enough to prevent known vulnerabilities, you also need to learn new development concepts:

1. **Be prepared for possible mistakes.** Any meaningful smart contract is more or less buggy. Therefore your code must be able to correctly handle the bugs and vulnerabilities that arise. The following rules are always guaranteed: - stop the contract when there is an error in the smart contract, ("circuit breaker") - manage the funds risk of the account (limit (transfer) rate, maximum (transfer) amount)
   Efficient way to implement bug fixes and feature enhancements
2. **Release smart contracts with caution.** Try to find and fix possible bugs before the smart contract is officially released. - Thoroughly test the smart contract and test it in time after any new attack method is discovered (including the released contract) - Provide a bug bounty program from the release of the alpha version on the test network (testnet)
   Staged releases, each stage providing sufficient testing
3. **Keep smart contracts simple.** Complexity increases the risk of error.
   1. Ensure smart contract logic is concise
   2. Ensure contracts and functions are modular
   3. Use contracts or tools that are already widely used (e.g. don't write your own random number generator)
   4. When conditions permit, clarity is more important than performance
   5. Use blockchain only for decentralized parts of your system
4. **Keep updating.** 
   1. Check your smart contracts when any new vulnerabilities are discovered
   2. Update the used libraries or tools to the latest as soon as possible
   3. Use the latest security technology
5. **Understand the characteristics of blockchain.** Even though your previous programming experience can also be applied to Ethereum development, there are still some pitfalls you need to be aware of:
   1. Be especially careful with calls to external contracts, because you may execute a piece of malicious code and change the flow of control
   2. Be clear that your public function is public, which means it can be called maliciously. (on Ethereum) your private data is also visible to others
   3. Know the cost of gas and the gas limit of the block





### Read Blogs

Here are some places where newly discovered vulnerabilities in Ethereum or Solidity are commonly reported. The official source for security advisories is the Ethereum Blog, but generally vulnerabilities are first disclosed and discussed elsewhere.

- [Ethereum Blog](https://link.zhihu.com/?target=https%3A//blog.ethereum.org/): The official Ethereum blog

- - [Ethereum Blog - Security only](https://link.zhihu.com/?target=https%3A//blog.ethereum.org/category/security/): All related blogs are marked with **Security* *Label

- [Ethereum Gitter](https://link.zhihu.com/?target=https%3A//gitter.im/orgs/ethereum/rooms) chat room

- - [Solidity](https://link.zhihu.com/?target=https%3A//gitter.im/ethereum/solidity)
   - [Go-Ethereum](https://link.zhihu.com/?target=https%3A//gitter.im/ethereum/go-ethereum)
   - [CPP-Ethereum](https://link.zhihu.com/?target=https%3A//gitter.im/ethereum/cpp-ethereum)
   - [Research](https://link.zhihu.com/?target=https%3A//gitter.im/ethereum/research)

- [Reddit](https://link.zhihu.com/?target=https%3A//www.reddit.com/r/ethereum)
- [Network Stats](https://link.zhihu.com/?target=https%3A//ethstats.net/)

It is strongly recommended that you regularly browse these sites, especially for the vulnerabilities they mention that may affect your smart contracts.

In addition, here is a list of core development members involved in the security module of Ethereum, browse [bibliography](https://link.zhihu.com/?target=https%3A//github.com/ConsenSys/smart-contract- best-practices%23smart-contract-security-bibliography) for more information.

- **Vitalik Buterin**: [Twitter](https://link.zhihu.com/?target=https%3A//twitter.com/vitalikbuterin), [Github](https://link.zhihu.com /?target=https%3A//github.com/vbuterin), [Reddit](https://link.zhihu.com/?target=https%3A//www.reddit.com/user/vbuterin), [ Ethereum Blog](https://link.zhihu.com/?target=https%3A//blog.ethereum.org/author/vitalik-buterin/)
- **Dr. Christian Reitwiessner**: [Twitter](https://link.zhihu.com/?target=https%3A//twitter.com/ethchris), [Github](https://link.zhihu .com/?target=https%3A//github.com/chriseth), [Ethereum Blog](https://link.zhihu.com/?target=https%3A//blog.ethereum.org/author/christian_r /)
- **Dr. Gavin Wood**: [Twitter](https://link.zhihu.com/?target=https%3A//twitter.com/gavofyork), [Blog](https://link.zhihu .com/?target=http%3A//gavwood.com/), [Github](https://link.zhihu.com/?target=https%3A//github.com/gavofyork)
- **Vlad Zamfir**: [Twitter](https://link.zhihu.com/?target=https%3A//twitter.com/vladzamfir), [Github](https://link.zhihu.com /?target=https%3A//github.com/vladzamfir), [Ethereum Blog](https://link.zhihu.com/?target=https%3A//blog.ethereum.org/author/vlad/)

In addition to paying attention to core development members, it is also important to participate in various blockchain security communities, because the disclosure or research of security vulnerabilities will be conducted through all parties.



### Call Other Contracts

##### Try to avoid external calls

Calling untrusted external contracts can introduce a whole host of unintended risks and errors. An external call may execute malicious code within its contract and other contracts it depends on. Therefore, every external call is a potential security threat. Remove external calls from your smart contracts as much as possible. When it is not possible to completely remove external calls, use the advice provided elsewhere in this section to minimize risk.

##### Carefully weigh "send()", "transfer()", and "call.value()"

When transferring Ether, you need to carefully weigh the differences between "someAddress.send()", "someAddress.transfer()", and "someAddress.call.value()()".

1. x.transfer(y) and if (!x.send(y)) throw; are equivalent. send is the underlying implementation of transfer, it is recommended to use transfer as directly as possible.
2. someAddress.send() and someAddress.transfer() are reentrant safe. Although the functions of these external smart contracts can be triggered to execute, the 2,300 gas subsidized to the external smart contract means that it is only enough to record an event in the log.
3. someAddress.call.value()() will send the specified amount of Ether and trigger the execution of the corresponding code. The called external smart contract code will enjoy all the remaining gas. Transferring money in this way is easy to have reentrancy loopholes and is very insecure.
4. Using send() or transfer() can prevent reentrancy by specifying the gas value, but doing so may cause problems when calling the fallback function with the contract, because the gas may be insufficient, and the execution of the contract's fallback function requires at least 2,300 gas consume.

A mechanism called push and pull tries to balance the two, using send() or transfer() on the push part and call.value()() on the pull part. (*Translator’s Note: Use send() or transfer() when you need to transfer Ether to an external unknown address, and use call.value()() to transfer Ether to an address that is known to have no malicious code inside)

It should be noted that using send() or transfer() to transfer money does not guarantee the reentry security of the smart contract itself, it only guarantees the reentry security of the transfer operation.

##### Handle external call errors

Solidity provides a series of low-level methods to perform operations on raw addresses, such as: address.call(), address.callcode(), address.delegatecall() and address.send. These underlying methods don't throw exceptions (throw), they just return false when an error is encountered. On the other hand, contract calls (eg, ExternalContract.doSomething()) will automatically propagate exceptions, (eg, if doSomething() throws an exception, then ExternalContract.doSomething() will also throw)).

If you choose to use low-level methods, be sure to check the return value to handle possible errors.

```
// bad
someAddress. send(55);
someAddress.call.value(55)(); // this is doubly dangerous, as it will forward all remaining gas and doesn't check for result
someAddress.call.value(100)(bytes4(sha3("deposit()"))); // if deposit throws an exception, the raw call() will only return false and transaction will NOT be reverted

// good
if(!someAddress. send(55)) {
     // Some failure code
}
ExternalContract(someAddress).deposit.value(100);
```

##### Don't assume you know the control flow of external calls

Whether using raw calls or contract calls, if the ExternalContract is untrusted, malicious code should be assumed. Even if the ExternalContract does not contain malicious code, the code of other contracts it calls may contain malicious code. A concrete example of danger is the possibility of malicious code hijacking control flow and causing a race condition.



### Prefer pull over push for external contracts

External calls may fail intentionally or unintentionally. In order to minimize the loss caused by these external call failures, it is usually a good practice to isolate the external call function from the rest of the code, and ultimately the payment originator is responsible for initiating the call to the function. This practice is especially important for payment operations, such as letting users withdraw assets themselves instead of sending them directly. (Translator's Note: Set the value of the asset that needs to be paid to a certain party in advance, indicating the amount that the receiver can withdraw funds from the current account, and then the receiver calls the withdrawal function of the current contract to complete the transfer). (This method also avoids gas limit related problems.)



```solidity
// bad
contract auction {
    address highestBidder;
    uint highestBid;

    function bid() payable {
        if (msg.value < highestBid) throw;

        if (highestBidder != 0) {
            if (!highestBidder.send(highestBid)) { // if this call consistently fails, no one else can bid
                throw;
            }
        }

       highestBidder = msg.sender;
       highestBid = msg.value;
    }
}

// good
contract auction {
    address highestBidder;
    uint highestBid;
    mapping(address => uint) refunds;

    function bid() payable external {
        if (msg.value < highestBid) throw;

        if (highestBidder != 0) {
            refunds[highestBidder] += highestBid; // record the refund that this user can claim
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
    }

    function withdrawRefund() external {
        uint refund = refunds[msg.sender];
        refunds[msg.sender] = 0;
        if (!msg.sender.send(refund)) {
            refunds[msg.sender] = refund; // reverting state because send failed
        }
    }
}
```



##### Mark untrusted contracts

When your own functions call external contracts, your variables, methods, and contract interface names should indicate that they may be unsafe.



```solidity
// bad
Bank.withdraw(100); // Unclear whether trusted or untrusted

function makeWithdrawal(uint amount) { // Isn't clear that this function is potentially unsafe
    Bank.withdraw(amount);
}

// good
UntrustedBank.withdraw(100); // untrusted external call
TrustedBank.withdraw(100); // external but trusted bank contract maintained by XYZ Corp

function makeUntrustedWithdrawal(uint amount) {
    UntrustedBank.withdraw(amount);
}
```



### Enforce immutability with assert()

Assertion guards are triggered when the assertion condition is not met -- such as when an immutable property changes. For example, the issuance ratio of tokens on Ethereum can be resolved in this way in the token issuance contract. Assertion protection often needs to be combined with other techniques, such as suspending the contract and then upgrading when the assertion is triggered. (Otherwise the assert will keep firing and you will deadlock)

For example:



```solidity
contract Token {
     mapping(address => uint) public balanceOf;
     uint public totalSupply;
     function deposit() public payable {
     balanceOf[msg.sender] += msg.value;
     totalSupply += msg. value;
     assert(address(this).balance >= totalSupply);
 }
 }
```
}
Note that assertion protection is not a balance check in the strict sense, because smart contracts can be forced to send Ether without using the deposit() function!

### Correct use of assert() and require()

assert() and require() were added in Solidity 0.4.10. require(condition) is used to validate user input, and an exception will be thrown if the condition is not met. It should be used to validate all user input. assert(condition) also throws an exception if the condition is not met, but is best used only for fixed variables: internal errors or your smart contract stuck in an invalid state. Following these paradigms, use profiling tools to verify that these invalid opcodes are never executed: meaning that no invariants exist in the code, and the code has been formally verified.

### Be careful with rounding of integer division

All integer divisors are rounded to the nearest integer. If you need more precision, consider using a multiplier, or storing the numerator and denominator.

(In the future Solidity will have a fixed-point type to make this easier.)

```
// bad
uint x = 5 / 2; // Result is 2, all integer division rounds DOWN to the nearest integer

// good
uint multiplier = 10;
uint x = (5 * multiplier) / 2;

uint numerator = 5;
uint denominator = 2;

```

### **Remember that Ether can be forcefully sent to the account**

Carefully write invariants that check account balances.

The attacker can force send wei to any account, and this cannot be blocked (even if the fallback function is thrown)

An attacker can create a contract using only 1 wei, and then call selfdestruct(victimAddress). No code is executed in victimAddress, so this cannot be blocked.

### Don't assume that the balance is zero when the contract is created

An attacker can send wei to the address of the contract before the contract is created. A contract cannot assume that its initial state contains a balance of zero. See issue 61 for more information.

### Remember that on-chain data is public

Many applications need to submit data that is private and will not work until a certain point in time. Games (eg, on-chain games rock-paper-scissors) and auction machines (eg, sealed-bid second-price auctions) are two typical examples. If your application has privacy protection issues, be sure to avoid publishing user information prematurely.



### Weighing Abstract Contracts and Interfaces

Both Interfaces and Abstract contracts are used to enable smart contracts to be better customized and reused. Interfaces were introduced in Solidity 0.4.11. They are very similar to Abstract contracts but cannot define methods and can only be declared. Interfaces have some limitations such as not being able to access storage or inherit from other Interfaces, usually these make Abstract contracts more practical. Nevertheless, Interfaces are still very useful in the stage of designing smart contracts before implementing them. In addition, it should be noted that if a smart contract inherits from another Abstract contract, it must implement all the functions declared in the Abstract contract that have not been implemented, otherwise it will also become an Abstract contract.

### In smart contracts involving two or more parties, participants may "go offline" and never return

Don't make chargeback and claims processes dependent on a particular action being taken by a party without another way to get funds. For example, in a game of rock-paper-scissors, a common mistake is not to pay until both players have submitted their plans of action. However a malicious player can cause the other party to lose money by never submitting its action plan -- in fact, if the player sees the other player's leaked action plan and decides whether or not he will lose, Then he has every reason not to submit his own plan of action. These problems also appear in channel settlement. Problems arise when these situations arise: (1) provide a way to circumvent non-participants and participants, possibly by setting time limits, and (2) consider providing additional financial incentives for participants to do so when they should In all cases the information is still submitted.

### Keep the Fallback function as simple as possible

The Fallback function will be called when the contract execution message is sent without parameters (or when there is no matching function to call), and when calling .send() or .transfer(), only 2,300 gas will be used after the failure The execution of the fallback function (Translator's Note: The contract receives Ether will also trigger the execution of the fallback function). If you want to be able to listen to .send() or .transfer() to receive Ether, you can use event in the fallback function. Carefully write the fallback function to avoid running out of gas.

```solidity
// bad
function() payable { balances[msg.sender] += msg.value; }

// good
function deposit() payable external { balances[msg. sender] += msg. value; }

function() payable { LogDepositReceived(msg.sender); }

Explicitly mark the visibility of functions and state variables
```

Clearly indicate the visibility of functions and state variables. Functions can be declared external, public, internal or private. Distinguish the difference between them, for example external may be sufficient instead of public. For state variables, external is not possible. Explicitly annotating visibility will make it easier to avoid false assumptions about who can call the function or access the variable.

```solidity
// bad
uint x; // the default is private for state variables, but it should be made explicit
function buy() { // the default is public
     // public code
}

// good
uint private y;
function buy() external {
     // only callable externally
}

function utility() public {
     // callable externally, as well as internally: changing this code requires thinking about both cases.
}

function internalAction() internal {
     // internal code
}
```

### Lock a program to a specific compiler version

Smart contracts should be deployed with the same version of the compiler that they are tested with the most. Locking the compiler version helps ensure that contracts are not deployed with the latest compilers that may have undiscovered bugs. Smart contracts may also be deployed by others, and pragma indicates which version of the compiler the contract author wants to use to deploy the contract.

```solidity
// bad
pragma solidity ^0.4.4;


// good
pragma solidity 0.4.4;
```

(Translator's Note: This will of course also pay the price of compatibility)

### **Beware of zero denominators (Solidity < 0.4)**

Prior to version 0.4, Solidity returned zero and did not throw an exception when a number was attempted to be divided by zero. Make sure you are using at least Solidity version 0.4.

### Distinguish between functions and events

In order to prevent confusion between functions and events (Event), name an event using uppercase and add a prefix (we recommend LOG). For functions, always start with a lowercase letter, except for constructors.

```solidity
// bad
event Transfer() {}
function transfer() {}

// good
event LogTransfer() {}
function transfer() external {}
```

### Using Solidity's updated constructor

More appropriate constructors/aliases like selfdestruct (old version suicide) and keccak256 (old version sha3). Patterns like require(msg.sender.send(1 ether)) can also be simplified to use transfer(), like msg.sender.transfer(1 ether) .



### Upgrade a problematic contract

If a bug is found in the code or if some part needs to be improved, the code needs to be changed. It makes too much sense to find a bug on Ethereum and have no way to deal with them.

How to design a contract upgrade system on Ethereum is an area of active research, and we cannot cover all complex areas in this article. However, there are two general basic approaches here. The simplest is to design a registration contract and save the address of the latest version of the contract in the registration contract. A more seamless way for contract users is to design a contract and use it to forward call requests and data to the latest version of the contract.

Regardless of the technology used, there needs to be modularity and good separation between components so that code changes don't break legacy functionality, create orphan data, or incur significant costs. Especially separating complex logic from data storage so you don't have to recreate all the data when using changed functionality.

It is also critical when multiple parties are involved in deciding how to upgrade the code. Depending on your contract, code upgrades may need to be voted on by a single or multiple trusted parties. If this process takes a long time, you have to consider whether to switch to a more efficient way to prevent attacks, such as emergency stops or circuit breakers.

Example 1: Using the registry contract to store the latest version of the contract

In this example, the calls are not forwarded, so the user must fetch the latest contract address every time before interacting.

```solidity
contract SomeRegister {
    address backendContract;
    address[] previousBackends;
    address owner;

    function SomeRegister() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        if (msg.sender != owner) {
            throw;
        }
        _;
    }
    
    function changeBackend(address newBackend) public
    onlyOwner()
    returns (bool)
    {
        if(newBackend != backendContract) {
            previousBackends.push(backendContract);
            backendContract = newBackend;
            return true;
        }

        return false;
    }
}
```

This approach has two major disadvantages:

1. Users must always look up the current contract address, otherwise anyone who does not do this may use an old version of the contract 2. After you replace the contract, you need to carefully consider what to do with the data in the original contract

Another way is to design a contract that forwards the call request and data to the latest version:

EXAMPLE 2: FORWARDING DATA AND CALLING USING DELEGATECALL

```solidity
contract Relay {
    address public currentVersion;
    address public owner;

    modifier onlyOwner() {
        if (msg.sender != owner) {
            throw;
        }
        _;
    }

    function Relay(address initAddr) {
        currentVersion = initAddr;
        owner = msg.sender; // this owner may be another contract with multisig, not a single contract owner
    }

    function changeContract(address newVersion) public
    onlyOwner()
    {
        currentVersion = newVersion;
    }

    function() {
        if(!currentVersion.delegatecall(msg.data)) throw;
    }
}
```



This approach avoids the previous problems, but has its own problems. It forces you to store data carefully in contracts. If the new contract has a different storage layer than the previous contract, your data could be corrupted. Also, the pattern in this example cannot return values from functions, only forwards them, thus limiting its applicability. (Here's a more complex implementation that would solve this with inline assembly and a registry of return sizes)

Regardless of your approach, it is important to have some way to upgrade your contract, otherwise the contract will become unusable when the inevitable bugs are discovered.



## Circuit breaker (pause contract function)

Since the circuit breaker will stop execution when a certain condition is met, the circuit breaker can be used if an error is found. For example, most operations may be suspended in the contract if an error is found, the only operation being undo. You can authorize any party you trust, giving them the ability to trigger a circuit breaker, or design a program rule that automatically triggers a certain circuit breaker when certain conditions are met.

For example:

```text
bool private stopped = false;
address private owner;

modifier isAdmin() {
    if(msg.sender != owner) {
        throw;
    }
    _;
}

function toggleContractActive() isAdmin public
{
    // You can add an additional modifier that restricts stopping a contract to be based on another action, such as a vote of users
    stopped = !stopped;
}

modifier stopInEmergency { if (!stopped) _; }
modifier onlyInEmergency { if (stopped) _; }

function deposit() stopInEmergency public
{
    // some code
}

function withdraw() onlyInEmergency public
{
    // some code
}
```

## Velocity collision (delay contract action)

Speed bumps slow down the action so there is time to recover if something malicious happens. For example, [The DAO](https://link.zhihu.com/?target=https%3A//github.com/slockit/DAO/) takes 27 days from the initiation of the split DAO request to the actual execution of the action. This ensures that the funds are locked in the contract during this period, increasing the recoverability of the system. In the DAO attack event, although no effective measures can be taken within a given time period of speed collision, they are very effective in combination with our other technologies.

For example:

```text
struct RequestedWithdrawal {
    uint amount;
    uint time;
}

mapping (address => uint) private balances;
mapping (address => RequestedWithdrawal) private requestedWithdrawals;
uint constant withdrawalWaitPeriod = 28 days; // 4 weeks

function requestWithdrawal() public {
    if (balances[msg.sender] > 0) {
        uint amountToWithdraw = balances[msg.sender];
        balances[msg.sender] = 0; // for simplicity, we withdraw everything;
        // presumably, the deposit function prevents new deposits when withdrawals are in progress

        requestedWithdrawals[msg.sender] = RequestedWithdrawal({
            amount: amountToWithdraw,
            time: now
        });
    }
}

function withdraw() public {
    if(requestedWithdrawals[msg.sender].amount > 0 && now > requestedWithdrawals[msg.sender].time + withdrawalWaitPeriod) {
        uint amountToWithdraw = requestedWithdrawals[msg.sender].amount;
        requestedWithdrawals[msg.sender].amount = 0;

        if(!msg.sender.send(amountToWithdraw)) {
            throw;
        }
    }
}
```

## Rate Limiting

Rate limits are suspended or require approval for substantive changes. For example, a depositor is only allowed to withdraw a certain amount or percentage of the total deposit (eg, a maximum of 100 ether in 1 day) for a period of time - additional withdrawals during that time period may fail or require some kind of special approval. Or set the rate limit at the contract level, and only a certain number of tokens can be sent within the contract period.



## Contract release

Contracts should go through a lot of long-term testing before putting a lot of money into a contract.

At least it should:

- A full test suite with 100% test coverage (or close to it)
- Deploy on your own testnet
- Deployment of extensive testing and bug bounties on the public testnet
- Thorough testing should allow various players to interact with contracts at scale
- Deploy beta version on mainnet to limit total risk

## Automatic deprecation

During contract testing, you can enforce automatic deprecation after a period of time to prevent any operations from proceeding. For example, an alpha version of a contract works for a few weeks, then automatically shuts down all operations except the final exit operation.

```text
modifier isActive() {
    if (block.number > SOME_BLOCK_NUMBER) {
        throw;
    }
    _;
}

function deposit() public
isActive() {
    // some code
}

function withdraw() public {
    // some code
}
```



### Limit the amount of Ether per user/contract

In the early stages, you can limit the amount of Ether any user (or the entire contract) can have - to reduce risk.



## Bug Bounty Program

Some tips for running a bounty program:

- Decide which token the bounty will be distributed in (BTC and/or ETH)
- Determines the total budget for bounty rewards
- In terms of budget, determine three tiers of rewards: - the smallest reward you are willing to give out - the highest reward you can usually give out - set additional limits to avoid very serious bugs from being discovered
- Determine who the bounty goes to (3 is a typical)
- The core developer should be one of the bounty judges
- When a bug report is received, core developers should assess the severity of the bug
- Work at this stage should be done in private repositories and issues in the issues board on Github
- If the bug needs to be fixed, the developer should write a test case in the private repository to reproduce the bug
- Developers need to fix bugs and write additional test code to test to ensure that all tests pass
- show bounty hunter's fix; and merging the fix back to the public repo is also a way
- Check if bounty hunters have any other feedback on fixes
- Bounty judges determine the size of the reward based on the bug's *likelihood* and *impact*
- Keep bounty hunters engaged in discussions throughout the process and make sure bounties are not delayed

See [Ethereum's Bounty Program](https://link.zhihu.com/?target=https%3A//bounty.ethereum.org/):

> The value of the reward will vary according to the severity of the impact. Rewards for minor "harmless" bugs start at 0.05 BTC. Major bugs, such as issues leading to consensus, will be rewarded with up to 5 BTC. In case of very serious bugs, higher rewards are possible (up to 25 BTC).