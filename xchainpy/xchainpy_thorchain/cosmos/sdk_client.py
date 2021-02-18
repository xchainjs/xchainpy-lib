import hashlib

import bech32
import ecdsa
import hdwallets
import mnemonic

import http3
import json
import base64

# import httpx

class CosmosSDKClient:
    server = chain_id = prefix = derive_path = ''

    _account_num = None

    def __init__(self, server, prefix='cosmos', derive_path="44'/118'/0'/0/0", chain_id="thorchain"):
        self.prefix = prefix
        self.derive_path = derive_path
        self.server = server
        self.chain_id = chain_id

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

        self.privkey = derived_privkey

        return derived_privkey
    
    def privkey_to_pubkey(self, privkey: bytes) -> bytes:
        privkey_obj = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
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

    async def get_balance(self, address):
        try:
            api_url = f'{self.server}/bank/balances/{address}'

            client = http3.AsyncClient()

            response = await client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return None
        except Exception as err:
            raise Exception(err)

    async def txs_hash_get(self, tx_id):
        try:
            api_url = f'{self.server}/txs/{tx_id}'

            client = http3.AsyncClient()

            response = await client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return None
        except Exception as err:
            raise Exception(err)

    async def account_address_get(self, address):
        try:
            if not address:
                raise Exception('address is expected!')

            api_url = f'{self.server}/auth/accounts/{address}'

            client = http3.AsyncClient()

            response = await client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                raise Exception(json.loads(response.content.decode('utf-8'))['error'])

        except Exception as err:
            raise Exception(err)


    async def make_transaction( self, privkey: bytes, from_address: str, fee_denom: str = "rune", memo: str = "", sync_mode: str = "block"):
        if not self._account_num:
            account = await self.account_address_get(address=from_address)
            print(account)
            self._account_num = account['result']['value']['account_number']
            self._sequence = account['result']['value']['sequence']

        self._gas = "10000000"
        self._fee = "10000000"
        self._privkey = self.privkey
        self._fee_denom = fee_denom
        self._memo = memo
        self._chain_id = self.chain_id
        self._hrp = "tthor"
        self._sync_mode = sync_mode
        self._msgs = []

    def add_transfer(self, recipient: str, amount: int, denom: str = "rune") -> None:
        transfer = {
            "type": "thorchain/MsgSend",
            "value": {
                "from_address": self.privkey_to_address(self._privkey),
                "to_address": recipient,
                "amount": [{"denom": denom, "amount": str(amount*(10**8))}],
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
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                    }
                ],
            },
            "mode": self._sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    async def do_transfer(self, content):
        api_url = f'{self.server}/txs'

        client = http3.AsyncClient()

        print(content)

        response = await client.post(api_url, data=content)

        print(response)

        print(response.content.decode('utf-8'))



    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
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
        
    