# Retail Sales Data Engineering Pipeline

An end-to-end **data engineering and analytics pipeline** built with Python and PostgreSQL that processes **10,000 retail sales records** from raw CSV data into an analytics-ready dimensional data warehouse.

The project demonstrates a complete data engineering workflow including **ETL processing, PostgreSQL integration, dimensional modeling, automated data-quality validation, Pytest testing, Docker containerization, Prefect workflow orchestration, GitHub Actions continuous integration, and Power BI analytics**.

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
        +-----------------------+
        |                       |
        v                       v
 Dimension Tables           Fact Table
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
        Power BI Analytics
```

The complete workflow can be executed locally using **Docker Compose**, while **Prefect** provides workflow orchestration and **GitHub Actions** automatically runs CI checks when code is pushed to the repository.

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
* Docker
* Docker Compose
* Prefect
* GitHub Actions
* Power BI
* Git / GitHub

---

## Project Structure

```text
retail-sales-data-engineering-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   └── sales.csv
│
├── src/
│   ├── database.py
│   ├── extract.py
│   ├── generate.py
│   ├── load.py
│   ├── logger_config.py
│   ├── pipeline.py
│   ├── prefect_pipeline.py
│   ├── transform.py
│   ├── validate.py
│   └── warehouse.py
│
├── tests/
│   ├── test_transform.py
│   └── test_validation.py
│
├── logs/
│   └── pipeline.log
│
├── Retail_Sales_Analytics_Dashboard.pbix
├── compose.yaml
├── Dockerfile
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## ETL Pipeline

### 1. Extract

The extraction stage reads **10,000 retail sales records** from CSV using Pandas.

The source dataset contains:

* Order ID
* Order date
* Customer
* Product
* Category
* Quantity
* Price
* Region

Example output:

```text
Extracting data...
Extracted 10000 sales records.
```

### 2. Transform

The transformation stage cleans and prepares the raw data and calculates the sales value for each transaction:

```text
total_sales = quantity × price
```

The transformed dataset is then ready for PostgreSQL storage and downstream analytics.

### 3. Load

The transformed dataset is loaded into the PostgreSQL `sales_data` staging table.

Example:

```text
Loaded 10000 rows into PostgreSQL table: sales_data
```

The staging layer separates the ETL process from the dimensional warehouse and acts as the source for warehouse construction.

### 4. Build the Data Warehouse

The pipeline transforms staging data into an analytics-oriented dimensional model.

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

It also contains foreign keys connecting transactions to the corresponding product, customer, region, and date dimensions.

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

The fact table sits at the center of the model and connects transactional sales metrics with descriptive dimensions.

This architecture simplifies analytical queries and provides a structure suitable for reporting, business intelligence, and dashboard development.

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

**Pytest** is used to verify important pipeline functionality.

Current tests cover:

* Transformation logic
* Data-quality validation

Run the test suite with:

```bash
pytest
```

Latest successful result:

```text
collected 2 items

tests/test_transform.py .      [ 50%]
tests/test_validation.py .     [100%]

2 passed
```

Automated testing helps detect regressions when pipeline logic is modified.

---

## Docker Containerization

The project is containerized with **Docker** and **Docker Compose**.

Docker provides a reproducible environment for the application and PostgreSQL database.

Start the containers with:

```bash
docker compose up -d
```

Check their status with:

```bash
docker compose ps
```

Stop the environment with:

```bash
docker compose down
```

Docker Compose manages the application and PostgreSQL services together, reducing the amount of manual local configuration required to run the project.

---

## Prefect Workflow Orchestration

**Prefect** is used to orchestrate the data pipeline.

The Prefect workflow coordinates the major pipeline stages and provides a structured workflow for executing the ETL and warehouse process.

The orchestration layer helps organize pipeline tasks and provides a foundation for future scheduling, monitoring, retries, and production workflow management.

The Prefect workflow is defined in:

```text
src/prefect_pipeline.py
```

---

## GitHub Actions Continuous Integration

The repository includes a **GitHub Actions CI workflow**.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

GitHub Actions provides automated validation of the project when changes are pushed to the repository.

This introduces continuous integration practices into the development workflow and helps detect problems before changes are considered complete.

---

## Pipeline Logging

Pipeline execution is logged to help monitor processing and troubleshoot failures.

Logs are written to:

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

## Power BI Analytics Dashboard

The project includes an interactive **Power BI dashboard** connected to the PostgreSQL dimensional warehouse.

Dashboard file:

```text
Retail_Sales_Analytics_Dashboard.pbix
```

The dashboard provides an analytics layer on top of the engineered data warehouse.

### Key Performance Indicators

The dashboard displays:

* **Total Sales:** approximately $10.22M
* **Total Orders:** 10K
* **Average Order Value:** approximately $1.02K

### Dashboard Visualizations

The report includes:

* Monthly Sales Trend
* Sales by Category
* Sales by Region
* Sales by Product
* Region filtering

The Region slicer allows users to interactively filter the dashboard and analyze sales performance across different geographic regions.

This demonstrates how an engineered PostgreSQL warehouse can support downstream business intelligence and analytics.

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

### 5. Start Docker

Start the application and PostgreSQL containers:

```bash
docker compose up -d
```

Verify that the containers are running:

```bash
docker compose ps
```

### 6. Run the Full Pipeline

From the project root:

```bash
python -m src.pipeline
```

The pipeline executes:

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

A successful execution ends with:

```text
All data quality checks passed.

Full data pipeline completed successfully.
```

### 7. Run Tests

```bash
pytest
```

---

## Example Analytics

The dimensional warehouse can answer business questions such as:

* Which product categories generate the most revenue?
* Which regions generate the most sales?
* Which products generate the most revenue?
* Which customers generate the most revenue?
* How does revenue change over time?
* What are the monthly sales trends?

Example SQL query:

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

The star-schema design allows analytical queries to combine transaction metrics from `fact_sales` with descriptive information stored in dimension tables.

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
* Docker containerization
* Docker Compose
* Prefect workflow orchestration
* GitHub Actions continuous integration
* Power BI dashboard development
* Git version control

---

## Future Improvements

Potential future enhancements include:

* Incremental data loading and change-data-capture strategies
* Upsert-based warehouse loading
* Cloud deployment using AWS, Azure, or GCP
* Scheduled production pipeline execution
* Expanded automated data-quality monitoring
* Larger externally sourced datasets
* Power BI Service deployment and scheduled dashboard refresh

---

## Project Purpose

This project demonstrates how raw transactional data can move through a complete **data engineering lifecycle**:

**Raw Data → ETL → PostgreSQL → Dimensional Warehouse → Validation → Testing → Power BI Analytics**

The pipeline processes **10,000 sales transactions** and automatically builds and validates an analytics-ready dimensional warehouse.

The project demonstrates practical experience with technologies and concepts commonly used in **Data Engineering, Analytics Engineering, and Data Analytics** roles while connecting backend data engineering work to an interactive business intelligence dashboard.
