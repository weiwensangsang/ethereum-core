# Create an Account

There are two types of accounts in Ethereum, 

1. Externally Owned Account (EOA) 
2. Contract Account.

An EOA is a regular account controlled by a private key. In Ethereum, EOAs manage their assets and transactions through their private keys. EOAs send Ether or call contracts by signing transactions with their private keys and then broadcasting them to the Ethereum network.

A Contract Account is an account managed by contract code, also known as a smart contract. It contains programmable code and persistent storage space that can be invoked and executed by other accounts. Contract accounts can receive Ether and other tokens and process them according to predetermined logic.

The main difference between Contract Accounts and EOAs is that Contract Accounts can implement more complex logic through code and can enable automation of transactions, smart contracts, decentralized applications, and other features. Additionally, Contract Accounts have their own address and private key, but the private key is managed by the contract code rather than an individual.



```go
// Account is the Ethereum consensus representation of accounts.
// These objects are stored in the main account trie.
type Account struct {
   Nonce    uint64
   Balance  *big.Int
   Root     common.Hash // merkle root of the storage trie
   CodeHash []byte
}
```



Nonce: If it is an EOA account, it indicates the serial number of the sending transaction; if it is a CA account, Nonce indicates the serial number of the contract creation

Balance: Indicates the balance of the account, the account balance corresponding to the account address

Root: store the root of the merkle tree, if it is an EOA account root is nil

CodeHash: EVM Code bound to the account, if it is EOA, CodeHash is nil



### Create

Use this to create,

```go
personal.newAccount()

func (ks *KeyStore) NewAccount(passphrase string) (accounts.Account, error) {
   _, account, err := storeNewKey(ks.storage, crand.Reader, passphrase)
   if err != nil {
      return accounts.Account{}, err
   }
   // Add the account to the cache immediately rather
   // than waiting for file system notifications to pick it up.
   ks.cache.add(account)
   ks.refreshWallets()
   return account, nil
}

// Get PubKey, PrevKey and address
func storeNewKey(ks keyStore, rand io.Reader, auth string) (*Key, accounts.Account, error) {
   key, err := newKey(rand)
   if err != nil {
      return nil, accounts.Account{}, err
   }
   a := accounts.Account{Address: key.Address, URL: accounts.URL{Scheme: KeyStoreScheme, Path: ks.JoinPath(keyFileName(key.Address))}}
   if err := ks.StoreKey(a.URL.Path, key, auth); err != nil {
      zeroKey(key.PrivateKey)
      return nil, a, err
   }
   return key, a, err
}

func newKey(rand io.Reader) (*Key, error) {
   privateKeyECDSA, err := ecdsa.GenerateKey(crypto.S256(), rand)
   if err != nil {
      return nil, err
   }
   return newKeyFromECDSA(privateKeyECDSA), nil
}

func GenerateKey(c elliptic.Curve, rand io.Reader) (*PrivateKey, error) {
   k, err := randFieldElement(c, rand)
   if err != nil {
      return nil, err
   }
​
   priv := new(PrivateKey)
   priv.PublicKey.Curve = c
   priv.D = k
   priv.PublicKey.X, priv.PublicKey.Y = c.ScalarBaseMult(k.Bytes())
   return priv, nil
}
func randFieldElement(c elliptic.Curve, rand io.Reader) (k *big.Int, err error) {
   params := c.Params()
   b := make([]byte, params.BitSize/8+8)
   _, err = io.ReadFull(rand, b)
   if err != nil {
      return
   }
​
   k = new(big.Int).SetBytes(b)
   n := new(big.Int).Sub(params.N, one)
   k.Mod(k, n)
   k.Add(k, one)
   return
}
func newKeyFromECDSA(privateKeyECDSA *ecdsa.PrivateKey) *Key {
   id := uuid.NewRandom()
   key := &Key{
      Id:         id,
      Address:    crypto.PubkeyToAddress(privateKeyECDSA.PublicKey),
      PrivateKey: privateKeyECDSA,
   }
   return key
}
```



Get Private Key => Get Public Key by Private Key =>   Get Address by Public Key
