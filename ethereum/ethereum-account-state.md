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



### StateDB

StateDB is the main object in the state module. It records the information of each account, including balance (number of ether), nonce and other information.

The process of **transactions** being collected into **blocks** by **miners** is the process of **miners** performing **state** **transitions**. Even if there is no **transaction**, **miners** can directly migrate the world state to a new state, such as digging out empty blocks.

Even in the early days of Ethereum, when Ethereum was running for three months, the local folder storage of Ethereum clients ballooned to a staggering 10 to 40 GB. As of block height 9001290, an Ethereum archive node that retains all state needs to occupy 216 GB of space. If these states are all recorded on the blockchain, then this will be a nightmare.

This will make micro-devices such as Internet of Things devices, personal notebooks, and mobile phones unable to use the Ethereum client, which will lead to a decrease in the number of network nodes and affect user usage. Therefore, these states are not directly stored on the blockchain, but these states are maintained in the Merkle prefix tree, and only the corresponding tree Root value is recorded on the blockchain. Use a simple database to maintain the persistent content of the tree, and the database used to maintain the mapping is called StateDB.

There are 2 types of state.

- World state
- Account state

The following information is stored in the account status

1. **nonce**: This value is equal to the number of transactions issued by this account, or the number of contracts created by this account (when this account has an associated code).
2. **balance**: Indicates the account balance of this account.
3. **storageRoot**: Indicates the hash value of the root node of the MPT tree that saves the account storage content.
4. **codeHash**: Indicates the EVM code hash value of the account. When this address receives a message call, these codes will be executed; it is different from other fields and cannot be changed after creation. If codeHash is empty, it means that the account is a simple external account with only nonce and balance.

![state](..\pictures\state.webp)



As shown in the figure above, all account states are maintained through the account address as the key, and the Merkle tree maintained is the world state.
All accounts also have a tree representing the stored data of this account, which is independent and unique.

The account status (such as account balance) can be found from the world state tree through the account address. If it is a contract address, you can also continue to use storageRoot to find the corresponding contract information from the account storage data tree (such as: in the auction contract. product information).



### How to init StateDB

StateDB has many uses:

1. Maintain a mapping from account state to world state.
2. Support modification, rollback, commit status.
3. Supports persistent state to the database.
4. Is the medium through which states enter and exit the Merkle tree.



At first, we should init a stateDB instance. 

First, we need to tell StateDB which state we want to use. Therefore, StateRoot needs to be provided as the root of the Merkle tree to build the tree. 

**The value of StateRoot is equivalent to the data version number**, according to the version number, it can be clearly known which version of the state to use. Of course, the data content is not in the tree and needs to be read in a database. Therefore, stateRoot and db need to be provided when building State DB to complete the build.



```go
db: = state.NewDatabase(levelDB)
statedb, err := state.New(block.Root(), db)

//core/state/statedb.go:92
func New(root common.Hash, db Database) (*StateDB, error) {
	tr, err := db.OpenTrie(root)//①
	if err != nil {
		return nil, err
	}
	return &StateDB{
		db:                db,//②
		trie:              tr,
		stateObjects:      make(map[common.Address]*stateObject),
		stateObjectsDirty: make(map[common.Address]struct{}),
		logs:              make(map[common.Hash][]*types.Log),
		preimages:         make(map[common.Hash][]byte),
		journal:           newJournal(),
	}, nil
}

//core/state/statedb.go:59
type StateDB struct {
	db   Database
	trie Trie
	stateObjects      map[common.Address]*stateObject
	stateObjectsDirty map[common.Address]struct{}
	dbErr error
	refund uint64

	thash, bhash common.Hash
	txIndex      int
	logs         map[common.Hash][]*types.Log
	logSize      uint

	preimages map[common.Hash][]byte
	journal        *journal // change log, can use this to revert change
	validRevisions []revision
	nextRevisionId int
}

// core/state/database.go:42
type Database interface {
	OpenTrie(root common.Hash) (Trie, error)  // Opens the top-level tree containing the world state for the specified state version (root).
	OpenStorageTrie(addrHash, root common.Hash) (Trie, error) // Open the account data storage tree of the specified state version (root) under the addrHash. addrHash is the account
	CopyTrie(Trie) Trie
	ContractCode(addrHash, codeHash common.Hash) ([]byte, error) // Get the contract of the addrHash, which must match the contract hash (codeHash)
	ContractCodeSize(addrHash, codeHash common.Hash) (int, error)

	// TrieDB retrieves the low level trie database used for data storage.
	TrieDB() *trie.Database
}
```

Currently, there are two types of DBs that implement the Database interface, odrDatabase used by light nodes, and cachingDB with cache used by normal nodes. 

Because **light nodes do not store data**, they need to obtain data by querying other nodes, and odrDatabase is the encapsulation of this data reading method. 

An ordinary node has a built-in levelDB. In order to improve read and write performance, it is encapsulated once with cachingDB.



### How to use StateDB to change state

All states are based on accounts. Any data must belong to a certain account state, and the world state is only a tree to establish a safe mapping. Accessible data can be divided into the following types:

1. Access account basic properties: Balance, Nonce, Root, CodeHash
2. Read contract account code
3. Read the content stored in the contract account

For example, when we try to obtain the balance of an account, we need to specify the account address from the world state tree Trie, and then read the account state.



```go
db: = state.NewDatabase(levelDB)
block = blockchain.CurrentBlock()
statedb, err := state.New(block.Root(), db)
balance := statedb.GetBalance(addr1)

//core/state/statedb.go:207
func (self *StateDB) GetBalance(addr common.Address) *big.Int {
	stateObject := self.getStateObject(addr)//①
	if stateObject != nil {
		return stateObject.Balance()//③
	}
	return common.Big0//②
}

// core/state/statedb.go:408
func (self *StateDB) getStateObject(addr common.Address) (stateObject *stateObject) {
	if obj := self.stateObjects[addr]; obj != nil {//①
		if obj.deleted {
			return nil
		}
		return obj
	}

	enc, err := self.trie.TryGet(addr[:])//②
	if len(enc) == 0 {
		self.setError(err)
		return nil
	}
	var data Account
	if err := rlp.DecodeBytes(enc, &data); err != nil {//③
		log.Error("Failed to decode state object", "addr", addr, "err", err)
		return nil
	}
	obj := newObject(self, addr, data)//④
	self.setStateObject(obj)
	return obj
}

type stateObject struct {
	address  common.Address/
	addrHash common.Hash 
	data     Account 
	db       *StateDB 

    //../ 存储树，第一次访问时初始化
	code Code // contract bytecode, which gets set when code is loaded
    //...
}
type Account struct {
	Nonce    uint64
	Balance  *big.Int
	Root     common.Hash // merkle root of the storage trie
	CodeHash []byte
}
```



##### How to send ETH to another account?

In Ethereum, A transfers 100 ETH to B, and actually completes two state modification operations in the current state:

1. A's account balance decreases by 100 ETH.
2. B's account balance increases by 100 ETH.



```go
db: = state.NewDatabase(levelDB)
block = blockchain.CurrentBlock()
statedb, err := state.New(block.Root(), db)

statedb.SubBalance(A,100 ETH)
statedb.AddBalance(B,100 ETH)
```



### How to use StateDB to read contract?

The biggest difference between contract accounts and ordinary accounts is that they have their own storage tree

```go
// core/state/state_object.go:152
func (c *stateObject) getTrie(db Database) Trie {
	if c.trie == nil {
		var err error
		c.trie, err = db.OpenStorageTrie(c.addrHash, c.data.Root)//①
		if err != nil {
			c.trie, _ = db.OpenStorageTrie(c.addrHash, common.Hash{})//②
			c.setError(fmt.Errorf("can't create storage trie: %v", err))
		}
	}
	return c.trie
}
```



### How to set changes StateDB into a real DB?

StateDB can be regarded as an in-memory database. State data is first modified in the in-memory database, and all calculations about the state are completed in memory. When the block is persisted, the update storage from the memory to the database is completed. This update is an incremental update, and only the modification involves the modified part.

```go
// core/state/statedb.go:680
func (s *StateDB) Commit(deleteEmptyObjects bool) (root common.Hash, err error) {
	defer s.clearJournalAndRefund()

	for addr := range s.journal.dirties {//①⑧⑨⑩
		s.stateObjectsDirty[addr] = struct{}{}
	}
	for addr, stateObject := range s.stateObjects {//②
		_, isDirty := s.stateObjectsDirty[addr]
		switch {
		case stateObject.suicided || (isDirty && deleteEmptyObjects && stateObject.empty()):
			//③
			s.deleteStateObject(stateObject)
		case isDirty:
			if stateObject.code != nil && stateObject.dirtyCode {//④
				s.db.TrieDB().InsertBlob(common.BytesToHash(stateObject.CodeHash()), stateObject.code)
				stateObject.dirtyCode = false
			}
			if err := stateObject.CommitTrie(s.db); err != nil {//⑤
				return common.Hash{}, err
			}
			s.updateStateObject(stateObject)//⑥
		}
		delete(s.stateObjectsDirty, addr)
	}
	//...
	root, err = s.trie.Commit(func(leaf []byte, parent common.Hash) error {//⑦
		var account Account
		if err := rlp.DecodeBytes(leaf, &account); err != nil {
			return nil
		}
		if account.Root != emptyRoot {
			s.db.TrieDB().Reference(account.Root, parent)
		}
		code := common.BytesToHash(account.CodeHash)
		if code != emptyCode {
			s.db.TrieDB().Reference(code, parent)
		}
		return nil
	})
	return root, err
}
```



stateDB.Commit() will save the change to the db.

![commit](..\pictures\commit.png)

### How StateDB revert change?

When a transaction is packaged into a block, when one of the transactions fails to execute, the transaction will not be included in the block, and the state needs to be rolled back to the state before the execution of the transaction. The code below is the logic code for the mining module to process transactions.

```go
snap := w.current.state.Snapshot()
receipt, _, err := core.ApplyTransaction(w.config, w.chain, &coinbase, w.current.gasPool, w.current.state, w.current.header, tx, &w.current.header.GasUsed, *w.chain.GetVMConfig())
if err != nil {
	w.current.state.RevertToSnapshot(snap)
	return nil, err
}
```