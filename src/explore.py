import pandas as pd


def create_dataframe_from_csv(raw_data):
    """
    Create a pandas DataFrame from raw CSV data.
    """
    return pd.read_csv(raw_data)


def explore_dataframe(dataframe, dataset_name):
    """Print exploratory information about a DataFrame."""

    print("\n")
    print(f"{dataset_name.upper()} DATASET")

    print("\n=== Preview ===")
    print(dataframe.head())

    print("\n=== Structure ===")
    dataframe.info()

    print("\n=== Data Types ===")
    print(dataframe.dtypes)

    print("\n=== Summary Statistics ===")
    print(dataframe.describe())

    print("\n=== Missing Values ===")
    print(dataframe.isnull().sum())


def run_exploration():
    flavours = create_dataframe_from_csv("data/raw_data/flavours.csv")
    sales = create_dataframe_from_csv("data/raw_data/sales.csv")
    stores = create_dataframe_from_csv("data/raw_data/stores.csv")

    explore_dataframe(flavours, "Flavours")
    explore_dataframe(sales, "Sales")
    explore_dataframe(stores, "Stores")


if __name__ == "__main__":
    run_exploration()