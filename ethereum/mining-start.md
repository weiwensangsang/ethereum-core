# Mining: Start

Mining involves three channels.

1. newWorkCh
2. txsCh
3. chainSideCh

![miner-loop](..\pictures\miner-loop.png)

Once we received the **newWorkCh**. We should start to mining.

```go
//miner/worker.go:409
case req := <-w.newWorkCh:
   w.commitNewWork(req.interrupt, req.noempty, req.timestamp)
```

The **txsCh** message is triggered when a new transaction is received.

```go
//miner/worker.go:451
case ev := <-w.txsCh:
   if !w.isRunning() && w.current != nil {
      w.mu.RLock()
      coinbase := w.coinbase
      w.mu.RUnlock()

      txs := make(map[common.Address]types.Transactions)
      for _, tx := range ev.Txs {
         acc, _ := types.Sender(w.current.signer, tx)
         txs[acc] = append(txs[acc], tx)
      }
      txset := types.NewTransactionsByPriceAndNonce(w.current.signer, txs)
      w.commitTransactions(txset, coinbase, nil)
      w.updateSnapshot()
   } else {
      if w.config.Clique != nil && w.config.Clique.Period == 0 {
         w.commitNewWork(nil, false, time.Now().Unix())
      }
   }
   atomic.AddInt32(&w.newTxs, int32(len(ev.Txs)))
```

In the process, the new transactions will be sorted according to the price and Nonce value, and after forming an ordered transaction set, they will be committed in sequence.
It can be seen that the process of receiving and processing new transactions does not interfere with mining. There is also no need to consider whether the transaction has been processed, because when the transaction is duplicated, the second committed will fail.

**chainSideCh**

This message is triggered when a local block is added to the side chain. After receiving this message, the block in the message (that is, the block added to the side chain) is added to the "uncle block" list, and according to the current state, two uncle blocks may be selected to submit a block generation task. (This channel is the embodiment of Ethereum encouraging uncle blocks)

```go
//miner/worker.go:412
case ev := <-w.chainSideCh:
   if _, exist := w.localUncles[ev.Block.Hash()]; exist {//❶
      continue
   }
   if _, exist := w.remoteUncles[ev.Block.Hash()]; exist {
      continue
   }
   if w.isLocalBlock != nil && w.isLocalBlock(ev.Block) {//❷
      w.localUncles[ev.Block.Hash()] = ev.Block
   } else {
      w.remoteUncles[ev.Block.Hash()] = ev.Block
   }
   if w.isRunning() && w.current != nil && w.current.uncles.Cardinality() < 2 {//❸
      start := time.Now()
      if err := w.commitUncle(w.current, ev.Block.Header()); err == nil {//❹
         var uncles []*types.Header
         w.current.uncles.Each(func(item interface{}) bool {
            //...
         })
         w.commit(uncles, nil, true, start)//❺
      }
   }
```



### Set New Block Info

```go
//miner/worker.go:829
parent := w.chain.CurrentBlock()//Mining is to compete to dig the next block, and the block with the latest height needs to be used as the parent block

if parent.Time() >= uint64(timestamp) {// Change the timestamp
   timestamp = int64(parent.Time() + 1)
}
if now := time.Now().Unix(); timestamp > now+1 {
   wait := time.Duration(timestamp-now) * time.Second
   log.Info("Mining too far in the future", "wait", common.PrettyDuration(wait))
   time.Sleep(wait)
}
num := parent.Number()
header := &types.Header{
   ParentHash: parent.Hash(),
   Number:     num.Add(num, common.Big1),
   GasLimit:   core.CalcGasLimit(parent, w.gasFloor, w.gasCeil),
   Extra:      w.extra,
   Time:       uint64(timestamp),
}
if w.isRunning() {
		if w.coinbase == (common.Address{}) {
			log.Error("Refusing to mine without etherbase")
			return
		}
		header.Coinbase = w.coinbase// Set account to get the ETH rewards
}


...

err := w.makeCurrent(parent, header) // Update stateDB by transaction
	if err != nil {
		log.Error("Failed to create mining context", "err", err)
		return
	}
```

### Add Uncle Blocks

We can see the code listen the chainSideCh and add a uncle blocks set. But why we need Uncle Blocks?

In a distributed system, due to network delay and asynchronous communication between nodes, there is a certain delay and uncertainty. This can result in two or more miners mining a new block almost simultaneously, but only one of the blocks can be added to the blockchain.

Uncle Blocks can motivate more miners to participate in the consensus process, even if their blocks are not confirmed and added to the main chain.



### PoW find Nonce

```go
//miner/worker.go:508
case task := <-w.taskCh:
   //...
   sealHash := w.engine.SealHash(task.block.Header())//get the hash of block
   if sealHash == prev {
      continue
   }
   interrupt()
   stopCh, prev = make(chan struct{}), sealHash

   if w.skipSealHook != nil && w.skipSealHook(task) {
      continue
   }
   w.pendingMu.Lock()
   w.pendingTasks[w.engine.SealHash(task.block.Header())] = task
   w.pendingMu.Unlock()

   if err := w.engine.Seal(w.chain, task.block, w.resultCh, stopCh); err != nil { // find nonce and send resultCh
      log.Warn("Block sealing failed", "err", err)
   }

//miner/worker.go:542
select {
case block := <-w.resultCh: 
   if block == nil {
      continue
   
   if w.chain.HasBlock(block.Hash(), block.NumberU64()) {
      continue
   }
   var (
      sealhash = w.engine.SealHash(block.Header())
      hash     = block.Hash()
   )
```



Finally, Broadcast the new Block.

```go
//eth/handler.go:771
func (pm *ProtocolManager) minedBroadcastLoop() {
   for obj := range pm.minedBlockSub.Chan() {
      if ev, ok := obj.Data.(core.NewMinedBlockEvent); ok {
         pm.BroadcastBlock(ev.Block, true) //❼
         pm.BroadcastBlock(ev.Block, false) //❽
      }
   }
}
```



![mining-process](..\pictures\mining-process.png)





### One more thing: How to use GPU to mining?

Ethereum uses a hashing algorithm called Ethash, which is a memory-hard algorithm, meaning it requires a lot of memory to mine efficiently. The purpose of this algorithm design is to avoid the emergence of ASIC (application-specific integrated circuit) mining machines, so that ordinary computers can also have the opportunity to participate in mining.

CPUs usually only have smaller caches, while GPUs have larger memory and higher memory bandwidth, which makes GPUs more suitable for the memory-intensive calculations required in the Ethash algorithm. In contrast, the performance of CPUs is mainly determined by the clock speed and computing power of individual cores, and their memory bandwidth is relatively small.

Therefore, using GPU mining is more efficient than using CPU mining, and it is also the current mainstream method of Ethereum mining.

The basic principle of the Ethash algorithm is to use a data structure called DAG (Directed Acyclic Graph) for hash calculation. This DAG is computed iteratively as a series of hash functions, each of which depends on the results of previous hash functions. Therefore, the calculation of DAG is a very memory-intensive process.

Specifically, the Ethash algorithm first generates a 256MB DAG using a random number called a "hash seed". Miners then need to perform hash calculations using the DAG and some other data such as mining parameters and Nonce to find eligible blocks. Each calculation process needs to use some random data in the DAG, which needs to be stored in memory. Since the DAG is very large, a lot of memory is required to store it. The greater the amount of memory used by the miner, the faster the calculations because more data can be cached.

In addition, the Ethash algorithm also designs a data structure called "cache" to speed up hash calculations. The size of the cache is determined by the hardware of the miner. A larger cache means that the miner can calculate the correct hash value faster, thus achieving higher mining efficiency.

The reason why a lot of memory is needed is because the Ethash algorithm uses the DAG data structure for hash calculations, and the DAG is very large and requires a lot of memory to store it. Since miners need to frequently use DAG for hash calculations, a large amount of memory is required to cache these data, thereby improving computing efficiency.

The RTX 3090, for example, has 24 GB of GDDR6X memory.