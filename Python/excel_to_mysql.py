# ============================================================
# LRF PROJECT
# EXCEL → MYSQL USING SQLALCHEMY
# ============================================================

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
from pathlib import Path
import os

# ============================================================
# 1. EXCEL FILE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FILE = PROJECT_ROOT / "Data" / "LRF_Data_Validation.xlsx""



# ============================================================
# 2. MYSQL CONNECTION DETAILS
# ============================================================

user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD")

if not password:
    raise ValueError("MYSQL_PASSWORD environment variable is not set.")

pw = quote(password)

host = os.getenv("MYSQL_HOST", "localhost")
PORT = int(os.getenv("MYSQL_PORT", "3306"))
db = os.getenv("MYSQL_DATABASE", "LRF_Analytics")


# ============================================================
# 3. CREATE SQLALCHEMY ENGINE
# ============================================================

engine = create_engine(
    f"mysql+pymysql://{user}:{pw}@{host}:{PORT}/{db}"
)


# ============================================================
# 4. EXCEL SHEET → MYSQL TABLE MAPPING
# ============================================================

sheet_to_table = {

    # --------------------------------------------------------
    # TRANSACTION TABLES
    # --------------------------------------------------------

    "01_Heat_Transactions":
        "fact_heat",

    "02_Sample_Transactions":
        "fact_sample",

    "03_Adjustment_Transactions":
        "fact_adjustment",

    "04_ProcessEvent_Transactions":
        "fact_process_event",

    "05_Energy_Transactions":
        "fact_energy",

    "06_Temperature_Transactions":
        "fact_temperature",


    # --------------------------------------------------------
    # DIMENSION / SOURCE TABLES
    # --------------------------------------------------------

    "07_Dim_Grade_Source":
        "dim_grade",

    "08_Dim_Element_Source":
        "dim_element",

    "09_Dim_Material_Source":
        "dim_material",

    "10_Dim_Furnace_Source":
        "dim_furnace",

    "11_Dim_Ladle_Source":
        "dim_ladle",

    "12_Dim_Operator_Source":
        "dim_operator",

    "13_Dim_ProcessStage_Source":
        "dim_process_stage",

    "14_Dim_Date_Source":
        "dim_date",

    "15_Dim_Grade_Specification":
        "dim_grade_specification",

    "16_Dim_Grade_Spec_Long":
        "dim_grade_spec_long",

    "17_Dim_Temperature_Recipe":
        "dim_temperature_recipe",
}


# ============================================================
# 5. LOAD EXCEL SHEETS INTO MYSQL
# ============================================================

for sheet, table in sheet_to_table.items():

    print("\n" + "-" * 70)
    print(f"Reading Excel sheet: {sheet}")

    df = pd.read_excel(
        FILE,
        sheet_name=sheet
    )

    print(f"Rows found: {len(df)}")

    df.to_sql(
        table,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        f"Loaded successfully: "
        f"{sheet} → {table}"
    )


# ============================================================
# 6. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("LRF DATA LOADING COMPLETED")
print("=" * 70)
