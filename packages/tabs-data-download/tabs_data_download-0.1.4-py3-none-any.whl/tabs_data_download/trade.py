import asyncio
import datetime

from tabs_settings.config.basket import Basket
from tabs_settings.config.exchange_type import ExchangeType
from tabs_storage.storage import Storage


def get_dates(_from: str, to: str) -> tuple[str]:
    from_date = datetime.datetime.strptime(_from, "%Y%m%d")
    to_date = datetime.datetime.strptime(to, "%Y%m%d")
    dates = (
        (from_date + datetime.timedelta(days=i)).strftime("%Y%m%d")
        for i in range((to_date - from_date).days + 1)
    )
    return tuple(dates)


def download(
    basket: Basket,
    settings: dict,
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int = 1,
) -> None:
    dates = get_dates(str(settings["dates"]["from"]), str(settings["dates"]["to"]))

    # handle binance
    from tabs_data_download.binance.trades import download as _download

    asyncio.run(
        _download(
            frozenset(
                [
                    trading_pair
                    for trading_pair in basket
                    if trading_pair.exchange is ExchangeType.BINANCE
                ]
            ),
            dates,
            storage,
            overwrite,
        )
    )

    # handle kraken
    from tabs_data_download.kraken.trades import download as _download

    _download(
        frozenset(
            [
                trading_pair
                for trading_pair in basket
                if trading_pair.exchange is ExchangeType.KRAKEN
            ]
        ),
        dates,
        storage,
        overwrite,
        n_jobs,
    )
