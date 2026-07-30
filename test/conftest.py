import pandas as pd
import pytest
import psycopg2


@pytest.fixture
def raw_flavours_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": [
                "Vanilla",
                "Chocolate",
                "Strawberry",
                "Pistachio",
                "Salted Caramel",
            ],
            "contains_nuts": [
                "true",
                "Y",
                "no",
                "1",
                "FALSE",
            ],
            "cost_price_in_pence": [
                45,
                65,
                55,
                95,
                60,
            ],
        }
    )


@pytest.fixture
def raw_sales_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "store_id": [1, 2, 3, 4, 5],
            "timestamp": [
                "2023-01-01 10:00:00",
                "01/06/2024 11:40:21",
                "2023-01-03 14:15:00",
                "2023-01-04 09:45:00",
                "2023-01-05 16:20:00",
            ],
            "flavour_id": [1, 2, 3, 4, 5],
            "price_in_pence": [100, 150, 120, 800, 180],
        }
    )


@pytest.fixture
def raw_stores_df():
    return pd.DataFrame(
        {
            "store_id": ["S001", "S002", "S003", "S004", "S005"],
            "store_name": [
                "Central Perk",
                "Scoops Ahoy",
                "The Ice Creamery",
                "Frosty Treats",
                "Sweet Scoops",
            ],
            "region": [
                "East Anglia",
                "Great Yarmouth",
                "North Norfolk",
                "South Norfolk",
                "West Norfolk",
            ],
            "latitude": [52.2053, 52.6085, 52.6309, 52.6309, 52.6309],
            "longitude": [0.1218, 1.7302, 1.2974, 1.2974, 1.2974],
        }
    )


@pytest.fixture
def test_connection():
    connection = psycopg2.connect(dbname="scoops_sales_test")

    yield connection

    connection.rollback()
    connection.close()
