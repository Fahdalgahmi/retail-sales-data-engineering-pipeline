import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/retail_sales"
)

engine = create_engine(DATABASE_URL)


def test_connection():
    try:
        with engine.connect():
            print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:")
        print(e)


if __name__ == "__main__":
    test_connection()