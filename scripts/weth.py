from scripts.helpful_scripts import get_account
from brownie import config, interface, network


def get_weth(amount):
    """
    Mint WETH with ETH.

        Args:
            amount (number): amount in wei

        Returns:
        brownie.network.transaction.TransactionReceipt: The transaction receipt
    """
    account = get_account()
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"])
    print("Minting WETH...")
    return weth.deposit({"from": account, "value": amount})


def get_eth_back(amount):
    """
    Withdraw ETH from the WETH token contract.

    Args:
        amount (number): ETH amount

    Returns:
        brownie.network.transaction.TransactionReceipt: The transaction receipt
    """
    account = get_account()
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"])
    print("Withdrawing ETH...")
    return weth.withdraw(amount, {"from": account})
