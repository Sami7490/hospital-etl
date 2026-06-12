from extract.read_csv import read_patients_csv, read_encounters_csv
from transform.clean_patients import clean_patients, clean_encounters
from load.load_postgres import load_patients, load_encounters

def run():
    print("--- EXTRACT ---")
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
    run()