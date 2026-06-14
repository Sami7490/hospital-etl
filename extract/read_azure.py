from azure.storage.blob import BlobServiceClient
from config import AZURE_CONNECTION_STRING, AZURE_CONTAINER
import pandas as pd
import io

def read_blob_csv(filename):
    client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    blob = client.get_blob_client(container=AZURE_CONTAINER, blob=filename)
    data = blob.download_blob().readall()
    df = pd.read_csv(io.BytesIO(data))
    print(f"Loaded {len(df)} rows from Azure blob: {filename}")
    print(df.head())
    return df