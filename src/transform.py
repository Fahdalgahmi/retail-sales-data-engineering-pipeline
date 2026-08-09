import pandas as pd
from src.extract import extract_sales_data

def transform_sales_data(df):
    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Calculate total sales for each order
    df["total_sales"] = df["quantity"] * df["price"]

    # Clean text columns
    df["product"] = df["product"].str.strip()
    df["region"] = df["region"].str.strip()

    return df


if __name__ == "__main__":
    sales_df = extract_sales_data("data/sales.csv")

    transformed_df = transform_sales_data(sales_df)

    print("\nTransformed Sales Data:")
    print(transformed_df.head())