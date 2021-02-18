import asyncio

async def main():
    import xchainpy.xchainpy_thorchain.client as thorchain

    client = thorchain.Client(network="testnet", phrase="history dice polar glad split follow tired invest lemon mask all industry")

    # balance = await client.get_balance(address='tthor13gym97tmw3axj3hpewdggy2cr288d3qffr8skg')

    # print(balance)

    # tx = await client.get_transaction_data(tx_id='1FC324D895907EF076288E130376B3EB00D9F0B4B1C42FD4C3F950BA29F4807C')

    # print(tx)

    print(client.get_address())

    await client.transfer(1, "tthor13gym97tmw3axj3hpewdggy2cr288d3qffr8skg")



asyncio.run(main())