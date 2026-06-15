# Databricks notebook source
# MAGIC %sql
# MAGIC -- Notebook 01: Zz patient spine
# MAGIC CREATE OR REPLACE TEMP VIEW zz_patients AS
# MAGIC SELECT
# MAGIC     PatientKey,
# MAGIC     DurableKey,
# MAGIC     Name,
# MAGIC     FirstName,
# MAGIC     LastName,
# MAGIC     BirthDate,
# MAGIC     Sex,
# MAGIC     PrimaryMrn,
# MAGIC     City,
# MAGIC     StateOrProvince,
# MAGIC     PostalCode,
# MAGIC     Status,
# MAGIC     IsCurrent
# MAGIC FROM clinical_prod.epic_caboodle_silver.s_patientdim
# MAGIC WHERE Test = 1
# MAGIC   AND IsCurrent = true
# MAGIC   AND _IsDeleted = 0;
# MAGIC
# MAGIC SELECT COUNT(*) FROM zz_patients;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW fact_encounter_summary AS
# MAGIC SELECT
# MAGIC     e.EncounterKey,
# MAGIC     e.PatientKey,
# MAGIC     p.BirthDate,
# MAGIC     DATEDIFF(to_date(e.Date), p.BirthDate) / 365.25 AS age_at_encounter,
# MAGIC     to_date(e.Date) AS contact_date,
# MAGIC     e.Type,
# MAGIC     e.DepartmentKey,
# MAGIC     e.ProviderKey,
# MAGIC     e.PrimaryDiagnosisKey,
# MAGIC     e.AppointmentSchedulingMode
# MAGIC FROM clinical_prod.epic_caboodle_silver.s_encounterfact e
# MAGIC JOIN zz_patients p ON e.PatientKey = p.PatientKey
# MAGIC WHERE e.Type IN (
# MAGIC     'Hospital Encounter',
# MAGIC     'Surgery',
# MAGIC     'Office Visit',
# MAGIC     'Appointment',
# MAGIC     'Treatment',
# MAGIC     'Multidisciplinary Visit',
# MAGIC     'Pre-Admission Testing',
# MAGIC     'Consult'
# MAGIC   );
# MAGIC
# MAGIC SELECT COUNT(*) FROM fact_encounter_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW fact_readmission AS
# MAGIC SELECT
# MAGIC     EncounterKey,
# MAGIC     PatientKey,
# MAGIC     contact_date,
# MAGIC     LAG(contact_date) OVER (PARTITION BY PatientKey ORDER BY contact_date) AS prev_encounter_date,
# MAGIC     DATEDIFF(
# MAGIC         contact_date,
# MAGIC         LAG(contact_date) OVER (PARTITION BY PatientKey ORDER BY contact_date)
# MAGIC     ) AS days_since_last_encounter,
# MAGIC     CASE
# MAGIC         WHEN DATEDIFF(
# MAGIC             contact_date,
# MAGIC             LAG(contact_date) OVER (PARTITION BY PatientKey ORDER BY contact_date)
# MAGIC         ) <= 30 THEN 1 ELSE 0
# MAGIC     END AS is_30day_readmit
# MAGIC FROM fact_encounter_summary;
# MAGIC
# MAGIC SELECT 
# MAGIC     COUNT(*) AS total_encounters,
# MAGIC     SUM(is_30day_readmit) AS readmits_30day,
# MAGIC     ROUND(SUM(is_30day_readmit) / COUNT(*) * 100, 1) AS readmit_rate_pct
# MAGIC FROM fact_readmission;