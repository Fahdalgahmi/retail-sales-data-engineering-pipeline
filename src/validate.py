from database import engine
from sqlalchemy import text
from logger_config import get_logger

logger = get_logger(__name__)

def validate_data():
    print("Running data quality checks...")

    with engine.begin() as connection:

        # Check 1: Make sure fact_sales is not empty
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM fact_sales;
        """))

        fact_count = result.scalar()

        print(f"fact_sales row count: {fact_count}")

        if fact_count == 0:
            raise ValueError("Validation failed: fact_sales is empty.")

        # Check 2: Look for missing foreign keys
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM fact_sales
            WHERE date_id IS NULL
               OR customer_id IS NULL
               OR product_id IS NULL
               OR region_id IS NULL;
        """))

        null_foreign_keys = result.scalar()

        print(f"Rows with missing dimension IDs: {null_foreign_keys}")

        if null_foreign_keys > 0:
            raise ValueError(
                "Validation failed: fact_sales contains missing dimension IDs."
            )

        # Check 3: Look for invalid sales totals
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM fact_sales
            WHERE total_sales != quantity * price;
        """))

        invalid_totals = result.scalar()

        print(f"Rows with incorrect total_sales: {invalid_totals}")

        if invalid_totals > 0:
            raise ValueError(
                "Validation failed: incorrect total_sales values found."
            )

        # Check 4: Make sure order IDs are unique
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM fact_sales
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) duplicates;
        """))

        duplicate_orders = result.scalar()

        print(f"Duplicate order IDs: {duplicate_orders}")

        if duplicate_orders > 0:
            raise ValueError(
                "Validation failed: duplicate order IDs found."
            )

    print("All data quality checks passed.")


if __name__ == "__main__":
    validate_data()

    logger.info("All data quality checks passed.")