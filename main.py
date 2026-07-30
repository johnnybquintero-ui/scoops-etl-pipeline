import logging

from src.pipeline import run_pipeline


def main():
    run_pipeline(
        raw_data_dir="data/raw_data",
        cleaned_data_dir="data/cleaned_data",
        star_schema_dir="data/star_schema",
        dbname="scoops_sales",
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )

    main()
