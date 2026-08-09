from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Radad410531266367$@localhost:5432/retail_sales_db"

engine = create_engine(DATABASE_URL)


def test_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:")
        print(e)


if __name__ == "__main__":
    test_connection()