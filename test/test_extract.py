from src.extract import extract_flavours, extract_sales, extract_stores
import pandas as pd

def test_extract_flavours_returns_dataframe():
    # Arrange
    file_path = "data/raw_data/flavours.csv"

    # Act
    result = extract_flavours(file_path)

    # Assert
    assert isinstance(result, pd.DataFrame)

def test_extract_sales_returns_dataframe():
    # Arrange
    file_path = "data/raw_data/sales.csv"

    # Act
    result = extract_sales(file_path)

    # Assert
    assert isinstance(result, pd.DataFrame)

def test_extract_stores_returns_dataframe():
    # Arrange
    file_path = "data/raw_data/stores.csv"

    # Act
    result = extract_stores(file_path)

    # Assert
    assert isinstance(result, pd.DataFrame)