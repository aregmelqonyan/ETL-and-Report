# Project Cars

This repository contains a scraper, data wrangling, and database management system for car listings from [auto.am](https://auto.am).  
It also includes data cleaning, analysis, and automated HTML report generation.

---

## Features

- Scrape car listings from auto.am.
- Filter, group, and clean scraped data.
- Store data in a PostgreSQL database with proper schema and partitions.
- Generate HTML reports with business queries and EXPLAIN ANALYZE for performance.
- Logging for all scripts.

---

## Requirements

- Python 3.11+  
- PostgreSQL
- Google Chrome (for Selenium WebDriver)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aregmelqonyan/ETL-and-Report
```
2. Navigate to the project directory:
```bash
cd ETL-and-Report
```
3. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
4. Install the required packages:
```bash
pip install -r requirements.txt
pip install --upgrade setuptools
```

## Project Structure
```
ETL-and-Report/
├── data/                  # Raw and processed CSV files
│   ├── raw/               # Raw scraped CSVs
│   └── processed/         # Cleaned and processed CSVs
├── database/              # Database connection and queries
│   ├── db_connect.py
│   ├── insertion.py
│   └── queries/           # SQL queries (creation, selection, etc.)
├── scripts/
│   ├── create_db.py
│   ├── insert_db.py               # Scripts for scraping, cleaning, reports
│   ├── scrapper.py
│   ├── data_wrangling.py
│   ├── data_cleaning.py
│   └── generate_report.py
├── utils/                 # Utility functions
│   └── utils.py
├── config/                # Logging and config
│   └── logging_config.py
├── docs/                  # Generated HTML reports
├── logs/                  # Log files from scripts
├── requirements.txt
├── main.py
├── .gitignore              #.log, venv, etc.
└── README.md
```

## Usage (Run E2E all flow)
```bash
python main.py
```

## Usage (Sequentially)
```bash
python scripts/scrapper.py
python scripts/data_wrangling.py
python scripts/data_cleaning.py
python scripts/create_db.py
python scripts/insert_db.py
python scripts/generate_report.py
```

## Reports

The `docs/` folder contains three HTML files:  
1. **Before Cleaning(before_data_clean_report.html)** – report on the raw data before cleaning.  
2. **After Cleaning(after_data_clean_report.html)** – report on the data after cleaning.  
3. **Final Report(top_queries_report.html)** – report based on business queries.

## Data Folders

The following folders are **created automatically** when the `scrapper.py` script is executed:

- `data/raw/` – contains the raw scraped data  
- `data/processed/` – contains cleaned and processed data  

You do **not** need to create these folders manually.

## Database Configuration

Database connection information is stored in the `.env` file, which is **not tracked by Git**.  
You must create and configure this file with your PostgreSQL credentials, for example:

```env
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432


