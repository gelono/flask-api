import json
from web3 import Web3
from constants import USDC_CONTRACT_ADDRESS, ERC20_ABI
# hyperliquid imports
from hyperliquid.info import Info
from hyperliquid.utils import constants
import example_utils


class Web3WalletManager:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.web3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))
        self.main_wallet_address = self.config['main_wallet']['public_key']
        self.main_wallet_private_key = self.config['main_wallet']['private_key']
        self.HL_exchange_address = self.config['exchange_addresses']['HL']

    def get_hyperliquid_user_state(self):
        info = Info(constants.MAINNET_API_URL, skip_ws=True)
        user_state = info.user_state(self.main_wallet_address)
        # return user_state['crossMarginSummary']['accountValue']
        return user_state

    def get_usdc_balance(self):
        usdc_contract = self.web3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=ERC20_ABI)
        balance = usdc_contract.functions.balanceOf(self.main_wallet_address).call()
        return self.web3.from_wei(balance, 'gwei') * 1000

    def send_usdc_to_hl(self, amount):
        usdc_contract = self.web3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=ERC20_ABI)

        main_wallet_address_checksum = self.web3.to_checksum_address(self.main_wallet_address)
        whitelist_address_checksum = self.web3.to_checksum_address(self.HL_exchange_address)

        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': main_wallet_address_checksum,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(main_wallet_address_checksum),
        }

        usdc_decimals = usdc_contract.functions.decimals().call()
        usdc_amount = amount * 10 ** usdc_decimals

        transaction = usdc_contract.functions.transfer(
            whitelist_address_checksum, usdc_amount
        ).build_transaction(dict_transaction)

        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.main_wallet_private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            print(f"Успешно отправлено {amount} USDC на адрес {whitelist_address_checksum}. Tx hash: {tx_hash}")
        else:
            print(f"Ошибка при отправке USDC: {receipt['status']}")

    def send_usdc_to_another_wallet(self, recipient, amount):
        usdc_contract = self.web3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=ERC20_ABI)

        main_wallet_address_checksum = self.web3.to_checksum_address(self.main_wallet_address)
        whitelist_address_checksum = self.web3.to_checksum_address(recipient)

        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': main_wallet_address_checksum,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(main_wallet_address_checksum),
        }

        usdc_decimals = usdc_contract.functions.decimals().call()
        usdc_amount = amount * 10 ** usdc_decimals

        transaction = usdc_contract.functions.transfer(
            whitelist_address_checksum, usdc_amount
        ).build_transaction(dict_transaction)

        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.main_wallet_private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] == 1:
            print(f"Успешно отправлено {amount} USDC на адрес {whitelist_address_checksum}. Tx hash: {tx_hash}")
        else:
            print(f"Ошибка при отправке USDC: {receipt['status']}")

    def hl_withdraw_test(self, usdc_amount):
        address, info, exchange = example_utils.setup(base_url=constants.MAINNET_API_URL, skip_ws=True)
        hl_data = self.get_hyperliquid_user_state()
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
