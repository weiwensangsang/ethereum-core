# Ethereum Core
This project will give a detailed introduction to the technical history, working principles, development trends, and security discussions of Ethereum. It will also attempt to build a minimal blockchain project based on Ethereum.



### Ethereum: new blcokchain

0. [Why We Want a New Blockchain?](./ethereum/why-we-want-a-new-blockchain.md)

1. [Ethereum Should Do Something New](./ethereum/ethereum-should-do-something-new.md)

2. [Ethereum Trie](./ethereum/ethereum-trie.md)

3. [Ethereum Account and State](./ethereum/ethereum-account-state.md)

4. [Ethereum Block and Network](./ethereum/ethereum-block-and-network.md)

5. [Why Use GoLang to Build a Blockchain?](./ethereum/why-use-golang-to-build-a-blockchain.md)

6. EIP-1559

   



### Security 

1. How do you handle security in web3 applications and what are some best practices

2. What is the difference between proof of work pow and proof of stake pos differ

3. What is Cryptography?

4. How does a blockchain achieve consensus and what are some common consensus algorithm

5. What is the Encryption Function in the Blockchain?

6. Blockchain Ecosystem: What Are the Essential Elements? Explain.**

7. zero knowledge proof

8. 区块链的共识过程是什么？

9. 以太坊挖矿操作的工作原理是什么呢？

10. 区块链中最常用的两种共识协议是什么？

11. 请简述权益证明的工作原理。

12. 以太坊使用哪种共识协议呢？

13. Classical Smart contract Securilty problems

14. 挖矿选项中的“etherbase”是什么？

    



### EVM

1. What is the importance of EVM in Ethereum
2. 以太坊虚拟机都包含哪些部分？以太坊虚拟机的内存都有哪些部分？

3. 请解释一下存储（Storage）。

4. 请解释一下内存（Memory）。

5. 请解释一下Calldata。

6. 存储区和内存区分别存储了哪些变量？

7. EVM调用和非EVM调用之间有什么区别呢？
8. 以太坊虚拟机需要什么工具来运行智能合约？



### Token

1. How is Ether used in the Ethereum blockchain?
2. 在以太坊中，Wei和Ether(以太币)有什么区别？
3. 以太币是如何产生的？



### Smart Contract

1. What is a smart contract?
2. Which languages are used commonly for smart contract development?
3. How can smart contracts serve real-world use cases?
4. Do you know about the components of a smart contract?
5. How can you reduce gas costs for smart contracts?
6. What are the steps involved in smart contract verification?
7. How is a smart contract library useful?
8. What must be in place before smart contracts can be used?
9. What steps are there to verify a smart contract?
10. How can we Developing MyContract?
11. How can we return mapping list in Solidity?
12. Solidity是静态类型语言（类型的检查是在运行前做的，如编译阶段）还是动态类型语言（类型的检查是在运行时做的）？
13. Solidity中的什么结构与Java中的类（Class）相对应？
14. 智能合约的实例是什么？
15. 在Solidity文件中需要指定的第一个参数是什么？
16. 一个智能合约包含什么？
17. 智能合约中都有哪些类型的函数？
18. 如果我将多个智能合约定义放入单个Solidity文件中，会出现什么样的错误？
19. 两个智能合约可以通过哪些方式进行交互？
20. 当你尝试部署具有多个智能合约的文件时会发生什么？
21. 如果我有一个庞大的项目，我是否需要将所有相关的智能合约保存在一个文件中？
22. 我是否只能导入本地文件？
23. ABI是什么？

24. 智能合约的执行是免费的吗？

25. 查看智能合约的状态是免费的吗？

26. 谁来执行智能合约？
27. 如何设定智能合约的以太币余额限制，如果向有余额限制的智能合约中发送超额的以太币会发生什么？
28. 如何在智能合约帐户中设置msg.val的值？
29. 如果执行智能合约的花费少于交易者支付的燃料费用，他是否会获得退款？
30. 问：节点在哪里运行智能合约的代码呢？
31. What are the recommended methods for testing smart contracts?
32. Do you know the specific methods for automated and manual testing of smart contracts?
33. What are the mandatory prerequisites for deploying smart contracts?
34. [How to attack a smart contract?](problems/how-to-attack-smart-contract.md)



### Account

1. Which types of accounts can you find in Ethereum?
2. What are the important fields in Ethereum accounts?
3. 在私钥丢失后，用户是否还可以恢复以太坊帐户？



### Transaction 

1.  What is a transaction request?
2. What is the recommended method for checking the ETH balance?
3. 以太坊的交易记录存放在哪里？
4. Can you explain the difference between on chain and off chain transactions in web3
5. 你是否能在以太坊中“隐藏”一笔交易？
6. 为什么以太坊中要引入燃料费用呢？
7. 燃料价格是否能决定交易被处理的时间？
8. 交易中的燃料使用量取决于什么？
9. 交易费该如何计算？
10. 签署一笔交易需要用到什么工具？

#### 

#### DApp

1. Can you describe a decentralized application?
2. Are there any Popular Platforms for Building Blockchain Applications?**
3. DApp与智能合约有何不同？
4. DApp和智能合约如何交互？



### Geth

1. 以太坊中异常火爆的Geth是什么呢？

2. 连接到Geth客户端的默认方式是什么？

3. 你可以使用哪些RPC通过网络连接到Geth客户端？

4. Geth的“快速”同步是什么，为什么它更快速呢？

5. 如何使用IPC-RPC连接两个Geth客户端？

6. Geth客户端中帐户存储在哪里？

7. 如何使用Geth给账户发起一笔交易？

8. Geth客户端是否能用来挖矿？

   


### Tools

1. What is Metamask? ：Metamask使用什么节点？ 相比于传统以太坊钱包，有哪些功能是Metamask不支持的？
2. What is Truffle?
3. Remix是什么？
4. 在Remix中，你可以连接哪些节点？
5. How is Vyper a suitable alternative to Solidity for smart contract programming?
6. Are Yul and Yul+ reliable for smart contract programming?
