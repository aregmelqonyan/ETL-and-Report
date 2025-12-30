from scripts.scrapper import AutoAmScraper
from scripts.data_wrangling import DataWrangler
from scripts.data_cleaning import DataCleaner
from scripts.generate_report import generate_html_report
from scripts.create_db import initialize_database
from scripts.insert_db import insert_all_from_csv

scrapper = AutoAmScraper("data/raw/data.csv", start_page=1, end_page=10)
wrangler = DataWrangler()
cleaner = DataCleaner(
        input_path="data/processed/to_clean.csv",
        output_path="data/processed/output.csv",
    )

scrapper.scrape()
wrangler.run()
cleaner.run()

initialize_database()
insert_all_from_csv("data/processed/output.csv")
generate_html_report(report_file="docs/top_queries_report.html")