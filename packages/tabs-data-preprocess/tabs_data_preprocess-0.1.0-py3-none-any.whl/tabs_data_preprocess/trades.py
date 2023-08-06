import polars as pl
import xarray as xr
from joblib import Parallel, delayed
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.exchange_type import ExchangeType
from tabs_settings.config.trading_pair import TradingPair
from tabs_storage.storage import Storage

COLUMNS = {
    (ExchangeType.BINANCE, AssetType.SPOT): [
        "trade_id",
        "price",
        "quantity",
        "quote_quantity",
        "timestamp",
        "is_buyer_maker",
        "is_best_match",
    ],
    # (ExchangeType.BINANCE, AssetType.FUTURE): [
    #     "id",
    #     "price",
    #     "quantity",
    #     "quote_quantity",
    #     "timestamp",
    #     "is_buyer_maker",
    # ],
    (ExchangeType.KRAKEN, AssetType.SPOT): [
        "price",
        "quantity",
        "timestamp",
        "aggressive_direction",
        "order_type",
        "unused",
        "order_id",
    ],
    (ExchangeType.KRAKEN, AssetType.FUTURE): [
        "price",
        "quantity",
        "timestamp",
        "aggressive_direction",
        "order_type",
        "unused",
        "order_id",
    ],
}

FINAL_COLUMNS = {
    "price",
    "base_quantity",
    "timestamp",
    "is_buyer_maker",
}
# timestamp are always given in nanoseconds


def process(
    basket: Basket,
    dates: tuple[str],
    storage: Storage,
    overwrite: bool = False,
    n_jobs: int | None = 1,
):
    tasks = []
    for trading_pair in basket:
        for date in dates:
            if storage.exists(
                DataSegment.RAW_TRADES,
                date,
                is_reading=True,
                trading_pair=trading_pair,
            ):
                if not overwrite and storage.exists(
                    DataSegment.TRADES,
                    date,
                    is_reading=False,
                    trading_pair=trading_pair,
                ):
                    continue
                task = (trading_pair, date, storage)
                tasks.append(task)
            else:
                print(f"skip {trading_pair.full_name} {date}")
    Parallel(n_jobs=n_jobs)(delayed(_process_date)(*task) for task in tasks)


def _process_json_future(records):
    processed_records = []
    for record in records:
        execution = record["event"]["Execution"]["execution"]

        execution_formatted = {
            k: v
            for k, v in execution.items()
            if k not in {"makerOrder", "takerOrder", "uid", "oldTakerOrder"}
        }
        maker = {
            f"{k}_maker": v for k, v in execution["makerOrder"].items() if k != "uid"
        }
        taker = {
            f"{k}_taker": v for k, v in execution["takerOrder"].items() if k != "uid"
        }

        processed_record = {**execution_formatted, **maker, **taker}
        processed_records.append(processed_record)

    return processed_records


def _process_date(
    trading_pair: TradingPair,
    date: str,
    storage: Storage,
) -> None:
    # set the column names based on exchange and asset type
    data = storage.load(
        DataSegment.RAW_TRADES,
        date,
        trading_pair,
    )

    if len(data) == 0:
        print(f"empty {trading_pair} {date}")
        return

    # to pandas and header
    if trading_pair.exchange is ExchangeType.BINANCE:
        df = data
        if trading_pair.asset_type is AssetType.SPOT:
            df.columns = COLUMNS[(ExchangeType.BINANCE, AssetType.SPOT)]

    elif trading_pair.exchange is ExchangeType.KRAKEN:
        if trading_pair.asset_type is AssetType.SPOT:
            df = pl.DataFrame(data)
            df.columns = COLUMNS[(ExchangeType.KRAKEN, trading_pair.asset_type)]
        else:
            df = pl.DataFrame(_process_json_future(data))

    df = df.lazy()

    # normalization
    if trading_pair.exchange is ExchangeType.BINANCE:
        if trading_pair.asset_type is AssetType.SPOT:
            df = (
                df.drop(["is_best_match", "trade_id"])
                .rename({"quantity": "base_quantity"})
                .drop("quote_quantity")
            )

        elif trading_pair.asset_type is AssetType.FUTURE:
            df = df.drop(["id", "quote_qty"]).rename(
                {
                    "qty": "base_quantity",
                    "time": "timestamp",
                }
            )
        df = df.with_columns(
            (pl.col("timestamp") * 10**6).cast(pl.Int64).alias("timestamp")
        )

    elif trading_pair.exchange is ExchangeType.KRAKEN:
        if trading_pair.asset_type is AssetType.SPOT:
            df = (
                df.with_columns(
                    pl.when(pl.col("aggressive_direction") == "b")
                    .then(pl.lit(True))
                    .otherwise(pl.lit(False))
                    .alias("is_buyer_maker")
                )
                .drop("aggressive_direction")
                .drop(["order_type", "unused", "order_id"])
                .with_columns(
                    (pl.col("timestamp") * 10**9).cast(pl.Int64).alias("timestamp")
                )
                .with_columns(pl.col("price").cast(pl.Float64).alias("price"))
                .with_columns(
                    pl.col("quantity").cast(pl.Float64).alias("base_quantity")
                )
                .drop("quantity")
            )

        elif trading_pair.asset_type is AssetType.FUTURE:
            df = (
                df.rename({"quantity": "base_quantity"})
                .with_columns(
                    (pl.col("direction_maker") == "Buy").alias("is_buyer_maker")
                )
                .with_columns(
                    (pl.col("timestamp") * 10**6).cast(pl.Int64).alias("timestamp")
                )
                .with_columns(
                    [
                        pl.col("price").cast(pl.Float64).alias("price"),
                        pl.col("base_quantity").cast(pl.Float64).alias("base_quantity"),
                    ]
                )
                .select(FINAL_COLUMNS)
            )

    df = df.collect()
    assert set(df.columns) == FINAL_COLUMNS

    # add missing columns with default values
    ds = xr.Dataset.from_dataframe(df.to_pandas())
    storage.save(ds, DataSegment.TRADES, date, trading_pair)
