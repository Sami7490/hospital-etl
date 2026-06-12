# Hospital ETL Pipeline

A Python ETL pipeline that extracts clinical data from CSV files, transforms and validates it, and loads it into a PostgreSQL data warehouse modeled after Epic Clarity/Caboodle schema patterns.

## Stack
- Python 3.13
- pandas
- psycopg2
- PostgreSQL 18

## Project Structure
- extract/ - CSV ingestion
- transform/ - data cleaning and validation
- load/ - PostgreSQL inserts
- pipeline.py - orchestrator

## Schema
Clinical schema with dim/fact tables: dim_patient, dim_department, dim_provider, fact_encounter, fact_diagnosis, fact_procedure

## Running the pipeline
python3 pipeline.py