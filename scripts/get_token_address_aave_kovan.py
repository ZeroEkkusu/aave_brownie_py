from brownie import interface, network, config


def get_token_address_aave(symbol):
    """
    Fetch the correct address for an using the Protocol Data Provider.
    You must get addresses this way when on the Kovan testnet.

    Args:
        symbol (str): token symbol

    Returns:
        str: The token contract address
    """
    protocol_data_provider = interface.IProtocolDataProvider(
        config["networks"][network.show_active()]["protocol_data_provider"])
    tokens = protocol_data_provider.getAllReservesTokens()
    for token in tokens:
        if (token[0] == symbol):
            return token[1]
