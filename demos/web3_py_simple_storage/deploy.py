from solcx import compile_standard
import json
from web3 import Web3
import os

with open("demos/web3_py_simple_storage/SimpleStorage.sol","r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile Our solidity

compile_sol = compile_standard(
    {
        "language":"Solidity",
        "sources":{"SimpleStorage.sol" : {"content" : simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*": { "*": ["abi", "metadata", "evm.bytecode","evm.sourceMap"]}
            }   
        },  
    },
    solc_version="0.6.0",
)

with open("demos/web3_py_simple_storage/compile_code.json","w") as file:
    json.dump(compile_sol, file)

# get bytcode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for coneecting to ganaceh
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x4686767d11DBdE6d1016C634362E1784C78b66BE"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

#Create the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().build_transaction({"chainId":chain_id,"from":my_address, "nonce":nonce})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)