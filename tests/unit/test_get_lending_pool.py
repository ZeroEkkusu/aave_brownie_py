from brownie import interface, network, config


def test_get_lending_pool(test_only_locally):
    # Arrange/Act
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    # Assert
    lending_pool.address == "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
