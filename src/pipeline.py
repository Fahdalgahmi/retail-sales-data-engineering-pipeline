from extract import extract_sales_data
from transform import transform_sales_data
from load import load_sales_data
from warehouse import build_warehouse
from validate import validate_data
from logger_config import get_logger
from database import engine


logger = get_logger(__name__)


def run_pipeline():
    try:
        print("Starting full data pipeline...")
        logger.info("Pipeline started.")

        # -----------------------------
        # Step 1: Extract
        # -----------------------------
        print("\n1. Extracting data...")

        data = extract_sales_data("data/sales.csv")

        logger.info(f"Extracted {len(data)} records.")

        # -----------------------------
        # Step 2: Transform
        # -----------------------------
        print("\n2. Transforming data...")

        transformed_data = transform_sales_data(data)

        logger.info("Data transformation completed.")

        # -----------------------------
        # Step 3: Load staging table
        # -----------------------------
        print("\n3. Loading data into PostgreSQL...")

        load_sales_data(transformed_data, engine)

        logger.info("Data loaded into sales_data.")

        # -----------------------------
        # Step 4: Build warehouse
        # -----------------------------
        print("\n4. Building data warehouse...")

        build_warehouse()

        logger.info("Data warehouse built successfully.")

        # -----------------------------
        # Step 5: Validate data
        # -----------------------------
        print("\n5. Running data quality checks...")

        validate_data()

        logger.info("Data validation completed.")

        print("\nFull data pipeline completed successfully.")
        logger.info("Pipeline completed successfully.")

    except Exception as error:
        logger.exception(f"Pipeline failed: {error}")

        print("\nPipeline failed.")
        print(error)

        raise


if __name__ == "__main__":
    run_pipeline()