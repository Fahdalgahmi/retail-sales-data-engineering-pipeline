from src.database import engine
from sqlalchemy import text


def build_warehouse():
    print("Building data warehouse...")

    with engine.begin() as connection:
        print("Connected to PostgreSQL.")

        # -----------------------------
        # Product dimension
        # -----------------------------
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_product (
                product TEXT,
                category TEXT,
                product_id SERIAL PRIMARY KEY
            );
        """))

        connection.execute(text("""
            INSERT INTO dim_product (product, category)
            SELECT DISTINCT product, category
            FROM sales_data
            WHERE NOT EXISTS (
                SELECT 1
                FROM dim_product d
                WHERE d.product = sales_data.product
                  AND d.category = sales_data.category
            );
        """))

        print("dim_product table ready.")
        print("dim_product data loaded.")

        # -----------------------------
        # Customer dimension
        # -----------------------------
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_customer (
                customer_id SERIAL PRIMARY KEY,
                customer_name TEXT UNIQUE
            );
        """))

        connection.execute(text("""
            INSERT INTO dim_customer (customer_name)
            SELECT DISTINCT customer
            FROM sales_data
            WHERE NOT EXISTS (
                SELECT 1
                FROM dim_customer d
                WHERE d.customer_name = sales_data.customer
            );
        """))

        print("dim_customer table ready.")
        print("dim_customer data loaded.")

        # -----------------------------
        # Region dimension
        # -----------------------------
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_region (
                region_id SERIAL PRIMARY KEY,
                region_name TEXT UNIQUE
            );
        """))

        connection.execute(text("""
            INSERT INTO dim_region (region_name)
            SELECT DISTINCT region
            FROM sales_data
            WHERE NOT EXISTS (
                SELECT 1
                FROM dim_region d
                WHERE d.region_name = sales_data.region
            );
        """))

        print("dim_region table ready.")
        print("dim_region data loaded.")

        # -----------------------------
        # Date dimension
        # -----------------------------
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_date (
                date_id SERIAL PRIMARY KEY,
                full_date DATE UNIQUE,
                day INTEGER,
                month INTEGER,
                year INTEGER
            );
        """))

        connection.execute(text("""
            INSERT INTO dim_date (
                full_date,
                day,
                month,
                year
            )
            SELECT DISTINCT
                order_date::date,
                EXTRACT(DAY FROM order_date)::INTEGER,
                EXTRACT(MONTH FROM order_date)::INTEGER,
                EXTRACT(YEAR FROM order_date)::INTEGER
            FROM sales_data
            WHERE NOT EXISTS (
                SELECT 1
                FROM dim_date d
                WHERE d.full_date = sales_data.order_date::date
            );
        """))

        print("dim_date table ready.")
        print("dim_date data loaded.")

        # -----------------------------
        # Sales fact table
        # -----------------------------
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                sales_id SERIAL PRIMARY KEY,
                order_id INTEGER UNIQUE,
                date_id INTEGER,
                customer_id INTEGER,
                product_id INTEGER,
                region_id INTEGER,
                quantity INTEGER,
                price NUMERIC(10, 2),
                total_sales NUMERIC(10, 2),

                FOREIGN KEY (date_id)
                    REFERENCES dim_date(date_id),

                FOREIGN KEY (customer_id)
                    REFERENCES dim_customer(customer_id),

                FOREIGN KEY (product_id)
                    REFERENCES dim_product(product_id),

                FOREIGN KEY (region_id)
                    REFERENCES dim_region(region_id)
            );
        """))

        print("fact_sales table ready.")

        # -----------------------------
        # Load fact table
        # -----------------------------
        connection.execute(text("""
            INSERT INTO fact_sales (
                order_id,
                date_id,
                customer_id,
                product_id,
                region_id,
                quantity,
                price,
                total_sales
            )
            SELECT
                s.order_id,
                d.date_id,
                c.customer_id,
                p.product_id,
                r.region_id,
                s.quantity,
                s.price,
                s.total_sales
            FROM sales_data s

            JOIN dim_date d
                ON d.full_date = s.order_date::date

            JOIN dim_customer c
                ON c.customer_name = s.customer

            JOIN dim_product p
                ON p.product = s.product
                AND p.category = s.category

            JOIN dim_region r
                ON r.region_name = s.region

            WHERE NOT EXISTS (
                SELECT 1
                FROM fact_sales f
                WHERE f.order_id = s.order_id
            );
        """))

        print("fact_sales data loaded.")

    print("Data warehouse build complete.")


if __name__ == "__main__":
    build_warehouse()