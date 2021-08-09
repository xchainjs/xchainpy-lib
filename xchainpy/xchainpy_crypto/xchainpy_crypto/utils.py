import asyncio
from Crypto.Protocol.KDF import PBKDF2


async def pbkdf2(passphrase, salt, iterations, keylen, digest):
    async_PBKDF2 = asyncio.coroutine(PBKDF2)
    return await async_PBKDF2(password=passphrase,salt=salt,count=iterations,dkLen=keylen,hmac_hash_module=digest)