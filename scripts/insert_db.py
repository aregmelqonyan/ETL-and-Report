import sys 
import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.queries.creation_queries import SET_SEARCH_PATH_QUERY
from database.db_connect import with_db_cursor
from database.insertion import (
    insert_manufacturers,
    get_manufacturer_ids, 
    insert_models,
    get_model_ids,
    insert_specifications,
    get_specification_ids,
    insert_cars
)


@with_db_cursor(commit=True) 
def insert_all_from_csv(cur, csv_file_path):
    df = pd.read_csv(csv_file_path)

    cur.execute(SET_SEARCH_PATH_QUERY)

    manufacturers = df[["Make"]].drop_duplicates().rename(columns={"Make": "name"})
    insert_manufacturers(cur, manufacturers.to_dict(orient="records"))
    manufacturer_ids = get_manufacturer_ids(cur)
    df["manufacturer_id"] = df["Make"].map(manufacturer_ids)

    models = df[["manufacturer_id", "Model", "Body style"]].drop_duplicates()
    models = models.rename(columns={"Model": "model_name", "Body style": "body_style"})
    insert_models(cur, models.to_dict(orient="records"))
    model_ids = get_model_ids(cur)
    df["model_id"] = df.apply(lambda row: model_ids[(row["manufacturer_id"], row["Model"], row["Body style"])], axis=1)

    specs = df[["Engine", "Gearbox", "Hand drive"]].drop_duplicates()
    specs = specs.rename(columns={"Engine": "engine", "Gearbox": "gearbox", "Hand drive": "hand_drive"})
    insert_specifications(cur, specs.to_dict(orient="records"))
    spec_ids = get_specification_ids(cur)
    df["specification_id"] = df.apply(
        lambda row: spec_ids[(row["Engine"], int(row["Gearbox"]), row["Hand drive"])], axis=1
    )

    cars = df[[
        "model_id", "specification_id", "Price", "Year", "Mileage", "Color", "Custom cleared"
    ]].rename(columns={
        "Price": "price",
        "Year": "year",
        "Mileage": "mileage",
        "Color": "color",
        "Custom cleared": "custom_cleared"
    })

    insert_cars(cur, cars.to_dict(orient="records"))

if __name__ == "__main__":
    csv_relative_path = "data/processed/output.csv"
    csv_file_path = os.path.abspath(os.path.join(PROJECT_ROOT, csv_relative_path))
    
    insert_all_from_csv(csv_file_path)