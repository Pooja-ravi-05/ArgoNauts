import chromadb
from chromadb.utils import embedding_functions
import pandas as pd

# Create Chroma client
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection("argo_metadata")

def load_metadata(df):
    """
    Load ARGO data metadata into Chroma vector database for RAG retrieval.
    """
    for idx, row in df.iterrows():
        collection.add(
            ids=[str(row['float_id']) + "_" + str(idx)],
            metadatas=[{
                "float_id": row['float_id'],
                "latitude": row['latitude'],
                "longitude": row['longitude'],
                "date": str(row['date'])
            }],
            documents=[f"Temperature: {row['temperature']}, Salinity: {row['salinity']}"]
        )
    print("Metadata loaded to Chroma!")
