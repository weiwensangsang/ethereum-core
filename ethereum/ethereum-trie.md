# Trie



Trie (Merkle Patricia Tree, also known as MPT) is a tree structure used to encrypt and store any (key, value) data pair in ethereum. Its insertion, search and deletion efficiency are all O(log(N)), but it is simpler and easier to understand than other tree structures such as red-black trees, and it also has the characteristics of Merkle trees.



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





Fixme:

https://zhuanlan.zhihu.com/p/50242014