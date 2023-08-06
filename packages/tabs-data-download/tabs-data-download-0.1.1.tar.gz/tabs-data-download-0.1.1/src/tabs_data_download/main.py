import argparse
import asyncio

import yaml
from immutables import Map
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_storage.storage import Storage
from tabs_type.version import VersionManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", type=str, help="Can be local, hdd or google")
    parser.add_argument(
        "--storage-settings-path", type=str, help="Path to the storage settings to use"
    )
    parser.add_argument(
        "--download-settings-path",
        type=str,
        help="Path to the download settings to use",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing data"
    )
    parser.add_argument(
        "--n-jobs", required=False, type=int, help="Number of cpus to use"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--book", action="store_true", help="Download book data")
    group.add_argument("--trade", action="store_true", help="Download trade data")
    group.add_argument("--ticker", action="store_true", help="Download ticker data")

    args = parser.parse_args()
    version = VersionManager.get_version(__name__.split(".")[0])

    # load storage and rolling learn config
    with open(args.storage_settings_path, "r") as f:
        storage_settings = yaml.safe_load(f)
    with open(args.download_settings_path, "r") as f:
        data_download_settings = yaml.safe_load(f)

    storage = Storage.from_settings(
        args.home,
        storage_settings,
        writing_version=version,
        reading_versions=Map(
            {
                DataSegment.RAW_TRADES: version,
                DataSegment.RAW_PRICE_LEVEL_BOOK: version,
            }
        ),
    )
    basket = Basket.from_yaml(data_download_settings["basket"])

    if args.book:
        from tabs_data_download.book import download

        asyncio.run(download(basket, data_download_settings, storage))

    elif args.trade:
        from tabs_data_download.trade import download

        download(basket, data_download_settings, storage, args.overwrite, args.n_jobs)

    else:
        from tabs_data_download.ticker import print_tickers

        print_tickers(basket)
        print_tickers(basket)
