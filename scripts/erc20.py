from brownie import interface


def approve_erc20(amount, spender, erc20_address, account):
    # Modified from PatrickAlphaC/aave_brownie_py (https://github.com/PatrickAlphaC/aave_brownie_py). See NOTICE.md.
    """
    Approve a contract to spend my ERC20 token.

    Args:
        amount (number): max amount in wei
        spender (str): contract address
        erc20_address (str): token address
        account (str): my address

    Returns:
        brownie.network.transaction.TransactionReceipt: The transaction receipt
    """
    erc20 = interface.IERC20(erc20_address)
    print("Approving ERC20 Token...")
    return erc20.approve(spender, amount, {"from": account})


def get_balance_of_erc20(erc20_address, account):
    """
    Get the amount of a token held by an account.

    Args:
        account (str): account address

    Returns:
        int: The token balance of the account.
    """
    return interface.IERC20(erc20_address).balanceOf(account)
