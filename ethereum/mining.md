# Mining

Mining is the process of encapsulating a series of recent unencapsulated transactions into a new block.

Let us start with some context.



### Byzantine generals problem

The state synchronization problem of distributed systems. Each node in a distributed system is a general, and when these nodes want to synchronize their state, they will face the Byzantine general problem.

>  The Byzantine Empire was prosperous, and the generals of several small countries around it coveted it for a long time, but each had their own secrets. More than half of their generals must agree to attack Byzantium and cannot betray on the battlefield (reach a consensus), otherwise the attack will fail and burn themselves. And the general's territory may be divided up by several other generals. Based on this situation, the communication among the generals is very problematic. Some people have duplicity, and some people are loyal to the interests of the organization. How to finally reach a consensus is a problem.

#### POW(Proof Of Work)

In order to solve the Byzantine general problem, we need to determine a method first: 

Select a loyal "general" from among these equal generals, and the other generals can just listen to his decision.

> This seems to violate the idea of decentralization, but after careful analysis, these generals are decentralized equal nodes before making this decision, and the selected generals are only for this decision. Decided to choose again. Instead of a centralized and permanently fixed general.

How to choose a general?
These generals are equal nodes, so we asked them to give a statement on this decision. Generals need to calculate based on known battlefield information, try to draw conclusions (blocks), and then broadcast the conclusions to other generals. If his conclusions are recognized by most generals, then he is the general of this round.
At the same time, the general must always monitor the broadcast content from other generals. Once the conclusion broadcast from other generals is received, the generals will immediately stop the calculations in their hands to verify the content of the broadcast. If all the generals pass the verification, then the first The first general who broadcasts this verifiable result is selected as a general, and this time he decided to listen to his conclusion.

So there are two important factors in this process:

1. The first is speed, the first one who passes the verification can be selected as a general, and the second one who is a step slower has no chance. The problem of speed is the problem of computing power. For example, the computing power of an 8-core 32G computer is definitely faster than that of a single-core 1G.

2. Then there is correctness, that is, whether the conclusion issued by the general is correct or not, and needs to be verified successfully by other generals.

POW provides a way that is difficult to calculate and easy to verify, which is realized based on the characteristics of the hash function.

A hash encryption function can be issued to each node, and each node calculates an encrypted hash by adding a nonce value to the block information to be sealed. This encrypted hash needs to meet certain rules (such as the first four bits must be 1111)
The workload refers to the workload that the node is constantly trying to calculate. After obtaining the eligible block hash, after broadcasting, the ongoing and completed workload of other nodes will be invalidated (in fact, this is also a kind of computing power. waste), this is the block.



This way is not prefect.

##### Question 1: 

What if two nodes produce blocks with the same content at the same time? 

Compare timestamps. The one with an earlier time will be confirmed and kept on-chain, while the one with a later time will be discarded.

##### Question 2:  Fork

If a node publishes a new consensus rule, other nodes do not synchronize the consensus rule?
Nodes that have not synchronized the new rules will continue to mine, and the blocks they dig will not be consensus or recognized by the nodes of the new rules. At this time, the chain is forked and divided into two chains, 1.0 (old consensus rules) and 2.0 (new consensus rules). At this point chains with a larger mass (miner) base will stay.

Of course, some people still use the original 1.0 chain, but its vitality is definitely gone, because **no one will do it for nothing**.



### Source code for Miner