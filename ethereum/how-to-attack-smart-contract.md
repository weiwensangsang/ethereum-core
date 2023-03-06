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





几个点：

智能合约内的变量可以视作合约内部的全局变量。

智能合约的所有函数都可以被访问，

智能合约的所有数据都是可见的，即使列为私有变量也是可以被取出的。

智能合约可以调用外部合约，这意味外部合约也可以基于调用外部合约

#### send()”、“transfer()”、“call.value()







http://yangzhe.me/2022/09/05/solidity-contract-vulnerability/
https://www.zhihu.com/column/p/29690785

How do you handle security in web3 applications and what are some best practices?