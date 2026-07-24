from src.explore import create_dataframe_from_csv
import pandas as pd

def test_create_dataframe_from_csv_returns_dataframe():
    #Arrange
    raw_data = "data/raw_data/flavours.csv"

    #Act
    result = create_dataframe_from_csv(raw_data)

    #Assert
    assert isinstance(result, pd.DataFrame)
    