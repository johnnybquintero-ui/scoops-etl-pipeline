import pandas as pd

def extract_flavours(file_path):
    """
    Extracts flavours from a CSV file and returns a DataFrame.

    Args:
        file_path (str): The path to the CSV file containing flavours.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted flavours.
    """
    return pd.read_csv(file_path)

def extract_sales(file_path):
    """
    Extracts sales data from a CSV file and returns a DataFrame.

    Args:
        file_path (str): The path to the CSV file containing sales data.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted sales data.
    """
    return pd.read_csv(file_path)

def extract_stores(file_path):
    """
    Extracts store data from a CSV file and returns a DataFrame.

    Args:
        file_path (str): The path to the CSV file containing store data.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted store data.
    """
    return pd.read_csv(file_path)

def run_extraction():
    flavours = extract_flavours("data/raw_data/flavours.csv")
    sales = extract_sales("data/raw_data/sales.csv")
    stores = extract_stores("data/raw_data/stores.csv")

    return flavours, sales, stores