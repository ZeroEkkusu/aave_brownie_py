from brownie import interface, config, network
from web3 import Web3
from scripts.weth import get_weth
from scripts.helpful_scripts import get_account


def test_get_balance_of_erc20(test_only_locally):
    # Arrange
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    amount = Web3.toWei(0.1, "ether")
    get_weth(amount)
    # Act/Assert
    assert interface.IERC20(weth_address).balanceOf(account) == amount
