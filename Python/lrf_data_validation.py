"""
LRF DATA VALIDATION
===================
This script validates the LRF transaction dataset against the rules
defined in the '19_Student_Validation_Rules' worksheet.

Structure:
    1. Setup and configuration
    2. Load source tables
    3. Helper functions
    4. Validation Rules R01–R26
    5. Validation summary
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 2. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FILE_PATH = PROJECT_ROOT / "Data" / "LRF_Data_Validation.xlsx"
pd.set_option("display.max_colwidth", None)


# ============================================================
# 3. LOAD WORKBOOK AND SOURCE TABLES
# ============================================================

excel_file = pd.ExcelFile(FILE_PATH)

print("=" * 70)
print("LRF DATA VALIDATION")
print("=" * 70)
print("\nAvailable Sheets:")
print(excel_file.sheet_names)

validation_rules = pd.read_excel(
    FILE_PATH,
    sheet_name="19_Student_Validation_Rules"
)

heat = pd.read_excel(FILE_PATH, sheet_name="01_Heat_Transactions")
sample = pd.read_excel(FILE_PATH, sheet_name="02_Sample_Transactions")
adjustment = pd.read_excel(FILE_PATH, sheet_name="03_Adjustment_Transactions")
process_event = pd.read_excel(FILE_PATH, sheet_name="04_ProcessEvent_Transactions")
energy = pd.read_excel(FILE_PATH, sheet_name="05_Energy_Transactions")
temperature = pd.read_excel(FILE_PATH, sheet_name="06_Temperature_Transactions")
grade_dim = pd.read_excel(FILE_PATH, sheet_name="07_Dim_Grade_Source")
grade_spec = pd.read_excel(FILE_PATH, sheet_name="15_Dim_Grade_Specification")

# Process stage sheet contains the detailed concurrency table
# starting from Excel row 12.

process_stage_raw = pd.read_excel(
    FILE_PATH,
    sheet_name="13_Dim_ProcessStage_Source",
    header=None
)

# Excel row 12 = pandas index 11
process_stage = process_stage_raw.iloc[11:].copy()

# Use the first row of the detailed table as column headers
process_stage.columns = process_stage.iloc[0]

# Remove the header row from the data
process_stage = process_stage.iloc[1:].reset_index(drop=True)

# Clean column names
process_stage.columns = (
    process_stage.columns.astype(str).str.strip()
)

print(process_stage.columns.tolist())

# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

validation_summary = []


def print_rule(rule_id):
    """Print a validation rule heading and its definition."""
    print("\n" + "=" * 70)
    print(f"{rule_id} - DATA VALIDATION")
    print("=" * 70)

    rule = validation_rules[
        validation_rules["RuleID"] == rule_id
    ]

    if not rule.empty:
        print(rule.to_string(index=False))


def add_result(rule_id, validation_name, invalid_records):
    """Store and print a validation result."""
    count = len(invalid_records)

    validation_summary.append({
        "RuleID": rule_id,
        "Validation": validation_name,
        "InvalidRecords": count
    })

    print(f"\n{validation_name}: {count}")


def clean_grade_spec_id(series):
    """Convert GradeSpecID values such as GS-101 into numeric IDs."""
    return (
        series.astype(str)
        .str.replace("GS-", "", regex=False)
        .astype(int)
    )


def find_invalid_sequence(df, group_column, sequence_column):
    """Check whether each group has a sequence of 1, 2, 3, ..."""
    invalid_groups = []

    for group_id, group in df.groupby(group_column):
        actual = sorted(group[sequence_column].tolist())
        expected = list(range(1, len(actual) + 1))

        if actual != expected:
            invalid_groups.append({
                group_column: group_id,
                "Actual": actual,
                "Expected": expected
            })

    return pd.DataFrame(invalid_groups)


# ============================================================
# R01 - PRIMARY KEY COMPLETENESS AND UNIQUENESS
# ============================================================

# ============================================================
# R01 - PRIMARY KEY VALIDATION
# ============================================================

print(
    validation_rules[
        validation_rules["RuleID"] == "R01"
    ].to_string(index=False)
)


# ------------------------------------------------------------
# R01.1 - HEAT TRANSACTIONS
# Validate HeatID for missing and duplicate values
# ------------------------------------------------------------

# Check missing HeatID values
missing_heat_ids = heat["HeatID"].isnull().sum()

# Check duplicate HeatID values
duplicate_heat_ids = heat["HeatID"].duplicated().sum()

# Get total number of rows
total_heat_rows = len(heat)

print("\n--- Heat Transactions Validation ---")
print("Total Rows:", total_heat_rows)
print("Missing HeatID:", missing_heat_ids)
print("Duplicate HeatID:", duplicate_heat_ids)


# ------------------------------------------------------------
# R01.2 - SAMPLE TRANSACTIONS
# Validate SampleID for missing and duplicate values
# ------------------------------------------------------------

# Check missing SampleID values
missing_sample_ids = sample["SampleID"].isnull().sum()

# Check duplicate SampleID values
duplicate_sample_ids = sample["SampleID"].duplicated().sum()

# Get total number of rows
total_sample_rows = len(sample)

print("\n--- Sample Transactions Validation ---")
print("Total Rows:", total_sample_rows)
print("Missing SampleID:", missing_sample_ids)
print("Duplicate SampleID:", duplicate_sample_ids)


# ------------------------------------------------------------
# R01.3 - ADJUSTMENT TRANSACTIONS
# Validate AdjustmentID for missing and duplicate values
# ------------------------------------------------------------

# Check missing AdjustmentID values
missing_adjustment_ids = adjustment["AdjustmentID"].isnull().sum()

# Check duplicate AdjustmentID values
duplicate_adjustment_ids = adjustment["AdjustmentID"].duplicated().sum()

# Get total number of rows
total_adjustment_rows = len(adjustment)

print("\n--- Adjustment Transactions Validation ---")
print("Total Rows:", total_adjustment_rows)
print("Missing AdjustmentID:", missing_adjustment_ids)
print("Duplicate AdjustmentID:", duplicate_adjustment_ids)


# ------------------------------------------------------------
# R01.4 - PROCESS EVENT TRANSACTIONS
# Validate EventID for missing and duplicate values
# ------------------------------------------------------------

# Check missing EventID values
missing_event_ids = process_event["EventID"].isnull().sum()

# Check duplicate EventID values
duplicate_event_ids = process_event["EventID"].duplicated().sum()

# Get total number of rows
total_event_rows = len(process_event)

print("\n--- Process Event Transactions Validation ---")
print("Total Rows:", total_event_rows)
print("Missing EventID:", missing_event_ids)
print("Duplicate EventID:", duplicate_event_ids)


# ------------------------------------------------------------
# R01.5 - ENERGY TRANSACTIONS
# Validate EnergyEventID for missing and duplicate values
# ------------------------------------------------------------

# Check missing EnergyEventID values
missing_energy_ids = energy["EnergyEventID"].isnull().sum()

# Check duplicate EnergyEventID values
duplicate_energy_ids = energy["EnergyEventID"].duplicated().sum()

# Get total number of rows
total_energy_rows = len(energy)

print("\n--- Energy Transactions Validation ---")
print("Total Rows:", total_energy_rows)
print("Missing EnergyEventID:", missing_energy_ids)
print("Duplicate EnergyEventID:", duplicate_energy_ids)


# ------------------------------------------------------------
# R01.6 - TEMPERATURE TRANSACTIONS
# Validate TemperatureEventID for missing and duplicate values
# ------------------------------------------------------------

# Check missing TemperatureEventID values
missing_temperature_ids = temperature["TemperatureEventID"].isnull().sum()

# Check duplicate TemperatureEventID values
duplicate_temperature_ids = (
    temperature["TemperatureEventID"].duplicated().sum()
)

# Get total number of rows
total_temperature_rows = len(temperature)

print("\n--- Temperature Transactions Validation ---")
print("Total Rows:", total_temperature_rows)
print("Missing TemperatureEventID:", missing_temperature_ids)
print("Duplicate TemperatureEventID:", duplicate_temperature_ids)


# ============================================================
# R02 - HEATID REFERENTIAL INTEGRITY
# ============================================================

print_rule("R02")

valid_heat_ids = set(heat["HeatID"].dropna())

heat_id_checks = [
    ("Sample", sample),
    ("Adjustment", adjustment),
    ("Process Event", process_event),
    ("Energy", energy),
    ("Temperature", temperature)
]

for table_name, df in heat_id_checks:
    invalid = df[
        ~df["HeatID"].isin(valid_heat_ids)
    ]

    add_result(
        "R02",
        f"{table_name} records with invalid HeatID",
        invalid
    )


# ============================================================
# R03 - GRADEID AND GRADE CONSISTENCY
# ============================================================

print_rule("R03")

grade_mapping = dict(
    zip(grade_dim["GradeID"], grade_dim["Grade"])
)

grade_checks = [
    ("Heat", heat),
    ("Sample", sample),
    ("Adjustment", adjustment),
    ("Process Event", process_event),
    ("Energy", energy),
    ("Temperature", temperature)
]

for table_name, df in grade_checks:
    expected_grade = df["GradeID"].map(grade_mapping)

    invalid = df[
        df["Grade"] != expected_grade
    ]

    add_result(
        "R03",
        f"{table_name} records with invalid Grade",
        invalid
    )


# ============================================================
# R04 - GRADE SPECIFICATION VALIDATION
# ============================================================

print_rule("R04")

elements = [
    "C", "SI", "S", "P", "MN", "NI", "CR", "CU",
    "MO", "NB", "B", "V", "TI", "AL", "PB", "CA"
]

invalid_spec_records = []

for element in elements:
    min_col = f"{element}_MIN"
    aim_col = f"{element}_AIM"
    max_col = f"{element}_MAX"

    invalid = grade_spec[
        ~(
            (grade_spec[min_col] <= grade_spec[aim_col]) &
            (grade_spec[aim_col] <= grade_spec[max_col])
        )
    ]

    if not invalid.empty:
        invalid_spec_records.append({
            "Element": element,
            "InvalidRecords": len(invalid)
        })

invalid_spec_df = pd.DataFrame(invalid_spec_records)

print("\nInvalid MIN <= AIM <= MAX records:")
print(invalid_spec_df)

valid_grade_spec_ids = set(grade_spec["ID"])

heat_spec_id = clean_grade_spec_id(heat["GradeSpecID"])
sample_spec_id = clean_grade_spec_id(sample["GradeSpecID"])

invalid_heat_spec = heat[
    ~heat_spec_id.isin(valid_grade_spec_ids)
]

invalid_sample_spec = sample[
    ~sample_spec_id.isin(valid_grade_spec_ids)
]

add_result(
    "R04",
    "Heat records with invalid GradeSpecID",
    invalid_heat_spec
)

add_result(
    "R04",
    "Sample records with invalid GradeSpecID",
    invalid_sample_spec
)


# ============================================================
# R05 - SAMPLE NUMBER SEQUENCE
# ============================================================

print_rule("R05")

invalid_sample_sequence = find_invalid_sequence(
    sample,
    "HeatID",
    "SampleNumber"
)

add_result(
    "R05",
    "Heats with invalid SampleNumber sequence",
    invalid_sample_sequence
)


# ============================================================
# R06 - SAMPLE TIMELINE VALIDATION
# ============================================================

print_rule("R06")

invalid_sample_time = sample[
    (sample["SampleRequestedTime"] > sample["SampleTakenTime"]) |
    (sample["SampleTakenTime"] > sample["LabResultTime"])
]

add_result(
    "R06",
    "Invalid sample timeline records",
    invalid_sample_time
)


# ============================================================
# R07 - SAMPLE WAITING TIME CALCULATION
# ============================================================

print_rule("R07")

expected_waiting_time = (
    sample["SampleTakenTime"] -
    sample["SampleRequestedTime"]
).dt.total_seconds() / 60

invalid_waiting_time = sample[
    ~np.isclose(
        sample["SampleWaitingTimeMin"],
        expected_waiting_time,
        rtol=1e-5,
        atol=0.01
    )
]

add_result(
    "R07",
    "Incorrect SampleWaitingTimeMin records",
    invalid_waiting_time
)


# ============================================================
# R08 - LAB ANALYSIS TIME CALCULATION
# ============================================================

print_rule("R08")

expected_lab_time = (
    sample["LabResultTime"] -
    sample["SampleTakenTime"]
).dt.total_seconds() / 60

invalid_lab_time = sample[
    ~np.isclose(
        sample["LabAnalysisTimeMin"],
        expected_lab_time,
        rtol=1e-5,
        atol=0.01
    )
]

add_result(
    "R08",
    "Incorrect LabAnalysisTimeMin records",
    invalid_lab_time
)


# ============================================================
# R09 - CHEMISTRY RANGE AND STATUS VALIDATION
# ============================================================

print_rule("R09")

chemistry_results = []

for element in elements:
    actual_col = f"{element}_Actual"
    min_col = f"{element}_MIN"
    max_col = f"{element}_MAX"
    status_col = f"{element}_Status"

    within_range = (
        (sample[actual_col] >= sample[min_col]) &
        (sample[actual_col] <= sample[max_col])
    )

    outside_range = sample[~within_range]

    expected_status = within_range.map({
        True: "PASS",
        False: "FAIL"
    })

    incorrect_status = sample[
        sample[status_col] != expected_status
    ]

    chemistry_results.append({
        "Element": element,
        "OutsideRange": len(outside_range),
        "IncorrectStatus": len(incorrect_status)
    })

    validation_summary.append({
        "RuleID": "R09",
        "Validation": f"{element} values outside specification",
        "InvalidRecords": len(outside_range)
    })

    validation_summary.append({
        "RuleID": "R09",
        "Validation": f"{element} incorrect status labels",
        "InvalidRecords": len(incorrect_status)
    })

chemistry_results = pd.DataFrame(chemistry_results)

print("\nChemistry Validation Results:")
print(chemistry_results.to_string(index=False))


# ============================================================
# R10 - OVERALL CHEMISTRY STATUS
# ============================================================

print_rule("R10")

status_columns = [
    f"{element}_Status"
    for element in elements
]

expected_overall_status = sample[status_columns].apply(
    lambda row: "PASS" if (row == "PASS").all() else "FAIL",
    axis=1
)

invalid_overall_status = sample[
    sample["OverallChemistryStatus"] != expected_overall_status
]

add_result(
    "R10",
    "Incorrect OverallChemistryStatus records",
    invalid_overall_status
)


# ============================================================
# R11 - ADJUSTMENT NUMBER SEQUENCE
# ============================================================

print_rule("R11")

invalid_adjustment_sequence = find_invalid_sequence(
    adjustment,
    "HeatID",
    "AdjustmentNumber"
)

add_result(
    "R11",
    "Heats with invalid AdjustmentNumber sequence",
    invalid_adjustment_sequence
)


# ============================================================
# R12 - REPEAT ADJUSTMENT FLAG
# ============================================================

print_rule("R12")

adjustment = adjustment.sort_values(
    ["HeatID", "AdjustmentNumber"]
).copy()

adjustment["ElementAdjustmentSequence"] = (
    adjustment
    .groupby(["HeatID", "ElementAdjusted"])
    .cumcount() + 1
)

expected_repeat_flag = adjustment[
    "ElementAdjustmentSequence"
].map(
    lambda value: "YES" if value > 1 else "NO"
)

invalid_repeat_flag = adjustment[
    adjustment["RepeatAdjustmentFlag"] != expected_repeat_flag
]

add_result(
    "R12",
    "Incorrect RepeatAdjustmentFlag records",
    invalid_repeat_flag
)


# ============================================================
# R13 - REPEAT ADJUSTMENT LOGIC
# ============================================================

print_rule("R13")

invalid_r13 = adjustment[
    (adjustment["RepeatAdjustmentFlag"] == "YES") &
    (adjustment["ElementAdjustmentSequence"] == 1)
]

add_result(
    "R13",
    "Invalid YES RepeatAdjustmentFlag records",
    invalid_r13
)


# ============================================================
# R14 - ADJUSTMENT REASON CONSISTENCY
# ============================================================

print_rule("R14")

reason_element = adjustment["Reason"].str.extract(
    r"Correct (\w+) deviation"
)[0]

invalid_adjustment_reason = adjustment[
    adjustment["ElementAdjusted"] != reason_element
]

add_result(
    "R14",
    "Invalid adjustment reason records",
    invalid_adjustment_reason
)


# ============================================================
# R15 - PROCESS EVENT SEQUENCE
# ============================================================

print_rule("R15")

invalid_event_sequence = find_invalid_sequence(
    process_event,
    "HeatID",
    "EventSequence"
)

add_result(
    "R15",
    "Heats with invalid EventSequence",
    invalid_event_sequence
)


# ============================================================
# R16 - PROCESS EVENT TIMELINE AND OVERLAP VALIDATION
# ============================================================
print_rule("R16")

process_stage_raw = pd.read_excel(
    excel_file,
    sheet_name="13_Dim_ProcessStage_Source",
    header=None
)

process_stage = process_stage_raw.iloc[11:].copy()
process_stage.columns = process_stage.iloc[0]
process_stage = process_stage.iloc[1:].reset_index(drop=True)

process_stage.columns = (
    process_stage.columns.astype(str).str.strip()
)

stage_category_map = (
    process_stage
    .set_index("ProcessStage")["EventCategory"]
    .to_dict()
)

process_merged = process_event.merge(
    process_stage[
        [
            "ProcessStageID",
            "EventCategory",
            "Concurrency",
            "Can Overlap With"
        ]
    ],
    on="ProcessStageID",
    how="left",
    suffixes=("", "_Dim")
)

process_merged["EventCategory"] = (
    process_merged["ProcessStage"].map(stage_category_map)
)

process_merged = process_merged.sort_values(
    ["HeatID", "EventSequence"]
).copy()

process_merged["PreviousStage"] = (
    process_merged.groupby("HeatID")["ProcessStage"].shift(1)
)

process_merged["PreviousCategory"] = (
    process_merged.groupby("HeatID")["EventCategory"].shift(1)
)

process_merged["PreviousEventEnd"] = (
    process_merged.groupby("HeatID")["EventEndDateTime"].shift(1)
)


def check_timeline(row):

    if pd.isna(row["PreviousEventEnd"]):
        return True

    if row["EventStartDateTime"] >= row["PreviousEventEnd"]:
        return True

    if pd.isna(row["Can Overlap With"]):
        return False

    allowed = str(row["Can Overlap With"]).replace("*", "")

    if allowed.strip() in ["", "-", "—"]:
        return False

    allowed_categories = [
        item.strip()
        for part in allowed.split(",")
        for item in part.split("/")
        if item.strip()
    ]

    return row["PreviousCategory"] in allowed_categories


process_merged["TimelineValid"] = process_merged.apply(
    check_timeline,
    axis=1
)

invalid_timeline = process_merged[
    ~process_merged["TimelineValid"]
]

r16_invalid = len(invalid_timeline)

print("Events with invalid timeline:", r16_invalid)

if r16_invalid > 0:
    print(
        invalid_timeline[
            [
                "HeatID",
                "EventSequence",
                "PreviousStage",
                "ProcessStage",
                "PreviousCategory",
                "EventStartDateTime",
                "PreviousEventEnd",
                "Can Overlap With"
            ]
        ].head(20)
    )


# ============================================================
# R17 - REPEAT CYCLE FLAG
# ============================================================

print_rule("R17")

expected_repeat_cycle = process_event["CycleNumber"].map(
    lambda value: "YES" if value > 0 else "NO"
)

invalid_repeat_cycle = process_event[
    process_event["RepeatCycleFlag"] != expected_repeat_cycle
]

add_result(
    "R17",
    "Incorrect RepeatCycleFlag records",
    invalid_repeat_cycle
)


# ============================================================
# R18 - REPEATED STAGE FLAG
# ============================================================

print_rule("R18")

expected_repeated_stage = process_event["StageOccurrence"].map(
    lambda value: "YES" if value > 1 else "NO"
)

invalid_repeated_stage = process_event[
    process_event["RepeatedStageFlag"] != expected_repeated_stage
]

add_result(
    "R18",
    "Incorrect RepeatedStageFlag records",
    invalid_repeated_stage
)


# ============================================================
# R19 - ADDITIONAL HEATING FLAG
# ============================================================

print_rule("R19")

expected_additional_heating = (
    (process_event["ProcessStage"] == "Heating") &
    (process_event["StageOccurrence"] > 1)
).map({
    True: "YES",
    False: "NO"
})

invalid_additional_heating = process_event[
    process_event["AdditionalHeatingFlag"] != expected_additional_heating
]

add_result(
    "R19",
    "Incorrect AdditionalHeatingFlag records",
    invalid_additional_heating
)


# ============================================================
# R20 - TEMPERATURE STATUS
# ============================================================

print_rule("R20")

expected_temperature_status = (
    (
        temperature["ActualTemperatureC"] >=
        temperature["TemperatureMinC"]
    ) &
    (
        temperature["ActualTemperatureC"] <=
        temperature["TemperatureMaxC"]
    )
).map({
    True: "PASS",
    False: "FAIL"
})

invalid_temperature_status = temperature[
    temperature["TemperatureStatus"] != expected_temperature_status
]

add_result(
    "R20",
    "Incorrect TemperatureStatus records",
    invalid_temperature_status
)


# ============================================================
# R21 - TEMPERATURE SEQUENCE AND CHRONOLOGY
# ============================================================

print_rule("R21")

temperature_sorted = temperature.sort_values(
    ["HeatID", "TemperatureSequence"]
).copy()

invalid_temperature_sequence = []

for heat_id, group in temperature_sorted.groupby("HeatID"):
    sequences = group["TemperatureSequence"].tolist()
    expected_sequence = list(range(1, len(group) + 1))

    times = group["MeasurementDateTime"].tolist()

    chronological = all(
        times[index] <= times[index + 1]
        for index in range(len(times) - 1)
    )

    if sequences != expected_sequence or not chronological:
        invalid_temperature_sequence.append({
            "HeatID": heat_id,
            "SequenceValid": sequences == expected_sequence,
            "Chronological": chronological
        })

invalid_temperature_sequence = pd.DataFrame(
    invalid_temperature_sequence
)

add_result(
    "R21",
    "Heats with invalid temperature sequence or chronology",
    invalid_temperature_sequence
)


# ============================================================
# R22 - ENERGY KWH CALCULATION
# ============================================================

print_rule("R22")

expected_energy = (
    energy["PowerMW"] *
    energy["HeatingDurationMin"] / 60 *
    1000
)

invalid_energy = energy[
    ~np.isclose(
        energy["EnergyKWh"],
        expected_energy,
        rtol=1e-5,
        atol=0.01
    )
]

add_result(
    "R22",
    "Incorrect EnergyKWh records",
    invalid_energy
)


# ============================================================
# R23 - ENERGY KWH PER TON CALCULATION
# ============================================================

print_rule("R23")

energy_merged = energy.merge(
    heat[["HeatID", "SteelWeightTon"]],
    on="HeatID",
    how="left"
)

expected_energy_per_ton = (
    energy_merged["EnergyKWh"] /
    energy_merged["SteelWeightTon"]
)

invalid_energy_intensity = energy_merged[
    ~np.isclose(
        energy_merged["EnergyKWhPerTon"],
        expected_energy_per_ton,
        rtol=1e-5,
        atol=0.01
    )
]

add_result(
    "R23",
    "Incorrect EnergyKWhPerTon records",
    invalid_energy_intensity
)


# ============================================================
# R24 - HEAT LEVEL RECONCILIATION
# ============================================================

print_rule("R24")

sample_count = (
    sample
    .groupby("HeatID")
    .size()
    .reset_index(name="ActualSampleCount")
)

adjustment_count = (
    adjustment
    .groupby("HeatID")
    .size()
    .reset_index(name="ActualAdjustmentCount")
)

energy_total = (
    energy
    .groupby("HeatID")["EnergyKWh"]
    .sum()
    .reset_index(name="ActualEnergyKWh")
)

heat_reconciliation = (
    heat[
        [
            "HeatID",
            "SampleCount",
            "AdjustmentCount",
            "EnergyKWh"
        ]
    ]
    .merge(sample_count, on="HeatID", how="left")
    .merge(adjustment_count, on="HeatID", how="left")
    .merge(energy_total, on="HeatID", how="left")
)

actual_columns = [
    "ActualSampleCount",
    "ActualAdjustmentCount",
    "ActualEnergyKWh"
]

heat_reconciliation[actual_columns] = (
    heat_reconciliation[actual_columns].fillna(0)
)

invalid_sample_count = heat_reconciliation[
    heat_reconciliation["SampleCount"] !=
    heat_reconciliation["ActualSampleCount"]
]

invalid_adjustment_count = heat_reconciliation[
    heat_reconciliation["AdjustmentCount"] !=
    heat_reconciliation["ActualAdjustmentCount"]
]

invalid_energy_total = heat_reconciliation[
    ~np.isclose(
        heat_reconciliation["EnergyKWh"],
        heat_reconciliation["ActualEnergyKWh"],
        rtol=1e-5,
        atol=0.01
    )
]

add_result(
    "R24",
    "Incorrect SampleCount",
    invalid_sample_count
)

add_result(
    "R24",
    "Incorrect AdjustmentCount",
    invalid_adjustment_count
)

add_result(
    "R24",
    "Incorrect total EnergyKWh",
    invalid_energy_total
)


# ============================================================
# R25 - HEAT STATUS VALIDATION
# ============================================================

print_rule("R25")

expected_heat_status = (
    (heat["ChemistryFinalStatus"] == "PASS") &
    (heat["TemperatureFinalStatus"] == "PASS")
).map({
    True: "PASS",
    False: "FAIL"
})

invalid_heat_status = heat[
    heat["HeatStatus"] != expected_heat_status
]

add_result(
    "R25",
    "Incorrect HeatStatus records",
    invalid_heat_status
)


# ============================================================
# R26 - FIRST PASS FLAG VALIDATION
# ============================================================

print_rule("R26")

expected_first_pass = (
    (heat["HeatStatus"] == "PASS") &
    (heat["RepeatCycleFlag"] == "NO")
).map({
    True: "YES",
    False: "NO"
})

invalid_first_pass = heat[
    heat["FirstPassFlag"] != expected_first_pass
]

add_result(
    "R26",
    "Incorrect FirstPassFlag records",
    invalid_first_pass
)


# ============================================================
# 5. FINAL VALIDATION SUMMARY
# ============================================================

summary_df = pd.DataFrame(validation_summary)

print("\n" + "=" * 70)
print("FINAL VALIDATION SUMMARY")
print("=" * 70)

print(
    summary_df.to_string(index=False)
)

print("\nTotal Invalid Records Found:")
print(summary_df["InvalidRecords"].sum())
