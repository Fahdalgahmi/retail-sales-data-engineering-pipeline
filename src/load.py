def load_sales_data(df, engine):
    df.to_sql(
        "sales_data",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into PostgreSQL table: sales_data")