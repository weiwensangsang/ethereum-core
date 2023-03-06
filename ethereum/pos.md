# PoS



The consensus mechanism is the method to ensure the consistency of each transaction in the blockchain.
As an ordinary user, it is very difficult to run a full node to verify and record data on the blockchain.
At present, to run an Ethereum full node, at least 800G of data must be stored, and the number is still increasing. The computing power of Ethereum miners is becoming more and more concentrated, and the full nodes are also becoming more and more concentrated. This is obviously detrimental to the security of the entire protocol.

One of the goals of Ethereum 2 is to allow more ordinary people to participate in the consensus mechanism, and to make it easier for more people to run an Ethereum node.

Therefore, Ethereum 2 introduces these two points:

1. POS
2. shard



### Proof of Stake

The consensus algorithm used by Ethereum, Bitcoin and many mature blockchains is POW, Proof of work, and proof of work. Participating in POW is what we often call mining.

POW participants have to invest a lot of money to buy hardware, and continue to consume electricity to compete to generate blocks and get rewards.

POW can easily lead to the concentration of computing power to professional miners.

The participants of POS are called validators—verifiers.

Validator does not need to purchase special hardware and consume a lot of power. It only needs to run a program on an ordinary computer and pledge a part of virtual assets. On Ethereum it is 32 ETH.

The entire network randomly selects participants in proportion to the number of participants' pledged assets and the length of participation to generate new blocks and receive rewards.



### Shard

To improve the performance of Ethereum, we can of course expand the block size so that each block contains more data.
But this will require nodes that store blocks to have larger hard disks and better network bandwidth. This further increases the cost of mining and running a node.

So the Ethereum community abandoned this solution.

The solution that Ethereum wants to adopt is called shard chain.

Simply put, one chain is not enough, we run multiple chains

There will be 64 blockchains running at the same time in Ethereum 2, which may increase in the future.

Another advantage is that the node on the shard only needs to verify and save the data of the current shard, not the data of the entire Ethereum. This can make the node smaller and lighter, reduce the demand for hardware computing power and storage, enable more people to participate, and increase the decentralization and security of the entire Ethereum.

Can shard be implemented under the POW mechanism?

The answer is no. Because after sharding, the difficulty of destroying a single shard chain is actually reduced.

The way POS solves this problem is to let the verifier pledge the ether currency, and if you find that you are sabotaging, you will be fined, or even all the tokens you pledged will be fined.

But the punishment method of POW is to prevent those who do damage from digging blocks. All he loses is the electricity consumed while mining the blocks. In order to achieve the effect of POS confiscating pledges on POW, it is necessary to confiscate even the bad guys’ mining machines, which is obviously impossible.

On the other hand, Ethereum's POS mechanism will randomly assign validators' shards. This mechanism also makes it impossible for vandals to stare at a certain chain for damage, thus increasing the difficulty of its attack.



### Beacon Chain

The beacon chain is at the heart of Ethereum 2. Its main function is to implement the POS mechanism and coordinate and synchronize each shard chain. There is a chain to control the chain.

The beacon chain has been launched on December 1, 2020, and users can already use the smart contract on Ethereum to pledge ETH to participate in POS to obtain rewards.

Although the beacon chain has been launched, its current function is only to verify various basic functions of Ethereum 2 such as POS in the actual combat environment, and it does not have the ability to process transactions and execute smart contracts. Moreover, the currently pledged ETH and the rewards obtained cannot be withdrawn by the lock owner.

The beacon chain and the current Ethereum blockchain run in parallel, that is, the current operation of Ethereum is basically not affected by the beacon chain.



### Next

In the next stage, 64 shard chains will be launched and connected with the beacon chain to form a whole that can cooperate with each other.

The current Ethereum blockchain is linked into the beacon chain. The official name is the docking.

The current Ethereum blockchain will become one of the 64 shard chains, which also marks the official exit of POW mining from the stage of Ethereum.