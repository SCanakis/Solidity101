from solcx import compile_standard
import json

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