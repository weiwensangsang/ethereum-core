# How Ethereum Works
This project will give a detailed introduction to the technical history, working principles, development trends, and security discussions of Ethereum. It will also attempt to build a minimal blockchain project based on Ethereum.



## Tech Map

0. [Why We Want a New Blockchain?](./ethereum/00.why-we-want-a-new-blockchain.md)
1. [Ethereum Should Do Something New](./ethereum/01.ethereum-should-do-something-new.md)
2. [Ethereum Code Structure](./ethereum/02.ethereum-code-structure.md)
3. [Ethereum Should Do Something New](./ethereum/01.ethereum-should-do-something-new.md)
4. [Ethereum Should Do Something New](./ethereum/01.ethereum-should-do-something-new.md)

5. [Why Use GoLang to Build a Blockchain?](./ethereum/02.why-use-golang-to-build-a-blockchain.md)



### References

1. [Merkle Tree and Zero Knowledge Proof](https://blog.csdn.net/qq_32651245/article/details/110403770)





#### **1. Can you describe Ethereum?**

#### **2. What is the importance of EVM in Ethereum?**

#### **3. How is Ether used in the Ethereum blockchain?**

#### **4. What is a smart contract?**

#### **5. What is a transaction request?**

#### **6. How many types of ETH denominations do you know?**

#### **7. What is the recommended method for checking the ETH balance?**

#### **8. Can you describe a decentralized application?**

#### **9. How are decentralized applications helpful for users?**

#### **10. What are the challenges in dApp development?**

#### **11. Which languages are used commonly for smart contract development?**

#### **12. How can smart contracts serve real-world use cases?**

#### **13. What are the important traits of Solidity for smart contract development?**e.

#### **14. How is Vyper a suitable alternative to Solidity for smart contract programming?**

#### **15. Are Yul and Yul+ reliable for smart contract programming?**

#### **16. Which types of accounts can you find in Ethereum?**

#### **17. What are the important fields in Ethereum accounts?**

#### **18. Do you know about the components of a smart contract?**

#### **19. How is a smart contract library useful?**

#### **20. What are the recommended methods for testing smart contracts?**

#### **21. Do you know the specific methods for automated and manual testing of smart contracts?**

#### **22. What are the mandatory prerequisites for deploying smart contracts?**

#### **23. What is EIP-1559?**

#### **24. How can you reduce gas costs for smart contracts?**

#### **25. What are the steps involved in smart contract verification?**







**. In Ethereum, what kinds of accounts can you find?**



**2. Which fields in an Ethereum account are the most important?**



**3. Do you know what a smart contract is made up of?**



**4. How is a library of smart contracts helpful?**



**5. What are some good ways to test smart contracts?**

> 

**6. Do you know the specific ways that smart contracts can be tested both automatically and by hand?**



**7. What must be in place before smart contracts can be used?**



**8. What is the EIP-1559?**



**9. How can you get smart contracts to pay less for gas?**



**10. What steps are there to verify a smart contract?**



(1) 以太坊常见问题

问：在以太坊中，Wei和Ether(以太币)有什么区别？

问：以太坊的平均区块间隔时间是多少？

问：以太坊的平均区块大小是多少？

问：以太币是如何产生的？

问：以太坊中的节点是什么？

问：以太坊都有哪些网络？

问：与以太坊网络交互都哪些方法？

问：你是否能在以太坊中“隐藏”一笔交易？

问：以太坊的交易记录存放在哪里？

问：以太坊主链已经很强大了，为什么还要使用以太坊私有链？

问：如何查看一笔交易或一个区块的详细信息？

问：如何查看私有链中一笔交易或一个区块的详细信息？

问：区块链的共识过程是什么？

问：以太坊挖矿操作的工作原理是什么呢？

问：区块链中最常用的两种共识协议是什么？

问：请简述权益证明的工作原理。

问：以太坊使用哪种共识协议呢？

问：签署一笔交易需要用到什么工具？

问：在私钥丢失后，用户是否还可以恢复以太坊帐户？

问：用什么方法可以连接到以太坊节点？

问：以太坊中异常火爆的Geth是什么呢？

问：连接到Geth客户端的默认方式是什么？

问：Geth客户端中都有哪些API（Application Programming Interface，应用程序编程接口）？

问：你可以使用哪些RPC通过网络连接到Geth客户端？

问：如果你输入命令“—rpc”，启用的是哪一个RPC？

问：默认情况下哪些RPC API是启用的？

问：如何为JSON-RPC启用admin api？

问：命令“—datadir”有什么功能？

问：Geth的“快速”同步是什么，为什么它更快速呢？

问：命令“—testnet”有什么功能？

问：启动Geth客户端会在屏幕上打印大量的输出信息，如果不想被这些繁杂信息干扰该怎么办？

问：如何使用IPC-RPC连接两个Geth客户端？

问：如何将自定义javascript文件加载到Geth控制台？

问：Geth客户端中帐户存储在哪里？

问：如何使用给定的账户发起一笔交易？

问：我们刚才说到了有关索引的内容。账户的索引取决于什么？

问：Geth客户端是否能用来挖矿？

问：挖矿选项中的“etherbase”是什么？

(2) 智能合约常见问题

问：ABI是什么？

问：智能合约是什么？

问：智能合约可以用哪种语言编写？

问：智能合约都有什么样的使用场景呢？

问：什么是MetaMask？

问：Metamask使用什么节点？

问：相比于传统以太坊钱包，有哪些功能是Metamask不支持的？

问：智能合约的执行是免费的吗？

问：查看智能合约的状态是免费的吗？

问：谁来执行智能合约？

问：为什么调用智能合约中的函数需要花钱？

问：为什么以太坊中要引入燃料费用呢？

问：燃料价格是否能决定交易被处理的时间？

问：交易中的燃料使用量取决于什么？

问：交易费该如何计算？

问：如果执行智能合约的花费少于交易者支付的燃料费用，他是否会获得退款？

问：如果执行智能合约的花费超过了交易者支付的燃料费用，这时会发生什么？

问：谁来支付调用智能合约的费用？

问：节点在哪里运行智能合约的代码呢？

问：以太坊虚拟机需要什么工具来运行智能合约？

问：以太坊虚拟机都包含哪些部分？

问：Remix是什么？

问：在Remix中，你可以连接哪些节点？

问：什么是DApp，它与普通App有什么不同？

(3) Solidity常见问题

问：Solidity是静态类型语言（类型的检查是在运行前做的，如编译阶段）还是动态类型语言（类型的检查是在运行时做的）？

问：Solidity中的什么结构与Java中的类（Class）相对应？

问：智能合约的实例是什么？

问：Java和Solidity之间存在哪些差异。

问：在Solidity文件中需要指定的第一个参数是什么？

问：一个智能合约包含什么？

问：智能合约中都有哪些类型的函数？

问：如果我将多个智能合约定义放入单个Solidity文件中，会出现什么样的错误？

问：两个智能合约可以通过哪些方式进行交互？

问：当你尝试部署具有多个智能合约的文件时会发生什么？

问：如果我有一个庞大的项目，我是否需要将所有相关的智能合约保存在一个文件中？

问：我是否只能导入本地文件？

问：以太坊虚拟机的内存都有哪些部分？

问：请解释一下存储（Storage）。

问：请解释一下内存（Memory）。

问：请解释一下Calldata。

问：存储区和内存区分别存储了哪些变量？

问：阅读以下代码，请解释代码的哪一部分对应哪个内存区域：

问：我是否可以这样定义一个函数：

问：EVM调用和非EVM调用之间有什么区别呢？

问：如何设定智能合约的以太币余额限制，如果向有余额限制的智能合约中发送超额的以太币会发生什么？

问：如何在智能合约帐户中设置msg.val的值？

(4) DApp和web3.0常见问题

问：DApp是什么？

问：DApp与智能合约有何不同？

问：前端使用什么工具连接到后端的智能合约？

问：请列几个你所知道的DApp。

问：你需要什么工具与DApp的智能合约进行交互？

问：ABI的作用是什么？

问：字节码的作用是什么？

问：为什么要使用大数运算程序库（BigNumber library）？

问：为什么要始终检查DApp代码的开头是否设置了web3提供程序（provider）？

问：为什么使用web3 js的1.x版本而不是0.2x.x版本？

问：在web3 1.x版本中如何列出所有帐户？

问：“.call”和“.send”有什么区别？

问：是否可以通过这样的命令“.send（{value：1}）”发送一个以太币？

问：那是否意味着，为了发送一个以太币，我需要将值设置为10^18？

问：调用“.send（）”时我需要指定什么？

问：将以太币发送到特定地址的函数是否只有

问：以太坊的可扩展性问题有什么解决方案？

02 面试核心要点梳理

(1) Solidity文件的布局

Pragma版本（Version Pragma）

导入其他源文件

注释

(2) 以太坊存储区域

(3) Solidity中的数据类型

布尔类型

整型

地址类型

字符串类型

(4) 运算符

算术运算符

增量运算符

位运算符

逻辑运算符

(5) Solidity中的数据结构

结构体

数组

映射

(6) 程序控制结构

(7) 函数

(8) 函数修改器

(9) 继承





1. What is Ethereum?
2. What are some Real-World Applications of Ethereum?
3. What are the features of Ethereum?
4. What is Solidity in Ethereum?
5. How can we Developing MyContract?
6. What is Cryptography?
7. What is dApps?
8. Name some Types of Ethereum Networks?
9. What is Metamask?
10. What languages are used to write Smart Contracts?
11. What is an Ethereum Client?
12. What is Truffle?
13. How can we return mapping list in Solidity?

**1.** [What is the difference between a private and a public blockchain](https://web3.career/learn-web3/web3-interview-questions#what-is-the-difference-between-a-private-and-a-public-blockchain)

**2.** [Can you explain the concept of decentralization and its importance in web3](https://web3.career/learn-web3/web3-interview-questions#can-you-explain-the-concept-of-decentralization-and-its-importance-in-web3)

**3.** [How does a blockchain achieve consensus and what are some common consensus algorithms](https://web3.career/learn-web3/web3-interview-questions#how-does-a-blockchain-achieve-consensus-and-what-are-some-common-consensus-algorithms)

**4.** [Can you explain the concept of smart contracts and how they are used in web3 applications](https://web3.career/learn-web3/web3-interview-questions#can-you-explain-the-concept-of-smart-contracts-and-how-they-are-used-in-web3-applications)

**5.** [What is the ethereum virtual machine evm and how does it work](https://web3.career/learn-web3/web3-interview-questions#what-is-the-ethereum-virtual-machine-evm-and-how-does-it-work)

**6.** [Can you explain the difference between on chain and off chain transactions in web3](https://web3.career/learn-web3/web3-interview-questions#can-you-explain-the-difference-between-on-chain-and-off-chain-transactions-in-web3)

**7.** [How do you handle security in web3 applications and what are some best practices](https://web3.career/learn-web3/web3-interview-questions#how-do-you-handle-security-in-web3-applications-and-what-are-some-best-practices)

**8.** [Write a code that uses html and javascript with the web3 js library to create a button that allows users to pay 1 eth](https://web3.career/learn-web3/web3-interview-questions#write-a-code-that-uses-html-and-javascript-with-the-web3-js-library-to-create-a-button-that-allows-users-to-pay-1-eth)

**9.** [Write a simple example of a smart contract written in solidity](https://web3.career/learn-web3/web3-interview-questions#write-a-simple-example-of-a-smart-contract-written-in-solidity)

**10.** [What is the difference between proof of work pow and proof of stake pos differ](https://web3.career/learn-web3/web3-interview-questions#what-is-the-difference-between-proof-of-work-pow-and-proof-of-stake-pos-differ)





#### **1. Explain Blockchain Technology?**

#### **2. What is the fundamental tenet of the blockchain?**

#### **3. As a part of blockchain technology, what exactly are Blocks?**



#### **4. Name the different types of Blockchain networks.**

- **Public Blockchain**



- **Private Blockchain**



- **Consortium or Cooperative Blockchains**



#### **5. How does a blockchain recognize a Block?**



#### **6. In a Blockchain database, what various kinds of records can you find?**

#### **7. Is it possible to make changes to the data after it has been written in a block?**



#### **8. Are there any prerequisites for using blockchain technology in an organization?**



#### **9. What is the Encryption Function in the Blockchain?**



#### **10. What are the reasons for the trustworthiness of Blockchain?**



#### **11. Blockchain Ecosystem: What Are the Essential Elements? Explain.**

- 

#### **12. Why is blockchain referred to as “resilient and lasting”?**



#### **13. Is “Proof of Stake” and “Proof of Work” the Same Thing?**



#### **14. Are there any Popular Platforms for Building Blockchain Applications?**



#### **15. What Kinds of Records can Be Stored on a Blockchain?**
