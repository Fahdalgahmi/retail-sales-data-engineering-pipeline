import pandas as pd

from src.transform import transform_sales_data


def test_total_sales_calculation():
    data = pd.DataFrame({
        "order_id": [1],
        "order_date": ["2026-01-01"],
        "customer": ["Test Customer"],
        "product": ["Laptop"],
        "category": ["Electronics"],
        "quantity": [2],
        "price": [500],
        "region": ["East"]
    })

    result = transform_sales_data(data)

    assert result.loc[0, "total_sales"] == 1000