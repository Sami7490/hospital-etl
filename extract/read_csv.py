import pandas as pd
import os
from config import RAW_DATA_DIR

def read_patients_csv(filename="patients.csv"):
    filepath = os.path.join(RAW_DATA_DIR, filename)
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filename}")
    print(df.head())
    return df

def read_encounters_csv(filename="encounters.csv"):
    filepath = os.path.join(RAW_DATA_DIR, filename)
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from {filename}")
    print(df.head())
    return df