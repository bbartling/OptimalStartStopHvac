import time
import random

# Configuration Parameters
BUILDING_START_TIME = "07:00"  # Building start time (24-hour format)
BUILDING_END_TIME = "18:00"    # Building end time (24-hour format)
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Occupied days
OVERRIDE_COMMAND = "Dampers_Closed"
RELEASE_COMMAND = "Release_Control"
ECON_HIGH_LIMIT_TEMP = 60  # Maximum outdoor air temperature for enabling free cooling (°F)
ECON_LOW_LIMIT_TEMP = 50   # Minimum outdoor air temperature for enabling free cooling (°F)

# Helper Functions
def is_building_occupied(random_day, random_time):
    """Check if the building is occupied based on the schedule."""
    return random_day in DAYS_OF_WEEK and BUILDING_START_TIME <= random_time <= BUILDING_END_TIME

def is_free_cooling_enabled(OAT):
    """Check if the outdoor air temperature is within the free cooling range."""
    return ECON_LOW_LIMIT_TEMP <= OAT <= ECON_HIGH_LIMIT_TEMP

def generate_random_time_and_day():
    """Generate a random day and time for simulation purposes."""
    random_day = random.choice(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    return random_day, f"{random_hour:02}:{random_minute:02}"

# Main Logic
def control_ahu_dampers():
    """Control AHU dampers based on occupancy, AHU status, and OAT."""
    while True:
        # Generate random day, time, and AHU status
        random_day, random_time = generate_random_time_and_day()
        AHU_ACTIVE = random.choice([True, False])  # Randomly simulate AHU activity
        current_OAT = random.uniform(40, 70)  # Simulate fluctuating outdoor air temperature

        # Check if the building is occupied
        occupied = is_building_occupied(random_day, random_time)

        if not occupied:
            if AHU_ACTIVE:
                if is_free_cooling_enabled(current_OAT):
                    print(f"{random_day} {random_time}: Building is unoccupied. AHU is active. Free cooling enabled (OAT: {current_OAT:.2f}°F). {RELEASE_COMMAND}")
                else:
                    print(f"{random_day} {random_time}: Building is unoccupied. AHU is active. Free cooling disabled (OAT: {current_OAT:.2f}°F). {OVERRIDE_COMMAND}")
            else:
                print(f"{random_day} {random_time}: Building is unoccupied. AHU is inactive. No action required.")
        else:
            print(f"{random_day} {random_time}: Building is occupied. {RELEASE_COMMAND}")

        time.sleep(2)  # Sleep for simulation purposes

if __name__ == "__main__":
    print("Starting Night Recirculation Mode Control Simulation...")
    control_ahu_dampers()
