from utils import read_csv, process_all_data

# File path to the CSV data
csv_path = "./Cold_Snap_Data.csv"

building_start_hour = 8
earliest_start_hour = 6



# Read and process the CSV data
data = read_csv(csv_path)
data = process_all_data(data)

cache = {}
start_recording_cache = False

for row in data:
    # Get values directly from the dictionary
    outdoor_temp = row.get("OutsideAirTemp")
    space_temp = row.get("SpaceTemp")
    fan_status = row.get("FanStatus")
    timestamp = row.get("timestamp")
    hour = timestamp.hour
    minute = timestamp.minute

    # Handle cache recording logic based on FanStatus and time
    if fan_status == 1 and not start_recording_cache and earliest_start_hour <= hour < building_start_hour:
        start_recording_cache = True
        print(f"Starting cache: {hour:02}:{minute:02} (FanStatus = {fan_status}) (SpaceTemp = {space_temp}) (outdoor_temp = {outdoor_temp})")

    elif hour == building_start_hour and minute == 0:
        start_recording_cache = False
        print(f"Stopping cache: {hour:02}:{minute:02} (FanStatus = {fan_status}) (SpaceTemp = {space_temp}) (outdoor_temp = {outdoor_temp})")


