import asyncio




async def main():



    from xchainpy_client.models.types import Network, XChainClientParams
    from .client import Client
    from xchainpy_client.models.tx_types import TxHistoryParams


    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

    address = client.get_address()

    params = TxHistoryParams(address=address, limit=1)
    transactions = await client.get_transactions(params)

    for a in transactions.txs[0].dir():
        print(a)

    # balances = await client.get_balance(address=address)

    # for balance in balances:
    #     print(f'asset: {balance.asset}, amount: {balance.amount}')



    # fees = await client.get_fees()
    
    # multi_send_fees = await client.get_multi_send_fees()

    # single_and_multi_fees = await client.get_single_and_multi_fees()

    # print(f'''fees: 
    # average: {fees.average}
    # fast: {fees.fast}
    # fastest: {fees.fastest}\n''')
    
    # print(f'''multi_send_fees: 
    # average: {multi_send_fees.average}
    # fast: {multi_send_fees.fast}
    # fastest: {multi_send_fees.fastest}\n''')

    # print(f'''single_and_multi_fees: 
    # single:
    #     average: {single_and_multi_fees['single'].average}
    #     fast: {single_and_multi_fees['single'].fast}
    #     fastest: {single_and_multi_fees['single'].fastest}
    # multi:
    #     average: {single_and_multi_fees['single'].average}
    #     fast: {single_and_multi_fees['single'].fast}
    #     fastest: {single_and_multi_fees['single'].fastest}''')


    # get_transactions
    # get_transaction_data




    # transaction = await client.get_transaction_data(transactions['tx'][0].tx_hash)


    # transfer

    a = 9




loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
