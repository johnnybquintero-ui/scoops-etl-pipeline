from pathlib import Path
import logging

import pandas as pd

from src.clean import (
    clean_flavours,
    clean_sales,
    clean_stores,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

def main():
    raw_dir = Path("data/raw_data")
    cleaned_dir = Path("data/cleaned_data")
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    flavours_raw_df = pd.read_csv(raw_dir / "flavours.csv")
    stores_raw_df = pd.read_csv(raw_dir / "stores.csv")
    sales_raw_df = pd.read_csv(raw_dir / "sales.csv")

    flavours_rows_in = len(flavours_raw_df)
    stores_rows_in = len(stores_raw_df)
    sales_rows_in = len(sales_raw_df)

    flavours_clean_df = clean_flavours(flavours_raw_df)
    stores_clean_df = clean_stores(stores_raw_df)
    sales_clean_df = clean_sales(sales_raw_df)

    flavours_rows_out = len(flavours_clean_df)
    stores_rows_out = len(stores_clean_df)
    sales_rows_out = len(sales_clean_df)

    flavours_clean_df.to_csv(cleaned_dir / "flavours.csv", index=False)
    stores_clean_df.to_csv(cleaned_dir / "stores.csv", index=False)
    sales_clean_df.to_csv(cleaned_dir / "sales.csv", index=False)

    logging.info(
    "Flavours: %s rows in, %s rows out, %s rows dropped during cleaning",
    flavours_rows_in,
    flavours_rows_out,
    flavours_rows_in - flavours_rows_out,
)

    logging.info(
        "Stores: %s rows in, %s rows out, %s rows dropped during cleaning",
        stores_rows_in,
        stores_rows_out,
        stores_rows_in - stores_rows_out,
    )

    logging.info(
        "Sales: %s rows in, %s rows out, %s rows dropped during cleaning",
        sales_rows_in,
        sales_rows_out,
        sales_rows_in - sales_rows_out,
    )
    
if __name__ == "__main__":
    main()