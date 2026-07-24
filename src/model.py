import pandas as pd
from pathlib import Path

star_schema_dir = Path("data/star_schema")
star_schema_dir.mkdir(parents=True, exist_ok=True)

# Read the cleaned data
flavours_df = pd.read_csv(
    "data/cleaned_data/flavours.csv"
)

dim_store = pd.read_csv(
    "data/cleaned_data/stores.csv"
)

sales_df = pd.read_csv(
    "data/cleaned_data/sales.csv"
)


# Create the star schema table for dim_flavour
dim_flavour = flavours_df.rename(
    columns={
        "id": "flavour_id"
    }
)

dim_flavour = dim_flavour[
    [
        "flavour_id",
        "name",
        "contains_nuts",
        "cost_price_in_pence",
    ]
]

print("\n=== DIM_FLAVOUR ===")
print(dim_flavour.head())

dim_flavour.to_csv(
    star_schema_dir / "dim_flavour.csv",
    index=False,
)


# Create the star schema table for dim_store
dim_store = dim_store[
    [
        "store_id",
        "store_name",
        "region",
        "latitude",
        "longitude",
    ]
]

print("\n=== DIM_STORE ===")
print(dim_store.head())

dim_store.to_csv(
    star_schema_dir / "dim_store.csv",
    index=False,
)


# Parse the sales timestamp
sales_df["timestamp"] = pd.to_datetime(
    sales_df["timestamp"],
    format="mixed",
    dayfirst=True,
    errors="raise",
)

# Create a date-only version of each sale timestamp
sales_df["full_date"] = (
    sales_df["timestamp"]
    .dt.normalize()
)


# Create the star schema table for dim_date
date_range = pd.date_range(
    start="2024-01-01",
    end="2024-12-31",
    freq="D",
)

dim_date = pd.DataFrame(
    {
        "full_date": date_range
    }
)

dim_date["date_id"] = (
    dim_date["full_date"]
    .dt.strftime("%Y%m%d")
    .astype("int64")
)

dim_date["day"] = dim_date["full_date"].dt.day
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["day_of_week"] = dim_date["full_date"].dt.day_name()
dim_date["is_weekend"] = (
    dim_date["full_date"].dt.dayofweek >= 5
)

dim_date = dim_date[
    [
        "date_id",
        "full_date",
        "day",
        "month",
        "month_name",
        "quarter",
        "year",
        "day_of_week",
        "is_weekend",
    ]
]

print("\n=== DIM_DATE ===")
print(dim_date.head())

dim_date.to_csv(
    star_schema_dir / "dim_date.csv",
    index=False,
)


# Create the star schema table for fact_sales
fact_sales = sales_df.merge(
    dim_date[
        [
            "date_id",
            "full_date",
        ]
    ],
    on="full_date",
    how="left",
    validate="many_to_one",
)

fact_sales = fact_sales.rename(
    columns={
        "id": "sale_id",
    }
)

fact_sales = fact_sales[
    [
        "sale_id",
        "date_id",
        "store_id",
        "flavour_id",
        "price_in_pence",
    ]
]

print("\n=== FACT_SALES ===")
print(fact_sales.head())

fact_sales.to_csv(
    star_schema_dir / "fact_sales.csv",
    index=False,
)