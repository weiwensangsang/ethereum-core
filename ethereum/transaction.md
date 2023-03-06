# Transaction

The complete process of an Ethereum transaction is divided into the following steps:

1. Initiate a transaction: specify the target address and transaction amount, as well as the required gas/gaslimit
2. Transaction signature: use the account private key to sign the transaction
3. Submit the transaction: add the transaction to the transaction buffer pool txpool (the transaction signature will be verified first)
4. Broadcast transaction: notify EVM to execute, and broadcast transaction information to other nodes at the same time



### Initiate a transaction

The code in internal/ethapi/api.go.

```go
func (s *PublicTransactionPoolAPI) SendTransaction(ctx context.Context, args SendTxArgs) (common.Hash, error) {

    // Look up the wallet containing the requested signer
    account := accounts.Account{Address: args.From}

    wallet, err := s.b.AccountManager().Find(account)
    if err != nil {
        return common.Hash{}, err
    }

    if args.Nonce == nil {
        // Hold the addresse's mutex around signing to prevent concurrent assignment of
        // the same nonce to multiple accounts.
        s.nonceLock.LockAddr(args.From)
        defer s.nonceLock.UnlockAddr(args.From)
    }

    // Set some sanity defaults and terminate on failure
    if err := args.setDefaults(ctx, s.b); err != nil {
        return common.Hash{}, err
    }
    // Assemble the transaction and sign with the wallet
    tx := args.toTransaction()

    var chainID *big.Int
    if config := s.b.ChainConfig(); config.IsEIP155(s.b.CurrentBlock().Number()) {
        chainID = config.ChainId
    }
    signed, err := wallet.SignTx(account, tx, chainID)
    if err != nil {
        return common.Hash{}, err
    }
    return submitTransaction(ctx, s.b, signed)
}

func (args *SendTxArgs) toTransaction() *types.Transaction {
    var input []byte
    if args.Data != nil {
        input = *args.Data
    } else if args.Input != nil {
        input = *args.Input
    }
    if args.To == nil {
        return types.NewContractCreation(uint64(*args.Nonce), (*big.Int)(args.Value), uint64(*args.Gas), (*big.Int)(args.GasPrice), input)
    }
    return types.NewTransaction(uint64(*args.Nonce), *args.To, (*big.Int)(args.Value), uint64(*args.Gas), (*big.Int)(args.GasPrice), input)
}

type txdata struct {
    AccountNonce uint64          `json:"nonce"    gencodec:"required"`
    Price        *big.Int        `json:"gasPrice" gencodec:"required"`
    GasLimit     uint64          `json:"gas"      gencodec:"required"`
    Recipient    *common.Address `json:"to"       rlp:"nil"` // nil means contract creation
    Amount       *big.Int        `json:"value"    gencodec:"required"`
    Payload      []byte          `json:"input"    gencodec:"required"`

    // Signature values
    V *big.Int `json:"v" gencodec:"required"`
    R *big.Int `json:"r" gencodec:"required"`
    S *big.Int `json:"s" gencodec:"required"`

    // This is only used when marshaling to JSON.
    Hash *common.Hash `json:"hash" rlp:"-"`
}
```



### Transaction signature

TxData calculates the hash value of transaction data through the Keccak-256 algorithm, and then combines the private key of the account to generate signature data through ECDSA (Elliptic Curve Digital Signature Algorithm), which is the elliptic curve digital signature algorithm.

Of course, we can also send the private key to others for direct verification. But in this case, our account has no security at all. Once the private key is exposed, our account balance will be quickly removed.



#### Keccak-256

Keccak-256 algorithm is a hash function defined in the SHA-3 standard, which is a member of the Keccak hash function family designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche. The algorithm is based on the Keccak-f permutation function and uses the SPONGE construction method to compute the hash of any input data with a fixed output length of 256 bits.

The specific steps of the Keccak-256 algorithm are as follows:

1. Padding the data

First, the input data is padded to a length that is a multiple of 136 bytes. The padding rules are as follows:

- Append a binary 1 to the end of the data.
- Append several binary 0s to the end of the data to make the length a multiple of 136 bytes.
- Append a 32-bit binary integer to the end of the padded data to represent the length of the original data (in bits).

1. Computing the hash

Divide the padded data into several 136-byte blocks and compute the hash of each block. The hash calculation process includes the following steps:

- Divide each block into 17 8-byte slices called "states".
- Perform a series of permutation operations on the states, called the Keccak-f permutation function.
- Repeat the permutation operation on each block until all blocks have been processed.

1. Output the hash value

The state of the last block is used as the output hash value.

The Keccak-256 algorithm is relatively simple, but it uses advanced techniques to enhance security, making it effective against various attacks.



### ECDSA 



Then let's see how this value pair is created for signing:

1. generate a random number k
2. Calculate using dot multiplication p = k * G
3. R = xP, hash of txData is z
4. mod p



So, the sender should send R, S, PubKey, in header, and txData in Body.

The receiver can check if the sign is correct.

The receiver  just do this.

P = S ^ -1 * z * G + S^-1 * R * PubKey 

if xP = R, the data is correct. In this way, a verification is completed without exposing the private key.

We can prove this.

```go
P = S ^ -1 * z * G + S^-1 * R * PubKey
//PubKey = privKey * G, so
P = S ^ -1 * z * G + S^-1 * R * privKey * G
P = S ^ -1 * z * G + S^-1 * R * privKey * G
P = S ^ -1  * G * ( z +  R * privKey)
// if P is a point in ECC, there must be some K make P = K * G, so
K * G = S ^ -1  * G * ( z +  R * privKey)
K  = S ^ -1 * ( z +  R * privKey)


// And we know how sender create S.
S = k ^ -1( z + privKey * R) 
k =  S ^ -1 * ( z +  R * privKey)

So, k = K
```



### Questions

- Can you explain the difference between on chain and off chain transactions in web3?

  - On-chain transactions refer to transactions that are recorded and executed directly on the blockchain. These transactions involve sending or receiving cryptocurrency or tokens, executing smart contracts, and updating the state of the blockchain. On-chain transactions require gas fees to be paid in order to incentivize miners to validate and process the transaction. Once a transaction is processed and confirmed by the network, it is permanently recorded on the blockchain and can be viewed by anyone.

    Off-chain transactions, on the other hand, refer to transactions that occur outside of the blockchain, but are still related to the blockchain. These transactions can include transferring cryptocurrency or tokens between two parties using an off-chain payment channel, such as the Lightning Network, which allows for instant and low-cost transactions. Off-chain transactions can also include any interactions between two or more parties that do not involve updating the state of the blockchain. Off-chain transactions do not require gas fees and can occur instantly without the need for confirmation by the network.

    In summary, on-chain transactions involve interacting directly with the blockchain and updating its state, while off-chain transactions occur outside of the blockchain and can involve various forms of payment channels or other interactions between parties. Both types of transactions have their advantages and disadvantages, and their suitability depends on the specific use case and requirements.

- Can you "hide" a transaction in Ethereum?

  - In Ethereum, you cannot truly "hide" a transaction because Ethereum's transaction records are public and can be viewed by anyone. However, there are some techniques that can obscure the traceability of a transaction, making it more difficult to discover.

    One method is to use smart contracts to proxy the transaction. This method can hide the sender and receiver of the transaction behind the smart contract, making the transaction appear to be sent by the contract itself rather than the actual sender. However, this method still leaves a record of the contract transaction, so it is still traceable.

    Another method is to use cryptocurrency mixers. These services mix a user's cryptocurrency with other users' cryptocurrency to make it more difficult to trace the sender and receiver of each specific transaction. However, this method can still be traceable as the mixer service may leave some traces in the transaction.

    In summary, while transactions cannot truly be "hidden" in Ethereum, there are techniques that can be used to increase transaction privacy and security. However, it should be noted that these methods may not be entirely reliable and have some risks and vulnerabilities, so they should be used with caution.

- What tools are needed to sign a transaction?

  - Private Key
