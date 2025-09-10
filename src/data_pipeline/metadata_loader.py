import chromadb
import pandas as pd

# Initialize Chroma client
client = chromadb.Client()
collection = client.create_collection("argo_metadata")

def load_metadata(df):
    """
    Store ARGO float metadata and simple summaries into ChromaDB.
    """
    for idx, row in df.iterrows():
        collection.add(
            ids=[str(row['float_id']) + "_" + str(idx)],
            metadatas=[{
                "float_id": row['float_id'],
                "latitude": row['latitude'],
                "longitude": row['longitude'],
                "date": str(row['time'])
            }],
            documents=[f"Temperature: {row['temperature']}, Salinity: {row['salinity']}, Pressure: {row['pressure']}"]
        )
    print("Metadata loaded into ChromaDB!")
