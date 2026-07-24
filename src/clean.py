import pandas as pd

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
