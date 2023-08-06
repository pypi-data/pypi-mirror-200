from __future__ import annotations

from datetime import datetime, timezone

from joblib import Parallel, delayed
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.trading_pair import TradingPair
from tabs_storage.storage import Storage

from tabs_data_download.kraken.facilities.cfRestApiV3 import cfApiMethods

FUTURE_API_PATH = "https://futures.kraken.com"
SPOT_API_PATH = "https://api.kraken.com"

MILLESECONDS_SECONDS_PER_DAY = 24 * 3600 * 10**3


def download(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int = 1,
) -> None:
    tasks = []
    for trading_pair in basket:
        for date in dates:
            if not overwrite and storage.exists(
                trading_pair=trading_pair,
                data_segment=DataSegment.RAW_TRADES,
                date=date,
                is_reading=False,
            ):
                continue
            task = (trading_pair, date, storage)
            tasks.append(task)
    Parallel(n_jobs=n_jobs)(delayed(_download)(*task) for task in tasks)


def _download(
    trading_pair: TradingPair,
    date: str,
    storage: Storage,
) -> None:
    since = datetime.strptime(date, "%Y%m%d").replace(tzinfo=timezone.utc).timestamp()

    if trading_pair.asset_type is AssetType.FUTURE:
        api_path = FUTURE_API_PATH
        since = int(since) * 1000
        before = since + MILLESECONDS_SECONDS_PER_DAY - 1
    else:
        api_path = SPOT_API_PATH
        since = int(since)
        before = since + int(MILLESECONDS_SECONDS_PER_DAY / 1000) - 1

    timeout = 20
    checkCertificate = (
        True  # when using the test environment, this must be set to "False"
    )
    cfPublic = cfApiMethods(
        api_path, timeout=timeout, checkCertificate=checkCertificate
    )

    data = cfPublic.get_market_executions(
        trading_pair,
        since,
        before,
        sort="asc",
        limit=10**12,
    )
    storage.save(
        data,
        trading_pair=trading_pair,
        data_segment=DataSegment.RAW_TRADES,
        date=date,
    )
    print(f"Downloaded {trading_pair.full_name} {date}")
