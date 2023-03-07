## How to Attack a Smart Contract?

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





### Reed Blogs

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



几个点：

智能合约内的变量可以视作合约内部的全局变量。

智能合约的所有函数都可以被访问，

智能合约的所有数据都是可见的，即使列为私有变量也是可以被取出的。

智能合约可以调用外部合约，这意味外部合约也可以基于调用外部合约

#### send()”、“transfer()”、“call.value()







http://yangzhe.me/2022/09/05/solidity-contract-vulnerability/
https://www.zhihu.com/column/p/29690785

How do you handle security in web3 applications and what are some best practices?





### 使用`assert()`强制不变性

当断言条件不满足时将触发断言保护 -- 比如不变的属性发生了变化。举个例子，代币在以太坊上的发行比例，在代币的发行合约里可以通过这种方式得到解决。断言保护经常需要和其他技术组合使用，比如当断言被触发时先挂起合约然后升级。（否则将一直触发断言，你将陷入僵局）

例如：

```
contract Token {
    mapping(address => uint) public balanceOf;
    uint public totalSupply;

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
        totalSupply += msg.value;
        assert(address(this).balance >= totalSupply);
    }
}
```

注意断言保护 **不是** 严格意义的余额检测， 因为智能合约可以不通过`deposit()` 函数被 [强制发送Ether](https://github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md#ether-forcibly-sent)！

### 正确使用`assert()`和`require()`

在Solidity 0.4.10 中`assert()`和`require()`被加入。`require(condition)`被用来验证用户的输入，如果条件不满足便会抛出异常，应当使用它验证所有用户的输入。 `assert(condition)` 在条件不满足也会抛出异常，但是最好只用于固定变量：内部错误或你的智能合约陷入无效的状态。遵循这些范例，使用分析工具来验证永远不会执行这些无效操作码：意味着代码中不存在任何不变量，并且代码已经正式验证。



### 小心整数除法的四舍五入

所有整数除数都会四舍五入到最接近的整数。 如果您需要更高精度，请考虑使用乘数，或存储分子和分母。

（将来Solidity会有一个fixed-point类型来让这一切变得容易。）

```
// bad
uint x = 5 / 2; // Result is 2, all integer divison rounds DOWN to the nearest integer

// good
uint multiplier = 10;
uint x = (5 * multiplier) / 2;

uint numerator = 5;
uint denominator = 2;
```



### 记住Ether可以被强制发送到账户

谨慎编写用来检查账户余额的不变量。

攻击者可以强制发送wei到任何账户，而且这是不能被阻止的（即使让fallback函数`throw`也不行）

攻击者可以仅仅使用1 wei来创建一个合约，然后调用`selfdestruct(victimAddress)`。在`victimAddress`中没有代码被执行，所以这是不能被阻止的。

### 不要假设合约创建时余额为零

攻击者可以在合约创建之前向合约的地址发送wei。合约不能假设它的初始状态包含的余额为零。浏览[issue 61](https://github.com/ConsenSys/smart-contract-best-practices/issues/61) 获取更多信息。

### 记住链上的数据是公开的

许多应用需要提交的数据是私有的，直到某个时间点才能工作。游戏（比如，链上游戏rock-paper-scissors（石头剪刀布））和拍卖机（比如，sealed-bid second-price auctions）是两个典型的例子。如果你的应用存在隐私保护问题，一定要避免过早发布用户信息。

例如：

- 在游戏石头剪刀布中，需要参与游戏的双方提交他们“行动计划”的hash值，然后需要双方随后提交他们的行动计划；如果双方的“行动计划”和先前提交的hash值对不上则抛出异常。
- 在拍卖中，要求玩家在初始阶段提交其所出价格的hash值（以及超过其出价的保证金），然后在第二阶段提交他们所出价格的资金。
- 当开发一个依赖随机数生成器的应用时，正确的顺序应当是（1）玩家提交行动计划，（2）生成随机数，（3）玩家支付。产生随机数是一个值得研究的领域；当前最优的解决方案包括比特币区块头（通过[http://btcrelay.org验证），hash-commit-reveal方案（比如，一方产生number后，将其散列值提交作为对这个number的“提交”，然后在随后再暴露这个number本身）和](http://btcrelay.xn--org)%2Chash-commit-reveal(%2Cnumber%2Cnumber%2Cnumber)-rr42anb08835bhzbja53fr9oja1my45b02ml1rhibe6rum6asaa781fjz9bmo6aos8aczam382bma117zqqfea327pmjikvwwn6d801ess0czlxagf70b68ubnputa0417lvplz44e/) [RANDAO](http://github.com/randao/randao)。
- 如果你正在实现频繁的批量拍卖，那么hash-commit机制也是个不错的选择。

### 权衡Abstract合约和Interfaces

Interfaces和Abstract合约都是用来使智能合约能更好的被定制和重用。Interfaces是在Solidity 0.4.11中被引入的，和Abstract合约很像但是不能定义方法只能申明。Interfaces存在一些限制比如不能够访问storage或者从其他Interfaces那继承，通常这些使Abstract合约更实用。尽管如此，Interfaces在实现智能合约之前的设计智能合约阶段仍然有很大用处。另外，需要注意的是如果一个智能合约从另一个Abstract合约继承而来那么它必须实现所有Abstract合约内的申明并未实现的函数，否则它也会成为一个Abstract合约。



### 使Fallback函数尽量简单

[Fallback函数](http://solidity.readthedocs.io/en/latest/contracts.html#fallback-function)在合约执行消息发送没有携带参数（或当没有匹配的函数可供调用）时将会被调用，而且当调用 `.send()` or `.transfer()`时，只会有2,300 gas 用于失败后fallback函数的执行（*译者注：合约收到Ether也会触发fallback函数执行*）。如果你希望能够监听`.send（）`或`.transfer（）`接收到Ether，则可以在fallback函数中使用event（译者注：让客户端监听相应事件做相应处理）。谨慎编写fallback函数以免gas不够用。

```
// bad
function() payable { balances[msg.sender] += msg.value; }

// good
function deposit() payable external { balances[msg.sender] += msg.value; }

function() payable { LogDepositReceived(msg.sender); }
```



### 明确标明函数和状态变量的可见性

明确标明函数和状态变量的可见性。函数可以声明为 `external`，`public`， `internal` 或 `private`。 分清楚它们之间的差异， 例如`external` 可能已够用而不是使用 `public`。对于状态变量，`external`是不可能的。明确标注可见性将使得更容易避免关于谁可以调用该函数或访问变量的错误假设。

```
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



### 将程序锁定到特定的编译器版本

智能合约应该应该使用和它们测试时使用最多的编译器相同的版本来部署。锁定编译器版本有助于确保合约不会被用于最新的可能还有bug未被发现的编译器去部署。智能合约也可能会由他人部署，而pragma标明了合约作者希望使用哪个版本的编译器来部署合约。

```
// bad
pragma solidity ^0.4.4;


// good
pragma solidity 0.4.4;
```



（*译者注：这当然也会付出兼容性的代价*）

### 小心分母为零 (Solidity < 0.4)

早于0.4版本, 当一个数尝试除以零时，Solidity [返回zero](https://github.com/ethereum/solidity/issues/670) 并没有 `throw` 一个异常。确保你使用的Solidity版本至少为 0.4。



### 区分函数和事件

为了防止函数和事件（Event）产生混淆，命名一个事件使用大写并加入前缀（我们建议**LOG**）。对于函数， 始终以小写字母开头，构造函数除外。

```
// bad
event Transfer() {}
function transfer() {}

// good
event LogTransfer() {}
function transfer() external {}
```



### 使用Solidity更新的构造器

更合适的构造器/别名，如`selfdestruct`（旧版本为`suicide`）和`keccak256`（旧版本为`sha3`）。 像`require(msg.sender.send(1 ether))`的模式也可以简化为使用`transfer()`，如`msg.sender.transfer(1 ether)`。





## 软件工程开发技巧

正如我们先前在[基本理念](https://link.zhihu.com/?target=https%3A//github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md%23general-philosophy) 章节所讨论的那样，避免自己遭受已知的攻击是不够的。由于在链上遭受攻击损失是巨大的，因此你还必须改变你编写软件的方式来抵御各种攻击。

我们倡导“时刻准备失败"，提前知道你的代码是否安全是不可能的。然而，我们可以允许合约以可预知的方式失败，然后最小化失败带来的损失。本章将带你了解如何为可预知的失败做准备。

注意：当你向你的系统添加新的组件时总是伴随着风险的。一个不良设计本身会成为漏洞-一些精心设计的组件在交互过程中同样会出现漏洞。仔细考虑你在合约里使用的每一项技术，以及如何将它们整合共同创建一个稳定可靠的系统。

## 升级有问题的合约

如果代码中发现了错误或者需要对某些部分做改进都需要更改代码。在以太坊上发现一个错误却没有办法处理他们是太多意义的。

关于如何在以太坊上设计一个合约升级系统是一个正处于积极研究的领域，在这篇文章当中我们没法覆盖所有复杂的领域。然而，这里有两个通用的基本方法。最简单的是专门设计一个注册合约，在注册合约中保存最新版合约的地址。对于合约使用者来说更能实现无缝衔接的方法是设计一个合约，使用它转发调用请求和数据到最新版的合约。

无论采用何种技术，组件之间都要进行模块化和良好的分离，由此代码的更改才不会破坏原有的功能，造成孤儿数据，或者带来巨大的成本。 尤其是将复杂的逻辑与数据存储分开，这样你在使用更改后的功能时不必重新创建所有数据。

当需要多方参与决定升级代码的方式也是至关重要的。根据你的合约，升级代码可能会需要通过单个或多个受信任方参与投票决定。如果这个过程会持续很长时间，你就必须要考虑是否要换成一种更加高效的方式以防止遭受到攻击，例如[紧急停止或断路器](https://link.zhihu.com/?target=https%3A//github.com/ConsenSys/smart-contract-best-practices/blob/master/README-zh.md%23circuit-breakers-pause-contract-functionality)。

**Example 1：使用注册合约存储合约的最新版本**

在这个例子中，调用没有被转发，因此用户必须每次在交互之前都先获取最新的合约地址。

```text
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

这种方法有两个主要的缺点：

1、用户必须始终查找当前合约地址，否则任何未执行此操作的人都可能会使用旧版本的合约 2、在你替换了合约后你需要仔细考虑如何处理原合约中的数据

另外一种方法是设计一个用来转发调用请求和数据到最新版的合约：

**例2：** **href="[http://ethereum.stackexchange.com/questions/2404/upgradeable-contracts](https://link.zhihu.com/?target=http%3A//ethereum.stackexchange.com/questions/2404/upgradeable-contracts)">使用DELEGATECALL** **转发数据和调用**

```text
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

这种方法避免了先前的问题，但也有自己的问题。它使得你必须在合约里小心的存储数据。如果新的合约和先前的合约有不同的存储层，你的数据可能会被破坏。另外，这个例子中的模式没法从函数里返回值，只负责转发它们，由此限制了它的适用性。（这里有一个[更复杂的实现](https://link.zhihu.com/?target=https%3A//github.com/ownage-ltd/ether-router) 想通过内联汇编和返回大小的注册表来解决这个问题）

无论你的方法如何，重要的是要有一些方法来升级你的合约，否则当被发现不可避免的错误时合约将没法使用。

## 断路器（暂停合约功能）

由于断路器在满足一定条件时将会停止执行，如果发现错误时可以使用断路器。例如，如果发现错误，大多数操作可能会在合约中被挂起，这是唯一的操作就是撤销。你可以授权给任何你受信任的一方，提供给他们触发断路器的能力，或者设计一个在满足某些条件时自动触发某个断路器的程序规则。

例如：

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

## 速度碰撞（延迟合约动作）

速度碰撞使动作变慢，所以如果发生了恶意操作便有时间恢复。例如，[The DAO](https://link.zhihu.com/?target=https%3A//github.com/slockit/DAO/) 从发起分割DAO请求到真正执行动作需要27天。这样保证了资金在此期间被锁定在合约里，增加了系统的可恢复性。在DAO攻击事件中，虽然在速度碰撞给定的时间段内没有有效的措施可以采取，但结合我们其他的技术，它们是非常有效的。

例如：

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

## 速率限制

速率限制暂停或需要批准进行实质性更改。 例如，只允许存款人在一段时间内提取总存款的一定数量或百分比（例如，1天内最多100个ether） - 该时间段内的额外提款可能会失败或需要某种特别批准。 或者将速率限制做在合约级别，合约期限内只能发出发送一定数量的代币。

[浏览例程](https://link.zhihu.com/?target=https%3A//gist.github.com/PeterBorah/110c331dca7d23236f80e69c83a9d58c%23file-circuitbreaker-sol)



## 合约发布

在将大量资金放入合约之前，合约应当进行大量的长时间的测试。

至少应该：

- 拥有100％测试覆盖率的完整测试套件（或接近它）
- 在自己的testnet上部署
- 在公共测试网上部署大量测试和错误奖励
- 彻底的测试应该允许各种玩家与合约进行大规模互动
- 在主网上部署beta版以限制风险总额

## 自动弃用

在合约测试期间，你可以在一段时间后强制执行自动弃用以阻止任何操作继续进行。例如，alpha版本的合约工作几周，然后自动关闭所有除最终退出操作的操作。

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

\#####限制每个用户/合约的Ether数量

在早期阶段，你可以限制任何用户（或整个合约）的Ether数量 - 以降低风险。



## Bug赏金计划

运行赏金计划的一些提示：

- 决定赏金以哪一种代币分配（BTC和/或ETH）
- 决定赏金奖励的预算总额
- 从预算来看，确定三级奖励： - 你愿意发放的最小奖励 - 通常可发放的最高奖励 - 设置额外的限额以避免非常严重的漏洞被发现
- 确定赏金发放给谁（3是一个典型）
- 核心开发人员应该是赏金评委之一
- 当收到错误报告时，核心开发人员应该评估bug的严重性
- 在这个阶段的工作应该在私有仓库进行，并且在Github上的issue板块提出问题
- 如果这个bug需要被修复，开发人员应该在私有仓库编写测试用例来复现这个bug
- 开发人员需要修复bug并编写额外测试代码进行测试确保所有测试都通过
- 展示赏金猎人的修复；并将修复合并回公共仓库也是一种方式
- 确定赏金猎人是否有任何关于修复的其他反馈
- 赏金评委根据bug的*可能性*和*影响*来确定奖励的大小
- 在整个过程中保持赏金猎人参与讨论，并确保赏金发放不会延迟

有关三级奖励的例子，参见 [Ethereum's Bounty Program](https://link.zhihu.com/?target=https%3A//bounty.ethereum.org/)：

> 奖励的价值将根据影响的严重程度而变化。 奖励轻微的“无害”错误从0.05 BTC开始。 主要错误，例如导致协商一致的问题，将获得最多5个BTC的奖励。 在非常严重的漏洞的情况下，更高的奖励是可能的（高达25 BTC）。