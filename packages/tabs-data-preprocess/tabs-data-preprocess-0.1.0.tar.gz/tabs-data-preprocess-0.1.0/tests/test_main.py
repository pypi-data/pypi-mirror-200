# from datetime import datetime
#
# import pytest
#
# from tabs_data_preprocess.main import get_date_range
#
#
# @pytest.mark.parametrize(
#     "base_date, n_days, expected",
#     [
#         (datetime(2022, 1, 1, 0, 0, 0), 0, []),
#         (datetime(2022, 1, 1, 0, 0, 0), 1, ["2022-01-01"]),
#         (datetime(2022, 1, 1, 0, 0, 0), 2, ["2022-01-01", "2021-12-31"]),
#     ],
# )
# def test_get_date_range(base_date, n_days, expected):
#     assert get_date_range(base_date, n_days) == expected
