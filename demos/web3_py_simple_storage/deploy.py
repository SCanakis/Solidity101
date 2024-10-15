from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

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

# for coneecting to Sepolia
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/f753a5e49ac84ad8bb1d7026d2a4065a"))
chain_id = 11155111
my_address = "0x40eCAC93f6fd35b2459Ec85fa6F64E071d4F4D0B"
private_key = os.getenv("PRIVATE_KEY")
#print(private_key)

#Create the contract in python
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().build_transaction({"chainId":chain_id,"from":my_address, "nonce":nonce})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)
# Send this Singed Transaction
print("Deploying Contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")


# Working with a contract, you always need 
# Contract Address
# Contract ABI


simple_storage = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

# Call -> Simulate making the call and getting a return value { No state change }
# Transaciton -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).build_transaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce+1}
)
singed_store_txn = w3.eth.account.sign_transaction(
    store_transaction,private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(singed_store_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")

print(simple_storage.functions.retrieve().call())
