import pandas as pd
from config.logging_config import get_logger

from database.queries.insertion_queries import (
    INSERT_MANUFACTURER,
    INSERT_MODEL,
    INSERT_SPECIFICATION,
    INSERT_CAR
)

logger = get_logger(__name__)


def insert_manufacturers(cur, manufacturers):
    for m in manufacturers:
        cur.execute(INSERT_MANUFACTURER, (m["name"],))
        logger.info(f"Inserted manufacturer: {m['name']}")


def get_manufacturer_ids(cur):
    cur.execute("SELECT id, name FROM manufacturers")
    return {row[1]: row[0] for row in cur.fetchall()}


def insert_models(cur, models):
    for m in models:
        cur.execute(INSERT_MODEL, (m["manufacturer_id"], m["model_name"], m.get("body_style")))
        logger.info(f"Inserted model: {m['model_name']}")


def get_model_ids(cur):
    cur.execute("SELECT id, manufacturer_id, model_name, body_style FROM models")
    return {(row[1], row[2], row[3]): row[0] for row in cur.fetchall()}


def insert_specifications(cur, specifications):
    for s in specifications:
        cur.execute(
            INSERT_SPECIFICATION,
            (s["engine"], s["gearbox"], s["hand_drive"])
        )
        logger.info(
            f"Inserted specification: {s['engine']} / {s['gearbox']} / {s['hand_drive']}"
        )


def get_specification_ids(cur):
    cur.execute("SELECT id, engine, gearbox, hand_drive FROM specifications")
    return {(row[1], int(row[2]), row[3]): row[0] for row in cur.fetchall()}


def insert_cars(cur, cars):
    for c in cars:
        cur.execute(
            INSERT_CAR,
            (
                c["model_id"],
                c["specification_id"],
                c["price"],
                c["year"],
                c["mileage"],
                c.get("color"),
                c.get("custom_cleared", 0)
            )
        )
        logger.info(f"Inserted car: {c['model_id']} / {c['year']}")
