import pandas as pd
from pathlib import Path

import logging
logger = logging.getLogger(__name__)


def build_dim_flavour(flavours_df):
    dim_flavour = flavours_df.rename(
        columns={
            "id": "flavour_id"
        }
    )

    return dim_flavour[
        [
            "flavour_id",
            "name",
            "contains_nuts",
            "cost_price_in_pence",
        ]
    ]


def build_dim_store(stores_df):
    return stores_df[
        [
            "store_id",
            "store_name",
            "region",
            "latitude",
            "longitude",
        ]
    ]


def build_dim_date(start_date, end_date):
    date_range = pd.date_range(
        start=start_date,
        end=end_date,
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

    return dim_date[
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


def build_fact_sales(sales_df, dim_date):
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

    return fact_sales[
        [
            "sale_id",
            "date_id",
            "store_id",
            "flavour_id",
            "price_in_pence",
        ]
    ]


def run_model(
    cleaned_data_dir="data/cleaned_data",
    star_schema_dir="data/star_schema",
):
    cleaned_data_dir = Path(cleaned_data_dir)
    star_schema_dir = Path(star_schema_dir)

    star_schema_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    flavours_df = pd.read_csv(
        cleaned_data_dir / "flavours.csv"
    )

    stores_df = pd.read_csv(
        cleaned_data_dir / "stores.csv"
    )

    sales_df = pd.read_csv(
        cleaned_data_dir / "sales.csv"
    )

    # Prepare the sales dates once for both dim_date and fact_sales
    sales_df["timestamp"] = pd.to_datetime(
        sales_df["timestamp"],
        format="mixed",
        dayfirst=True,
        errors="raise",
    )

    sales_df["full_date"] = (
        sales_df["timestamp"]
        .dt.normalize()
    )

    dim_flavour = build_dim_flavour(
        flavours_df
    )

    dim_store = build_dim_store(
        stores_df
    )

    dim_date = build_dim_date(
        start_date=sales_df["full_date"].min(),
        end_date=sales_df["full_date"].max(),
    )

    fact_sales = build_fact_sales(
        sales_df,
        dim_date,
    )

    dim_flavour.to_csv(
        star_schema_dir / "dim_flavour.csv",
        index=False,
    )

    dim_store.to_csv(
        star_schema_dir / "dim_store.csv",
        index=False,
    )

    dim_date.to_csv(
        star_schema_dir / "dim_date.csv",
        index=False,
    )

    fact_sales.to_csv(
        star_schema_dir / "fact_sales.csv",
        index=False,
    )

    logger.info("Star schema files created successfully")

if __name__ == "__main__":
    run_model()