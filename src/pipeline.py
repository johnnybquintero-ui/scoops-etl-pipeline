import logging

from src.clean import run_clean
from src.extract import run_extraction
from src.load import run_load
from src.model import run_model


logger = logging.getLogger(__name__)


def run_pipeline(
    raw_data_dir="data/raw_data",
    cleaned_data_dir="data/cleaned_data",
    star_schema_dir="data/star_schema",
    dbname="scoops_sales",
):
    logger.info("Starting extract stage")

    flavours_raw_df, sales_raw_df, stores_raw_df = (
        run_extraction(raw_data_dir)
    )

    logger.info("Starting clean stage")

    run_clean(
        flavours_raw_df,
        sales_raw_df,
        stores_raw_df,
        cleaned_data_dir=cleaned_data_dir,
    )

    logger.info("Starting model stage")

    run_model(
        cleaned_data_dir=cleaned_data_dir,
        star_schema_dir=star_schema_dir,
    )

    logger.info("Starting load stage")

    run_load(
        star_schema_dir=star_schema_dir,
        dbname=dbname,
    )

    logger.info("Pipeline completed successfully")