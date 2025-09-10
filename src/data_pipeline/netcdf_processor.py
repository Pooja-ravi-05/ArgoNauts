import os
import numpy as np
import pandas as pd
import netCDF4 as nc

def process_netcdf(file_path):
    """
    Process a single NetCDF ARGO file and return a DataFrame
    """
    ds = nc.Dataset(file_path)
    
    # Measurement arrays (2D: profile x depth)
    temp = ds.variables['temp'][:]
    psal = ds.variables['psal'][:]
    pres = ds.variables['pres'][:]
    
    n_profiles, n_depths = temp.shape
    n_measurements = n_profiles * n_depths
    
    # Flatten measurement arrays
    temp_flat = temp.flatten()
    psal_flat = psal.flatten()
    pres_flat = pres.flatten()
    
    # Metadata arrays (1D per profile)
    latitude = ds.variables['latitude'][:]
    longitude = ds.variables['longitude'][:]
    juld = ds.variables['juld'][:]
    platform_number = ds.variables['platform_number'][:].flatten()
    cycle_number = ds.variables['cycle_number'][:].flatten()
    
    # Repeat metadata to match number of measurements
    latitude_flat = np.repeat(latitude, n_depths)
    longitude_flat = np.repeat(longitude, n_depths)
    juld_flat = np.repeat(juld, n_depths)
    
    float_id = np.repeat([f"{p}_{c}" for p, c in zip(platform_number, cycle_number)], n_depths)
    
    # Convert ARGO reference time
    reference_date = pd.to_datetime('1950-01-01')
    date_flat = reference_date + pd.to_timedelta(juld_flat, unit='D')
    
    # Build DataFrame
    df = pd.DataFrame({
        "float_id": float_id,
        "temperature": temp_flat,
        "salinity": psal_flat,
        "pressure": pres_flat,
        "latitude": latitude_flat,
        "longitude": longitude_flat,
        "time": date_flat
    })
    
    return df

def process_all_netcdfs(folder_path='data/raw/'):
    """
    Process all NetCDF files in a folder and return a single concatenated DataFrame
    """
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.nc')]
    
    df_list = []
    for f in all_files:
        print(f"Processing {f} ...")
        df = process_netcdf(f)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    print(f"All files processed. Total rows: {combined_df.shape[0]}")
    
    return combined_df
