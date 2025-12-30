import numpy as np
import pandas as pd
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.utils import create_data_report, miles_to_km


class DataCleaner:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.headers = [
            "Removable",
            "Price",
            "Year",
            "Make",
            "Model",
            "Mileage",
            "Body style",
            "Engine",
            "Gearbox",
            "Hand drive",
            "Color",
            "Custom cleared",
        ]

        self.df = None

    def load_data(self):
        self.df = pd.read_csv(
            self.input_path,
            engine="python",
            on_bad_lines="skip",
            header=None,
            names=self.headers,
        )

        self.df = self.df.iloc[:-1]
        self.df.drop("Removable", axis=1, inplace=True)

    def report_before(self):
        create_data_report(
            self.df,
            "Prev Cleaning Report",
            os.path.join(PROJECT_ROOT, "docs", "before_data_clean_report.html"),
        )

    def clean_price(self):
        self.df.loc[self.df["Price"] == "Պայմ.", "Price"] = np.nan
        self.df["Price"] = self.df["Price"].where(
            self.df["Price"].str.startswith("$"),
            np.nan,
        )
        self.df = self.df.dropna()

        self.df["Price"] = self.df["Price"].str.replace("$", "")
        self.df["Price"] = self.df["Price"].str.replace(" ", "")
        self.df["Price"] = self.df["Price"].astype(int)

    def clean_mileage(self):
        self.df["Mileage"] = self.df["Mileage"].str.replace("կմ", "")
        self.df["Mileage"] = self.df.apply(miles_to_km, axis=1)
        self.df["Mileage"] = self.df["Mileage"].astype(float)

    def encode_columns(self):
        self.df["Hand drive"] = np.where(
            self.df["Hand drive"] == " Ձախ",
            1,
            np.where(self.df["Hand drive"] == " Աջ", 0, np.nan),
        )
        self.df = self.df.dropna()

        self.df["Gearbox"] = np.where(
            self.df["Gearbox"] == " Մեխանիկական",
            1,
            np.where(self.df["Gearbox"] == " Ավտոմատ", 0, np.nan),
        )
        self.df = self.df.dropna()

        self.df["Custom cleared"] = np.where(
            self.df["Custom cleared"].str.strip() == "Մաքսազերծված",
            1,
            np.where(
                self.df["Custom cleared"].str.strip() == "մաքսազերծված չ",
                0,
                np.where(
                    self.df["Custom cleared"].str.strip() == "Աճուրդում",
                    2,
                    np.nan,
                ),
            ),
        )

        self.df = self.df.dropna()

        self.df["Custom cleared"] = self.df["Custom cleared"].astype(int)
        self.df["Hand drive"] = self.df["Hand drive"].astype(int)
        self.df["Gearbox"] = self.df["Gearbox"].astype(int)
        self.df["Engine"] = self.df["Engine"].astype(str).str.strip()
        self.df["Make"] = self.df["Make"].astype(str).str.strip()
        self.df["Model"] = self.df["Model"].astype(str).str.strip()
        self.df["Body style"] = self.df["Body style"].astype(str).str.strip()
        self.df["Color"] = self.df["Color"].astype(str).str.strip()

    def fix_tesla_engine(self):
        tesla_engine = (self.df["Make"] == "Tesla") & (
            self.df["Engine"] != " Էլեկտրական"
        )
        self.df.loc[tesla_engine, "Engine"] = " Էլեկտրական"

    def report_after(self):
        create_data_report(
            self.df,
            "After Cleaning Report",
            os.path.join(PROJECT_ROOT, "docs", "after_data_clean_report.html"),
        )

    def save(self):
        self.df.to_csv(
            self.output_path,
            index=False,
            encoding="utf-8-sig",
        )

    def run(self):
        self.load_data()
        self.report_before()
        self.clean_price()
        self.clean_mileage()
        self.encode_columns()
        self.fix_tesla_engine()
        self.report_after()
        self.save()


if __name__ == "__main__":
    input_csv = os.path.join(PROJECT_ROOT, "data", "processed", "to_clean.csv")
    output_csv = os.path.join(PROJECT_ROOT, "data", "processed", "output.csv")

    cleaner = DataCleaner(
        input_path=input_csv,
        output_path=output_csv,
    )
    cleaner.run()
