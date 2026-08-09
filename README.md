# Retail Sales Data Engineering Pipeline

A Python and PostgreSQL data engineering project that builds an end-to-end ETL pipeline for retail sales data.

The pipeline extracts sales data from a CSV file, transforms and cleans the data, loads it into PostgreSQL, builds a dimensional data warehouse, performs data-quality validation, and logs pipeline execution.

## Project Architecture

```text
CSV Sales Data
      |
      v
   Extract
      |
      v
  Transform
      |
      v
PostgreSQL Staging Table
   (sales_data)
      |
      v
Dimensional Data Warehouse
      |
      +-------------------+
      |                   |
      v                   v
 Dimension Tables     Fact Table
      |                   |
      |              fact_sales
      |
      +-- dim_product
      +-- dim_customer
      +-- dim_region
      +-- dim_date
              |
              v
      Data Quality Checks
              |
              v
            Logs
```

## Technologies

- Python
- PostgreSQL
- SQLAlchemy
- Pandas
- psycopg2
- python-dotenv
- Pytest

## Project Structure

```text
retail_sales_pipeline/
│
├── data/
│   └── sales.csv
│
├── src/
│   ├── database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── warehouse.py
│   ├── validate.py
│   ├── logger_config.py
│   └── pipeline.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## ETL Process

### 1. Extract

The extraction stage reads raw retail sales data from a CSV file using Pandas.

### 2. Transform

The transformation stage prepares the data for loading and calculates:

```text
total_sales = quantity × price
```

### 3. Load

The transformed data is loaded into the PostgreSQL `sales_data` staging table.

### 4. Build Data Warehouse

The pipeline converts the staging data into a dimensional model.

Dimension tables:

- `dim_product`
- `dim_customer`
- `dim_region`
- `dim_date`

Fact table:

- `fact_sales`

The fact table stores sales measurements and foreign keys connecting each transaction to its dimensions.

## Dimensional Model

```text
                 dim_product
                      |
                      |
dim_customer ---- fact_sales ---- dim_region
                      |
                      |
                   dim_date
```

This structure makes analytical SQL queries easier and more efficient.

## Data Quality Validation

The pipeline automatically checks for:

- Empty fact tables
- Missing dimension IDs
- Incorrect sales calculations
- Duplicate order IDs

Example successful validation:

```text
fact_sales row count: 10
Rows with missing dimension IDs: 0
Rows with incorrect total_sales: 0
Duplicate order IDs: 0
All data quality checks passed.
```

## Pipeline Logging

Pipeline execution is recorded in:

```text
logs/pipeline.log
```

Logging makes it easier to track successful pipeline runs and troubleshoot failures.

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd retail_sales_pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a `.env` file for your local database configuration.

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_sales
```

Do not commit the `.env` file to GitHub.

### 5. Run the full pipeline

```bash
python src/pipeline.py
```

The pipeline automatically performs:

```text
Extract
   ↓
Transform
   ↓
Load
   ↓
Build Warehouse
   ↓
Validate
   ↓
Log
```

## Example Analytics

The warehouse can be queried to answer business questions such as:

- Which product category generates the most revenue?
- Which region generates the most sales?
- Which products sell the most units?
- How do sales change over time?

Example:

```sql
SELECT
    p.category,
    SUM(f.total_sales) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;
```

Example output:

```text
Electronics    3300.00
Furniture       950.00
Accessories     590.00
```

## Key Concepts Demonstrated

This project demonstrates:

- ETL pipeline development
- Python data processing
- PostgreSQL integration
- SQL
- Relational database design
- Dimensional modeling
- Star schema design
- Fact and dimension tables
- Data-quality validation
- Pipeline logging
- Environment variable management
- Pipeline orchestration

## Future Improvements

Planned enhancements include:

- Automated testing with Pytest
- Workflow orchestration with Prefect
- Larger retail datasets
- Incremental data loading
- Additional data-quality rules
- BI/dashboard integration