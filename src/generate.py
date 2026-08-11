import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


OUTPUT_FILE = Path("data/sales.csv")
NUM_ROWS = 10_000


products = [
    ("Laptop", "Electronics", 1200),
    ("Monitor", "Electronics", 300),
    ("Headphones", "Accessories", 120),
    ("Keyboard", "Accessories", 80),
    ("Mouse", "Accessories", 25),
    ("Desk", "Furniture", 450),
    ("Chair", "Furniture", 250),
    ("Tablet", "Electronics", 600),
    ("Webcam", "Accessories", 90),
    ("Printer", "Electronics", 220),
]

customers = [
    "John Smith",
    "Alice Brown",
    "Bob Lee",
    "Sarah Kim",
    "David Jones",
    "Emma Wilson",
    "Michael Davis",
    "Olivia Miller",
    "Daniel Garcia",
    "Sophia Martinez",
    "James Anderson",
    "Emily Taylor",
    "William Thomas",
    "Ava Moore",
    "Benjamin Jackson",
]

regions = ["East", "West", "North", "South"]


def random_date(start_date, end_date):
    date_range = end_date - start_date
    random_days = random.randint(0, date_range.days)
    return start_date + timedelta(days=random_days)


def generate_sales_data():
    rows = []

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 12, 31)

    for order_id in range(1001, 1001 + NUM_ROWS):
        product, category, base_price = random.choice(products)

        # Add small realistic price variation
        price_multiplier = random.uniform(0.90, 1.10)
        price = round(base_price * price_multiplier, 2)

        quantity = random.randint(1, 5)

        rows.append(
            {
                "order_id": order_id,
                "order_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
                "customer": random.choice(customers),
                "product": product,
                "category": category,
                "quantity": quantity,
                "price": price,
                "region": random.choice(regions),
            }
        )

    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(df):,} sales records.")
    print(f"Saved dataset to: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_sales_data()