import asyncio
from decimal import Decimal
from pprint import pprint

from eth_typing import ChecksumAddress
from hyperliquid.utils import constants
from hyperliquid.info import Info
from web3 import Web3
from constants import ERC20_ABI, USDC_CONTRACT_ADDRESS
from sock import example_utils
from functional import Web3WalletManager


def get_usdc_balance():
    web3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))

    usdc_contract_address = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831'
    main_wallet_address = "0x2D3b14e79fB9263b7B44Aa6d985f8334351ed3AF"

    usdc_contract = web3.eth.contract(address=usdc_contract_address, abi=ERC20_ABI)
    balance = usdc_contract.functions.balanceOf(main_wallet_address).call()
    return web3.from_wei(balance, 'gwei') * 1000


wallet = '0x2D3b14e79fB9263b7B44Aa6d985f8334351ed3AF'

async def get_hyperliquid_user_state(wallet):
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    user_state = info.user_state(wallet)
    return user_state


async def hl_withdraw_test(usdc_amount):
    address, info, exchange = example_utils.setup(base_url=constants.MAINNET_API_URL, skip_ws=True)
    hl_data = await get_hyperliquid_user_state(address)
    hl_acc_value = hl_data['crossMarginSummary']['accountValue']
    hl_total_raw_usd = hl_data['crossMarginSummary']['totalRawUsd']
    hl_withdrawable = float(hl_data['withdrawable'])

    # get cur balance of hl
    # print(f"hl_data {json.dumps(hl_data, indent=4)}")
    print(
        f"address {address} hl_acc_value {hl_acc_value} | hl_total_raw_usd {hl_total_raw_usd} | hl_withdrawable {hl_withdrawable} |"
        f"Withrdaw Request: {usdc_amount}")

    # withdraw
    if exchange.account_address != exchange.wallet.address:
        raise Exception(f"Agents do not have permission to perform withdrawals \n"
                        f"Acc {exchange.account_address} | Wallet {exchange.wallet.address}")

    withdraw_result = exchange.withdraw_from_bridge(usdc_amount, address)
    print(f"withdraw_result {withdraw_result}")
    withdraw_status = withdraw_result['status']

    return withdraw_status


# async def main():
#     # wallet = '0x2D3b14e79fB9263b7B44Aa6d985f8334351ed3AF'
#     # user_state = await get_hyperliquid_user_state(wallet)
#     # pprint(user_state)
#     withdraw_status = await hl_withdraw_test(5)
#     pprint(withdraw_status)
#
# # Запускаем асинхронную функцию main()
# asyncio.run(main())


# def send_usdc_to_whitelist(whitelist_address, amount):
#     web3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))
#     usdc_contract = web3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=ERC20_ABI)
#
#     main_wallet_address = '0x2D3b14e79fB9263b7B44Aa6d985f8334351ed3AF'
#     main_wallet_address = web3.to_checksum_address(main_wallet_address)
#     whitelist_address = web3.to_checksum_address(whitelist_address)
#
#     dict_transaction = {
#         'chainId': web3.eth.chain_id,
#         'from': main_wallet_address,
#         'gasPrice': web3.eth.gas_price,
#         'nonce': web3.eth.get_transaction_count(main_wallet_address),
#     }
#
#     usdc_decimals = usdc_contract.functions.decimals().call()
#     usdc_amount = amount * 10 ** usdc_decimals
#
#     transaction = usdc_contract.functions.transfer(
#         whitelist_address, usdc_amount
#     ).build_transaction(dict_transaction)
#
#     main_wallet_private_key = "a1d88f2749e2e3e0688623df56c22fdd0d11d6a0c4a74cbd940696fb886f5dfe"
#     signed_txn = web3.eth.account.sign_transaction(transaction, main_wallet_private_key)
#     tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#
#     if receipt['status'] == 1:
#         print(f"Успешно отправлено {amount} USDC на адрес {whitelist_address}. Tx hash: {tx_hash}")
#     else:
#         print(f"Ошибка при отправке USDC: {receipt['status']}")


# send_usdc_to_whitelist("0x2df1c51e09aecf9cacb7bc98cb1742757f163df7", 1)
obj = Web3WalletManager("options.json")
# obj.send_usdc_to_hl(amount=1.5)
# print(obj.get_hyperliquid_user_state())
res = obj.get_usdc_balance()
print(res)