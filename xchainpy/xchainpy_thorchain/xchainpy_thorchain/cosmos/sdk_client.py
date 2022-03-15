import hashlib
from ..cosmos.models.StdTx import StdTx
from .cosmosUtil import set_bech32_prefix
from .. import utils
import bech32
import ecdsa
import hdwallets
import mnemonic
import http3
import json
import base64
import re
from urllib.parse import quote

BASE_PATH = re.sub(r'\/+$','',"https://api.cosmos.network")

class CosmosSDKClient:
    

    _account_num = None

    def __init__(self, server, prefix: str = 'cosmos', derive_path: str = "m/44'/118'/0'/0/0", chain_id: str = "thorchain") -> None:
        self.prefix = prefix
        self.derive_path = derive_path
        self.server = server
        self.chain_id = chain_id
        self.client = http3.AsyncClient(timeout=10)

    def seed_to_privkey(self, seed: str) -> bytes:
        """
        Get a private key from a mnemonic seed and a derivation path.
        Assumes a BIP39 mnemonic seed with no passphrase. Raises
        `cosmospy.BIP32DerivationError` if the resulting private key is
        invalid.
        """
        seed_bytes = mnemonic.Mnemonic.to_seed(seed, passphrase="")
        hd_wallet = hdwallets.BIP32.from_seed(seed_bytes)
        # This can raise a `hdwallets.BIP32DerivationError` (which we alias so
        # that the same exception type is also in the `cosmospy` namespace).
        derived_privkey = hd_wallet.get_privkey_from_path(self.derive_path)

        self._privkey = derived_privkey

        return derived_privkey

    def privkey_to_pubkey(self, privkey: bytes) -> bytes:
        privkey_obj = ecdsa.SigningKey.from_string(
            privkey, curve=ecdsa.SECP256k1)
        pubkey_obj = privkey_obj.get_verifying_key()

        return pubkey_obj.to_string("compressed")

    def pubkey_to_address(self, pubkey: bytes) -> str:
        s = hashlib.new("sha256", pubkey).digest()
        r = hashlib.new("ripemd160", s).digest()
        five_bit_r = bech32.convertbits(r, 8, 5)

        assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"

        return bech32.bech32_encode(self.prefix, five_bit_r)

    def privkey_to_address(self, privkey: bytes) -> str:
        pubkey = self.privkey_to_pubkey(privkey)
        return self.pubkey_to_address(pubkey)

    async def get_balance(self, address:str):
        try:
            api_url = f'{self.server}/bank/balances/{address}'

            response = await self.client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return None
        except Exception as err:
            raise Exception(err)

    async def txs_hash_get(self, tx_id: str):
        try:
            api_url = f'{self.server}/txs/{tx_id}'

            response = await self.client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return None
        except Exception as err:
            raise Exception(err)

    async def account_address_get(self, address: str):
        try:
            if not address:
                raise Exception('address is expected!')

            api_url = f'{self.server}/auth/accounts/{address}'

            response = await self.client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                raise Exception(json.loads(
                    response.content.decode('utf-8'))['error'])

        except Exception as err:
            raise Exception(err)

    async def make_transaction(self, privkey: bytes, from_address: str, fee_denom: str = "rune", memo: str = "", sync_mode: str = "block") -> None:
        try:
            self.set_prefix()
            acc_address = utils.frombech32(from_address)
            account = await self.account_address_get(acc_address)
            account = {
                "address": utils.frombech32(account["value"]["address"]) if account["value"]["address"] else "",
                "public_key": account["value"]["public_key"]["value"] if account["value"]["public_key"] else base64.b64encode(self.privkey_to_pubkey(privkey)).decode("utf-8"),
                "coins": account["value"]["coins"] if "coins" in account["value"] else [],
                "account_number": account["value"]["account_number"],
                # there is no "sequence" for a fresh wallet, so we use "get" with default
                "sequence": account["value"]["sequence"] if "sequence" in account["value"] else "0"
            }
            self._account_num = account["account_number"]
            self._sequence = account["sequence"]
            self._gas = "10000000"
            self._fee = "10000000"
            self._privkey = privkey
            self._fee_denom = fee_denom
            self._memo = memo
            self._chain_id = self.chain_id
            self._hrp = "tthor"
            self._sync_mode = sync_mode
            self._msgs = []
        except Exception as err:
            raise Exception(str(err))

    def add_transfer(self, recipient: str, amount: int, denom: str = "rune") -> None:
        transfer = {
            "type": "thorchain/MsgSend",
            "value": {
                "from_address": self.privkey_to_address(self._privkey),
                "to_address": recipient,
                "amount": [{"denom": denom, "amount": utils.cnv_big_number(amount, utils.DECIMAL)}],
            },
        }
        self._msgs.append(transfer)

    def get_pushable(self) -> str:
        pubkey = self.privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(pubkey).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self._msgs,
                "fee": {
                    "gas": str(self._gas),
                    "amount": [],
                },
                "memo": self._memo,
                "signatures": [
                    {
                        "signature": self._sign_simple(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                    }
                ],
            },
            "mode": self._sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    async def do_transfer(self, content):
        api_url = f'{self.server}/txs'

        response = await self.client.post(api_url, data=content)

        #print(response)

        #print(response.content.decode('utf-8'))
        return response.content.decode('utf-8')

    def _sign_simple(self) -> str:
        message_str = json.dumps(
            self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = ecdsa.SigningKey.from_string(
            self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(
            signature_compact).decode("utf-8")
        return signature_base64_str
    
    def _sign(self , sign_bytes , priv_key) -> str:
        privkey = ecdsa.SigningKey.from_string(
            priv_key, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            sign_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(
            signature_compact).decode("utf-8")
        return signature_base64_str

    def _get_sign_message(self):
        return {
            "chain_id": self._chain_id,
            "account_number": str(self._account_num),
            "fee": {
                "gas": str(self._gas),
                "amount": [],
            },
            "memo": self._memo,
            "sequence": str(self._sequence),
            "msgs": self._msgs,
        }
    
    def set_prefix(self):
        set_bech32_prefix(self.prefix , self.prefix + "pub" , self.prefix + "valoper" , self.prefix + "valoperpub" , self.prefix + "valcons" , self.prefix + "valconspub")

    async def account_address_get(self , address):
        if not address:
          raise Exception("address not provided")
        try:
            address = utils.tobech32(address)
            local_var_path = re.sub("{address}", quote(address.encode("utf-8")),"/auth/accounts/{address}")
            url = self.server + local_var_path
            response = await self.client.get(url)

            if response.status_code == 200:
                result = json.loads(response.content.decode('utf-8'))['result']
                return result
            else:
                err_obj = json.loads(response.content.decode('utf-8'))
                raise Exception(err_obj)
        except Exception as err:
                raise Exception(str(err))
    
    def sign_std_tx(self, privkey , unsigned_std_tx : StdTx, account_number : str, sequence : str , pub_key : str):
        sign_bytes = unsigned_std_tx.get_sign_bytes(self.chain_id ,account_number ,sequence)
        signature = {
            "pub_key" : pub_key,
            "signature" : self._sign(sign_bytes , privkey)
        }
        signature_param = None
        if unsigned_std_tx.signature:
            signature_param = [{**unsigned_std_tx.signature} , signature]
        else:
            signature_param = [signature]


        new_std_tx = StdTx(unsigned_std_tx.msg , unsigned_std_tx.fee , signature_param , unsigned_std_tx.memo)

        return new_std_tx

    def get_tx_post_data(self , tx : StdTx , mode) -> str:
        pushable_tx = {
            "tx": {
                "msg": tx.msg,
                "fee": {
                    "gas": str(tx.fee['gas']),
                    "amount": [],
                },
                "memo": tx.memo,
                "signatures": [
                    {
                        "signature": tx.signature[0]["signature"],
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": tx.signature[0]["pub_key"]},
                    }
                ],
            },
            "mode": mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    async def tx_post(self , tx : StdTx , mode): # broadcastReq
        if not tx:
          raise Exception("tx not provided")
        
        try:
            local_var_path = '/txs'
            

            api_url = self.server + local_var_path

            post_data = self.get_tx_post_data(tx , mode)

            response = await self.client.post(url=api_url, data=post_data)

            if response.status_code == 200:
                res = json.loads(response.content.decode('utf-8'))
                return res
            else:
                return json.loads(response.content.decode('utf-8'))
        except Exception as err:
            raise Exception(str(err))


    async def sign_and_broadcast(self , unsigned_std_tx , private_key , signer):
        try:
            self.set_prefix()
            account = await self.account_address_get(signer)
            account = {
                "address": utils.frombech32(account["value"]["address"]) if "address" in account["value"] else "",
                "public_key": account["value"]["public_key"]["value"] if "public_key" in account["value"] else base64.b64encode(self.privkey_to_pubkey(private_key)).decode("utf-8"),
                "coins": account["value"]["coins"] if "coins" in account["value"] else"",
                "account_number": account["value"]["account_number"] if "account_number" in account["value"] else"",
                "sequence": account["value"]["sequence"] if "sequence" in account["value"] else "0"
            }
            signed_std_tx = self.sign_std_tx(private_key, unsigned_std_tx, str(account["account_number"]), str(account["sequence"]), str(account["public_key"]) )
            result = await self.tx_post(signed_std_tx, 'block')
            return result

        except Exception as err:
            raise Exception(str(err))

    def get_priv_key_from_mnemonic(self, seed: str , derivation_path) -> bytes:
        """
        Get a private key from a mnemonic seed and a derivation path.
        Assumes a BIP39 mnemonic seed with no passphrase. Raises
        `cosmospy.BIP32DerivationError` if the resulting private key is
        invalid.
        """
        seed_bytes = mnemonic.Mnemonic.to_seed(seed, passphrase="")
        hd_wallet = hdwallets.BIP32.from_seed(seed_bytes)
        # This can raise a `hdwallets.BIP32DerivationError` (which we alias so
        # that the same exception type is also in the `cosmospy` namespace).
        derived_privkey = hd_wallet.get_privkey_from_path(derivation_path)

        return derived_privkey

    def get_address_from_mnemonic(self, mnemonic : str , derivation_path : str) -> str:
        self.set_prefix()

        priv_key = self.get_priv_key_from_mnemonic(mnemonic , derivation_path)

        return self.privkey_to_address(priv_key)


