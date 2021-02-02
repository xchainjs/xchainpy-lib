from Crypto.Protocol.KDF import PBKDF2

#TODO: must be async
def pbkdf2(passphrase , salt , iterations , keylen , digest):
    res = PBKDF2(password=passphrase,salt=salt,count=iterations,dkLen=keylen,hmac_hash_module=digest)
    return res