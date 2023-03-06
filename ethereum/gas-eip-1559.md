# EIP-1559

### Why need Token in BlockChain?

In blockchain technology, tokens are units of value or digital assets that are stored and transferred on a blockchain network. Tokens can be used to represent various things, such as cryptocurrencies, digital assets, voting rights, or access to a particular service or platform.

Tokens are necessary in blockchain for several reasons:

1. Facilitating Transactions: Tokens serve as a means of exchange and can be used to facilitate transactions within a blockchain network. For example, in a cryptocurrency blockchain, tokens are used to buy and sell goods and services.
2. Enabling Smart Contracts: Smart contracts are self-executing contracts with the terms of the agreement between buyer and seller being directly written into lines of code. Tokens are used in smart contracts as a way to execute the terms of the agreement.
3. Security and Transparency: Tokens can enhance security and transparency within blockchain networks. The use of tokens helps to prevent fraud and other forms of illegal activity by creating a clear and secure record of transactions.
4. Community Building: Tokens can also be used to incentivize community members to participate in a blockchain network, such as through mining or staking. This helps to build a strong and engaged community that can help to drive the success of the network.

Overall, tokens are an essential component of blockchain technology, as they serve as the building blocks for the creation of decentralized applications, digital assets, and cryptocurrencies.

I think the most important reason is that the blockchain is a distributed service that requires a large number of miners to join. Then there needs to be something to seduce others.



### Wei and Ether

Both Wei and Ether are units of cryptocurrency in the Ethereum blockchain network.

Wei is the smallest unit of Ether, similar to Satoshi in Bitcoin. 1 Ether is equal to 10^18 Wei, therefore, 1 Wei is equal to 0.000000000000000001 Ether.

Ether, the native cryptocurrency in the Ethereum network, is generated through mining and trading activities.

Smart contracts on the Ethereum network can pay transaction fees in Ether, which are paid in the form of Wei. Transaction fees are collected by miners to incentivize them to validate transactions on the network.

Below is a more detailed description of how Wei and Ether are minted, modified, queried and deleted:

1. Generation: Ether is generated through the mining process of the Ethereum network. Mining is a computationally intensive process designed to verify new transactions and add them to the blockchain. Miners earn new ether by solving complex mathematical puzzles, and they are also rewarded with transaction fees and other rewards.

2. Modification: Ether is stored on the Ethereum blockchain and cannot be modified or deleted. They can only be moved by executing a new transaction. When a transaction is executed, ether is transferred from one account to another, which creates a new transaction record on the blockchain.

3. Query: You can query the balance and transaction records of Ethereum and Wei through the blockchain browser on the Ethereum network. Users can use the Ethereum Wallet app or other third-party apps to check their account balances.

4. Deletion: Ether and Wei are digital assets on the Ethereum blockchain and cannot be deleted. However, if an account is deemed defunct or no longer in use, its balance may be considered "dead" and removed from the blockchain. This will show up on the blockchain explorer as the account balance is zero.



### Gas

Gas represents the computational cost required to complete an operation. When a transaction or smart contract is submitted to the Ethereum network, it needs to consume a certain amount of Gas, which will eventually be consumed by miners.

Ethereum needs Gas for the following reasons:

1. Prevent DDoS attacks: The Ethereum network needs to calculate the cost of each operation, so a certain Gas fee needs to be paid when performing the operation, which can prevent malicious users from exhausting network resources through a large number of meaningless operations.

2. Network economics: Since the Ethereum network is distributed, nodes need to communicate and collaborate with each other to reach consensus. By paying Gas, the efficient use of network resources can be ensured, thereby improving the economy of the network.

3. Encourage miners: Gas fees are one of the sources of income for Ethereum miners. Since miners need to consume electricity and computing power to verify transactions and blocks, paying enough gas fees can encourage miners to verify transactions faster and pack them into blocks.



### EIP-1559

From its purpose, it is a proposal to try to reduce transaction fees.

In the past, the efficiency of Ethereum was indeed not high. The reason is Ethereum's "first price auction".

When transactions are congested, Ethereum adopts the first-price auction principle to select transactions, in other words, "the one with the highest price wins". If 10 people bid 1 to 10 respectively, then miners will naturally choose the five transactions with bids 6 to 10 to be uploaded to the chain.



![fee1](..\pictures\fee1.png)

The result is that the more congested the network is, the more users are anxious to confirm the transaction, and the higher the transaction fee paid by the user.


The starting point of EIP-1559 is to change the above situation - this method is the uniform price auction.

Continuing to consider the previous situation, 10 people bid 1-10 respectively, and the miners choose 5 packs.

In the uniform price auction, each person who successfully goes on the chain does not need to pay his own asking price, but only needs to pay the bid of the person with the lowest bid among all the packaged transactions, and then the miners get the money as a reward. In this way, people who bid 6-10 are still packaged and uploaded to the chain, but each person only needs to pay 6.

![fee2](..\pictures\fee2.png)



This proposal is naturally good for users. For them, transaction fees are reduced
For miners, this auction method must be bad, because the income is significantly lower.

So a miner can do this. When he finds that the price of this round of packaging is obviously too low, such as 1, he might as well generate a transaction to raise the price by himself, such as 3!
When the network is already congested, these transactions generated by miners occupy the limited resources.

##### Burn base fee

How to do it?

In reality, there may not be many ways, but in the blockchain, there is really a way:

Miners do not receive fees, but burn instead. If the handling fee needs to be destroyed, then it is not feasible for the miners to send the transaction by themselves; now sending the transaction becomes really burning their own money, and the increased handling fee will not fall into their own hands.

EIP-1559 changed this handling fee to a word called basic fee. The basic fee must be destroyed.
But there is also a concept of tipping at the same time. If the user is really in a hurry, you can send a tip. Tips will be received by miners.

Even, this plan has another advantage, the total number of Ethereum will decrease, then the single value of Ethereum will rise in the long-term trend.

But is this really the case?
From the perspective of miners, they are not subordinates or hired by anyone - they are one of the most important partners of Ethereum, because they provide the most important computing power in a PoW blockchain.

For miners, the base fee will be burned, so they can ask traders "unless you give us enough tips, I will not accept your transaction even if you give the base fee." 

[According](https://ultrasound.money/) to data from Ultra Sound Money, 7.67 ETH is burned every minute, and up to 11,042 ETH is burned each day. At current rates, approximately 4 million ETH is burned every year. However, the blockchain currently emits about 5.4 million ETH per year.