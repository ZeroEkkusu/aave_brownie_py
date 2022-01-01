from brownie import config, network
from scripts.helpful_scripts import get_account
from scripts.weth import get_weth, get_eth_back
from scripts.lending_pool import get_lending_pool, get_borrowable_data, repay_max
from scripts.erc20 import approve_erc20, get_balance_of_erc20
from scripts.get_asset_price import get_asset_price
from scripts.get_token_address_aave import get_token_address_aave
from web3 import Web3

# MAKE SURE YOU HAVE EXCESS DAI IN YOUR ACCOUNT TO COMPLETE THE ENTIRE TEST
# THIS WILL CHANGE AFTER IMPLEMENTING THE FLASH LOAN + SWAP FUNCTIONALITY
#
# --------------------------------------------------------------
# MAKE SURE THE ACCOUNT IS DEBT-FREE BEFORE RUNNING THE TEST !!!
# --------------------------------------------------------------

# collateral
AMOUNT_ETH = Web3.toWei(0.1, "ether")
# interest rate mode
RATE_MODE = 1


def test_basic_integration(dont_test_locally):
    """
    Mint WETH, deposit WETH, borrow DAI, repay everything, withdraw WETH, unlock your ETH
    """
    # setup
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]

    # mint WETH
    get_weth(AMOUNT_ETH)

    # get Lending Pool
    lending_pool = get_lending_pool()

    # approve
    approve_erc20(AMOUNT_ETH, lending_pool.address,
                  weth_address, account.address)

    # deposit
    print("Depositing...")
    tx = lending_pool.deposit(weth_address, AMOUNT_ETH,
                              account.address, 0, {"from": account})
    tx.wait(2)

    # get data
    total_collateral, total_debt, borrowable_eth, treshold, ltv, health = get_borrowable_data(
        lending_pool, account.address)
    # Assert the deposit
    assert total_collateral >= Web3.fromWei(AMOUNT_ETH, "ether")

    # exchange rate
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"])

    # calculate how much to borrow
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"(i) Going to borrow {amount_dai_to_borrow} DAI")

    # setup
    dai_address = get_token_address_aave("DAI") if network.show_active(
    ) == "kovan" else config["networks"][network.show_active()]["dai_token"]

    # borrow
    print("Borrowing DAI...")
    tx = lending_pool.borrow(
        dai_address, amount_dai_to_borrow*1e18, RATE_MODE, 0, account.address, {"from": account})
    tx.wait(2)

    # Assert the debt
    debt = get_borrowable_data(lending_pool, account.address)[1]
    assert debt >= borrowable_eth * 0.945

    # repay max
    repaid, tx = repay_max(dai_address, lending_pool, account, RATE_MODE)
    tx.wait(2)

    # Assert the repayment
    new_debt = get_borrowable_data(lending_pool, account.address)[1]
    if (repaid == -1):
        assert new_debt >= debt
    elif (repaid == 0):
        assert new_debt < debt
    elif (repaid == 1):
        assert new_debt == 0

    # proceed if debt-free
    if repaid == 1:

        weth_balance = get_balance_of_erc20(weth_address, account.address)

        # withdraw
        print("Withdrawing...")
        tx = lending_pool.withdraw(
            weth_address, (2 ** 256) - 1, account, {"from": account})
        tx.wait(2)

        # Assert the WETH withdrawal
        weth_balance_diff = get_balance_of_erc20(
            weth_address, account.address) - weth_balance
        assert weth_balance_diff > 0

        eth_balance = account.balance()

        # unlock ETH
        tx = get_eth_back(weth_balance_diff)
        tx.wait(2)

        # Assert the ETH withdrawal
        eth_balance_diff = account.balance() - eth_balance
        assert eth_balance_diff > 0
