# EVM

Usually, the development process of a smart contract is to use solidity to write logic code, compile it into bytecode through a compiler, and then publish it on Ethereum. The bottom layer of Ethereum supports the execution and calling of contracts through the EVM module. When calling, the code is obtained according to the contract address, that is, The bytecode of the contract is loaded into the EVM for execution after the environment is generated.

The general flow is as shown in Figure 1. The execution process of the instructions is shown in Figure 2. The instructions are continuously fetched from the EVM code for execution, using Gas to realize the limit cycle, using the stack for operations, storing temporary variables in the memory, and storing data in the account state. .

EVM distinguishes between temporary storage (Memory, which exists in each VM instance and disappears after the execution of the VM) and permanent storage (Storage, which exists in the state layer of the blockchain).



![evm_process](..\pictures\evm_process.jpg)



![evm_process](..\pictures\evm_code_executed.png)





### Code

```go
type Context struct {
	CanTransfer CanTransferFunc
	Transfer TransferFunc
	GetHash GetHashFunc
	Origin   common.Address
	GasPrice *big.Int
	Coinbase    common.Address
	GasLimit    uint64
	BlockNumber *big.Int
	Time        *big.Int
	Difficulty  *big.Int
}

type EVM struct {
	Context
	StateDB StateDB
	depth int
	chainConfig *params.ChainConfig
	chainRules params.Rules
	vmConfig Config
	interpreter *Interpreter
	abort int32
	callGasTemp uint64
}

// create Contract
func (evm *EVM) create(caller ContractRef, code []byte, gas uint64, value *big.Int, address common.Address) ([]byte, common.Address, uint64, error) {
	if evm.depth > int(params.CallCreateDepth) { // less then 1024
		return nil, common.Address{}, gas, ErrDepth
	}
	if !evm.CanTransfer(evm.StateDB, caller.Address(), value) { // Check account balance
		return nil, common.Address{}, gas, ErrInsufficientBalance
	}
	nonce := evm.StateDB.GetNonce(caller.Address())
	evm.StateDB.SetNonce(caller.Address(), nonce+1)

	contractHash := evm.StateDB.GetCodeHash(address)
	if evm.StateDB.GetNonce(address) != 0 || (contractHash != (common.Hash{}) && contractHash != emptyCodeHash) {
		return nil, common.Address{}, 0, ErrContractAddressCollision
	}

	snapshot := evm.StateDB.Snapshot()
	evm.StateDB.CreateAccount(address)
	if evm.ChainConfig().IsEIP158(evm.BlockNumber) {
		evm.StateDB.SetNonce(address, 1)
	}
	evm.Transfer(evm.StateDB, caller.Address(), address, value)

	contract := NewContract(caller, AccountRef(address), value, gas)
	contract.SetCallCode(&address, crypto.Keccak256Hash(code), code)

	if evm.vmConfig.NoRecursion && evm.depth > 0 {
		return nil, address, gas, nil
	}

	if evm.vmConfig.Debug && evm.depth == 0 {
		evm.vmConfig.Tracer.CaptureStart(caller.Address(), address, true, code, gas, value)
	}
	start := time.Now()

	ret, err := run(evm, contract, nil)

	maxCodeSizeExceeded := evm.ChainConfig().IsEIP158(evm.BlockNumber) && len(ret) > params.MaxCodeSize

	if err == nil && !maxCodeSizeExceeded {
		createDataGas := uint64(len(ret)) * params.CreateDataGas
		if contract.UseGas(createDataGas) {
			evm.StateDB.SetCode(address, ret)
		} else {
			err = ErrCodeStoreOutOfGas
		}
	}

	if maxCodeSizeExceeded || (err != nil && (evm.ChainConfig().IsHomestead(evm.BlockNumber) || err != ErrCodeStoreOutOfGas)) {
		evm.StateDB.RevertToSnapshot(snapshot)
		if err != errExecutionReverted {
			contract.UseGas(contract.Gas)
		}
	}

	if maxCodeSizeExceeded && err == nil {
		err = errMaxCodeSizeExceeded
	}
	if evm.vmConfig.Debug && evm.depth == 0 {
		evm.vmConfig.Tracer.CaptureEnd(ret, gas-contract.Gas, time.Since(start), err)
	}
	return ret, address, contract.Gas, err

}
```



First, a series of verifications will be performed,

1. The depth of the call stack cannot exceed 1024;
2. The called account has enough balance; 
3. Initiate a transfer operation, subtract the value from the sender’s address balance, add the value to the balance of the contract account, and then call SetCallCode of the contract to initialize the contract according to the sender’s address, contract address, amount value, gas, contract code, and code hash Object, and then call run(evm, contract, nil) to execute the initialization code of the contract. The generated code has a certain length limit. When the contract is successfully created and no error is returned, the gas required to store the code is calculated.

It can be seen that the contract code is stored in the storage area pointed to by the codehash in the account through the SetCode of the state module. This part of the code belongs to the modification of the world state.

The fund transfer of the Create method occurs between the creating contract user account and the contract account



### Call

When transferring money or executing contract code, the Call method will be called, and the call instruction in the contract will also call this method.



```go
func (evm *EVM) Call(caller ContractRef, addr common.Address, input []byte, gas uint64, value *big.Int) (ret []byte, leftOverGas uint64, err error) {
	if evm.vmConfig.NoRecursion && evm.depth > 0 {
		return nil, gas, nil
	}

	if evm.depth > int(params.CallCreateDepth) {
		return nil, gas, ErrDepth
	}
	if !evm.Context.CanTransfer(evm.StateDB, caller.Address(), value) {
		return nil, gas, ErrInsufficientBalance
	}

	var (
		to       = AccountRef(addr)
		snapshot = evm.StateDB.Snapshot()
	)
	if !evm.StateDB.Exist(addr) {
		precompiles := PrecompiledContractsHomestead
		if evm.ChainConfig().IsByzantium(evm.BlockNumber) {
			precompiles = PrecompiledContractsByzantium
		}
		if precompiles[addr] == nil && evm.ChainConfig().IsEIP158(evm.BlockNumber) && value.Sign() == 0 {
			if evm.vmConfig.Debug && evm.depth == 0 {
				evm.vmConfig.Tracer.CaptureStart(caller.Address(), addr, false, input, gas, value)
				evm.vmConfig.Tracer.CaptureEnd(ret, 0, 0, nil)
			}
			return nil, gas, nil
		}
		evm.StateDB.CreateAccount(addr)
	}
	evm.Transfer(evm.StateDB, caller.Address(), to.Address(), value)

	contract := NewContract(caller, to, value, gas)
	contract.SetCallCode(&addr, evm.StateDB.GetCodeHash(addr), evm.StateDB.GetCode(addr))

	start := time.Now()

	if evm.vmConfig.Debug && evm.depth == 0 {
		evm.vmConfig.Tracer.CaptureStart(caller.Address(), addr, false, input, gas, value)

		defer func() {
			evm.vmConfig.Tracer.CaptureEnd(ret, gas-contract.Gas, time.Since(start), err)
		}()
	}
	ret, err = run(evm, contract, input) // run the code for smart contract

	if err != nil {
		evm.StateDB.RevertToSnapshot(snapshot)
		if err != errExecutionReverted {
			contract.UseGas(contract.Gas)
		}
	}
	return ret, contract.Gas, err
}

func run(evm *EVM, contract *Contract, input []byte) ([]byte, error) { //The Run method will execute the code of the contract in a loop,
	if contract.CodeAddr != nil {
		precompiles := PrecompiledContractsHomestead
		if evm.ChainConfig().IsByzantium(evm.BlockNumber) {
			precompiles = PrecompiledContractsByzantium
		}
		if p := precompiles[*contract.CodeAddr]; p != nil {
			return RunPrecompiledContract(p, input, contract)
		}
	}
	return evm.interpreter.Run(contract, input)
}
```



### Gas for execute a call

In order to optimize the execution efficiency of smart contracts and reduce Gas costs, the following measures can be taken:

1. Simplify the logic and code of smart contracts and reduce the computing resources required for execution.

2. Use Solidity to write efficient smart contract code, such as using appropriate data types and algorithms, and avoiding expensive operations such as loops and recursion.

3. 
   Reduce the number of smart contract interactions and avoid frequent calls to other smart contracts and external services, thereby reducing the gas cost of the interaction.

4. Use Gas optimization tools, such as Solidity's gas() function, Remix, etc., to analyze the Gas consumption of smart contracts and further optimize the smart contract code.



### Questions

- What are the components of the Ethereum Virtual Machine? What are the parts of the memory of the Ethereum virtual machine?
  - Stack: The stack is a data structure that stores values during the execution of a program. The EVM uses a stack-based architecture, which means that all operations are performed on the stack.
  - Memory: The memory is a linear array of bytes that can be used by a program to store data during execution. The memory is volatile, which means that it is cleared when the program terminates.
  - Storage: The storage is a persistent key-value store that is used to store data between transactions. The storage is backed by the blockchain, which means that it is immutable.
- Please explain Storage, which variables are stored? .
  - Storage is a persistent key-value store that is used to store data between transactions. Variables that are stored in storage are persistent across multiple executions of a smart contract. In Solidity, variables declared with the "storage" keyword are stored in storage.
- Please explain the memory (Memory), which variables are stored? 
  - Memory is a linear array of bytes that can be used by a program to store data during execution. Unlike storage, the memory is volatile, which means that it is cleared when the program terminates. Variables that are stored in memory are not persistent across multiple executions of a smart contract. In Solidity, variables declared with the "memory" keyword are stored in memory.
- Please explain Calldata.
  - Calldata is a read-only area of memory that contains the input data for a function call. When a function is called in a smart contract, the input data is passed to the function via the calldata. The calldata is immutable, which means that it cannot be modified by the function.
- What is the difference between EVM calls and non-EVM calls?
  - EVM calls are function calls that are executed within the Ethereum Virtual Machine. EVM calls are used to call functions within a smart contract or to call other smart contracts. Non-EVM calls are function calls that are executed outside of the Ethereum Virtual Machine. Non-EVM calls are used to interact with external systems, such as APIs or databases. EVM calls are more expensive than non-EVM calls because they require more computation and are executed within the context of the Ethereum blockchain.