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



Zcash is the first widespread application of zk-SNARKs, a novel form of zero-knowledge cryptography. Zcash's strong privacy guarantees stem from the fact that shielded transactions in Zcash can be fully encrypted on the blockchain, yet still verifiable under the network's consensus rules by using zk-SNARK proofs.

The acronym zk-SNARK stands for "Zero-Knowledge Succinct Non-Interactive Argument of Knowledge" and refers to a proof structure in which one can prove possession of certain information, such as a secret key, while There is no need to reveal that information, and there is no interaction between prover and verifier.



Zcash is the first widespread application of zk-SNARKs. Zcash's strong privacy guarantees stem from the fact that shielded transactions in Zcash can be fully encrypted on the blockchain, yet still verifiable under the network's consensus rules by using zk-SNARK proofs.

**One can prove possession of certain information, such as a private key, without revealing that information, and without any interaction between the prover and the verifier.**

"Zero-knowledge" proofs allow one party (the prover) to prove to another party (the verifier) that a statement is true without revealing any information beyond the validity of the statement itself. For example, given a hash of a random number, a prover can convince a verifier that there is indeed a number with that hash value, and that the prover really knows that number, without revealing what it is.

"Succinct" zero-knowledge proofs can be verified in milliseconds, even for statements about very large programs, and the proof length is only a few hundred bytes. In a "non-interactive" structure, a proof consists of a single message sent from the prover to the verifier.

Define V to represent the verifier, P to represent the prover, F(x), M(x) are polynomial functions, and the highest order is K



##### Polynomial Zero Problem

Suppose V has a function F(x) and P has a function M(x). P tries to prove that P knows F(x), ie M(x) = F(x)

Then first, P asks V to give it a random number a, and then P returns the value of M(a) to V.

V calculates F(a) == M(a).

This is because the zeros of the polynomial are finite and at most the order K of the equation. If M(x) recognized by P is not F(x). Then g(x) = F(x) - M(x) with only not many and K zeros. V is a value a randomly selected within the range of real numbers, which just satisfies g(a), and the probability of wrong judgment of V is extremely low.

In fact, V can repeat this operation 100 times. If these 100 P times give correct results, it is almost certain that P really knows F(x), that is, M(x) = F(x).

If P really doesn't know F(x), it is guessing, and the difficulty of guessing will even increase rapidly with the increase of K.



##### Digital Encryption

Choose a base number, such as 5, if we want to encrypt 3, the encryption method is 5^3= 125

Define the encryption function as E(v) = g^v mod n, where v is the number we need to encrypt. Obviously, if one obtains E(a) in a transmission, it is almost impossible for that person to deduce what a actually is.

What are the advantages of this function?



Suppose V knows F(x) = x^3 + x^2 + x, which can be expressed as (1, 1, 0 ) base g.

P tries to prove that he knows the equation.

Then V generates a random number a, and will send a set of numbers to P A0 = g<sup>a</sup>, A1 = g<sup>a<sup>2</sup></sup>, A2 = g< sup>a<sup>3</sup></sup>

P performs the following operations.

result = A0 * A1 * A2 = g<sup>a</sup> * g<sup>a<sup>2 </sup></sup>* g<sup>a<sup>3</sup></sup> = g<sup>a<sup>3</sup>+ a<sup>2</sup>+a</sup>

P just send the result back.



After V receives the result and knows g and a, he can quickly verify the result.



In this process,

V did not expose g, a.

It is difficult for P to guess the result without knowing F(x).



##### Restricting a Polynomial

Notice!

As V, our real expectation is that P use the A0 = g<sup>a</sup> sent by me, A1 = g<sup>a<sup>2</sup></sup>, A2 = g<sup >a<sup>3</sup></sup>, with polynomial coefficients for calculation.

But if there is a fake FP, it can hold the coefficient of g (initiate a random request first), such as B0 = g<sup>b</sup>, B1 = g<sup>b<sup>2</sup ></sup>, B2 = g<sup>b<sup>3</sup></sup>

Then use these numbers to violently piece together the result.



To solve this problem, we introduce Knowledge-of-Exponent Assumption” (KEA)

V first generates a random number r and an offset a, and sends two sets of data to P.

  A0 = g<sup>r</sup>, A1 = g<sup>r<sup>2</sup></sup>, A2 = g<sup>r<sup>3</sup></sup >

B0 = g<sup>ar</sup>, B1 = g<sup>ar<sup>2</sup></sup>, B2 = g<sup>ar<sup>3</sup></sup >



P must count the two groups at the same time.



So far, we have solved zero-knowledge. Obviously, it is completely impossible for P to gain any knowledge from the data given by V.

Why do we even need to have non-interactive?

Because the interactive proof is only valid for the original verifier V, no one else (other verifiers) can trust this proof,

Obviously, V can tell P about r and a. P can happily generate these fake data. The other V's certainly can't trust P's credibility.

Instead, each V requires P to interact with itself.



Use the elliptic curve to realize the following function, which satisfies the definition

e(g<sup>a</sup> , g<sup>b</sup> ) = e(g<sup>b</sup> , g<sup>a</sup> ) = e(g<sup>ab</sup>, g<sup>1</sup> ) = e(g<sup>1</sup> ,g<sup>ab</sup>)) = e(g<sup>1 </sup> , g<sup>a</sup> )<sup>b</sup> = e(g<sup>1</sup> , g<sup>1</sup> ) <sup>ab </sup>



We let an honest party generate secret values r and α. Once α and all necessary powers of r and their corresponding α offsets are generated and encrypted, the original data must be deleted. Call it common reference string or CRS

(g<sup>a</sup>, g<sup>r<sup>i</sup></sup> , g<sup>ar<sup>i</sup></sup> , r = 0 1,..., d ).



Among them, V needs to send g<sup>r<sup>i</sup></sup> , g<sup>ar<sup>i</sup></sup> to P.

P returns the calculation result to V according to the function coefficients it knows.

V uses (g<sup>a</sup>, g<sup>r<sup>i</sup></sup> ) verification.



Of course, if all nodes generate r and a continuously in the actual environment, this is the setup process.

Generally speaking, we don't need to prove "whether someone knows a polynomial", but "whether someone knows a secret value, which satisfies certain conditions (such as the hash value x)". So how to turn the problem of "does someone know a secret value, which satisfies certain conditions" into a question of "does someone know a polynomial"?

We can write a program to check whether this value satisfies the condition. If it is satisfied, it will output 1, and if it is not satisfied, it will output 0. And through some methods that people have developed, the program can be converted into a circuit, and the input and output of the circuit are the program. Input-Output (P(x) = A(x)B(x)-C(x)). And the circuit can be converted into a polynomial with a specific zero root (the coefficients of the polynomial are related to each input and output of the circuit).



### ZK Rollups

Rollup is a scaling solution that executes transactions outside L1 but publishes transaction data on L1. This way of working allows rollups to expand the network while still being securely protected by the Ethereum consensus. Moving computation off-chain can actually process more transactions. Because only some data of the rollup transaction needs to be put into the Ethereum block.

After executing the transactions on the rollup, the next step is to package these transactions into a batch and publish it to the Ethereum main chain. The whole process is basically executing transactions, extracting data, compressing them, rolling them into batches and sending them to the main chain, hence the name - "rollup".

How does Ethereum know that this data is valid and not submitted by malicious actors for profit? Each rollup deploys a set of smart contracts in L1 to process deposits, withdrawals, and verify proofs. Proof is also the main factor that differentiates the different types of rollups.


In ZK rollups, each batch published to L1 contains a cryptographic proof called a ZK-SNARK. After the transaction batch is submitted to L1, the contract on L1 can quickly verify the ZK-SNARK proof, and invalid batches will be directly rejected.
