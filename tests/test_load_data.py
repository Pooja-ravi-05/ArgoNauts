from src.data_pipeline.netcdf_processor import process_all_netcdfs
from src.data_pipeline.database_loader import load_to_postgres

# Process all NetCDF files
df = process_all_netcdfs('data/raw/')

print("Sample of processed data:")
print(df.head())

# Load into PostgreSQL
load_to_postgres(df)
