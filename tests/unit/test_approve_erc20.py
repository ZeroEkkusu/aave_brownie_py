from scripts.helpful_scripts import get_account
from brownie import config, interface, network
from web3 import Web3
from scripts.lending_pool import get_lending_pool
from scripts.weth import get_weth


def test_approve_erc20(test_only_locally):
    # Modified from PatrickAlphaC/aave_brownie_py (https://github.com/PatrickAlphaC/aave_brownie_py). See NOTICE.md.
    # Arrange
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    amount = Web3.toWei(0.1, "ether")
    get_weth(amount)
    lending_pool = get_lending_pool()
    # Act
    erc20 = interface.IERC20(weth_address)
    erc20.approve(lending_pool.address, amount, {"from": account})
    # Assert
    assert erc20.allowance(account.address, lending_pool.address) == amount
