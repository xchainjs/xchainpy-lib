from enum import Enum

Prefix = {
    "Cosmos" : "cosmos",
    "Public" : "pub",
    "Account" : "acc",
    "Validator" : "val",
    "Operator" : "oper",
    "Consensus" : "cons"
}

bech32_prefix = {
    "accAddr" : Prefix["Cosmos"],
    "accPub" : Prefix["Cosmos"] + Prefix["Public"],
    "valAddr" : Prefix["Cosmos"] + Prefix["Validator"] + Prefix["Operator"],
    "valPub" : Prefix["Cosmos"] + Prefix["Validator"] + Prefix["Operator"] + Prefix["Public"],
    "consAddr" : Prefix["Cosmos"] + Prefix["Validator"] + Prefix["Consensus"],
    "consPub" : Prefix["Cosmos"] + Prefix["Validator"] + Prefix["Consensus"] + Prefix["Public"]
}

def set_bech32_prefix(acc_addr : str , acc_pub : str , val_addr : str , val_pub : str , cons_addr : str , cons_pub : str):
    bech32_prefix["accAddr"] = acc_addr
    bech32_prefix["accPub"] = acc_pub
    bech32_prefix["valAddr"] = val_addr
    bech32_prefix["valPub"] = val_pub
    bech32_prefix["consAddr"] = cons_addr
    bech32_prefix["consPub"] = cons_pub