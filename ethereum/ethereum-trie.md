# Trie



Trie (Merkle Patricia Tree, also known as MPT) is a tree structure used to encrypt and store any (key, value) data pair in ethereum. Its insertion, search and deletion efficiency are all O(log(N)), but it is simpler and easier to understand than other tree structures such as red-black trees, and it also has the characteristics of Merkle trees.



Ethereum accounts have multiple attributes (balance, code, storage information), and attributes (status) need to be updated frequently. Therefore, a data structure is needed to meet several requirements:

1. A new tree root can be quickly calculated after performing an insert, modify, or delete operation without recalculating the entire tree.
2. Even if the attacker deliberately constructs a very deep tree, its depth is limited. Otherwise, an attacker could perform a denial of service attack by deliberately building a tree deep enough that each tree update is extremely slow.
3. The root value of the tree depends only on the data, not on the order of updates. Updating in a different order, or even recomputing the tree from scratch will not change the root value of the tree.







### Normal Trie

> Trie, also known as prefix tree or **dictionary tree**, is an ordered tree used to save associative arrays, the keys of which are usually strings. Unlike a binary search tree, the key is not stored directly in the node, but is determined by the node's position in the tree. All descendants of a node have the same prefix, which is the string corresponding to this node, and the root node corresponds to the empty string.

![trie](../pictures/trie.png)

In the figure above, each node is actually just a part of the key, or a character of the key. When traversing down according to a certain key until the last character of the key, the value corresponding to the key is also found.
This way of looking up value is exactly the same as looking up a dictionary m



![Patricia](../pictures/Patricia.png)

This is how we save 8 key-value pairs.

```text
Key			value
6c0a5c71ec20bq3w	5
6c0a5c71ec20CX7j	27
6c0a5c71781a1FXq	18
6c0a5c71781a9Dog	64
6c0a8f743b95zUfe	30
6c0a8f743b95jx5R	2
6c0a8f740d16y03G	43
6c0a8f740d16vcc1	48
```

#### **Merkle Tree**

Merkle Tree, also commonly called Hash Tree, as the name suggests, is a tree that stores hash values.
The main function of the Merkle Tree is that when the Top Hash is obtained, the hash value represents the information summary of the entire tree. When any data in the tree changes, the value of the Top Hash will change. The value of Top Hash will be stored in the block header of the blockchain.

![merkle](../pictures/merkle.png)



### Ethereum Trie

Every time Ethereum executes a transaction, the state of the world corresponding to Ethereum changes. As a public chain platform, Ethereum has a large number of states corresponding to a large number of contracts. Rebuilding the state tree every time a state change occurs will undoubtedly consume huge computing resources. To solve this problem, Ethereum proposes a method of incrementally modifying the state tree. Every time the state of Ethereum changes, the original MPT tree will not be modified, but some branches will be created, as shown in the figure below;



![tree_change](..\pictures\tree_change.png)

Every time the state of Ethereum changes, it will only affect a small number of nodes in the world state MPT tree. The newly generated world state tree only needs to recalculate the hashes of a small number of affected nodes and the nodes connected to them.

The state of Ethereum is very suitable for storage by MPT tree. The characteristics of MPT tree are very consistent with the characteristics of Ethereum state. When using MPT tree to store the state of Ethereum, it can bring the following advantages;

1. When the balance of an account changes, the hash of the corresponding path also changes, and then the hash value on the corresponding path is updated from the bottom up until the State Root, so that the minimum number of hashes can be calculated.
2. The full node in Ethereum maintains an incremental MPT state tree, because each block modifies only a small part of the world state. **Incremental modification** is not only conducive to block rollback, but also saves overhead.
3. Temporary block forks are common in Ethereum, but due to the complexity of Ethereum smart contracts, it is difficult to roll back the state according to the contract code if the original state is not recorded.