import csv
from datetime import datetime

# Function to parse all data into appropriate types
def process_all_data(data):
    for row in data:
        # Parse and replace timestamp with datetime object
        row["timestamp"] = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
        
        # Parse and convert other fields into proper types
        row["FanStatus"] = int(row["FanStatus"])  # Convert FanStatus to integer
        row["OutsideAirTemp"] = float(row["OutsideAirTemp"])  # Convert OutsideAirTemp to float
        row["SpaceTemp"] = float(row["SpaceTemp"])  # Convert SpaceTemp to float
    return data

def read_csv(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data