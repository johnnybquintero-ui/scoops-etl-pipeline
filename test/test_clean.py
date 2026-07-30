import pandas as pd
import pytest

from src.clean import clean_flavours, clean_sales, clean_stores


def test_clean_flavours_returns_dataframe(raw_flavours_df):
    result = clean_flavours(raw_flavours_df)

    assert isinstance(result, pd.DataFrame)


def test_clean_flavours_normalises_bool_contains_nuts(
    raw_flavours_df,
):
    result = clean_flavours(raw_flavours_df)

    assert result["contains_nuts"].tolist() == [
        True,
        True,
        False,
        True,
        False,
    ]


def test_clean_flavours_drops_negative_cost_price(raw_flavours_df):
    raw_flavours_df.loc[0, "cost_price_in_pence"] = -100
    rows_before = len(raw_flavours_df)

    result = clean_flavours(raw_flavours_df)

    assert (result["cost_price_in_pence"] >= 0).all()
    assert len(result) == rows_before - 1


def test_clean_flavours_converts_cost_price_to_numeric():
    raw_df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Vanilla", "Chocolate"],
            "contains_nuts": ["Y", "N"],
            "cost_price_in_pence": ["100", "200"],
        }
    )

    result = clean_flavours(raw_df)

    assert pd.api.types.is_numeric_dtype(result["cost_price_in_pence"])

    assert result["cost_price_in_pence"].tolist() == [100, 200]


def test_clean_flavours_raises_error_for_unknown_contains_nuts():
    raw_df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Vanilla"],
            "contains_nuts": ["maybe"],
            "cost_price_in_pence": [45],
        }
    )

    with pytest.raises(
        ValueError,
        match="Unrecognised values found in 'contains_nuts' column.",
    ):
        clean_flavours(raw_df)


def test_clean_sales_returns_dataframe(raw_sales_df):
    result = clean_sales(raw_sales_df)

    assert isinstance(result, pd.DataFrame)


def test_clean_sales_returns_coerced_timestamp(raw_sales_df):
    result = clean_sales(raw_sales_df)

    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_clean_sales_raises_error_for_invalid_timestamp(raw_sales_df):
    raw_sales_df.loc[0, "timestamp"] = "invalid_timestamp"

    with pytest.raises(ValueError, match="timestamp"):
        clean_sales(raw_sales_df)


def test_clean_sales_raises_error_for_non_numeric_price_in_pence(raw_sales_df):
    raw_sales_df["price_in_pence"] = raw_sales_df["price_in_pence"].astype("object")
    raw_sales_df.loc[0, "price_in_pence"] = "not_a_number"

    with pytest.raises(ValueError, match="price_in_pence"):
        clean_sales(raw_sales_df)


def test_clean_sales_drops_negative_price_in_pence(raw_sales_df):
    raw_sales_df.loc[0, "price_in_pence"] = -100
    rows_before = len(raw_sales_df)

    result = clean_sales(raw_sales_df)

    assert (result["price_in_pence"] >= 0).all()
    assert len(result) == rows_before - 1


def test_clean_stores_returns_dataframe(raw_stores_df):
    result = clean_stores(raw_stores_df)

    assert isinstance(result, pd.DataFrame)


def test_clean_stores_strips_whitespace_from_text_columns(raw_stores_df):
    raw_stores_df.loc[0, "store_name"] = " Central Perk "
    raw_stores_df.loc[0, "region"] = " East Anglia "

    result = clean_stores(raw_stores_df)

    assert result.loc[0, "store_name"] == "Central Perk"
    assert result.loc[0, "region"] == "East Anglia"


def test_clean_stores_raises_error_for_duplicate_store_ids(raw_stores_df):
    raw_stores_df.loc[1, "store_id"] = "S001"

    with pytest.raises(ValueError, match="Duplicate store_id values found"):
        clean_stores(raw_stores_df)


def test_clean_stores_returns_error_for_non_numeric_coordinates(raw_stores_df):
    raw_stores_df["latitude"] = raw_stores_df["latitude"].astype("object")
    raw_stores_df.loc[0, "latitude"] = "not_a_number"

    with pytest.raises(ValueError, match="latitude"):
        clean_stores(raw_stores_df)

    raw_stores_df["longitude"] = raw_stores_df["longitude"].astype("object")
    raw_stores_df.loc[0, "longitude"] = "not_a_number"

    with pytest.raises(ValueError, match="longitude"):
        clean_stores(raw_stores_df)


def test_clean_stores_raises_error_for_non_numeric_latitude(raw_stores_df):
    raw_stores_df["latitude"] = raw_stores_df["latitude"].astype("object")
    raw_stores_df.loc[0, "latitude"] = "not_a_number"

    with pytest.raises(ValueError, match="latitude"):
        clean_stores(raw_stores_df)


def test_clean_stores_raises_error_for_non_numeric_longitude(raw_stores_df):
    raw_stores_df["longitude"] = raw_stores_df["longitude"].astype("object")
    raw_stores_df.loc[0, "longitude"] = "not_a_number"

    with pytest.raises(ValueError, match="longitude"):
        clean_stores(raw_stores_df)
