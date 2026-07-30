from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)

def clean_flavours(raw_df):
    """
    Cleans the flavours data from a raw df and returns a cleaned df.
    """
    cleaned_df = raw_df.copy()

    cleaned_df = cleaned_df.dropna(
    subset=[
        "id",
        "name",
        "contains_nuts",
        "cost_price_in_pence",
    ]
)

    boolean_mapping = {
        "y": True,
        "yes": True,
        "true": True,
        "1": True,
        "n": False,
        "no": False,
        "false": False,
        "0": False,
    }

    cleaned_df["contains_nuts"] = (
        cleaned_df["contains_nuts"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(boolean_mapping)
    )

    if cleaned_df["contains_nuts"].isna().any():
        raise ValueError(
            "Unrecognised values found in 'contains_nuts' column."
        )

    try:
        cleaned_df["cost_price_in_pence"] = pd.to_numeric(
            cleaned_df["cost_price_in_pence"],
            errors="raise",
        )
    except ValueError as e:
        raise ValueError(
            "cost_price_in_pence contains invalid numeric values"
        ) from e

    cleaned_df = cleaned_df.loc[
        cleaned_df["cost_price_in_pence"] >= 0
    ]

    return cleaned_df

def clean_sales(raw_df):
    """
    Cleans the sales data from a raw df and returns a cleaned df.
    """
    cleaned_df = raw_df.copy()

    cleaned_df = cleaned_df.dropna(
    subset=[
        "id",
        "store_id",
        "timestamp",
        "flavour_id",
        "price_in_pence",
    ]
)

    cleaned_df["timestamp"] = pd.to_datetime(
        cleaned_df["timestamp"],
        format='mixed',
        dayfirst=True,
        errors="raise"
    )

    try:
        cleaned_df["price_in_pence"] = pd.to_numeric(
            cleaned_df["price_in_pence"],
            errors="raise"
        )
    except ValueError as e:
        raise ValueError("price_in_pence contains invalid numeric values") from e

    cleaned_df = cleaned_df.loc[
        cleaned_df["price_in_pence"] >= 0
    ]

    return cleaned_df

def clean_stores(raw_df):
    """
    Cleans the stores data from a raw df and returns a cleaned df.
    """
    cleaned_df = raw_df.copy()

    cleaned_df = cleaned_df.dropna(
    subset=[
        "store_id",
        "store_name",
        "region",
        "latitude",
        "longitude",
    ]
)

    text_columns = ["store_name", "region"]

    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].str.strip()

    if cleaned_df["store_id"].duplicated().any():
        raise ValueError("Duplicate store_id values found")

    try:
        cleaned_df["latitude"] = pd.to_numeric(
            cleaned_df["latitude"], errors="raise"
        )
        cleaned_df["longitude"] = pd.to_numeric(
            cleaned_df["longitude"], errors="raise"
        )
    except ValueError as e:
        raise ValueError("latitude or longitude contains invalid numeric values") from e

    if not cleaned_df["latitude"].between(-90, 90).all():
        raise ValueError("Latitude must be between -90 and 90.")

    if not cleaned_df["longitude"].between(-180, 180).all():
        raise ValueError("Longitude must be between -180 and 180.")

    return cleaned_df

def run_clean(
    flavours_raw_df,
    sales_raw_df,
    stores_raw_df,
    cleaned_data_dir="data/cleaned_data",
):
    """
    Run the complete clean stage.

    Cleans the raw DataFrames, writes cleaned CSV checkpoints,
    logs row counts, and returns the cleaned DataFrames.
    """
    cleaned_data_dir = Path(cleaned_data_dir)

    cleaned_data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    flavours_rows_in = len(flavours_raw_df)
    sales_rows_in = len(sales_raw_df)
    stores_rows_in = len(stores_raw_df)

    flavours_clean_df = clean_flavours(
        flavours_raw_df
    )

    sales_clean_df = clean_sales(
        sales_raw_df
    )

    stores_clean_df = clean_stores(
        stores_raw_df
    )

    flavours_clean_df.to_csv(
        cleaned_data_dir / "flavours.csv",
        index=False,
    )

    sales_clean_df.to_csv(
        cleaned_data_dir / "sales.csv",
        index=False,
    )

    stores_clean_df.to_csv(
        cleaned_data_dir / "stores.csv",
        index=False,
    )

    logger.info(
        "Flavours: %s rows in, %s rows out, "
        "%s rows dropped during cleaning",
        flavours_rows_in,
        len(flavours_clean_df),
        flavours_rows_in - len(flavours_clean_df),
    )

    logger.info(
        "Sales: %s rows in, %s rows out, "
        "%s rows dropped during cleaning",
        sales_rows_in,
        len(sales_clean_df),
        sales_rows_in - len(sales_clean_df),
    )

    logger.info(
        "Stores: %s rows in, %s rows out, "
        "%s rows dropped during cleaning",
        stores_rows_in,
        len(stores_clean_df),
        stores_rows_in - len(stores_clean_df),
    )

    return (
        flavours_clean_df,
        sales_clean_df,
        stores_clean_df,
    )