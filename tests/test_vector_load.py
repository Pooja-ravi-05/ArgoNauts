import pandas as pd
from src.ai_backend.vector_loader import load_metadata

# Example small dataframe (or fetch from PostgreSQL)
df = pd.DataFrame({
    'float_id': ['2902754', '2902755'],
    'latitude': [10.5, 11.0],
    'longitude': [72.0, 72.5],
    'temperature': [28.5, 28.7],
    'salinity': [34.5, 34.6],
    'date': ['2023-01-01', '2023-01-02']
})

load_metadata(df)
