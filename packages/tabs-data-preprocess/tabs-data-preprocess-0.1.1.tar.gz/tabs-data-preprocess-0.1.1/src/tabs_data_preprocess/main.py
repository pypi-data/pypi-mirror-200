import argparse
import datetime

import yaml
from immutables import Map
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_storage.storage import Storage
from tabs_type.version import VersionManager


def get_dates(_from: str, to: str) -> tuple[str]:
    from_date = datetime.datetime.strptime(_from, "%Y%m%d")
    to_date = datetime.datetime.strptime(to, "%Y%m%d")
    dates = (
        (from_date + datetime.timedelta(days=i)).strftime("%Y%m%d")
        for i in range((to_date - from_date).days + 1)
    )
    return tuple(dates)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", type=str, help="Can be local, hdd or google")
    parser.add_argument(
        "--storage-settings", type=str, help="Path to the storage settings to use"
    )
    parser.add_argument(
        "--download-settings",
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

    args = parser.parse_args()
    version = VersionManager.get_version(__name__.split(".")[0])
    data_download_version = VersionManager.get_version(
        "tabs-data-download".split(".")[0]
    )

    # load storage and rolling learn config
    with open(args.storage_settings, "r") as f:
        storage_settings = yaml.safe_load(f)
    with open(args.download_settings, "r") as f:
        data_download_settings = yaml.safe_load(f)

    storage = Storage.from_settings(
        args.home,
        storage_settings,
        writing_version=version,
        reading_versions=Map(
            {
                DataSegment.RAW_TRADES: data_download_version,
                DataSegment.RAW_PRICE_LEVEL_BOOK: data_download_version,
                DataSegment.TRADES: version,
                DataSegment.PRICE_LEVEL_BOOK: version,
                DataSegment.COMPRESSED_PRICE_LEVEL_BOOK: version,
            }
        ),
    )
    basket = Basket.from_yaml(data_download_settings["basket"])

    if args.book:
        from tabs_data_preprocess.book import process

        # in this case, dates are from date_from and date_to is yesterday
        dates = get_dates(
            str(data_download_settings["dates"]["from"]),
            (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"),
        )

        process(
            basket,
            dates,
            storage,
            args.overwrite,
            args.n_jobs,
        )

    else:
        from tabs_data_preprocess.trades import process

        dates = get_dates(
            str(data_download_settings["dates"]["from"]),
            str(data_download_settings["dates"]["to"]),
        )

        process(
            basket,
            dates,
            storage,
            args.overwrite,
            args.n_jobs,
        )
