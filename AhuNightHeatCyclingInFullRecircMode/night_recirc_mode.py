import time
from datetime import datetime

# Configuration Parameters
BUILDING_START_TIME = "07:00"  # Building start time (24-hour format)
BUILDING_END_TIME = "18:00"    # Building end time (24-hour format)
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Occupied days
OVERRIDE_COMMAND = "Dampers_Closed"
RELEASE_COMMAND = "Release_Control"

# Current System State
AHU_ACTIVE = False  # Simulate the AHU's activity status

# Helper Functions
def is_building_occupied(current_time):
    """Check if the building is occupied based on the schedule."""
    current_day = current_time.strftime("%A")
    current_hour_minute = current_time.strftime("%H:%M")

    if current_day in DAYS_OF_WEEK:
        return BUILDING_START_TIME <= current_hour_minute <= BUILDING_END_TIME
    return False

# Main Logic
def control_ahu_dampers():
    """Control AHU dampers based on occupancy and AHU status."""
    while True:
        current_time = datetime.now()
        occupied = is_building_occupied(current_time)

        if not occupied and AHU_ACTIVE:
            print(f"{current_time}: Building is unoccupied. AHU is active. {OVERRIDE_COMMAND}")
        elif occupied:
            print(f"{current_time}: Building is occupied. {RELEASE_COMMAND}")
        else:
            print(f"{current_time}: Building is unoccupied. AHU is inactive. No action required.")

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    print("Starting Night Recirculation Mode Control...")
    control_ahu_dampers()
