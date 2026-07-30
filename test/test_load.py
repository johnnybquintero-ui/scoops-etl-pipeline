import pandas as pd
import pytest
from src.load import load_dim_store, load_dim_flavour, load_dim_date, load_fact_sales

def test_load_dim_store_inserts_all_rows(test_connection):
    stores_df = pd.read_csv(
        "data/star_schema/dim_store.csv"
    )

    with test_connection.cursor() as cursor:

        load_dim_store(cursor, stores_df)

        cursor.execute("""
            SELECT COUNT(*)
            FROM dim_store;
        """)

        actual = cursor.fetchone()[0]

    expected = len(stores_df)

    assert actual == expected

def test_load_dim_store_inserts_correct_values(test_connection):
    stores_df = pd.read_csv(
        "data/star_schema/dim_store.csv"
    )

    with test_connection.cursor() as cursor:
        load_dim_store(cursor, stores_df)

        cursor.execute(
            """
            SELECT
                store_id,
                store_name,
                region,
                latitude,
                longitude
            FROM dim_store
            WHERE store_id = %s;
            """,
            ("S001",),
        )

        actual = cursor.fetchone()

    expected = stores_df.loc[
        stores_df["store_id"] == "S001"
    ].iloc[0]

    assert actual[0] == expected["store_id"]
    assert actual[1] == expected["store_name"]
    assert actual[2] == expected["region"]
    assert float(actual[3]) == pytest.approx(expected["latitude"])
    assert float(actual[4]) == pytest.approx(expected["longitude"])

def test_load_dim_flavour_inserts_all_rows(test_connection):
    flavours_df = pd.read_csv(
            "data/star_schema/dim_flavour.csv"
        )
    
    with test_connection.cursor() as cursor:

        load_dim_flavour(cursor, flavours_df)

        cursor.execute("""
            SELECT COUNT(*)
            FROM dim_flavour;
        """)

        actual = cursor.fetchone()[0]

    expected = len(flavours_df)

    assert actual == expected

def test_load_dim_flavour_inserts_correct_values(test_connection):
    flavours_df = pd.read_csv(
            "data/star_schema/dim_flavour.csv"
        )
    
    with test_connection.cursor() as cursor:

        load_dim_flavour(cursor, flavours_df)

        cursor.execute("""
            SELECT
                flavour_id,
                name,
                contains_nuts,
                cost_price_in_pence
            FROM dim_flavour
            WHERE flavour_id = %s;
            """,
            (1,),
            )
        actual = cursor.fetchone()
        
    expected = flavours_df.loc[
        flavours_df["flavour_id"] == 1
    ].iloc[0]

    assert actual[0] == expected["flavour_id"]
    assert actual[1] == expected["name"]
    assert actual[2] == expected["contains_nuts"]
    assert actual[3] == expected["cost_price_in_pence"]

def test_load_dim_date_inserts_all_rows(test_connection):
    dates_df = pd.read_csv(
        "data/star_schema/dim_date.csv",
        parse_dates=["full_date"],
    )

    with test_connection.cursor() as cursor:
        load_dim_date(cursor, dates_df)

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dim_date;
            """
        )
        actual = cursor.fetchone()[0]

    expected = len(dates_df)
    assert actual == expected

def test_load_dim_date_inserts_correct_values(test_connection):
    # parse_dates converts full_date from a string into a pandas Timestamp.
    dates_df = pd.read_csv(
        "data/star_schema/dim_date.csv",
        parse_dates=["full_date"],
    )

    # Use the first real row from the DataFrame.
    expected = dates_df.iloc[0]

    # Convert the pandas/numpy integer into a normal Python int for psycopg.
    date_id = int(expected["date_id"])

    with test_connection.cursor() as cursor:
        load_dim_date(cursor, dates_df)

        # Retrieve the database row with the same date_id as the chosen
        # DataFrame row.
        cursor.execute(
            """
            SELECT
                date_id,
                full_date,
                day,
                month,
                month_name,
                quarter,
                year,
                day_of_week,
                is_weekend
            FROM dim_date
            WHERE date_id = %s;
            """,
            (date_id,),
        )


        actual = cursor.fetchone()

    # Check that a matching database row was found.
    assert actual is not None

    # Compare each database value with the corresponding DataFrame value.
    assert actual[0] == expected["date_id"]

    # PostgreSQL returns full_date as a Python date object.
    # pandas stores it as a Timestamp, so .date() makes the types match.
    assert actual[1] == expected["full_date"].date()

    assert actual[2] == expected["day"]
    assert actual[3] == expected["month"]
    assert actual[4] == expected["month_name"]
    assert actual[5] == expected["quarter"]
    assert actual[6] == expected["year"]
    assert actual[7] == expected["day_of_week"]
    assert actual[8] == expected["is_weekend"]

def test_load_fact_sales_inserts_all_rows(test_connection):
    fact_sales_df = pd.read_csv(
        "data/star_schema/fact_sales.csv"
    )

    # Load the dimension DataFrames as well,
    # because fact_sales references them with foreign keys.
    dates_df = pd.read_csv(
        "data/star_schema/dim_date.csv",
        parse_dates=["full_date"],
    )

    stores_df = pd.read_csv(
        "data/star_schema/dim_store.csv"
    )

    flavours_df = pd.read_csv(
        "data/star_schema/dim_flavour.csv"
    )

    with test_connection.cursor() as cursor:
        load_dim_date(cursor, dates_df)
        load_dim_store(cursor, stores_df)
        load_dim_flavour(cursor, flavours_df)

        load_fact_sales(cursor, fact_sales_df)

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM fact_sales;
            """
        )

        actual = cursor.fetchone()[0]

    expected = len(fact_sales_df)

    assert actual == expected

def test_load_fact_sales_inserts_correct_values(test_connection):
    dates_df = pd.read_csv(
        "data/star_schema/dim_date.csv",
        parse_dates=["full_date"],
    )

    stores_df = pd.read_csv(
        "data/star_schema/dim_store.csv"
    )

    flavours_df = pd.read_csv(
        "data/star_schema/dim_flavour.csv"
    )

    fact_sales_df = pd.read_csv(
        "data/star_schema/fact_sales.csv"
    )

    # Pick a row that definitely exists.
    expected = fact_sales_df.iloc[0]
    sale_id = int(expected["sale_id"])

    with test_connection.cursor() as cursor:
        # Load parent tables first so the foreign keys are valid.
        load_dim_date(cursor, dates_df)
        load_dim_store(cursor, stores_df)
        load_dim_flavour(cursor, flavours_df)

        # Now the fact rows can be inserted.
        load_fact_sales(cursor, fact_sales_df)

        cursor.execute(
            """
            SELECT
                sale_id,
                date_id,
                store_id,
                flavour_id,
                price_in_pence
            FROM fact_sales
            WHERE sale_id = %s;
            """,
            (sale_id,),
        )

        actual = cursor.fetchone()

    assert actual is not None
    assert actual[0] == expected["sale_id"]
    assert actual[1] == expected["date_id"]
    assert actual[2] == expected["store_id"]
    assert actual[3] == expected["flavour_id"]
    assert actual[4] == expected["price_in_pence"]