import os
from web3 import Web3, WebsocketProvider, Account
import json

w3 = Web3(WebsocketProvider("wss://ropsten.infura.io/ws/v3/048d536048f5410cb17411edbdb4ef2c"))
print(w3.isConnected())

f = open("test/test_suite/mnemonic", "r")
mnemonic = f.readline()
f.close()
Account.enable_unaudited_hdwallet_features()
acct = w3.eth.account.from_mnemonic(mnemonic=mnemonic)

print(acct)
print(acct.address)
print(acct.privateKey)
balance = w3.eth.get_balance(acct.address)
print(w3.fromWei(balance, "ether"))
f = open("router_abi", "r")
abi = json.loads(f.readline())
f.close()
address = "0x9d496De78837f5a2bA64Cb40E62c19FBcB67f55a"
contract = w3.eth.contract(address=address, abi=abi)
totalSupply = contract.all_functions()
x = contract.functions.RUNE().call()
print(x)
print(totalSupply)