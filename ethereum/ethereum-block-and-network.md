# Ethereum Block and Network



In all blockchain projects, the data structure composed of blocks is one of the core. The reason why it is called "blockchain" is precisely because these projects organize all blocks in a chain structure, and Ethereum is no exception. Of course, in addition to the chain structure, some other functions have been added to Ethereum, such as the maintenance of uncle blocks, main chain and side chain, etc.



The code about the blockchain structure in Ethereum is located in three directories:

1. core (only contains go files in the directory)
2. core/rawdb
3. light



The go file in the core directory contains almost all important functions and is the core code of the Ethereum blockchain. Among them, the BlockChain structure and method implemented in blockchain.go is the core implementation; the HeaderChain implemented in headerchain.go realizes the management of block headers.

The core/rawdb directory implements methods for **reading and writing all block structures from the database**. From these codes you can see how the blockchain is organized in the code.

The code in the light directory implements the organization and maintenance of the blockchain **in the light synchronization mode** (described later).



### What is Block and Chain

From wiki,

> Blockchain is a series of transaction records (also known as blocks) that are connected and protected by cryptography. Each block contains the encrypted hash of the previous block, the corresponding time stamp and transaction data (usually represented by the hash value calculated by the Merkle tree algorithm) [7], this design makes the content of the block difficult to tamper characteristics. The distributed ledger connected by the blockchain allows two parties to effectively record the transaction, and the transaction can be permanently verified.

Almost all blockchain projects are essentially about recording and confirming **transactions**. And this recording and confirmation is carried out through blocks. That is to say, after the miners check the legality of some **transactions**, they are packaged in the form of **blocks**, thus generating a new block data.

In each block, there will be a field to record the hash of its parent block. It is the hash of this parent block that forms the block into a one-way list structure similar to the data structure, also known as a "chain".

This is what blockchain is about.
The method of using the hash of the parent block to form a chain can prevent the block from being tampered with, because if a block is modified, its hash will change, resulting in a discrepancy with the hash recorded in the child block, thus making this Such modifications are not recognized.
The benefits of forming a chain also include easier handling of branching (i.e. forking). Just imagine that if blocks are organized in the form of an array, if there is a branch, it will definitely not be as convenient as a linked list.



The chain maybe looks like this,

![chains](../pictures/chains.png)





Most blocks form a chain, and each block points to its own parent block until the **Genesis block**. But it is also easy to notice that there is not only one chain from the beginning to the end, but there are many long or short branch chains like "burrs". These branch chains are called **side chains**, and the main chain is the **main chain**, and this situation of branch chains is called a **fork**.

Each block will have a **height**, which is a count of the block's position on the chain. For example, the height of the genesis block is 0 because it is the first block. The height of the second block is 1, and so on. If we carefully observe the block height in the figure, we will find that the height of the last block on the main chain is not the largest. This shows that in Ethereum, the block height is not used to judge whether it is the main chain or the side chain. We will discuss this issue in more detail later.

Regardless of whether it is the main chain or the side chain, some blocks on the side chain are "included" back, that is to say, some blocks will not only point to the parent block, but may also point to the blocks of their own uncles. This is a more distinctive feature in Ethereum, called uncle block.

There are also some blocks that are not on the chain, these blocks are called **future blocks**. Ethereum sometimes receives some blocks with timestamps that are much larger than the parent block, so these blocks are temporarily stored as "future blocks". Try adding it to the chain when the time comes.



### Blocks

In core/types/block.go



```go
// Block represents an entire block in the Ethereum blockchain.
type Block struct {
   header       *Header  
   uncles       []*Header
   transactions Transactions
   withdrawals  Withdrawals

   // caches
   hash atomic.Value
   size atomic.Value

   // These fields are used by package eth to track
   // inter-peer block relay.
   ReceivedAt   time.Time
   ReceivedFrom interface{}
}
```



Fixme







### Questions

0. 以太坊的平均区块间隔时间是多少？

1. 以太坊的平均区块大小是多少？

2. 以太坊中的节点是什么？用什么方法可以连接到以太坊节点？

3. 与以太坊网络交互都哪些方法？

4. Name some Types of Ethereum Networks?

5. What is an Ethereum Client?

   

6. How does a blockchain recognize a Block?

7. In a Blockchain database, what various kinds of records can you find?

8. Is it possible to make changes to the data after it has been written in a block?

   The code about the blockchain structure in Ethereum is located in three directories:

   core directory (only contains go files in the directory)
   core/rawdb directory
   light directory

9. 以太坊主链已经很强大了，为什么还要使用以太坊私有链？

10. 如何查看一笔交易或一个区块的详细信息？

11. 如何查看私有链中一笔交易或一个区块的详细信息？