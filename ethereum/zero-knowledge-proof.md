# Zero Knowledge Proof and zk-SNARK

Here's the classic example given in every complexity course I've taken:
Let's say your friend is colorblind.

1. You have two billiard balls; one is red and one is green, but they are otherwise identical.
2. To your friend they look identical and he doubts they can really be distinguished.
3. You want to prove to him that they are actually different colors.
4. On the other hand, you don't want him to know which is red and which is green.

This is the proof system.

1. You give your friend two balls to hold one in each hand.
2. At this point you can see the ball, but you don't tell him which is which.
3. Then your friend puts his hands behind his back. Next, he either switches the balls between the hands or leaves them as they are, with probability 1/2 for each hand. Finally, he brought them out from behind.
4. You now have to "guess" if he switched the ball.

You can of course say for sure if he replaced them by looking at their color.
On the other hand, if they are the same color and are therefore indistinguishable, then it is impossible for you to guess correctly with a probability higher than 1/2.

If you and your friend repeat this "proof" 10000 times, your friend should be confident that the balls are indeed different colors; otherwise, your probability of successfully identifying all switches/non-switches is at most 2^(−10000).

Also, the proof is "zero-knowledge" because your friend will never know which ball is green and which is red;
In fact, he knew nothing about how to distinguish the balls.



### zk-SNARK

Around 2013, ZK-SNARKs (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge), an algorithm for constructing digital signatures based on interactive zero-knowledge proofs, was practically feasible and implemented, and actually used in applications.



fixme

Zcash 是 zk-SNARKs 的第一个广泛应用，zk-SNARKs 是一种新颖的零知识密码学形式。Zcash 强大的隐私保证源于这样一个事实，即 Zcash 中的屏蔽交易可以在区块链上完全加密，但仍然可以通过使用 zk-SNARK 证明在网络的共识规则下验证其有效性。

首字母缩略词 zk-SNARK 代表“零知识简洁的非交互式知识论证”，指的是一种证明结构，在这种结构中，人们可以证明拥有某些信息，例如一个秘密密钥，而无需透露该信息，并且之间没有任何交互证明者和验证者。



Zcash is the first widespread application of zk-SNARKs. Zcash's strong privacy guarantees stem from the fact that shielded transactions in Zcash can be fully encrypted on the blockchain, yet still verifiable under the network's consensus rules by using zk-SNARK proofs.

**One can prove possession of certain information, such as a private key, without revealing that information, and without any interaction between the prover and the verifier.**

"Zero-knowledge" proofs allow one party (the prover) to prove to another party (the verifier) that a statement is true without revealing any information beyond the validity of the statement itself. For example, given a hash of a random number, a prover can convince a verifier that there is indeed a number with that hash value, and that the prover really knows that number, without revealing what it is.

"Succinct" zero-knowledge proofs can be verified in milliseconds, even for statements about very large programs, and the proof length is only a few hundred bytes. In a "non-interactive" structure, a proof consists of a single message sent from the prover to the verifier.



https://rujia.uk/resource/ZK-SNARK.pdf



f(x) = x 3 − 6x 2 + 11x − 6



### ZK Rollups

Rollup is a scaling solution that executes transactions outside L1 but publishes transaction data on L1. This way of working allows rollups to expand the network while still being securely protected by the Ethereum consensus. Moving computation off-chain can actually process more transactions. Because only some data of the rollup transaction needs to be put into the Ethereum block.

After executing the transactions on the rollup, the next step is to package these transactions into a batch and publish it to the Ethereum main chain. The whole process is basically executing transactions, extracting data, compressing them, rolling them into batches and sending them to the main chain, hence the name - "rollup".

How does Ethereum know that this data is valid and not submitted by malicious actors for profit? Each rollup deploys a set of smart contracts in L1 to process deposits, withdrawals, and verify proofs. Proof is also the main factor that differentiates the different types of rollups.


In ZK rollups, each batch published to L1 contains a cryptographic proof called a ZK-SNARK. After the transaction batch is submitted to L1, the contract on L1 can quickly verify the ZK-SNARK proof, and invalid batches will be directly rejected.