import numpy as np
import xarray as xr
from joblib import Parallel, delayed
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.trading_pair import TradingPair
from tabs_storage.storage import Storage


def process_compression(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int | None = 1,
):
    tasks = []
    for trading_pair in basket:
        for date in dates:
            if not overwrite and storage.exists(
                DataSegment.COMPRESSED_PRICE_LEVEL_BOOK,
                date,
                is_reading=False,
                trading_pair=trading_pair,
            ):
                continue

            if storage.exists(
                DataSegment.RAW_PRICE_LEVEL_BOOK,
                date,
                is_reading=True,
                trading_pair=trading_pair,
            ):
                task = (trading_pair, date, storage)
                tasks.append(task)
    Parallel(n_jobs=n_jobs)(delayed(_process_compression_date)(*task) for task in tasks)


def _process_compression_date(
    trading_pair: TradingPair,
    date: str,
    storage: Storage,
) -> None:
    records = storage.load(DataSegment.RAW_PRICE_LEVEL_BOOK, date, trading_pair)
    storage.save(records, DataSegment.COMPRESSED_PRICE_LEVEL_BOOK, date, trading_pair)
    print("Compression done for", trading_pair.full_name, date, "...")


def process_dataset(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int | None = 1,
):
    tasks = []
    for trading_pair in basket:
        for date in dates:
            if not overwrite and storage.exists(
                DataSegment.PRICE_LEVEL_BOOK,
                date,
                is_reading=False,
                trading_pair=trading_pair,
            ):
                continue

            if storage.exists(
                DataSegment.COMPRESSED_PRICE_LEVEL_BOOK,
                date,
                is_reading=True,
                trading_pair=trading_pair,
            ):
                task = (trading_pair, date, storage)
                tasks.append(task)
    Parallel(n_jobs=n_jobs)(delayed(_process_dataset_date)(*task) for task in tasks)


def _process_dataset_date(
    trading_pair: TradingPair,
    date: str,
    storage: Storage,
) -> None:
    records = storage.load(
        DataSegment.COMPRESSED_PRICE_LEVEL_BOOK,
        date,
        trading_pair,
    )
    ds = _process_dataset_date_logic(records)
    storage.save(ds, DataSegment.PRICE_LEVEL_BOOK, date, trading_pair)
    print("Dataset done for", trading_pair.full_name, date, "...")


def _process_dataset_date_logic(
    records: list[dict[str, list[tuple[float, float]]]]
) -> xr.Dataset:
    # create empty numpy arrays to store price, quantity, and timestamp
    n_records = len(records)
    n_levels = max((len(r["bids"]) for r in records))
    price_array = np.nan * np.empty((n_records, 2, n_levels))
    quantity_array = np.nan * np.empty((n_records, 2, n_levels))
    timestamp_array = np.empty((n_records,), dtype=np.int64)

    # iterate through the records and fill the numpy arrays
    for i_record, record in enumerate(records):
        timestamp_array[i_record] = int(record["timestamp"]) * 10**6
        for i_side, side in enumerate(["bid", "ask"]):
            for level, (price, quantity) in enumerate(record[side + "s"]):
                price_array[i_record, i_side, level] = price
                quantity_array[i_record, i_side, level] = quantity
            if side == "bid":
                # ensure prices are sorted in descending order
                sort_idx = np.argsort(price_array[i_record, i_side, :])[::-1]
                price_array[i_record, i_side, :] = price_array[
                    i_record, i_side, sort_idx
                ]
                quantity_array[i_record, i_side, :] = quantity_array[
                    i_record, i_side, sort_idx
                ]
            else:
                # ensure prices are sorted in ascending order
                sort_idx = np.argsort(price_array[i_record, i_side, :])
                price_array[i_record, i_side, :] = price_array[
                    i_record, i_side, sort_idx
                ]
                quantity_array[i_record, i_side, :] = quantity_array[
                    i_record, i_side, sort_idx
                ]

    # create an xarray dataset from the numpy arrays
    ds = xr.Dataset(
        {
            "price": (["index", "side", "level"], price_array),
            "quantity": (["index", "side", "level"], quantity_array),
            "timestamp": (["index"], timestamp_array),
        },
        coords={"side": ["bid", "ask"]},
    )

    # not valid checks since we are using nan values to fill empty levels
    # # Check if the ask prices are sorted in ascending order,
    # # and the bid prices are sorted in descending order
    # assert np.all(np.diff(ds.price.sel(side="ask").values, axis=-1) >= 0)
    # assert np.all(np.diff(ds.price.sel(side="bid").values, axis=-1) <= 0)

    # for var_name in ds.data_vars:
    #     assert not ds[var_name].isnull().any().any()

    return ds


def process(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int | None = 1,
):
    # first compress existing raw files
    process_compression(basket, dates, storage, overwrite, n_jobs)
    # then build the xr.Dataset
    process_dataset(basket, dates, storage, overwrite, n_jobs)
