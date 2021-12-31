from scripts.helpful_scripts import get_account
from brownie import config, interface, network
from scripts.weth import get_weth
from web3 import Web3


def test_can_get_eth_back(test_only_locally):
    # Arrange
    account = get_account()
    amount = Web3.toWei(0.1, "ether")
    get_weth(amount)
    # Act
    balance = account.balance()
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"])
    weth.withdraw(amount, {"from": account})
    # Assert
    assert account.balance() > balance
