# import json
# from datetime import datetime

# import pytest

# from tabs_data_preprocess.kraken.facilities.futures_cfWebSocketApiV1 import (
#     CfWebSocketMethods,
# )


# @pytest.fixture
# def sample_json():
#     # create a sample JSON message
#     return {
#         "feed": "book_snapshot",
#         "product_id": "BTC-USD",
#         "timestamp": 1645424295000,
#         "bids": [
#             ["49500.0", "0.05", 1],
#             ["49495.5", "0.11", 1],
#             ["49488.5", "0.5", 1],
#             ["49482.5", "0.56", 1],
#             ["49476.5", "0.01", 1],
#         ],
#         "asks": [
#             ["49515.0", "0.57", 1],
#             ["49515.5", "0.6", 1],
#             ["49516.0", "0.36", 1],
#             ["49516.5", "0.05", 1],
#             ["49517.0", "0.02", 1],
#         ],
#     }


# def test_store_with_book_snapshot_message(sample_json, tmp_path):
#     # call the store method with a book_snapshot message
#     CfWebSocketMethods.store(sample_json, tmp_path)

#     # check that the output file was created and contains the message
#     symbol = sample_json["product_id"]
#     date = datetime.fromtimestamp(sample_json["timestamp"] / 1000).strftime("%Y%m%d")
#     output_abs_path = tmp_path / "kraken" / "futures" / symbol / f"{date}.json"
#     assert output_abs_path.is_file()
#     with open(output_abs_path) as f:
#         assert json.load(f) == sample_json

#     MILLISECONDS_PER_DAY = 24 * 3600 * 1000
#     sample_json["timestamp"] += MILLISECONDS_PER_DAY

#     # call the store method with a book_snapshot message
#     CfWebSocketMethods.store(sample_json, tmp_path)

#     # check that the output file was created and contains the message
#     symbol = sample_json["product_id"]
#     date = datetime.fromtimestamp(sample_json["timestamp"] / 1000).strftime("%Y%m%d")
#     output_abs_path = tmp_path / "kraken" / "futures" / symbol / f"{date}.json"
#     assert output_abs_path.is_file()
#     with open(output_abs_path) as f:
#         assert json.load(f) == sample_json
