from extract.read_azure import read_blob_csv
from extract.read_csv import read_patients_csv, read_encounters_csv
from transform.clean_patients import clean_patients, clean_encounters
from load.load_postgres import load_patients, load_encounters

def run(source="local"):
    print(f"--- EXTRACT ({source}) ---")
    if source == "azure":
        patients_df = read_blob_csv("patients.csv")
        encounters_df = read_blob_csv("encounters.csv")
    else:
        patients_df = read_patients_csv()
        encounters_df = read_encounters_csv()

    print("--- TRANSFORM ---")
    patients_df = clean_patients(patients_df)
    encounters_df = clean_encounters(encounters_df)

    print("--- LOAD ---")
    load_patients(patients_df)
    load_encounters(encounters_df)

    print("--- DONE ---")

if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else "local"
    run(source)