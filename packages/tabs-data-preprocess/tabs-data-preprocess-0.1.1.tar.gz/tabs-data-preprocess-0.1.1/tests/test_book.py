import xarray as xr

from tabs_data_preprocess.book import _process_dataset_date_logic


def test_process_dataset_date_logic():
    # Create some dummy data for testing
    records = [
        {
            "timestamp": 1647468000,
            "bids": [[10.0, 20], [9.9, 30]],
            "asks": [[11.0, 25], [11.1, 35]],
        },
        {
            "timestamp": 1647468100,
            "bids": [[10.1, 40], [10.2, 50]],
            "asks": [[11.2, 45], [11.3, 55]],
        },
    ]

    # Run the function with the dummy data
    ds = _process_dataset_date_logic(records)
    expected_ds = xr.Dataset.from_dict(
        {
            "coords": {
                "side": {"dims": ("side",), "attrs": {}, "data": ["bid", "ask"]}
            },
            "attrs": {},
            "dims": {"index": 2, "side": 2, "level": 2},
            "data_vars": {
                "price": {
                    "dims": ("index", "side", "level"),
                    "attrs": {},
                    "data": [[[10.0, 9.9], [11.0, 11.1]], [[10.2, 10.1], [11.2, 11.3]]],
                },
                "quantity": {
                    "dims": ("index", "side", "level"),
                    "attrs": {},
                    "data": [
                        [[20.0, 30.0], [25.0, 35.0]],
                        [[50.0, 40.0], [45.0, 55.0]],
                    ],
                },
                "timestamp": {
                    "dims": ("index",),
                    "attrs": {},
                    "data": [1647468000000000, 1647468100000000],
                },
            },
        }
    )

    xr.testing.assert_equal(ds, expected_ds)
