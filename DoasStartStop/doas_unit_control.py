import time
from datetime import datetime

# Configuration Parameters
BUILDING_START_TIME = "07:00"  # Building start time (24-hour format)
BUILDING_END_TIME = "18:00"    # Building end time (24-hour format)
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Occupied days
OVERRIDE_COMMAND = "DOAS_Off"
RELEASE_COMMAND = "Release_Control"

# Helper Functions
def is_building_occupied(current_time):
    """Check if the building is occupied based on the schedule."""
    current_day = current_time.strftime("%A")
    current_hour_minute = current_time.strftime("%H:%M")

    if current_day in DAYS_OF_WEEK:
        return BUILDING_START_TIME <= current_hour_minute <= BUILDING_END_TIME
    return False

# Main Logic
def control_doas():
    """Control the DOAS unit based on the building occupancy schedule."""
    while True:
        current_time = datetime.now()
        occupied = is_building_occupied(current_time)

        if occupied:
            print(f"{current_time}: Building is occupied. {RELEASE_COMMAND}")
        else:
            print(f"{current_time}: Building is unoccupied. {OVERRIDE_COMMAND}")

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    print("Starting DOAS Unit Control...")
    control_doas()
