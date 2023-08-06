# import pytest
# from pathlib import Path
#
# import requests
# from requests.structures import CaseInsensitiveDict
#
# from tabs_data_preprocess.download import download_symbol
#
#
# @pytest.fixture
# def mock_response():
#     """Return a mock response object with the specified attributes."""
#     response = requests.Response()
#     return response
#
# #
# # @pytest.fixture
# # def mock_request(mocker, mock_response):
# #     """Return a mock request object that returns the specified response."""
# #     mock_get = mocker.patch("requests.get")
# #     mock_get.return_value = mock_response
# #     return mock_get
#
# @pytest.mark.parametrize(
#     "url_base, symbol, date_range, mock_response_params, expected_filenames",
#     [
#         (
#             "https://example.com",
#             "AAPL",
#             ["2022-01-01", "2022-01-02"],
#             {"status_code": 200, "content": b"content1",
# "headers": {"Content-Type": "application/zip"}},
#             ["AAPL-trades-2022-01-01.zip", "AAPL-trades-2022-01-02.zip"],
#         ),
#         (
#             "https://example.com",
#             "AAPL",
#             ["2022-01-01", "2022-01-02"],
#             {"status_code": 404, "content": b"", "headers": {}},
#             [],
#         ),
#         (
#             "https://example.com",
#             "AAPL",
#             ["2022-01-01", "2022-01-02"],
#             {"status_code": 200, "content": b"content1",
# "headers": {"Content-Type": "text/plain"}},
#             [],
#         ),
#     ],
# )
# def test_download_symbol(tmpdir,
#     url_base,
#     symbol,
#     date_range,
#     mock_response_params,
#     expected_filenames,
#     mocker,):
#     store_dir_name = tmpdir.mkdir("data").strpath
#
#     # Create a mock response object with the specified attributes
#     mock_response = mocker.MagicMock(spec=requests.Response)
#     mock_response.status_code = 200
#     mock_response.content = b"content1"
#     mock_response.headers = {"Content-Type": "application/zip"}
#
#     # Create a mock request object that returns the mock response
#     mock_get = mocker.patch("requests.get")
#     mock_get.return_value = mock_response
#
#     import asyncio
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(download_symbol(url_base, symbol, date_range, store_dir_name))
#
#     # Check that the mock request was called with the expected parameters
#     mock_get.assert_called_once()
#     request_url = mock_get.call_args[0][0]
#     assert request_url.startswith(url_base)
#     assert request_url.endswith(".zip")
#     assert symbol in request_url
#
#     # Check that the store directory was created
#     store_dir_name_path = Path(store_dir_name)
#     assert store_dir_name_path.exists()
#     assert store_dir_name_path.is_dir()
#
#     # Check that the expected files were stored
#     stored_filenames = [file.name for file in store_dir_name_path.glob("*")]
#     assert stored_filenames == expected_filenames
