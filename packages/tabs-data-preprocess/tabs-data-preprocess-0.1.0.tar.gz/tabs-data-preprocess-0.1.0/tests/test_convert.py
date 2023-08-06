# import zipfile
#
# import numpy as np
# import xarray as xr
#
# from tabs_data_preprocess.convert_to_h5 import convert_file
#
#
# def test_convert_file(tmpdir):
#     # Create a sample CSV file and compress it with ZIP
#     csv_path = tmpdir.join("sample.csv.zip")
#     with zipfile.ZipFile(csv_path, "w") as zip_file:
#         zip_file.writestr("sample.csv", "col1,col2\n1,2\n3,4\n")
#
#     # Create a sample NetCDF file
#     nc_path = tmpdir.join("output.nc")
#
#     # Test the convert_file function
#     header = ["col1", "col2"]
#     convert_file(str(csv_path), str(nc_path), header)
#
#     # Check that the output file was created
#     assert nc_path.exists()
#
#     # Open the output file and check that it contains the expected data
#     with xr.open_dataset(nc_path) as ds:
#         assert "col1" in ds
#         assert "col2" in ds
#         np.testing.assert_array_equal(ds["col1"].values, [1, 3])
#         np.testing.assert_array_equal(ds["col2"].values, [2, 4])
