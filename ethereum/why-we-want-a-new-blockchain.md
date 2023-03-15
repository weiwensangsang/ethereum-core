# 00.Why We Want a New Blockchain?



#### Pros and Cons about Bitcoin

Despite some new use cases, such as China developing a crypto RMB based on blockchain and claiming that government allocations can reach the grassroots without any third-party involvement, some people's perception of blockchain is still getting rich overnight and gambling.

The high valuation of Bitcoin, which is the highest valued cryptocurrency, has largely influenced people's fascination with blockchain technology. However, from 2022 to 2023, the price of Bitcoin fell by about 70% and the financing of the blockchain industry suffered a significant decline as a result.

A decade ago, from 2012 to 2013, the price of Bitcoin increased dramatically, going from $12 to $1,200. This sparked interest in the technology behind it and countless people began to pursue the technology architecture of Bitcoin, which has since become an industry standard.

In short, the operation of Bitcoin is as follows.

- Create a new Wallet.

  1. Creating a Bitcoin wallet is equivalent to registering a tradeable account on the Bitcoin system. The wallet includes two key pieces of information: a Public Key and a Private Key. The public key can be made public and anyone can send Bitcoins to that address, similar to a bank account. The private key can be used to sign transactions, similar to a password.
  2. https://github.com/bitcoin/bitcoin/blob/master/src/wallet/wallet.cpp
  3. [http://bitaddress.org](https://link.zhihu.com/?target=http%3A//bitaddress.org)

- Create a New Bitcoin token.

  1. Transaction Collection: Bitcoin miners gather all unconfirmed transactions, as a "block".
  2. Proof-of-Work: The miner calculates a unique hash value. The miner compares the hash value with a difficulty target (such as the number of leading zeros).
  3. Transaction Confirmation: The block can be submitted to the Bitcoin network, and all transactions contained in it will be confirmed, the miner receives a certain amount of new bitcoins as a reward.

- Send token to another account.

  

We can conclude several things:

1. The security of transactions greatly depends on the current total computing power and the distribution of computing power in the blockchain.
   - If there is only one block and one miner, then the blockchain degenerates into a local database with no actual meaning to its data.
   - If a blockchain project's blocks and miners all belong to the same political organization or company, then the blockchain degenerates into a centralized database with no essential difference from using a traditional database, and even slower.
2. In order to maintain a decentralized blockchain, incentives are needed, such as tokens similar to Bitcoin, or else no one will waste their valuable computing resources on the blockchain.
3. The higher the economic value of the token, the more people will join the blockchain.
4. Bitcoin has only one practical function, transfer of funds.




#### Try to add new features for Bitcoin: Counterparty 

There's an interesting fact that you can make a Bitcoin transfer to yourself. This may seem like a silly thing to do because you have to pay a fee, but it actually serves a purpose.

In 2014, there was a difference of opinion within the Bitcoin community on what Bitcoin and blockchain were for. A lot of people, including some influencers, agreed that Bitcoin should only focus on transfers, and that blockchain was just for accounting purposes(In Bitcoin).

However, there were also those who believed that blockchain should have other uses. Looking back now, it's obvious that this was the case, as blockchain's unalterable properties are extremely valuable, and since it has already provided such excellent support for the highly accurate money transfer business, why not develop other businesses as well? In theory, any internet business could migrate their operations to the blockchain (for example, the tweets you send can't be deleted or modified by anyone).

With this in mind, Counterparty started trying to store more data on the Bitcoin blockchain. Their goal was to simply publish the data to the blockchain and then use other read interfaces to access the data and process it themselves.

The specific method was to transfer Bitcoin to their own account, and in this transaction, they would place their business data in the special field OP_Return of that transaction, and then spread the transaction, waiting for their business data to be stored by the miner.

This was obviously a hack-like solution. OP_Return is not designed for this. When this method was publicly announced, a lot of criticism emerged.

"Counterparty didn't participate in the existing community, they just flipped the switch and started using the Bitcoin P2P nodes as extra data storage."

https://www.btcstudy.org/2022/07/18/dapps-or-only-bitcoin-transactions-the-2014-debate/

This is somewhat reasonable, as Counterparty essentially inserts its own data into the Bitcoin network, and therefore, all Bitcoin miners are required to provide storage services for Counterparty's data. This doesn't seem ideal.



**So, what should engineers do?**
