from scripts.helpful_scripts import get_account
from brownie import config, interface, network
from web3 import Web3


def test_mint_weth(test_only_locally):
    # Arrange
    account = get_account()
    # Act
    amount = Web3.toWei(0.1, "ether")
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"])
    weth.deposit({"from": account, "value": amount})
    # Assert
    assert weth.balanceOf(account.address) == Web3.toWei(0.1, "ether")
