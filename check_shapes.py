import netCDF4 as nc

file_path = 'data/raw/nodc_D1900975_339.nc'
ds = nc.Dataset(file_path)

variables = ['temp', 'psal', 'pres', 'latitude', 'longitude', 'juld', 'platform_number', 'cycle_number']

for var in variables:
    data = ds.variables[var][:]
    print(f"{var}: shape = {data.shape}")
