# LRF Optimization — Project Documentation

## 1. Project Overview

LRF Optimization is an end-to-end Data Analytics project focused on analyzing Ladle Refining Furnace (LRF) process data.

The project combines data validation, database management, and business intelligence to create a structured analytics workflow.

### End-to-End Workflow

**Excel Data → Python Data Validation → MySQL → Power BI**

The main objective is to validate LRF process data, organize the validated data into a structured database, and create Power BI dashboards for analysis.

---

## 2. Project Objectives

The main objectives of this project are:

- Validate LRF transaction data using Python.
- Identify invalid or inconsistent records using defined business rules.
- Ensure data quality and consistency before analysis.
- Load structured data into MySQL.
- Organize data using fact and dimension tables.
- Build Power BI dashboards for process analysis.
- Analyze cycle time, temperature, energy, chemistry, quality, and yield-related metrics.
- Provide a heat-level investigation view for detailed analysis.

---

## 3. Data Validation

Python is used as the first major processing stage in the project.

The validation framework contains **26 business rules (R01–R26)** covering different aspects of the LRF dataset.

### Validation Areas

The validation rules include checks for:

- Heat ID uniqueness
- Heat-ladle relationship
- Grade consistency
- Sample sequence
- Sample timeline
- Waiting time
- Laboratory analysis time
- Element chemistry status
- Overall chemistry
- Adjustment sequence
- Element adjustment sequence
- Repeat adjustment
- Adjustment reason
- Event sequence
- Process timeline
- Repeat cycle
- Repeated stage
- Additional heating flag
- Temperature status
- Temperature sequence
- Energy formula
- Energy intensity
- Heat reconciliation
- Heat status
- First-pass yield

### Validation Result

The validation report contains:

- **26 Total Rules**
- **26 Passed Rules**
- **0 Failed Rules**
- **100% Validation Success Rate**
- **25,000 Records in the Clean Dataset**

The validation report is available here:

`Documentation/LRF_Data_Validation_Report.png`

---

## 4. Python Data Processing

Python is used to read the Excel workbook and perform data validation.

### Main Python Scripts

#### `lrf_data_validation.py`

This script:

1. Loads the LRF Excel workbook.
2. Reads the required transaction and dimension sheets.
3. Applies the R01–R26 validation rules.
4. Identifies invalid records.
5. Produces a final validation summary.

#### `excel_to_mysql.py`

This script is used to load the structured Excel data into MySQL.

The workflow separates data validation from database loading so that data can be checked before being used for analytics.

---

## 5. MySQL Database

The validated LRF data is organized into fact and dimension tables in MySQL.

### Fact Tables

- `fact_heat`
- `fact_sample`
- `fact_adjustment`
- `fact_process_event`
- `fact_energy`
- `fact_temperature`

### Dimension Tables

- `dim_date`
- `dim_element`
- `dim_grade`
- `dim_grade_specification`
- `dim_grade_spec_long`
- `dim_furnace`
- `dim_ladle`
- `dim_material`
- `dim_operator`
- `dim_process_stage`
- `dim_temperature_recipe`

This structure supports analytical queries and Power BI reporting.

---

## 6. Power BI Dashboard

Power BI is used to analyze the validated LRF data and present business-focused visualizations.

The dashboard contains multiple analytical sections.

### LRF Overview

Provides a high-level view of:

- Total heats
- Total steel production
- Average LRF duration
- Total energy consumption
- Energy per ton
- First-pass percentage
- Production trends
- Heats by furnace
- First-pass performance by grade

### Cycle & Heat Analysis

Focuses on process cycle time and heating activity.

Key analysis includes:

- Average LRF duration
- Average heating time
- Additional heating events
- Average cycle time by grade
- Cycle time trends
- Cycle time by furnace
- Heat-level cycle investigation

### Temperature & Energy

Focuses on temperature behavior and energy consumption.

Key analysis includes:

- Average actual temperature
- Energy per ton
- Average heating time
- Temperature journey
- Energy consumption by grade
- Heating time by grade
- Temperature deviation versus energy consumption
- Additional heating events
- Energy efficiency by furnace

### Quality & Yield

Focuses on production quality and first-pass performance.

Key analysis includes:

- Total heats
- Re-treatment percentage
- First-pass percentage
- First-pass performance by grade
- Normal versus re-treatment heats
- Average temperature deviation
- Re-treatment trend
- First-pass performance by furnace

---

## 7. Dashboard Documentation

Power BI dashboard screenshots are available in the `Documentation` folder.

| Dashboard | Screenshot |
|---|---|
| LRF Overview | `PowerBI_Overview.png` |
| Cycle & Heat Analysis | `PowerBI_Cycle_Heat_Analysis.png` |
| Temperature & Energy | `PowerBI_Temperature_Energy.png` |
| Quality & Yield | `PowerBI_Quality_Yield.png` |
| Data Validation Report | `LRF_Data_Validation_Report.png` |

---

## 8. Project Architecture

```text
                 LRF Excel Dataset
                        │
                        ▼
              Python Data Validation
                        │
                  R01 – R26
                        │
                        ▼
                Validated Dataset
                        │
                        ▼
                     MySQL
                        │
             ┌──────────┴──────────┐
             │                     │
        Fact Tables          Dimension Tables
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                    Power BI
                        │
                        ▼
              Interactive Dashboard