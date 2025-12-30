CREATE_SCHEMA_QUERY = "CREATE SCHEMA car_marketplace;"
SET_SEARCH_PATH_QUERY = "SET search_path TO car_marketplace;"

CREATE_MANUFACTURERS_TABLE = """
CREATE TABLE manufacturers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
"""

CREATE_MODELS_TABLE = """
CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    body_style VARCHAR(50),

    CONSTRAINT fk_manufacturer
        FOREIGN KEY (manufacturer_id)
        REFERENCES manufacturers(id)
);
"""

CREATE_SPECIFICATIONS_TABLE = """
CREATE TABLE specifications (
    id SERIAL PRIMARY KEY,
    engine VARCHAR(50) NOT NULL,
    gearbox INT NOT NULL,
    hand_drive SMALLINT NOT NULL
);
"""

CREATE_CARS_TABLE = """
CREATE TABLE cars (
    id SERIAL,
    model_id INTEGER NOT NULL,
    specification_id INTEGER NOT NULL,
    price INTEGER CHECK (price > 0),
    year INTEGER NOT NULL,
    mileage NUMERIC CHECK (mileage >= 0),
    color VARCHAR(50),
    custom_cleared SMALLINT CHECK (custom_cleared IN (0,1,2)),

    CONSTRAINT pk_cars PRIMARY KEY (id, year),

    CONSTRAINT fk_model
        FOREIGN KEY (model_id)
        REFERENCES models(id),

    CONSTRAINT fk_spec
        FOREIGN KEY (specification_id)
        REFERENCES specifications(id)
) PARTITION BY RANGE (year);
"""


CREATE_CARS_1900_2005_PARTITION = """
CREATE TABLE cars_2010_2019 PARTITION OF cars
FOR VALUES FROM (1900) TO (2005)
"""

CREATE_CARS_2005_2030_PARTITION = """
CREATE TABLE cars_2020_2029 PARTITION OF cars
FOR VALUES FROM (2005) TO (2030)
"""

CREATE_IDX_CARS_PRICE = """
CREATE INDEX idx_cars_price ON cars(price);
"""

CREATE_IDX_CARS_YEAR = """
CREATE INDEX idx_cars_year ON cars(year);
"""

CREATE_IDX_MODELS_MANUFACTURER = """
CREATE INDEX idx_models_manufacturer ON models(manufacturer_id);
"""

CREATE_VW_CAR_LISTINGS = """
CREATE VIEW vw_car_listings AS
SELECT
    c.id,
    mfr.name AS manufacturer,
    mdl.model_name,
    mdl.body_style,
    s.engine,
    s.gearbox,
    c.year,
    c.price,
    c.mileage,
    c.color,
    c.custom_cleared
FROM cars c
JOIN models mdl ON c.model_id = mdl.id
JOIN manufacturers mfr ON mdl.manufacturer_id = mfr.id
JOIN specifications s ON c.specification_id = s.id;
"""

CREATE_VW_AVG_PRICE_BY_MANUFACTURER = """
CREATE VIEW vw_avg_price_by_manufacturer AS
SELECT
    mfr.name,
    AVG(c.price) AS avg_price
FROM cars c
JOIN models mdl ON c.model_id = mdl.id
JOIN manufacturers mfr ON mdl.manufacturer_id = mfr.id
GROUP BY mfr.name;
"""

