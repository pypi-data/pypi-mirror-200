import asyncio
import datetime
import time

import ccxt.pro as ccxtpro
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.trading_pair import TradingPair
from tabs_storage.storage import Storage


async def _prune_book(book: dict, limit: int) -> dict:
    bids = book["bids"][:limit]
    asks = book["asks"][:limit]
    return {"bids": bids, "asks": asks, "timestamp": book["timestamp"]}


async def _dump_book(
    book: dict, trading_pair: TradingPair, storage: Storage, limit: int
) -> None:
    book = await _prune_book(book, limit)
    if book["timestamp"] is None:
        return
    timestamp = int(book["timestamp"])
    date = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime("%Y%m%d")
    storage.save(
        book,
        data_segment=DataSegment.RAW_PRICE_LEVEL_BOOK,
        date=date,
        trading_pair=trading_pair,
    )


async def _download(
    exchange: ExchangeType,
    asset_type: AssetType,
    basket: frozenset[TradingPair],
    book_settings: dict,
    storage: Storage,
) -> None:
    # Exchange details
    setting = {
        "enableRateLimit": True,
        "rateLimit": 500,
        "newUpdates": False,
    }
    if asset_type is AssetType.FUTURE:
        setting["options"] = {"defaultType": "future"}

    if str(exchange) in ccxtpro.exchanges:
        exchange = getattr(ccxtpro, str(exchange))(setting)
    else:
        print(f"{exchange} is not a supported exchange")

    # Watch order book for each symbol
    async def watch_order_book(trading_pair: TradingPair) -> None:
        while True:
            try:
                book = await exchange.watchOrderBook(
                    trading_pair.ccxt_name, limit=book_settings["limit"]
                )
                # add a t_capture as nanoseconds
                book["t_capture"] = time.time_ns()
                await _dump_book(book, trading_pair, storage, book_settings["limit"])
                # print(
                #     f"{asset_type} - {trading_pair.ccxt_name} - Bids:"
                #     f" {book['bids'][0]} - Asks: {book['asks'][0]}"
                # )
            except Exception as e:
                print(f"Error fetching order book for {trading_pair.full_name}: {e}")
            await asyncio.sleep(1)

    # Create a task for each symbol to watch its order book
    tasks = [
        asyncio.create_task(watch_order_book(trading_pair)) for trading_pair in basket
    ]

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


async def download(basket: Basket, settings: dict, storage: Storage) -> None:
    tasks = []
    # Create tasks for each group of trading pairs
    for exchange, asset_types in basket.as_grouped_dict.items():
        for asset_type, pairs in asset_types.items():
            tasks.append(
                _download(exchange, asset_type, pairs, settings["book"], storage)
            )

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
