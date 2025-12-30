INSERT_MANUFACTURER = """
INSERT INTO manufacturers (name)
VALUES (%s)
ON CONFLICT (name) DO NOTHING
"""

INSERT_MODEL = """
INSERT INTO models (manufacturer_id, model_name, body_style)
VALUES (%s, %s, %s)
"""

INSERT_SPECIFICATION = """
INSERT INTO specifications (engine, gearbox, hand_drive)
VALUES (%s, %s, %s)
"""

INSERT_CAR = """
INSERT INTO cars (model_id, specification_id, price, year, mileage, color, custom_cleared)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
