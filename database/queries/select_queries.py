
AVG_PRICE_BY_MANUFACTURER = """
SELECT
    mfr.name AS manufacturer,
    COUNT(c.id) AS total_cars,
    AVG(c.price) AS avg_price
FROM car_marketplace.cars c
JOIN car_marketplace.models mdl ON c.model_id = mdl.id
JOIN car_marketplace.manufacturers mfr ON mdl.manufacturer_id = mfr.id
GROUP BY mfr.name
ORDER BY avg_price DESC;
"""

TOP_5_EXPENSIVE_CARS = """
SELECT
    mfr.name AS manufacturer,
    mdl.model_name,
    c.year,
    c.price
FROM car_marketplace.cars c
JOIN car_marketplace.models mdl ON c.model_id = mdl.id
JOIN car_marketplace.manufacturers mfr ON mdl.manufacturer_id = mfr.id
ORDER BY c.price DESC
LIMIT 5;
"""

HIGH_MILEAGE_HIGH_PRICE = """
SELECT
    mfr.name AS manufacturer,
    mdl.model_name,
    c.mileage,
    c.price
FROM car_marketplace.cars c
JOIN car_marketplace.models mdl ON c.model_id = mdl.id
JOIN car_marketplace.manufacturers mfr ON mdl.manufacturer_id = mfr.id
WHERE c.mileage > 200000 AND c.price > 10000
ORDER BY c.price DESC;
"""

AVG_PRICE_BY_ENGINE = """
SELECT
    s.engine,
    COUNT(*) AS total_cars,
    AVG(c.price) AS avg_price
FROM car_marketplace.cars c
JOIN car_marketplace.specifications s ON c.specification_id = s.id
GROUP BY s.engine
HAVING COUNT(*) >= 10
ORDER BY avg_price DESC;
"""

YEAR_OVER_YEAR_PRICE = """
SELECT
    year,
    avg_price,
    avg_price - LAG(avg_price) OVER (ORDER BY year) AS price_change
FROM (
    SELECT
        year,
        AVG(price) AS avg_price
    FROM car_marketplace.cars
    GROUP BY year
) yearly_prices
ORDER BY year;
"""

RANK_MODELS_BY_PRICE = """
SELECT
    manufacturer,
    model_name,
    avg_price,
    RANK() OVER (PARTITION BY manufacturer ORDER BY avg_price DESC) AS price_rank
FROM (
    SELECT
        mfr.name AS manufacturer,
        mdl.model_name,
        AVG(c.price) AS avg_price
    FROM car_marketplace.cars c
    JOIN car_marketplace.models mdl ON c.model_id = mdl.id
    JOIN car_marketplace.manufacturers mfr ON mdl.manufacturer_id = mfr.id
    GROUP BY mfr.name, mdl.model_name
) ranked_models
ORDER BY manufacturer, price_rank;
"""

RECENT_CARS_PARTITION = """
SELECT
    COUNT(*) AS total_recent_cars,
    AVG(price) AS avg_price
FROM car_marketplace.cars
WHERE year BETWEEN 2018 AND 2024;
"""

MODELS_NO_CARS = """
SELECT
    mfr.name AS manufacturer,
    mdl.model_name
FROM car_marketplace.models mdl
LEFT JOIN car_marketplace.cars c ON mdl.id = c.model_id
JOIN car_marketplace.manufacturers mfr ON mdl.manufacturer_id = mfr.id
WHERE c.id IS NULL;
"""

CUSTOM_CLEARANCE_DISTRIBUTION = """
SELECT
    CASE c.custom_cleared
        WHEN 0 THEN 'Not cleared'
        WHEN 1 THEN 'Cleared'
        WHEN 2 THEN 'Partially cleared'
        ELSE 'Unknown'
    END AS clearance_status,
    COUNT(*) AS total_cars
FROM car_marketplace.cars c
GROUP BY clearance_status
ORDER BY total_cars DESC;
"""

EXPLAIN_AVG_PRICE_BY_MANUFACTURER = AVG_PRICE_BY_MANUFACTURER
EXPLAIN_RECENT_CARS_PARTITION = RECENT_CARS_PARTITION
