import pandas as pd

def clean_patients(df):
    # drop rows with no MRN
    df = df.dropna(subset=["mrn"])
    
    # standardize sex values
    df["sex"] = df["sex"].str.strip().str.capitalize()
    
    # standardize race values
    df["race"] = df["race"].str.strip().str.title()
    
    # parse dob as date
    df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
    
    # drop rows where dob couldn't be parsed
    df = df.dropna(subset=["dob"])
    
    print(f"After cleaning: {len(df)} valid rows")
    return df


def clean_encounters(df):
    df = df.dropna(subset=["mrn"])
    df["admit_dt"] = pd.to_datetime(df["admit_dt"], errors="coerce")
    df["discharge_dt"] = pd.to_datetime(df["discharge_dt"], errors="coerce")
    df = df.dropna(subset=["admit_dt"])
    df["enc_type"] = df["enc_type"].str.strip().str.lower()
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce").fillna(0)
    print(f"After cleaning: {len(df)} valid encounter rows")
    return df