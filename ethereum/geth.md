# Geth

- What is Geth?

  - Geth is an Ethereum client implemented in the Go programming language that allows users to interact with the Ethereum network. It provides a command-line interface for running a full node that can verify transactions, execute smart contracts, and participate in the consensus process.

- What RPCs can you use to connect to Geth clients over the network?

  - Geth supports several Remote Procedure Call (RPC) APIs that allow external applications to communicate with a Geth client over the network. Some of the most commonly used RPCs include:

    - eth_call: Executes a message call transaction on the Ethereum network.

    - eth_sendTransaction: Sends a transaction to the network for execution.

    - eth_getBalance: Returns the balance of an Ethereum account.

    - eth_blockNumber: Returns the number of the most recent block.

- What is Geth's "fast" sync, and why is it faster?

  - Geth's "fast" sync is a synchronization mode that allows new nodes to quickly synchronize with the Ethereum network. In fast sync mode, instead of downloading and processing every block from the genesis block, Geth downloads only the block headers and uses them to create a snapshot of the state of the network at a recent block. This allows new nodes to catch up to the current block more quickly.

- How to connect two Geth clients using IPC-RPC?

  - To connect two Geth clients using IPC-RPC, you can specify the IPC file path using the "--ipcpath" option when starting each client. For example:

    - Geth client 1: geth --ipcpath /path/to/geth1.ipc

    - Geth client 2: geth --ipcpath /path/to/geth2.ipc

- Where are accounts stored in the Geth client?

  - Accounts in the Geth client are stored in the keystore directory, which is typically located in the user's home directory under ".ethereum/keystore". Each account is represented by a file in the keystore directory that contains the account's private key.

- How to use Geth to initiate a transaction to an account?

  - To initiate a transaction to an account using Geth, you can use the "eth_sendTransaction" RPC. The RPC takes a JSON object as an argument, which includes the sender's address, the recipient's address, the amount to send, and other transaction parameters. For example:
    - eth_sendTransaction({from: "0x123...", to: "0x456...", value: "1000000000000000000"})

  - This would send 1 ETH from the account at address "0x123..." to the account at address "0x456...".

- Can the Geth client be used for mining?

  - Yes, the Geth client can be used for mining Ethereum. Geth includes a built-in miner that allows users to mine Ether and participate in the consensus process. To start mining with Geth, you can use the "miner.start" RPC. For example: miner.start(). This would start the miner and begin searching for new blocks to mine.