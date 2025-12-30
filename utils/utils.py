from ydata_profiling import ProfileReport
import os
import sys

def write_in_csv(data, seperator, path):
        data = data.text.split(seperator)

        for info in data:
            with open(path, "a") as f:
                f.write(info)
                f.write("\n")
                

def create_data_report(df, title, path):
     profile = ProfileReport(df, title=title, explorative=True)
     profile.to_file(path)

def miles_to_km(row):
        
    if "մղոն" in row["Mileage"]:
        distance = float(row["Mileage"].split()[0])
        return distance * 1.60934
    else:
        return row["Mileage"]
    
def check_file_exists(file_path):
     if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8"):
            pass 

def root_path():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)