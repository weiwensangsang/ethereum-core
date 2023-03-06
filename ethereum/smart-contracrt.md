# Smart Contract

Smart contracts are one of the most important concepts of Ethereum.
Bitcoin proves that data can be immutable through blockchain technology. Ethereum also puts the code on the blockchain, and has a built-in VM that can run the code.
Unalterable code and data, coupled with the operating environment, means that the Ethereum provides a complete, uncontrolled, immutable computer.

Imagine an Apple Store, where the app running logic is all open and will not be modified by anyone. There, in theory, we can put all the apps into this app  store and re-implement it again. 

This is web3.



### Context

"Smart contracts" are not real contracts, nor are they particularly smart, they just run code on the blockchain.

Smart contracts are kept in a special kind of account on the Ethereum network. We have user accounts and can also have smart contract accounts.

Smart contract accounts are:

- address
- Balance (how much is there: Ether)
- state:  The current state of all variables and variables declared in the smart contract. In fact, the easiest way to understand smart contracts can be compared to instantiating objects of a class, the only difference is that this object will always exist in the blockchain network, which is equivalent to a small database
- the code

Smart contracts can call other smart contracts. A smart contract typically consists of the following components:

1. Code: The code is the set of instructions that define the logic and behavior of the contract. It is written in a programming language that is compatible with the blockchain platform on which the contract is deployed.
2. State: The state is the current status of the contract, including the values of all variables and data structures used in the code. The state is updated each time the contract is executed.
3. Address: Each smart contract is assigned a unique address on the blockchain, which serves as its identifier.
4. Events: Events are messages that the contract can emit when certain conditions are met. These messages can be used to trigger other contracts or to notify external applications of important events.
5. Functions: Functions are the methods that can be called to interact with the contract. They are defined in the code and can be accessed by other contracts or by external users.
6. Gas: Gas is the fee paid by users to execute a smart contract. The amount of gas required for a transaction depends on the complexity of the code and the amount of data being processed.



Let us start with a demo.

```go
contract Counter {
    uint counter;

    function Counter() public {
        counter = 0;
    }
    function count() public {
        counter = counter + 1;
    }
}
```



The code has a variable named "counter" of type uint (unsigned integer). The content (value) of the counter variable is the state of the contract. Whenever we call the count() function, the zone state of this smart contract will be incremented by 1, and this state is visible to everyone.

![contract-demo](..\pictures\contract-demo.png)



Ethereum supports three types of transactions:

- Transfer of value (same as Bitcoin)
  - TO : receiving address
  - DATA : leave blank or leave a message
  - FROM : who issued
  - AMOUNT : how much to send
- create contract
  - **TO : ''''(this is what triggers the creation of the smart contract)**
  - DATA : Contains the smart contract code compiled to bytecode
  - FROM : who created
  - AMOUNT : Can be zero or any amount of ether, it is the deposit we want to give to the contract.
- Call the contract function
  - TO: target contract account address
  - DATA: Contains the function name and parameters - identifies how to call the smart contract function
  - FROM : who calls
  - AMOUNT: Can be zero or any amount of ether, for example to pay for contract services.

This also means that our call to the smart contract is achieved by creating a transaction.



### Language

There are several programming languages that can be used for smart contract development on various blockchain platforms. Here are some of the most common ones:

1. **Solidity**: Solidity is the most commonly used language for developing smart contracts on the Ethereum blockchain. It is a contract-oriented language that is similar to JavaScript and is designed specifically for writing smart contracts.
2. **Vyper**: Vyper is a newer language designed to address some of the security issues with Solidity. It is also used for developing smart contracts on the Ethereum blockchain.
3. **Chaincode** (Go): Chaincode, also known as smart contracts on the Hyperledger Fabric blockchain, can be developed using Go programming language.
4. **Cadence**: Cadence is a new language developed by Dapper Labs for writing smart contracts on the Flow blockchain.
5. **Rust**: Rust is a systems programming language that can be used for writing smart contracts on the NEAR Protocol blockchain.
6. **Michelson**: Michelson is a domain-specific language designed for smart contracts on the Tezos blockchain.

It's worth noting that some blockchains also support multiple programming languages for smart contract development, and new languages are constantly being developed to improve the security, efficiency, and flexibility of smart contracts.



### Smart Contract Can Do Something!

 Smart contracts have the potential to serve real-world use cases in many ways, including:

1. Decentralized Finance (DeFi): Smart contracts can be used to automate financial transactions, such as lending and borrowing, without the need for intermediaries. This can significantly reduce costs and increase efficiency in the financial system.
2. Supply Chain Management: Smart contracts can be used to track the movement of goods and ensure their authenticity, from the manufacturer to the end-user. This can help prevent fraud and improve transparency in supply chain management.
3. Real Estate: Smart contracts can be used to automate real estate transactions, such as property transfers and lease agreements. This can reduce the time and cost associated with traditional real estate transactions.
4. Identity Verification: Smart contracts can be used to verify the identity of individuals, which can be useful in areas such as voting, access to government services, and online transactions.
5. Gaming and Digital Collectibles: Smart contracts can be used to create digital assets, such as in-game items and collectibles, that are secured by the blockchain. This can prevent fraud and create a more transparent and secure gaming environment.
6. Insurance: Smart contracts can be used to automate insurance claims and payouts, which can reduce the time and cost associated with traditional insurance processes.

Overall, smart contracts have the potential to significantly improve efficiency, transparency, and security in many different industries and use cases. As blockchain technology continues to evolve, we can expect to see more innovative applications of smart contracts in the future.

Of course it's worth pointing out that these products aren't powerful enough to replace existing tools, they're just a possibility.
The most important thing about Smart Contract is to lower the threshold for people to create cryptocurrency. We can conduct quick financing through ICO.



### But

While smart contracts can theoretically do anything, they are not well suited for heavy computational work.

The Ethereum World Computer is like an old slow computer that can run simple programs. Keeping Ethereum smart contracts small and simple is critical for cost and security reasons.

The more computation a contract has, the more expensive it is to run it. The more complex the contract, the more likely it is that a security breach will occur. Security holes in smart contracts are difficult to fix because of the immutable nature of the blockchain.



### Questions

- How is a smart contract library useful?
  - a smart contract library can be a very useful tool for smart contract developers, allowing them to save time, improve efficiency, ensure consistency, and enhance security. It can also help to promote standardization and best practices in the development of smart contracts.
