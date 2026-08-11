# Retail Sales Data Engineering Pipeline

An end-to-end **data engineering pipeline** built with Python and PostgreSQL that processes **10,000 retail sales records** from raw CSV data into an analytics-ready dimensional data warehouse.

The project demonstrates a complete data engineering workflow including **ETL processing, PostgreSQL integration, dimensional modeling, automated data-quality validation, testing, logging, and pipeline orchestration**.

---

## Project Architecture

```text
Raw CSV Sales Data
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
        +----------------------+
        |                      |
        v                      v
 Dimension Tables          Fact Table
                           fact_sales
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

---

## Technologies

* Python
* PostgreSQL
* SQL
* Pandas
* SQLAlchemy
* psycopg2
* python-dotenv
* Pytest
* Git / GitHub

---

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
│   ├── test_transform.py
│   └── test_validation.py
│
├── logs/
│   └── pipeline.log
│
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## ETL Pipeline

### 1. Extract

The extraction stage reads **10,000 retail sales records** from a CSV file using Pandas.

The source dataset contains:

* Order ID
* Order date
* Customer
* Product
* Category
* Quantity
* Price
* Region

Example pipeline output:

```text
Extracting data...
Extracted 10000 sales records.
```

### 2. Transform

The transformation stage prepares the raw data for loading and calculates the sales value for each transaction:

```text
total_sales = quantity × price
```

This creates a clean dataset ready for PostgreSQL storage and downstream analytics.

### 3. Load

The transformed dataset is loaded into the PostgreSQL `sales_data` staging table.

Example:

```text
Loaded 10000 rows into PostgreSQL table: sales_data
```

The staging layer separates raw ETL processing from the dimensional warehouse and acts as the source for warehouse construction.

### 4. Build the Data Warehouse

The pipeline transforms the staging data into an analytics-oriented dimensional model.

#### Dimension Tables

* `dim_product`
* `dim_customer`
* `dim_region`
* `dim_date`

#### Fact Table

* `fact_sales`

The `fact_sales` table contains transactional measurements including:

* Order ID
* Quantity
* Price
* Total sales

It also contains foreign keys connecting each transaction to its corresponding product, customer, region, and date dimensions.

---

## Dimensional Model

The warehouse uses a **star schema**:

```text
                    dim_product
                         |
                         |
dim_customer ------ fact_sales ------ dim_region
                         |
                         |
                      dim_date
```

The fact table sits at the center of the model and connects transactional sales data with descriptive dimensions.

This design makes analytical SQL queries simpler and provides a structure suitable for reporting, dashboards, and business intelligence tools.

---

## Data Quality Validation

Automated data-quality checks run after the warehouse is built.

The pipeline validates:

* Fact table row count
* Missing dimension IDs
* Incorrect `total_sales` calculations
* Duplicate order IDs

Latest successful validation:

```text
fact_sales row count: 10000
Rows with missing dimension IDs: 0
Rows with incorrect total_sales: 0
Duplicate order IDs: 0

All data quality checks passed.
```

These checks help ensure that the warehouse contains complete, accurate, and internally consistent data.

---

## Automated Testing

Pytest is used to verify important pipeline functionality.

Current tests cover:

* Transformation logic
* Data-quality validation

Run the test suite with:

```bash
pytest
```

Latest test result:

```text
collected 2 items

tests/test_transform.py .      [ 50%]
tests/test_validation.py .     [100%]

2 passed
```

Automated testing helps detect regressions when pipeline logic is modified.

---

## Pipeline Logging

Pipeline execution is logged to help monitor processing and troubleshoot failures.

```text
logs/pipeline.log
```

The pipeline records events such as:

* Pipeline start
* Number of extracted records
* Transformation completion
* PostgreSQL loading
* Warehouse construction
* Validation completion
* Pipeline success or failure

---

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Fahdalgahmi/retail-sales-data-engineering-pipeline.git
cd retail-sales-data-engineering-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a `.env` file in the project root.

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_sales
```

The `.env` file is excluded from Git using `.gitignore` and should never be committed to the repository.

### 5. Run the Full Pipeline

From the project root, run:

```bash
python -m src.pipeline
```

The command executes the entire workflow:

```text
Extract
   ↓
Transform
   ↓
Load to PostgreSQL
   ↓
Build Dimensional Warehouse
   ↓
Run Data Quality Checks
   ↓
Log Pipeline Execution
```

A successful run ends with:

```text
All data quality checks passed.

Full data pipeline completed successfully.
```

### 6. Run Tests

```bash
pytest
```

---

## Example Analytics

The dimensional warehouse can be queried to answer business questions such as:

* Which product categories generate the most revenue?
* Which regions generate the most sales?
* Which products sell the most units?
* Which customers generate the most revenue?
* How does revenue change over time?
* What are monthly or daily sales trends?

Example query:

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

The star-schema design allows analytical queries to combine transaction metrics from `fact_sales` with descriptive information stored in the dimension tables.

---

## Pipeline Execution Example

A successful end-to-end execution processes the complete dataset:

```text
Starting full data pipeline...

1. Extracting data...
Extracted 10000 sales records.

2. Transforming data...
Data transformation completed.

3. Loading data into PostgreSQL...
Loaded 10000 rows into PostgreSQL table: sales_data.

4. Building data warehouse...
Connected to PostgreSQL.
dim_product table ready.
dim_product data loaded.
dim_customer table ready.
dim_customer data loaded.
dim_region table ready.
dim_region data loaded.
dim_date table ready.
dim_date data loaded.
fact_sales table ready.
fact_sales data loaded.
Data warehouse build complete.

5. Running data quality checks...
fact_sales row count: 10000
Rows with missing dimension IDs: 0
Rows with incorrect total_sales: 0
Duplicate order IDs: 0
All data quality checks passed.

Full data pipeline completed successfully.
```

---

## Key Concepts Demonstrated

This project demonstrates practical experience with:

* End-to-end ETL pipeline development
* Python data processing
* Pandas transformations
* PostgreSQL integration
* SQL querying
* SQLAlchemy database connectivity
* Relational database design
* Dimensional modeling
* Star-schema architecture
* Fact and dimension tables
* Data warehouse development
* Data-quality validation
* Automated testing with Pytest
* Pipeline logging
* Exception handling
* Environment variable management
* Pipeline orchestration
* Git version control

---

## Future Improvements

Potential enhancements include:

* Incremental data loading
* Upsert-based warehouse loading
* Apache Airflow or Prefect orchestration
* Docker containerization
* Additional automated data-quality rules
* Larger or externally sourced datasets
* Cloud-hosted PostgreSQL
* AWS, Azure, or GCP deployment
* Scheduled pipeline execution
* Power BI dashboard integration
* CI/CD testing with GitHub Actions

---

## Project Purpose

This project demonstrates how raw transactional data can move through a complete **data engineering lifecycle**:

**Raw Data → ETL → PostgreSQL → Dimensional Warehouse → Validation → Testing → Analytics**

The pipeline processes **10,000 sales transactions** and automatically builds and validates an analytics-ready warehouse.

It provides hands-on experience with technologies and concepts commonly used in **Data Engineering, Analytics Engineering, and Data Analytics** roles.
