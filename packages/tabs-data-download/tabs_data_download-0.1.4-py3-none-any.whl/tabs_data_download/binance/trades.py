from __future__ import annotations

import asyncio

import requests
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.exchange_type import ExchangeType
from tabs_storage.storage import Storage

# https://data.binance.vision/data/spot/daily/trades/ETHUSDT/ETHUSDT-trades-2021-01-01.zip
# https://data.binance.vision/data/futures/um/daily/trades/ETHUSDT/ETHUSDT-trades-2021-01-01.zip
# https://data.binance.vision/data/futures/um/daily/trades/BTCUSDT_220930/BTCUSDT_220930-trades-2022-09-30.zip
# https://static.okx.com/cdn/okex/traderecords/trades/daily/20221005/LINK-USDT-230331-trades-2022-10-05.zip
# https://static.okx.com/cdn/okex/traderecords/trades/daily/20220408/ALPHA-USDT-trades-2022-04-08.zip

URLS = {
    ExchangeType.BINANCE: {
        AssetType.SPOT: "https://data.binance.vision/data/spot/daily/trades/{base}{quote}/{base}{quote}-trades-{year}-{month}-{day}.zip",
        AssetType.FUTURE: "https://data.binance.vision/data/futures/um/daily/trades/{base}{quote}{maturity}/{base}{quote}{maturity}-trades-{year}-{month}-{day}.zip",
    },
    ExchangeType.OKX: {
        AssetType.SPOT: "https://static.okx.com/cdn/okex/traderecords/trades/daily/{year}{month}{day}/{base}-{quote}-trades-{year}-{month}-{day}.zip",
        AssetType.FUTURE: "https://static.okx.com/cdn/okex/traderecords/trades/daily/{year}{month}{day}/{base}-{quote}{maturity}trades-{year}-{month}-{day}.zip",
    },
}


async def download(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
) -> None:
    loop = asyncio.get_event_loop()
    all_requests = []

    for trading_pair in basket:
        base_url = URLS[trading_pair.exchange][trading_pair.asset_type]
        for date in dates:
            if not overwrite and storage.exists(
                data_segment=DataSegment.RAW_TRADES,
                trading_pair=trading_pair,
                date=date,
                is_reading=False,
            ):
                continue
            url = base_url.format(
                base=trading_pair.base_asset,
                quote=trading_pair.quote_asset,
                year=date[:4],
                month=date[4:6],
                day=date[6:],
                maturity=f"_{trading_pair.maturity.exchange_name}"
                if trading_pair.maturity
                and trading_pair.maturity.exchange_name is not None
                else "",
            )
            new_request = loop.run_in_executor(
                None,
                lambda url, trading_pair: (requests.get(url), trading_pair),
                url,
                trading_pair,
            )
            all_requests.append(new_request)

    responses = [await request for request in all_requests]
    for response, trading_pair in responses:
        if response.status_code == 200:
            filename = response.url.split("/")[-1]
            # extract date and trading_pair
            date = "".join(filename.split(".")[0].split("-")[-3:])
            trading_pair_str = filename.split("-")[0]
            assert trading_pair_str == trading_pair.exchange_name
            extension = filename.split(".")[1]
            assert extension == "zip"
            storage.save(
                response.content,
                data_segment=DataSegment.RAW_TRADES,
                trading_pair=trading_pair,
                date=date,
            )
            print(f"{trading_pair.full_name} {date} saved.")
        else:
            print(f"Error fetching {response.url}: {response.status_code}")
