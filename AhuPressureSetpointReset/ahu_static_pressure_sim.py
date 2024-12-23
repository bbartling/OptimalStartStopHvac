import time
import random

# Configuration Parameters
SP0 = 60  # Initial SAT setpoint in °F
SPmin = 55  # Minimum SAT setpoint in °F
SPmax = 65  # Maximum SAT setpoint in °F
OATmin = 60  # Minimum outside air temperature in °F
OATmax = 70  # Maximum outside air temperature in °F
HighZoneTempSpt = 75  # Zone temperature threshold to generate cooling requests in °F

Td = 2  # Delay timer in seconds for simulation
T = 1  # Time step in seconds for simulation
I = 2  # Number of ignored requests (top I zones excluded)

SPtrim = +0.2  # Trim adjustment in °F
SPres = -0.3  # Response adjustment in °F

NUM_ZONES = 10  # Fixed number of zones for simulation
current_SAT = SP0
device_on = False

# Helper Functions
def calculate_requests(zone_temps):
    """
    Calculate requests based on zone temperatures being greater than or equal to HighZoneTempSpt.
    Also, print the ignored zone temperatures (top I) and the max zone temperature after excluding the top I.
    """
    sorted_temps = sorted(zone_temps, reverse=True)  # Sort descending
    ignored_temps = sorted_temps[:I]  # Top I temperatures
    remaining_temps = sorted_temps[I:]  # Temperatures after ignoring top I
    max_remaining_temp = max(remaining_temps) if remaining_temps else None

    # Use a simple for loop to count requests
    num_requests = 0
    for temp in remaining_temps:
        if temp >= HighZoneTempSpt:
            num_requests += 1

    # Print results
    print(f"Ignored Zone Temperatures: {', '.join(f'{temp:.2f}' for temp in ignored_temps)}")
    if max_remaining_temp is not None:
        print(f"Max Zone Temperature (After Excluding Top {I}): {max_remaining_temp:.2f}°F")
    else:
        print(f"No remaining zones to evaluate after excluding the top {I}.")
    print(f"Net Requests (Factoring Ignored Zones): {num_requests}")
    
    return num_requests

def adjust_SAT(current_SAT, num_requests):
    """
    Adjust the SAT based on the number of requests.
    Trim if no requests, respond if requests exist.
    """
    if num_requests == 0:
        # Trim SAT
        adjustment = SPtrim
        current_SAT = min(SPmax, current_SAT + adjustment)  # SAT trim should not exceed SPmax
        print("We need less cooling!...")
    else:
        # Respond by decreasing SAT
        adjustment = SPres
        current_SAT = max(SPmin, current_SAT + adjustment)  # SAT decrease should not go below SPmin
        print("We need more cooling!...")
    return current_SAT, adjustment

# Simulation
print("Starting AHU Temperature Reset Simulation...")
print(f"High Zone Temperature Threshold: {HighZoneTempSpt}°F")
print(f"Ignore Var Set to {I} for the simulation...")
time.sleep(Td)  # Wait for delay timer

device_on = True
while device_on:
    # Simulate a fluctuating outside air temperature
    current_OAT = random.uniform(55, 75)
    
    # Simulate zone temperatures
    zone_temps = [random.uniform(65, 80) for _ in range(NUM_ZONES)]
    num_requests = calculate_requests(zone_temps)
    
    # Adjust SAT based on cooling requests
    previous_SAT = current_SAT
    current_SAT, adjustment = adjust_SAT(current_SAT, num_requests)
    adjustment_type = (
        "increased" if adjustment > 0 else "decreased"
    )
    
    # Print the results for this time step
    print(f"Current OAT: {current_OAT:.2f}°F")
    print(f"Previous SAT Setpoint: {previous_SAT:.2f}°F")
    print(f"Current SAT Setpoint: {current_SAT:.2f}°F ({adjustment_type})\n")
    
    # Sleep for the time step
    time.sleep(T)
