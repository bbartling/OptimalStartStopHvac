import time
import random

# Configuration Parameters
SP0 = 60  # Initial SAT setpoint in °F
SPmin = 55  # Minimum SAT setpoint in °F
SPmax_default = 65  # Default maximum SAT setpoint in °F
high_oat_SPmax = 60  # Maximum SAT setpoint at high OAT
OATmin = 60  # Minimum outside air temperature in °F
OATmax = 70  # Maximum outside air temperature in °F
HighZoneTempSpt = 75  # Zone temperature threshold to generate cooling requests in °F

Td = 5  # Delay timer in seconds for simulation
T = 5  # Time step in seconds for simulation
I = 2  # Number of ignored requests (top I zones excluded)

SPtrim = +0.2  # Trim adjustment in °F
SPres = -0.3  # Response adjustment in °F
SPres_max = 1.0  # Maximum allowable response adjustment (inches °F)

NUM_ZONES = 40  # Fixed number of zones for simulation
current_SAT = SP0
device_on = False

# Helper Functions
def calculate_dynamic_SPmax(OAT):
    """
    Calculate the dynamic maximum SAT setpoint (SPmax) based on the OAT.
    Linearly decreases SPmax from SPmax_default to high_oat_SPmax as OAT rises from OATmin to OATmax.
    """
    if OAT <= OATmin:
        return SPmax_default
    elif OAT >= OATmax:
        return high_oat_SPmax
    else:
        # Linear interpolation
        return SPmax_default - ((SPmax_default - high_oat_SPmax) * ((OAT - OATmin) / (OATmax - OATmin)))

def calculate_requests(zone_temps):
    """
    Calculate requests based on zone temperatures being greater than or equal to HighZoneTempSpt.
    Also, print the ignored zone temperatures (top I) and the max zone temperature after excluding the top I.
    """
    sorted_temps = sorted(zone_temps, reverse=True)  # Sort descending
    ignored_temps = sorted_temps[:I]  # Top I temperatures
    remaining_temps = sorted_temps[I:]  # Temperatures after ignoring top I
    max_remaining_temp = max(remaining_temps) if remaining_temps else None

    num_requests = sum(1 for temp in remaining_temps if temp >= HighZoneTempSpt)

    # Print results
    print(f"Ignored Zone Temperatures: {', '.join(f'{temp:.2f}' for temp in ignored_temps)}")
    if max_remaining_temp is not None:
        print(f"Max Zone Temperature (After Excluding Top {I}): {max_remaining_temp:.2f}°F")
    else:
        print(f"No remaining zones to evaluate after excluding the top {I}.")
    print(f"Net Requests (Factoring Ignored Zones): {num_requests}")
    
    return num_requests

def adjust_SAT(current_SAT, num_requests, dynamic_SPmax):
    """
    Adjust the SAT based on the number of requests.
    Trim if no requests, respond if requests exist.
    Limit adjustment to SPres_max.
    """
    total_adjustment = 0
    if num_requests == 0:
        # Trim SAT
        total_adjustment = SPtrim
    else:
        # Respond by decreasing SAT
        total_adjustment = SPres * num_requests

    # Cap the adjustment to SPres_max
    if total_adjustment > 0:
        total_adjustment = min(total_adjustment, SPres_max)
    elif total_adjustment < 0:
        total_adjustment = max(total_adjustment, -SPres_max)

    print(f"Total Adjustment is {total_adjustment:.2f}°F")

    # Update the current SAT with capped adjustment
    current_SAT = max(SPmin, min(dynamic_SPmax, current_SAT + total_adjustment))

    adjustment_type = "increased" if total_adjustment > 0 else "decreased"
    print(f"We need {'less' if total_adjustment > 0 else 'more'} cooling!...")

    return current_SAT, total_adjustment, adjustment_type

# Simulation
print("Starting AHU Temperature Reset Simulation...")
print(f"High Zone Temperature Threshold: {HighZoneTempSpt}°F")
print(f"Ignore Var Set to {I} for the simulation...")
time.sleep(Td)  # Wait for delay timer

device_on = True
while device_on:
    # Simulate a fluctuating outside air temperature
    current_OAT = random.uniform(55, 75)
    dynamic_SPmax = calculate_dynamic_SPmax(current_OAT)  # Adjust SPmax based on OAT

    # Simulate zone temperatures
    # zone_temps can be a fixed number to simulate increase and decrese logic
    zone_temps = [random.uniform(65, 80) for _ in range(NUM_ZONES)]
    num_requests = calculate_requests(zone_temps)

    # Adjust SAT based on cooling requests
    previous_SAT = current_SAT
    current_SAT, adjustment, adjustment_type = adjust_SAT(current_SAT, num_requests, dynamic_SPmax)

    # Print the results for this time step
    print(f"Current OAT: {current_OAT:.2f}°F")
    print(f"Dynamic SPmax: {dynamic_SPmax:.2f}°F")
    print(f"Previous SAT Setpoint: {previous_SAT:.2f}°F")
    print(f"Current SAT Setpoint: {current_SAT:.2f}°F ({adjustment_type})\n")

    # Sleep for the time step
    time.sleep(T)
