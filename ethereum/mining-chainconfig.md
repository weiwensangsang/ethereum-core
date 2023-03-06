# Mining:ChainConfig

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

Here is the UML for mining.

![miner-uml](..\pictures\miner-uml.png)

Here is the code.

```go
type Miner struct {
    mux *event.TypeMux // Mux
    worker *worker
    coinbase common.Address 
    mining   int32 // mining status
    eth      Backend // Backend
    engine   consensus.Engine //ethash, clique。
    canStart    int32 // Can i start mining?
    shouldStart int32 // Should i start mining after block sync?
}

type worker struct {
    config *params.ChainConfig
    engine consensus.Engine

    mu sync.Mutex

    // update loop
    mux          *event.TypeMux
    txCh         chan core.TxPreEvent
    txSub        event.Subscription
    chainHeadCh  chan core.ChainHeadEvent
    chainHeadSub event.Subscription
    chainSideCh  chan core.ChainSideEvent
    chainSideSub event.Subscription
    wg           sync.WaitGroup

    agents map[Agent]struct{} // worker have a map for Agents
    recv   chan *Result

    eth     Backend
    chain   *core.BlockChain
    proc    core.Validator
    chainDb ethdb.Database

    coinbase common.Address
    extra    []byte

    currentMu sync.Mutex
    current   *Work

    uncleMu        sync.Mutex
    possibleUncles map[common.Hash]*types.Block

    unconfirmed *unconfirmedBlocks // 本地挖出的待确认的块

    mining int32
    atWork int32
}

// ChainConfig is the core config which determines the blockchain settings.
//
// ChainConfig is stored in the database on a per block basis. This means
// that any network, identified by its genesis block, can have its own
// set of configuration options.
type ChainConfig struct {
	ChainID *big.Int `json:"chainId"` // chainId identifies the current chain and is used for replay protection

	HomesteadBlock *big.Int `json:"homesteadBlock,omitempty"` // Homestead switch block (nil = no fork, 0 = already homestead)

	DAOForkBlock   *big.Int `json:"daoForkBlock,omitempty"`   // TheDAO hard-fork switch block (nil = no fork)
	DAOForkSupport bool     `json:"daoForkSupport,omitempty"` // Whether the nodes supports or opposes the DAO hard-fork

	// EIP150 implements the Gas price changes (https://github.com/ethereum/EIPs/issues/150)
	EIP150Block *big.Int    `json:"eip150Block,omitempty"` // EIP150 HF block (nil = no fork)
	EIP150Hash  common.Hash `json:"eip150Hash,omitempty"`  // EIP150 HF hash (needed for header only clients as only gas pricing changed)

	EIP155Block *big.Int `json:"eip155Block,omitempty"` // EIP155 HF block
	EIP158Block *big.Int `json:"eip158Block,omitempty"` // EIP158 HF block

	ByzantiumBlock      *big.Int `json:"byzantiumBlock,omitempty"`      // Byzantium switch block (nil = no fork, 0 = already on byzantium)
	ConstantinopleBlock *big.Int `json:"constantinopleBlock,omitempty"` // Constantinople switch block (nil = no fork, 0 = already activated)
	PetersburgBlock     *big.Int `json:"petersburgBlock,omitempty"`     // Petersburg switch block (nil = same as Constantinople)
	IstanbulBlock       *big.Int `json:"istanbulBlock,omitempty"`       // Istanbul switch block (nil = no fork, 0 = already on istanbul)
	MuirGlacierBlock    *big.Int `json:"muirGlacierBlock,omitempty"`    // Eip-2384 (bomb delay) switch block (nil = no fork, 0 = already activated)
	BerlinBlock         *big.Int `json:"berlinBlock,omitempty"`         // Berlin switch block (nil = no fork, 0 = already on berlin)
	LondonBlock         *big.Int `json:"londonBlock,omitempty"`         // London switch block (nil = no fork, 0 = already on london)
	ArrowGlacierBlock   *big.Int `json:"arrowGlacierBlock,omitempty"`   // Eip-4345 (bomb delay) switch block (nil = no fork, 0 = already activated)
	GrayGlacierBlock    *big.Int `json:"grayGlacierBlock,omitempty"`    // Eip-5133 (bomb delay) switch block (nil = no fork, 0 = already activated)
	MergeNetsplitBlock  *big.Int `json:"mergeNetsplitBlock,omitempty"`  // Virtual fork after The Merge to use as a network splitter

	// Fork scheduling was switched from blocks to timestamps here

	ShanghaiTime *uint64 `json:"shanghaiTime,omitempty"` // Shanghai switch time (nil = no fork, 0 = already on shanghai)
	CancunTime   *uint64 `json:"cancunTime,omitempty"`   // Cancun switch time (nil = no fork, 0 = already on cancun)
	PragueTime   *uint64 `json:"pragueTime,omitempty"`   // Prague switch time (nil = no fork, 0 = already on prague)

	// TerminalTotalDifficulty is the amount of total difficulty reached by
	// the network that triggers the consensus upgrade.
	TerminalTotalDifficulty *big.Int `json:"terminalTotalDifficulty,omitempty"`

	// TerminalTotalDifficultyPassed is a flag specifying that the network already
	// passed the terminal total difficulty. Its purpose is to disable legacy sync
	// even without having seen the TTD locally (safer long term).
	TerminalTotalDifficultyPassed bool `json:"terminalTotalDifficultyPassed,omitempty"`

	// Various consensus engines
	Ethash *EthashConfig `json:"ethash,omitempty"`
	Clique *CliqueConfig `json:"clique,omitempty"`
}
```



We need to analyze ChainConfig, because this configuration is very important, and we can trace the update of Ethereum through this configuration.



### ChainID

The ChainID of Ethereum is an identifier used to differentiate between different Ethereum networks and prevent accidental interactions between them. In the Ethereum network, each block contains a ChainID field that specifies which network the block belongs to.

In Ethereum, replay protection is a mechanism used to prevent transactions from being executed repeatedly across different networks. Replay protection is achieved by using network-specific transaction formats that include the ChainID field. When a transaction is sent to the network, nodes check whether the ChainID field in the transaction matches the ChainID of the network. If it doesn't match, the transaction is rejected.

For example, when an Ethereum network forks, the new fork may use a different ChainID. If a user sends a transaction on the old network before the fork, that transaction may be replayed on the new fork by malicious nodes, resulting in unexpected loss of funds. By using ChainID to differentiate between networks and using network-specific transaction formats to protect against replay, this risk can be avoided.

The exact number of ChainIDs may change over time due to network upgrades and forks.  Here are some examples of ChainIDs for different Ethereum networks:

- Mainnet: 1
- Ropsten testnet: 3
- Rinkeby testnet: 4
- Kovan testnet: 42
- Goerli testnet: 5
- Ethereum Classic mainnet: 61



### HomesteadBlock

The Homestead upgrade was planned as the first hard fork of the Ethereum network, implemented on March 14, 2016 at block 1,150,000. The Homestead upgrade mainly includes three important improvements to Ethereum. First, it removes the canary contract, removing the centralized part of the network. Second, it introduces new code in Solidity, Ethereum’s contract programming language. Finally, it introduces the Mist wallet, which allows users to hold/trade ETH and write/deploy smart contracts.

The Homestead upgrade was one of the first Ethereum Improvement Proposals (EIPs) to be implemented.

When the HomesteadBlock attribute is specified in ChainConfig, the Ethereum node will enable the Homestead upgrade after the specified block height. This helps ensure that all nodes on the Ethereum network implement the Homestead upgrade at the same block height and correctly handle the new opcodes and exception handling mechanisms.



### DAOForkBlock

On the Ethereum blockchain, DAO (Decentralized Autonomous Organization) was a self-governing decentralized organization aimed at creating a decentralized investment fund through smart contracts. In 2016, DAO suffered a hack that resulted in over 3 million ether being stolen. To prevent further losses, the Ethereum community decided to perform a hard fork to roll back the transaction, which is known as the DAO fork.

DAOForkBlock is an attribute in the Ethereum ChainConfig that defines the block height of the DAO fork on the Ethereum blockchain. Its purpose is to specify the time at which the DAO fork will take effect in the Ethereum software code.

Specifically, if the DAO fork block height of an Ethereum node is lower than the DAOForkBlock attribute specified block height, then that node will follow the DAO smart contract. Otherwise, it will execute the new chain after the DAO fork. Therefore, the DAOForkBlock attribute is an important parameter in the Ethereum software that ensures the stability and security of the Ethereum blockchain.



### EIP150Block

The purpose of the EIP150Block attribute is to ensure that Ethereum nodes can promptly apply the protocol changes specified by EIP-150 once the specified block height is reached, in order to improve the security and performance of the Ethereum network.

Specifically, the changes introduced by EIP-150 include:

1. Adopting a more secure ECDSA signature algorithm (replacing the previous use of SECP256k1);
2. Modifying the miner reward mechanism, reducing block rewards and increasing the proportion of miner fees;
3. Modifying the state transition function to eliminate some potential security vulnerabilities.



### EIP155Block

Before the implementation of the EIP-155 specification, Ethereum and Ethereum Classic (ETC) shared the same network ID and chain ID for a period of time, which caused confusion with transactions being replayed on both networks. The implementation of the EIP-155 specification resolved this issue, but it needed to take effect after a specific block height. Therefore, the EIP155Block property is used to specify the block height at which the EIP-155 specification was implemented on the Ethereum network.



### ByzantiumBlock

After the Byzantium hard fork, the Ethereum network introduced some new features and improvements, including faster block confirmation times, better privacy and security, and better smart contract programming capabilities. These improvements require protocol upgrades to be implemented, so it is necessary to specify the ByzantiumBlock property to ensure that nodes on the network have already been upgraded.
	

### ShanghaiTime

Ethereum nodes use the ShanghaiTime property to calculate the timestamps of blocks, ensuring that the timestamps in the blockchain are accurate and consistent with Shanghai time. This can be important for certain blockchain applications and smart contracts that need to determine the exact time something happened, such as in time-sensitive transactions that require proof of certain events.
