import pandas as pd
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.logging_config import get_logger
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
from database.db_connect import with_db_cursor

REPORT_FILE = os.path.join(PROJECT_ROOT, "docs", "top_queries_report.html")

logger = get_logger(__name__)

def run_query(cur, query):
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    return pd.DataFrame(data, columns=columns)

def run_explain(cur, query):
    cur.execute(f"EXPLAIN ANALYZE {query}")
    return "\n".join(row[0] for row in cur.fetchall())

BUSINESS_QUERIES = [
    {"name": "Average Price by Manufacturer", "query": AVG_PRICE_BY_MANUFACTURER,
     "description": "Shows the average price of cars for each manufacturer to identify high-value brands."},
    {"name": "Top 5 Most Expensive Cars", "query": TOP_5_EXPENSIVE_CARS,
     "description": "Find the top 5 most expensive cars across all manufacturers."},
    {"name": "High Mileage & High Price Cars", "query": HIGH_MILEAGE_HIGH_PRICE,
     "description": "Identify cars that have high mileage but still maintain high market value."},
    {"name": "Average Price by Engine Type", "query": AVG_PRICE_BY_ENGINE,
     "description": "Analyze average prices for different engine types to inform pricing strategy."},
    {"name": "Year-Over-Year Price Trend", "query": YEAR_OVER_YEAR_PRICE,
     "description": "Show how average car prices change year over year to detect trends."},
    {"name": "Rank Models by Price", "query": RANK_MODELS_BY_PRICE,
     "description": "Rank models within each manufacturer by average price."},
    {"name": "Recent Cars Partition (2018-2024)", "query": RECENT_CARS_PARTITION,
     "description": "Aggregate summary for recent cars based on year partitioning."},
    {"name": "Models with No Cars", "query": MODELS_NO_CARS,
     "description": "List models that currently have no cars listed in the marketplace."},
    {"name": "Custom Clearance Distribution", "query": CUSTOM_CLEARANCE_DISTRIBUTION,
     "description": "Show distribution of custom clearance status for business compliance insights."},
]

EXPLAIN_QUERIES = [
    {"name": "EXPLAIN Average Price by Manufacturer", "query": EXPLAIN_AVG_PRICE_BY_MANUFACTURER,
     "description": "EXPLAIN ANALYZE for performance evaluation."},
    {"name": "EXPLAIN Recent Cars Partition", "query": EXPLAIN_RECENT_CARS_PARTITION,
     "description": "EXPLAIN ANALYZE for partition query optimization."},
]

@with_db_cursor(commit=False)
def generate_html_report(cur, report_file="car_marketplace_report.html"):
    html_sections = []

    html_sections.append("""
    <html>
    <head>
        <title>Car Marketplace Report</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
        <style>
            body { padding: 20px; font-family: Arial, sans-serif; }
            h1, h2 { margin-top: 30px; }
            pre { background-color: #f8f9fa; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
        <h1 class="text-center mb-4">Car Marketplace Business Report</h1>
    """)

    for q in BUSINESS_QUERIES:
        logger.info(f"Running query: {q['name']}")
        df = run_query(cur, q["query"])
        html_sections.append(f"<h2>{q['name']}</h2>")
        html_sections.append(f"<p>{q['description']}</p>")
        html_sections.append(df.to_html(index=False, border=0, classes="table table-striped table-hover"))

    for idx, q in enumerate(EXPLAIN_QUERIES):
        logger.info(f"Running EXPLAIN ANALYZE: {q['name']}")
        explain_text = run_explain(cur, q["query"])
        html_sections.append(f"""
        <h2>{q['name']}</h2>
        <p>{q['description']}</p>
        <button class="btn btn-sm btn-primary mb-2" type="button" data-bs-toggle="collapse" data-bs-target="#explain{idx}" aria-expanded="false" aria-controls="explain{idx}">
            Show/Hide EXPLAIN ANALYZE
        </button>
        <div class="collapse" id="explain{idx}">
            <pre>{explain_text}</pre>
        </div>
        """)

    html_sections.append("""
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_sections))

    logger.info(f"Beautiful HTML report generated: {report_file}")

if __name__ == "__main__":
    generate_html_report(report_file=REPORT_FILE)
