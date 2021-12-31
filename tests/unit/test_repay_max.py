from brownie import network, config, interface
from scripts.erc20 import approve_erc20, get_balance_of_erc20
from scripts.get_asset_price import get_asset_price
from scripts.helpful_scripts import get_account
from web3 import Web3
from scripts.lending_pool import get_borrowable_data, get_lending_pool

from scripts.weth import get_weth


def test_repay_max(test_only_locally):
    # Arrange
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    rate_mode = 1
    amount = Web3.toWei(0.1, "ether")
    get_weth(amount)
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address,
                  weth_address, account.address)
    lending_pool.deposit(weth_address, amount,
                         account.address, 0, {"from": account})
    total_collateral, total_debt, borrowable_eth, treshold, ltv, health = get_borrowable_data(
        lending_pool, account.address)
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"])
    # Act
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    dai_address = config["networks"][network.show_active()]["dai_token"]
    lending_pool.borrow(
        dai_address, amount_dai_to_borrow*1e18, rate_mode, 0, account.address, {"from": account})
    protocol_data_provider = interface.IProtocolDataProvider(
        config["networks"][network.show_active()]["protocol_data_provider"])
    debt_token_address = protocol_data_provider.getReserveTokensAddresses(dai_address)[
        rate_mode]
    debt_token_balance = get_balance_of_erc20(
        debt_token_address, account.address)

    approve_erc20((2 ** 256) - 1, lending_pool.address,
                  dai_address, account.address)
    token_balance = get_balance_of_erc20(dai_address, account.address)
    if (token_balance == 0):
        return
    amount_to_repay = (
        2 ** 256) - 1 if token_balance >= debt_token_balance else token_balance
    try:
        lending_pool.repay(dai_address, amount_to_repay,
                           rate_mode, account.address, {"from": account})
        # Assert
        assert get_balance_of_erc20(debt_token_address, account.address) == 0
    except:
        lending_pool.repay(dai_address, token_balance,
                           rate_mode, account.address, {"from": account})
        # Assert
        assert get_balance_of_erc20(
            debt_token_address, account.address) < debt_token_balance
