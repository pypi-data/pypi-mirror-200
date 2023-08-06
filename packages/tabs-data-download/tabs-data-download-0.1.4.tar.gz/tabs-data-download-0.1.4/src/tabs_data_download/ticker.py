import requests
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.exchange_type import ExchangeType

URLS = {
    ExchangeType.BINANCE: {
        AssetType.SPOT: "https://api.binance.com/api/v3/ticker/price",
        AssetType.FUTURE: "https://fapi.binance.com/fapi/v1/ticker/price",
    },
    ExchangeType.KRAKEN: {
        AssetType.SPOT: "https://api.kraken.com/0/public/AssetPairs",
        AssetType.FUTURE: "https://futures.kraken.com/derivatives/api/v3/tickers",
    },
}


def print_tickers(
    exchange: ExchangeType | None = None, asset_type: AssetType | None = None
) -> None:
    url = URLS[exchange][asset_type]
    response = requests.get(url)

    # Extract ticker symbols from the response JSON
    if exchange is ExchangeType.BINANCE:
        trading_pairs = [ticker["symbol"] for ticker in response.json()]

    elif exchange is ExchangeType.KRAKEN:
        if asset_type is AssetType.SPOT:
            trading_pairs = response.json()["result"].keys()
        elif asset_type is AssetType.FUTURE:
            trading_pairs = [ticker["symbol"] for ticker in response.json()["tickers"]]

    print(trading_pairs)
