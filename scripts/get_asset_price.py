from brownie import interface


def get_asset_price(price_feed_address):
    """
    Get the latest exchange rate of a trading pair.

    Args:
        price_feed_address (str): Price Feed address

    Returns:
        float: The latest exchange rate

    """
    price_feed = interface.AggregatorV3Interface(price_feed_address)
    # the answer
    latest_price = price_feed.latestRoundData()[1]
    converted_latest_price = latest_price / 10**price_feed.decimals()
    print(f"(i) {price_feed.description()} = {converted_latest_price}")
    return float(converted_latest_price)
