from pathlib import Path

import pandas as pd


def extract_sales_data(file_path: str | Path) -> pd.DataFrame:
    """
    Read raw sales data from a CSV file.

    Args:
        file_path: Location of the CSV file.

    Returns:
        A pandas DataFrame containing the sales records.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Sales file was not found: {path}")

    sales_df = pd.read_csv(path)

    print(f"Extracted {len(sales_df)} sales records.")
    return sales_df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    sales_file = project_root / "data" / "sales.csv"

    data = extract_sales_data(sales_file)
    print(data.head())