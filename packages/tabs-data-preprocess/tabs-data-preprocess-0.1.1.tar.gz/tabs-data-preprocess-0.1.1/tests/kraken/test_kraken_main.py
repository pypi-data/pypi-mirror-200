# import xarray as xr
#
# from tabs_data_preprocess.kraken.kraken_main import Kraken
#
#
# def test__download():
#     symbol = "PI_XBTUSD"
#     url = "https://futures.kraken.com/derivatives/api/v3/history"
#     url = "https://futures.kraken.com/api/history/v2/executions"
#     date = "20230103"
#     test = Kraken._download(
#         symbol,
#         date,
#         url,
#     )
#     assert False
#
#
# def test__process_json():
#     # got directly from the kraken api
#     records = [
#         {
#             "uid": "18fed591-35f4-4464-9577-6712f6b5236c",
#             "timestamp": 1672707582961,
#             "event": {
#                 "Execution": {
#                     "execution": {
#                         "uid": "0e95b7ee-1e64-42f0-a009-abae651dad24",
#                         "makerOrder": {
#                             "uid": "359ce3f0-f87d-4f52-a70d-4b14ada22207",
#                             "tradeable": "PI_XBTUSD",
#                             "direction": "Buy",
#                             "quantity": "5.0",
#                             "timestamp": 1672707480578,
#                             "limitPrice": "16689.5",
#                             "orderType": "Post",
#                             "reduceOnly": False,
#                             "lastUpdateTimestamp": 1672707582961,
#                         },
#                         "takerOrder": {
#                             "uid": "9d36864a-f9b9-4675-a955-7083b16fc919",
#                             "tradeable": "PI_XBTUSD",
#                             "direction": "Sell",
#                             "quantity": "5",
#                             "timestamp": 1672707582961,
#                             "limitPrice": "16689.5000000000",
#                             "orderType": "IoC",
#                             "reduceOnly": False,
#                             "lastUpdateTimestamp": 1672707582961,
#                         },
#                         "timestamp": 1672707582961,
#                         "quantity": "5.0",
#                         "price": "16689.5",
#                         "markPrice": "16689.64469073068",
#                         "limitFilled": True,
#                         "usdValue": "5.00",
#                     },
#                     "takerReducedQuantity": "",
#                 }
#             },
#         },
#         {
#             "uid": "b721aca4-1bdc-473e-bd6d-9c1468d01cc7",
#             "timestamp": 1672707582961,
#             "event": {
#                 "Execution": {
#                     "execution": {
#                         "uid": "3b212433-04aa-4eff-a168-861b4638231e",
#                         "makerOrder": {
#                             "uid": "359ce3f0-f87d-4f52-a70d-4b14ada22207",
#                             "tradeable": "PI_XBTUSD",
#                             "direction": "Buy",
#                             "quantity": "105.0",
#                             "timestamp": 1672707480578,
#                             "limitPrice": "16689.5",
#                             "orderType": "Post",
#                             "reduceOnly": False,
#                             "lastUpdateTimestamp": 1672707480578,
#                         },
#                         "takerOrder": {
#                             "uid": "b1d6ccad-7e2b-4799-a9ca-3219777e222a",
#                             "tradeable": "PI_XBTUSD",
#                             "direction": "Sell",
#                             "quantity": "100",
#                             "timestamp": 1672707582961,
#                             "limitPrice": "16689.5000000000",
#                             "orderType": "IoC",
#                             "reduceOnly": False,
#                             "lastUpdateTimestamp": 1672707582961,
#                         },
#                         "timestamp": 1672707582961,
#                         "quantity": "100",
#                         "price": "16689.5",
#                         "markPrice": "16689.64469073068",
#                         "limitFilled": False,
#                         "usdValue": "100.00",
#                     },
#                     "takerReducedQuantity": "",
#                 }
#             },
#         },
#     ]
#     expected = [
#         {
#             "timestamp": 1672707582961,
#             "quantity": "5.0",
#             "price": "16689.5",
#             "markPrice": "16689.64469073068",
#             "limitFilled": True,
#             "usdValue": "5.00",
#             "tradeable_maker": "PI_XBTUSD",
#             "direction_maker": "Buy",
#             "quantity_maker": "5.0",
#             "timestamp_maker": 1672707480578,
#             "limitPrice_maker": "16689.5",
#             "orderType_maker": "Post",
#             "reduceOnly_maker": False,
#             "lastUpdateTimestamp_maker": 1672707582961,
#             "tradeable_taker": "PI_XBTUSD",
#             "direction_taker": "Sell",
#             "quantity_taker": "5",
#             "timestamp_taker": 1672707582961,
#             "limitPrice_taker": "16689.5000000000",
#             "orderType_taker": "IoC",
#             "reduceOnly_taker": False,
#             "lastUpdateTimestamp_taker": 1672707582961,
#         },
#         {
#             "timestamp": 1672707582961,
#             "quantity": "100",
#             "price": "16689.5",
#             "markPrice": "16689.64469073068",
#             "limitFilled": False,
#             "usdValue": "100.00",
#             "tradeable_maker": "PI_XBTUSD",
#             "direction_maker": "Buy",
#             "quantity_maker": "105.0",
#             "timestamp_maker": 1672707480578,
#             "limitPrice_maker": "16689.5",
#             "orderType_maker": "Post",
#             "reduceOnly_maker": False,
#             "lastUpdateTimestamp_maker": 1672707480578,
#             "tradeable_taker": "PI_XBTUSD",
#             "direction_taker": "Sell",
#             "quantity_taker": "100",
#             "timestamp_taker": 1672707582961,
#             "limitPrice_taker": "16689.5000000000",
#             "orderType_taker": "IoC",
#             "reduceOnly_taker": False,
#             "lastUpdateTimestamp_taker": 1672707582961,
#         },
#     ]
#     processed_record = Kraken._process_json(records)
#     assert processed_record == expected
#
#
# def test__to_dataset():
#     records = [
#         {
#             "timestamp": 1672707582961,
#             "quantity": "5.0",
#         },
#         {
#             "timestamp": 1672707582961,
#             "quantity": "100",
#         },
#     ]
#     ds = Kraken._to_dataset(records)
#     expected = {
#         "coords": {"index": {"dims": ("index",), "attrs": {}, "data": [0, 1]}},
#         "attrs": {},
#         "dims": {"index": 2},
#         "data_vars": {
#             "timestamp": {
#                 "dims": ("index",),
#                 "attrs": {},
#                 "data": [1672707582961, 1672707582961],
#             },
#             "quantity": {"dims": ("index",), "attrs": {}, "data": ["5.0", "100"]},
#         },
#     }
#     assert ds == xr.Dataset.from_dict(expected)
