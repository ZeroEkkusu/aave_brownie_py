from brownie import interface, config, network


def test_can_get_asset_price(test_only_locally):
    # Arrange/Act
    price_feed = interface.AggregatorV3Interface(
        config["networks"][network.show_active()]["dai_eth_price_feed"])
    latest_price = price_feed.latestRoundData()[1]
    converted_latest_price = latest_price / 10**price_feed.decimals()
    # Assert
    assert float(converted_latest_price) > 0
