import netCDF4 as nc
import numpy as np

# Open your NetCDF file
file_path = "/Users/nithyashree/Documents/floatchat-ai/data/raw/nodc_D1900975_339.nc"
ds = nc.Dataset(file_path)

# List of floats (profiles)
float_ids = ds.variables['float_serial_no'][:]
print("Float IDs:", float_ids)

# Get latitude, longitude
lat = ds.variables['latitude'][:]
lon = ds.variables['longitude'][:]
print("Latitudes:", lat)
print("Longitudes:", lon)

# Pick the first profile (index 0) as an example
profile_index = 0
temperature = ds.variables['temp'][profile_index, :]
salinity = ds.variables['psal'][profile_index, :]
pressure = ds.variables['pres'][profile_index, :]

print("Temperature:", temperature)
print("Salinity:", salinity)
print("Pressure:", pressure)
