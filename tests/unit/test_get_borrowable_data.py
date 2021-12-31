from scripts.erc20 import approve_erc20
from scripts.helpful_scripts import get_account
from brownie import config, network
from web3 import Web3
from scripts.lending_pool import get_lending_pool

from scripts.weth import get_weth


def test_get_borrowable_data(test_only_locally):
    # Arrange
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    amount = Web3.toWei(0.1, "ether")
    get_weth(amount)
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address,
                  weth_address, account.address)
    # Act
    lending_pool.deposit(weth_address, amount,
                         account.address, 0, {"from": account})
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_treshold,
     ltv, health_factor) = lending_pool.getUserAccountData(account)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    current_liquidation_treshold /= 1e4
    ltv /= 1e4
    health_factor /= 1e18

    # Assert
    assert float(total_collateral_eth) >= Web3.fromWei(amount, "ether")
    assert float(total_debt_eth) == 0
    assert float(available_borrow_eth) > 0
    assert current_liquidation_treshold > 0
    assert ltv > 0
    assert health_factor > 1
