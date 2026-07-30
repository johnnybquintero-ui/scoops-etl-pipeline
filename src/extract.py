from pathlib import Path

import pandas as pd


def extract_flavours(file_path):
    return pd.read_csv(file_path)


def extract_sales(file_path):
    return pd.read_csv(file_path)


def extract_stores(file_path):
    return pd.read_csv(file_path)


def run_extraction(raw_data_dir="data/raw_data"):
    raw_data_dir = Path(raw_data_dir)

    flavours_df = extract_flavours(raw_data_dir / "flavours.csv")
    sales_df = extract_sales(raw_data_dir / "sales.csv")
    stores_df = extract_stores(raw_data_dir / "stores.csv")

    return flavours_df, sales_df, stores_df
