import psycopg2
from config import DB_CONFIG

def load_patients(df):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SET search_path TO clinical")
    
    inserted = 0
    skipped = 0
    
    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO dim_patient 
                    (mrn, first_name, last_name, dob, sex, race, zip_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (mrn) DO NOTHING
            """, (
                row["mrn"], row["first_name"], row["last_name"],
                row["dob"], row["sex"], row["race"], row["zip_code"]
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipping row {row['mrn']}: {e}")
            skipped += 1
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {inserted} patients, skipped {skipped}")

def load_encounters(df):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SET search_path TO clinical")

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            cur.execute("""
                SELECT patient_id FROM dim_patient WHERE mrn = %s
            """, (row["mrn"],))
            result = cur.fetchone()
            if result is None:
                print(f"No patient found for MRN {row['mrn']}, skipping")
                skipped += 1
                continue

            patient_id = result[0]
            cur.execute("""
                INSERT INTO fact_encounter
                    (patient_id, admit_dt, discharge_dt, enc_type, chief_complaint, disposition, total_charges)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                patient_id, row["admit_dt"], row["discharge_dt"],
                row["enc_type"], row["chief_complaint"],
                row["disposition"], row["total_charges"]
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipping row: {e}")
            skipped += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {inserted} encounters, skipped {skipped}")