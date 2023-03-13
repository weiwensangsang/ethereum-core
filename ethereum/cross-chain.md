# Cross Chain

For a long period of time in the early days of the industry, blockchain technology was based on the development of a single chain. At that time, it was generally recognized that the performance optimization and technical upgrade of the blockchain can be completed on a single chain. Once the members of the chain cannot reach an agreement on the development direction of the project, it can only be solved by hard forking or redesigning a chain.

It was not until 2012 that Ripple Labs proposed the Inter Ledger protocol to solve the coordination problem between different blockchain systems; in 2013, Herlihy proposed the atomic transfer (atomic transfer) scheme on the forum, which became an improved scheme after improvement. One main cross-chain mode, namely the hash lock mode.

More innovations followed, such as Litecoin, BitShares, and Ethereum, which accelerated the sense of crisis in the Bitcoin core development team. Therefore, in October 2014, BlockStream clearly proposed the concept of side chain for the first time.

In 2017, cross-chain projects Polkadot and Cosmos proposed a plan to build a cross-chain basic platform, through which all blockchain applications can be compatible.



### Tendermint

Cosmos can effectively address the existing problems of Bitcoin and Ethereum, and Cosmos proposes targeted solutions.

Bitcoin: The code base is very monolithic. All three layers — network, consensus, and application — are mixed together. And the Bitcoin scripting language is limited and user-unfriendly.

Ethereum: By turning the application layer into the Ethereum Virtual Machine (EVM). Virtual machines are able to process smart contracts, and any developer can deploy smart contracts to the open system of the Ethereum blockchain to build decentralized applications (dApps). But it does not simplify the development of the blockchain itself. It also has the disadvantages of limited scalability, relatively low flexibility granted to developers, and limited sovereignty per application.

Therefore, Cosmos proposes Tendermint, which is a solution that packages the network and consensus layers of the blockchain into a common engine, allowing developers to focus on application development rather than complex underlying protocols, making it easy to get started.

While Tendermint is ready for public or private blockchains and proposes POS, it has instant finality: as long as more than one-third of the validators are honest (Byzantine), a fork will never be created. Users can be sure that their transactions are completed immediately after the block is created (something that cannot be done in proof-of-work blockchains such as Bitcoin and Ethereum) and with high security.



### IBC

The full name is INTER‑BLOCKCHAIN COMMUNICATION PROTOCOL (inter-chain communication protocol). As the name suggests, it is a communication protocol between chains, which is equivalent to the TCP/IP protocol on the Internet.

So how does the IBC work? It first needs a middleman-like role called Relayer. Before officially crossing the chain, it first needs to request a connection (Connection) from the two chains and establish a channel (Channel). This channel is bidirectional and bound, because the channel needs to be assigned a unique ID and the number of channels that have been applied for by different chains is different, so we will see that the same channel is assigned different IDs in different chains (For example, the most commonly used channel between Cosmos Hub and Osmosis is Cosmos Hub/Channel-141 <=> Osmosis/Channel-0), when the channel is established, communication can begin.

Now that you two fellow villagers can start chatting, do you need to find a topic for chatting? Similarly, the content transmitted by IBC also needs to carry the "topic" (Port). For example, the "topic" agreed upon by both parties in the Cosmos ecological token cross-chain is transfer. When you want to cross from chain A to chain B, you first need to initiate a specific cross-chain transaction on chain A; after the transaction is confirmed by chain A, Relayer will forward the transaction and the relevant proof (Proof) to B B chain; B chain then verifies the transaction and its proof, and if it is normal, it will perform related operations according to the established logic. Students who want to learn more can see the official introduction of Cosmos.

Hey, wait, does my coin crossing from A to B mean that this coin has disappeared from the A chain? Not necessarily, we can look at the specific process:

You initiate a cross-chain transaction, intending to cross 0.01 OSMO from Osmosis to Cosmos Hub. Because currently Cosmos Hub/Channel-141 <=> Osmosis/Channel-0 is the most commonly used channel, and the agreed "topic" of token cross-chain is transfer. So you specify the sourceChannel as channel-0, the sourcePort as transfer, and the payee on the Cosmos Hub as cosmos186440u3pwts7s3jljngak37xnmy5le8nztf9az

When the node receives and recognizes that your transaction is a cross-chain transaction and also knows that you want to go from Osmosis to Cosmos Hub, it will not be destroyed at this time, but will transfer your OSMO to the custodial account. Where did this custodial account come from? Is it controlled by an external entity? Don't worry, it's not. The calculation logic of the custody account is:

```
pubkey = sha256(
   Buffer.from("ics20-1", "utf-8")

   + Buffer.from([0])
   + Buffer.from(`${sourcePort}/${sourceChannel}`, "utf-8")
     ).slice(0, 20)

Bech32.encode(addressPrefix, pubkey)
// At this point addressPrefix: "osmo", sourcePort: "transfer", sourceChannel: "channel-0"
```

Therefore, we can calculate that the custody account is osmo1a53udazy8ayufvy0s434pfwjcedzqv347h34au. If you are interested, you can click on this address to see how many coins have gone from Osmosis/Channel-0 to Cosmos Hub

Then Relayer will forward this cross-chain message to Cosmos Hub. After Cosmos Hub receives this message and fully verifies it, it will directly mint 0.01 ibc/14F9BC3E44B8A9C1BE1FB08980FAB87034C9905EF17CF2F5008FC085218811CC to the address cosmos186440u3pwts7s3jljngak37xnmy5le8nztf9az. Not OSMO? What the hell is this? In fact, this is the subtlety. Because this currency is minted out of thin air, and its "code name" (denom) cannot coincide with the existing currency, so it can be obtained in the following way:

```
"ibc/" + sha256(Buffer.from(`${dstPort}/${dstChannel}/${originDenom}`, 'utf-8')).toString("hex").toUpperCase()
// At this point dstPort: transfer, dstChannel: channel-141, originDenom: uosmo
```

 Of course, you don’t need to see this unreadable code name during the use of Cosmos Hub. The wallet or browser will intelligently replace its name with OSMO.

So far, by locking assets in Osmosis, and then minting assets in Cosmos Hub, you have crossed over your assets, and now you can play happily. So what if you want to go back to the Osmosis chain? akin:

You initiate another cross-chain transaction, specifying sourceChannel as channel-141, sourcePort as transfer and the payee on Osmosis as osmo186440u3pwts7s3jljngak37xnmy5le8n2s64ts
After the node receives the transaction, it detects that you want to return to Osmosis from the Cosmos Hub, so it will directly destroy the coin that was minted out of thin air at this time.
Then, after the Relayer forwards the cross-chain message to Osmosis, Osmosis will transfer the OSMO previously placed on the custodial address to your receiving address after full verification.
Students who want to know more details can also find the answer from the specification and source code

But if you are smart, you will definitely notice a detail, the process of minting coins out of thin air includes ChannelID. Isn't that equivalent to saying that the same currency will become different currencies when it comes through different channels, and they cannot share liquidity? Yes, this is why there are so many channels between different browser chains, but there is only one with traffic.