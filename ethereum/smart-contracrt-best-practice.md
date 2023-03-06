# Smart Contract Best Practice

### Best Practice

- If I have a huge project, do I need to keep all related smart contracts in one file?
  - No, you don't need to keep all related smart contracts in one file. You can put them in separate files and then use the Solidity import statement to include them in the main contract.
- Can I only import local files in smart contract?
  - Yes
- What is an ABI?
  - ABI (Application Binary Interface) refers to the specification of the functions and parameters required to interact with a smart contract.
- Is it free to check the status of the smart contract?
  - Yes
- How to set the Ether balance limit of the smart contract, what will happen if you send excess Ether to the smart contract with balance limit?
  - You can use the payable function and require statement to set the Ether balance limit of a smart contract. If you send excess Ether to a smart contract with a balance limit, the excess Ether will be rejected and returned to the sender's account.
- How to set the value of msg.val in the smart contract account?
  - msg.value is a global variable that stores the amount of Ether carried by the current transaction. You can use the payable function and require statement to set the value of msg.value to any value you want.
- Will the trader get a refund if the cost of executing the smart contract is less than the gas he paid?
  - It depends on the specific smart contract and the platform it is deployed on. Some smart contracts may have a refund mechanism built-in, while others may not. In general, if the cost of executing the smart contract is less than the gas paid by the trader, the excess gas will be lost and not refunded.
- In what ways can two smart contracts interact?
  - Two smart contracts can interact with each other in various ways, such as through function calls, events, and messaging. Function calls allow one smart contract to invoke a function on another smart contract, passing in parameters and receiving return values. Events allow smart contracts to emit and listen for events, enabling them to communicate with each other and react to specific conditions. Messaging is a more complex form of interaction that involves sending and receiving messages between smart contracts, allowing for more sophisticated forms of communication and coordination.



### Verification

What are the steps involved in smart contract verification?

1. Normalized Smart Contracts: Transform smart contracts into a mathematical model or specification so that their correctness can be more easily verified.

2. Static Analysis: Perform static analysis on the contract code to identify possible vulnerabilities and errors in the code.

3. Dynamic testing: Dynamic testing of the contract to ensure that the contract can be executed as expected in actual execution.

4. Formal Verification: Smart contracts are verified using formal methods to prove that they conform to the specification.

5. Manual review: A professional audit team will manually review the contract to find other possible loopholes and security issues.



### Deploy

- How to deploy a file with multi smart contracts？
  - When attempting to deploy a file with multiple smart contracts, each smart contract will need to be compiled and deployed separately. This is because each smart contract has its own address and bytecode and needs to be deployed independently of other smart contracts.
  - If you're using the Ethereum Virtual Machine (EVM), you can use development tools like Truffle to compile and deploy smart contracts. Truffle can help you automate this process and ensure that each contract is deployed correctly.
  - When deploying multiple smart contracts, you need to ensure that the communication between the smart contracts is correct. This can be achieved by defining interfaces and calling functions between smart contracts. You also need to ensure that each smart contract has access to the other contracts it needs.
  - In summary, deploying a file with multiple smart contracts requires separate compilation and deployment, and ensuring correct communication and dependencies between smart contracts.



### Test

To be done.