from web3 import Web3
from brownie import interface, network, config
from scripts.erc20 import approve_erc20, get_balance_of_erc20


def get_lending_pool():
    # Modified from PatrickAlphaC/aave_brownie_py (https://github.com/PatrickAlphaC/aave_brownie_py). See NOTICE.md.
    """
    Fetch the correct Lending Pool address via the Addresses Provider and make a contract object.

    Returns:
        brownie.network.contract.Contract: The Lending Pool contract
    """
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def get_borrowable_data(lending_pool, account):
    # Modified from PatrickAlphaC/aave_brownie_py (https://github.com/PatrickAlphaC/aave_brownie_py). See NOTICE.md.
    """
    Get data for an account across all the reserves.

    Args:
        lending_pool (brownie.network.contract.Contract): Lending Pool contract
        account (str): account address

    Returns:
        tuple:
            float: total collateral in ETH
            float: total debt in ETH
            float: borrowing power left in ETH
            float: current liquidation threshold in %
            float: Loan To Value in %
            float: current health factor

    """
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_treshold,
     ltv, health_factor) = lending_pool.getUserAccountData(account)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    current_liquidation_treshold /= 1e4
    ltv /= 1e4
    health_factor /= 1e18

    print(
        f"(i) Deposited in ETH: {total_collateral_eth} Borrowed in ETH: {total_debt_eth} Can borrow in ETH: {available_borrow_eth}")

    return (float(total_collateral_eth), float(total_debt_eth), float(available_borrow_eth), current_liquidation_treshold, ltv, health_factor)


def repay_max(token_address, lending_pool, account, rate_mode):
    """
    Repay a portion of/the entire debt with the token.

    Args:
        token_address (str): borrowed token address
        lending_pool (brownie.network.contract.Contract): Lending Pool contract
        account (brownie.network.account.Account): my account

    Returns:
        tuple:
            int: The outcome - (1) Fully Repayed, (0) Partially Repayed, (-1) Not Repayed
            brownie.network.transaction.TransactionReceipt: The transaction receipt
    """
    # get the debt token balance
    protocol_data_provider = interface.IProtocolDataProvider(
        config["networks"][network.show_active()]["protocol_data_provider"])
    debt_token_address = protocol_data_provider.getReserveTokensAddresses(token_address)[
        rate_mode]
    debt_token_balance = get_balance_of_erc20(
        debt_token_address, account.address)

    approve_erc20((2 ** 256) - 1, lending_pool.address,
                  token_address, account.address)

    print("Repaying...")
    token_balance = get_balance_of_erc20(token_address, account.address)
    if (token_balance == 0):
        print("Not Repayed!")
        return -1, None
    amount_to_repay = (
        2 ** 256) - 1 if token_balance >= debt_token_balance else token_balance
    try:
        tx = lending_pool.repay(token_address, amount_to_repay,
                                rate_mode, account.address, {"from": account})
        print("Fully Repayed!")
        return 1, tx
    except:
        tx = lending_pool.repay(token_address, token_balance,
                                rate_mode, account.address, {"from": account})
        print(f"Partially Repayed!")
        return 0, tx
