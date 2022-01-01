from brownie import interface, network, config


def test_get_token_address_aave(test_only_locally):
    protocol_data_provider = interface.IProtocolDataProvider(
        config["networks"][network.show_active()]["protocol_data_provider"])
    tokens = protocol_data_provider.getAllReservesTokens()
    for token in tokens:
        if (token[0] == "DAI"):
            assert token[1] == "0x6b175474e89094c44da98b954eedeac495271d0f"
