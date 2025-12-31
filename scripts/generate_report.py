import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config.logging_config import get_logger
from database.db_connect import with_db_cursor
from database.queries.select_queries import (
    AVG_PRICE_BY_MANUFACTURER,
    TOP_5_EXPENSIVE_CARS,
    HIGH_MILEAGE_HIGH_PRICE,
    AVG_PRICE_BY_ENGINE,
    YEAR_OVER_YEAR_PRICE,
    RANK_MODELS_BY_PRICE,
    RECENT_CARS_PARTITION,
    MODELS_NO_CARS,
    CUSTOM_CLEARANCE_DISTRIBUTION,
    EXPLAIN_AVG_PRICE_BY_MANUFACTURER,
    EXPLAIN_RECENT_CARS_PARTITION
)

logger = get_logger(__name__)

TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "templates", "report.html")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "docs", "top_queries_report.html")


def run_query(cur, query):
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    return pd.DataFrame(cur.fetchall(), columns=cols)


def run_explain(cur, query):
    cur.execute(f"EXPLAIN ANALYZE {query}")
    return "\n".join(row[0] for row in cur.fetchall())


BUSINESS_QUERIES = [
    ("Average Price by Manufacturer", AVG_PRICE_BY_MANUFACTURER,
     "Shows the average price of cars for each manufacturer."),
    ("Top 5 Most Expensive Cars", TOP_5_EXPENSIVE_CARS,
     "Find the top 5 most expensive cars."),
    ("High Mileage & High Price Cars", HIGH_MILEAGE_HIGH_PRICE,
     "Cars with high mileage but strong pricing."),
    ("Average Price by Engine Type", AVG_PRICE_BY_ENGINE,
     "Average prices by engine type."),
    ("Year-Over-Year Price Trend", YEAR_OVER_YEAR_PRICE,
     "Price trends over time."),
    ("Rank Models by Price", RANK_MODELS_BY_PRICE,
     "Ranking models by price."),
    ("Recent Cars Partition", RECENT_CARS_PARTITION,
     "Partitioned recent cars summary."),
    ("Models with No Cars", MODELS_NO_CARS,
     "Models without listings."),
    ("Custom Clearance Distribution", CUSTOM_CLEARANCE_DISTRIBUTION,
     "Custom clearance status distribution.")
]

EXPLAIN_QUERIES = [
    ("EXPLAIN Avg Price by Manufacturer", EXPLAIN_AVG_PRICE_BY_MANUFACTURER),
    ("EXPLAIN Recent Cars Partition", EXPLAIN_RECENT_CARS_PARTITION)
]


@with_db_cursor(commit=False)
def generate_report(cur):
    sections = []

    for title, query, desc in BUSINESS_QUERIES:
        logger.info(title)
        df = run_query(cur, query)

        sections.append(f"""
        <div class="report-section">
            <h2>{title}</h2>
            <p>{desc}</p>
            {df.to_html(index=False, border=0, classes="table table-hover")}
        </div>
        """)

    for i, (title, query) in enumerate(EXPLAIN_QUERIES):
        plan = run_explain(cur, query)

        sections.append(f"""
        <div class="report-section">
            <h2>{title}</h2>
            <button class="btn btn-primary mb-3" data-bs-toggle="collapse" data-bs-target="#ex{i}">
                Show / Hide EXPLAIN
            </button>
            <div class="collapse" id="ex{i}">
                <pre>{plan}</pre>
            </div>
        </div>
        """)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{ content }}", "\n".join(sections))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    logger.info(f"Report generated → {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_report()
