import pandas as pd

def load_dim_store(cursor, dim_store_df):
    '''Uses cursor connection to insert cleaned store data into db table'''

    for row in dim_store_df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO dim_store (
                store_id,
                store_name,
                region,
                latitude,
                longitude
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                row.store_id,
                row.store_name,
                row.region,
                row.latitude,
                row.longitude
            ),
        )

def load_dim_flavour(cursor, dim_flavour_df):
    '''Use cursor connection to insert cleaned flavour data into db table'''

    for row in dim_flavour_df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO dim_flavour (
                flavour_id,
                name,
                contains_nuts,
                cost_price_in_pence
                )
                VALUES(%s,%s,%s,%s);
                """,
                (
                    row.flavour_id,
                    row.name,
                    row.contains_nuts,
                    row.cost_price_in_pence
                ),
            )

def load_dim_date(cursor, dim_date_df):
    """Use cursor connection to insert date dimension data into the database."""

    for row in dim_date_df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO dim_date (
                date_id,
                full_date,
                day,
                month,
                month_name,
                quarter,
                year,
                day_of_week,
                is_weekend
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                row.date_id,
                row.full_date,
                row.day,
                row.month,
                row.month_name,
                row.quarter,
                row.year,
                row.day_of_week,
                row.is_weekend,
            ),
        )

def load_fact_sales(cursor, fact_sales_df):
    """Insert modelled sales data into the fact_sales table."""

    for row in fact_sales_df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO fact_sales (
                sale_id,
                date_id,
                store_id,
                flavour_id,
                price_in_pence
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                row.sale_id,
                row.date_id,
                row.store_id,
                row.flavour_id,
                row.price_in_pence,
            ),
        )

