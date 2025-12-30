import csv
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.utils import check_file_exists
from config.logging_config import get_logger

logger = get_logger(__name__)

class DataWrangler:
    def __init__(self):
        self.sep = ["$", "Պ", "պ", "֏", "€"]

        self.raw_file = os.path.join(PROJECT_ROOT, "data", "raw", "data.csv")
        self.filtered_file = os.path.join(PROJECT_ROOT, "data", "processed", "filtered_rows.csv")
        self.grouped_file = os.path.join(PROJECT_ROOT, "data", "processed", "groupe_per_car.csv")
        self.to_clean_file = os.path.join(PROJECT_ROOT, "data", "processed", "to_clean.csv")

        self._prepare_files()

    def _prepare_files(self):
        check_file_exists(self.filtered_file)
        check_file_exists(self.to_clean_file)

    def filter_rows(self):
        with open(self.filtered_file, "a") as file:
            with open(self.raw_file) as file1:
                for row in file1:
                    if not row.strip():
                        file.write("\n")

                    if row[0] in self.sep:
                        file.write(row)
                    else:
                        try:
                            if int(row[0]):
                                file.write(row)
                        except Exception:
                            pass

    def group_per_car(self):
        with open(self.filtered_file, "r") as file:
            lines = file.readlines()

        data = []
        temp_list = []

        for line in lines:
            if not line.strip():
                if temp_list:
                    data.append(temp_list)
                    temp_list = []
            else:
                temp_list.append(line.strip())

        data.append(temp_list)

        with open(self.grouped_file, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for row in data:
                writer.writerow(row)

    def clean_rows(self):
        with open(self.grouped_file, "r") as file, open(
            self.to_clean_file, "a"
        ) as file1:

            file1.write(",")

            try:
                for line in file:
                    line = line.split(",")

                    line[1] = line[1].replace("  ", ",")
                    line[1] = line[1].replace(" ", ",", 1)

                    for i in range(len(line)):
                        line[i] = line[i].replace('"', "")

                    line.remove(line[-2])

                    if len(line[-2]) > 12:
                        line.remove(line[-2])

                    for item in line[3:]:
                        try:
                            if item[1].isdigit() or item[1].isascii():
                                line.remove(item)
                        except Exception:
                            pass

                    if len(line) > 9:
                        line.remove(line[-2])

                    for item in line:
                        if len(line) != 9:
                            break
                        file1.write(item)
                        file1.write(",")

            except:
                pass

    def run(self):
        self.filter_rows()
        self.group_per_car()
        self.clean_rows()


if __name__ == "__main__":
    wrangler = DataWrangler()
    wrangler.run()
