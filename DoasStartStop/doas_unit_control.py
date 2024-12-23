import time
from datetime import datetime, timedelta
import random

# Configuration Parameters
BUILDING_START_TIME = "07:00"  # Building start time (24-hour format)
BUILDING_END_TIME = "18:00"    # Building end time (24-hour format)
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Occupied days
OVERRIDE_COMMAND = "Command_DOAS_Off"
RELEASE_COMMAND = "Release_DOAS_Overrides"

# Helper Functions
def is_building_occupied(random_time):
    """Check if the building is occupied based on the schedule."""
    random_day = random_time.strftime("%A")
    random_hour_minute = random_time.strftime("%H:%M")

    if random_day in DAYS_OF_WEEK:
        return BUILDING_START_TIME <= random_hour_minute <= BUILDING_END_TIME
    return False

def generate_random_time_and_day():
    """Generate a random day and time for simulation purposes."""
    random_day = random.choice(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    return random_day, f"{random_hour:02}:{random_minute:02}"

# Main Logic
def control_doas():
    """Control the DOAS unit based on the building occupancy schedule."""
    while True:
        # Generate a random time and day for simulation
        random_day, random_time = generate_random_time_and_day()

        # Check if the generated time and day are within the building's schedule
        occupied = (
            random_day in DAYS_OF_WEEK
            and BUILDING_START_TIME <= random_time <= BUILDING_END_TIME
        )

        # Print whether the building is occupied or not
        if occupied:
            print(f"{random_day} {random_time}: Building is occupied. Release back to the BAS! {RELEASE_COMMAND}")
        else:
            print(f"{random_day} {random_time}: Building is unoccupied. Override the BAS! {OVERRIDE_COMMAND}")

        # Sleep for the time step
        time.sleep(2)  # for simulation purposes

if __name__ == "__main__":
    print("Starting DOAS Unit Control Simulation...")
    control_doas()
