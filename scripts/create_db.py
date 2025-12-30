import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.logging_config import get_logger
from database.db_connect import with_db_cursor
from database.queries.creation_queries import (
    CREATE_SCHEMA_QUERY,
    SET_SEARCH_PATH_QUERY,
    CREATE_MANUFACTURERS_TABLE,
    CREATE_MODELS_TABLE,
    CREATE_SPECIFICATIONS_TABLE,
    CREATE_CARS_TABLE,
    CREATE_CARS_1900_2005_PARTITION,
    CREATE_CARS_2005_2030_PARTITION,
    CREATE_IDX_CARS_PRICE,
    CREATE_IDX_CARS_YEAR,
    CREATE_IDX_MODELS_MANUFACTURER,
    CREATE_VW_CAR_LISTINGS,
    CREATE_VW_AVG_PRICE_BY_MANUFACTURER,
)

logger = get_logger(__name__)


@with_db_cursor(commit=True)
def initialize_database(cur):
    cur.execute(CREATE_SCHEMA_QUERY)
    logger.info("Schema created.")


    cur.execute(SET_SEARCH_PATH_QUERY)
    logger.info("Search path set.")

    cur.execute(CREATE_MANUFACTURERS_TABLE)
    logger.info("Manufacturers table created.")

    cur.execute(CREATE_MODELS_TABLE)
    logger.info("Models table created.")

    cur.execute(CREATE_SPECIFICATIONS_TABLE)
    logger.info("Specifications table created.")

    cur.execute(CREATE_CARS_TABLE)
    logger.info("Cars table created.")

    cur.execute(CREATE_CARS_1900_2005_PARTITION)
    logger.info("Cars 1990-2005 partition created.")

    cur.execute(CREATE_CARS_2005_2030_PARTITION)
    logger.info("Cars 2005-2025 partition created.")

    cur.execute(CREATE_IDX_CARS_PRICE)
    logger.info("Index on cars(price) created.")

    cur.execute(CREATE_IDX_CARS_YEAR)
    logger.info("Index on cars(year) created.")

    cur.execute(CREATE_IDX_MODELS_MANUFACTURER)
    logger.info("Index on models(manufacturer_id) created.")

    cur.execute(CREATE_VW_CAR_LISTINGS)
    logger.info("View vw_car_listings created.")

    cur.execute(CREATE_VW_AVG_PRICE_BY_MANUFACTURER)
    logger.info("View vw_avg_price_by_manufacturer created.")

    logger.info("Database initialization successfully completed!")


if __name__ == "__main__":
    initialize_database()
