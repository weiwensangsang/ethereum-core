# Ethereum Account and State

There are two account models in the blockchain world: 

1. UTXO (Unspent Transaction Output) model 
2. account balance model



UTXO does not record the account balance, but only records each transaction, and the account balance is obtained by calculating all historical transactions of the account (imagine if you know every transaction in your wife/husband’s bank account transaction, then you can figure out how much money she/he has on the card now).

The account balance model is similar to the bank accounts we often use, and they all save the balance of our account. When someone transfers money to us, we add the value of the balance to the value of the transfer; when we transfer money to someone else, we subtract the value of the transfer from the number of the balance.

From this point of view, the account balance model is relatively easy to understand. Ethereum uses the account balance model, and it is the state module that implements this model. It records the status of each account, and changes the status of the corresponding account whenever a transaction occurs.



### Why does Ethereum use a balance model instead of a UTXO model?

1. Programmable transactions: Ethereum is a **smart contract** platform that allows users to write programmatic smart contracts on the blockchain. This means that transactions in Ethereum may involve multiple inputs and outputs, rather than just one input and one output like in Bitcoin. This complex transaction structure makes the UTXO model difficult to implement, while the balance model is better suited to support these complex transactions.
2. State storage: **Smart contracts** in Ethereum can modify the contract state, which needs to be stored on the blockchain. If a UTXO model is used, every state change would require the creation of new unspent transaction outputs, which would result in huge transaction volumes and high blockchain storage costs. The balance model only needs to update the balance of the contract address, making it more efficient.
3. Computational cost: The execution of **smart contracts** in Ethereum requires computational resources. If a UTXO model is used, since each transaction output has its own value, the outputs must be split and recombined during contract execution, resulting in additional computational costs. The balance model only needs to maintain the balance of each address, making it simpler and more efficient.

In summary, Ethereum uses the balance model to better support programmable transactions, reduce state storage costs, and computational costs.



### State Context

#### state definition

The information of an account is a **state**, and Ethereum is a collection of all **states**. For example, the initial **state** is: {A has 10 yuan, B has 0 yuan}, then A initiates a transaction and gives B 2 yuan, and the **state** becomes {A has 8 yuan, B has 2 yuan}, the intermediate process It's a **state** transition.

The actual initial **state** of Ethereum is the genesis block, which is transferred to a new state every time a new block is generated.



#### state indication

Ethereum uses root to represent **state**. Ethereum uses **Trie** to organize the **state**. Trie can be understood as a combination of dictionary tree and Merkle tree. It has a tree root root. With this root, you can access all **state** data, that is, the information of each account, so Use root to represent a state.



#### get state

There is a field Root in the block header, so if you find the block header, you can get the state of the blockchain.



#### Where does the state exist

**State** does not exist in blocks. The root is stored in the block header, which is just an address, and the **state** data cannot be found from the block.

**State is just temporary data that can be regenerated. The genesis block is the initial state. After executing all the transactions in the first block, a new state is obtained,** and the root of this state is stored in the Root of the first block header. If there are all blocks, all transactions can be executed, and then the state in the latest block can be generated.

The state is stored in an external database. The underlying database of Ethereum is LevelDB, where the blocks are stored and the status is also stored in it. But the state is a Trie, which cannot be directly stored in LevelDB.

Note: Although we can obtain the information of all accounts by traversing and executing all transactions in all blocks, the existence of state allows us to quickly obtain the balance of an account without performing such time-consuming operations every time.





http://yangzhe.me/2019/06/19/ethereum-state/

Fixme