from prefect import flow, task

from src.extract import extract_sales_data
from src.transform import transform_sales_data
from src.load import load_sales_data
from src.warehouse import build_warehouse
from src.validate import validate_data
from src.database import engine


@task
def extract_task():
    return extract_sales_data("data/sales.csv")


@task
def transform_task(data):
    return transform_sales_data(data)


@task(retries=2, retry_delay_seconds=5)
def load_task(data):
    load_sales_data(data, engine)


@task(retries=2, retry_delay_seconds=5)
def warehouse_task():
    build_warehouse()


@task(retries=2, retry_delay_seconds=5)
def validate_task():
    validate_data()


@flow(name="Retail Sales Data Pipeline")
def retail_sales_flow():
    raw_data = extract_task()
    transformed_data = transform_task(raw_data)
    load_task(transformed_data)
    warehouse_task()
    validate_task()


if __name__ == "__main__":
    retail_sales_flow()