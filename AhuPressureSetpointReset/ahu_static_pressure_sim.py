import time
import random

# Configuration Parameters
SP0 = 0.5  # Initial static pressure setpoint in inches WC
SPmin = 0.50  # Minimum allowable static pressure
SPmax = 1.5  # Maximum allowable static pressure
Td = 5  # Delay timer in seconds for simulation
T = 2  # Time step in seconds for simulation
I = 2  # Number of ignored requests (top I dampers excluded)
SPtrim = -0.02  # Trim adjustment in inches WC
SPres = 0.06  # Response adjustment in inches WC
SPres_max = 0.15  # Maximum allowable response adjustment (inches WC)
HighDamperSpt = 0.85
NUM_DAMPERS = 40  # Fixed number of VAV box dampers for the simulation only

# Current System State
current_static_pressure = SP0
device_on = False


def calculate_requests(vav_dampers):
    """Calculate requests based on VAV damper positions being greater than or equal to HighDamperSpt."""
    sorted_dampers = sorted(vav_dampers, reverse=True)  # Sort descending
    ignored_dampers = sorted_dampers[:I]  # Top I dampers
    remaining_dampers = sorted_dampers[I:]  # Dampers after ignoring top I
    max_remaining_damper = max(remaining_dampers) if remaining_dampers else None

    num_requests = sum(1 for pos in remaining_dampers if pos >= HighDamperSpt)

    # Print results
    print(f"Ignored Damper Positions: {ignored_dampers}")
    if max_remaining_damper is not None:
        print(
            f"Max Damper Position (After Excluding Top {I}): {max_remaining_damper:.2f}"
        )
    else:
        print(f"No remaining dampers to evaluate after excluding the top {I}.")
    print(f"Net Requests (Factoring Ignored Dampers): {num_requests}")

    return num_requests


def adjust_static_pressure(current_pressure, num_requests):
    """
    Adjust the static pressure based on the number of requests.
    Trim if no requests, respond if requests exist.
    Limit adjustment to SPres_max.
    """
    total_adjustment = 0
    if num_requests == 0:
        # Calculate trim adjustment
        total_adjustment = SPtrim
    else:
        # Calculate response adjustment proportional to number of requests
        total_adjustment = SPres * num_requests

    # Cap the adjustment to SPres_max
    if total_adjustment > 0:
        total_adjustment = min(total_adjustment, SPres_max)
    elif total_adjustment < 0:
        total_adjustment = max(total_adjustment, -SPres_max)

    print(f"Total Adjustment is {total_adjustment} Inch WC")

    # Update the current pressure with capped adjustment
    current_pressure = max(SPmin, min(SPmax, current_pressure + total_adjustment))

    adjustment_type = "increased" if total_adjustment > 0 else "decreased"
    print(f"We need {'more' if total_adjustment > 0 else 'less'} static!...")
    return current_pressure, total_adjustment, adjustment_type


# Simulation
print("Starting AHU Static Pressure Simulation...")
print(f"Ignore Var Set to {I} for the simulation...")

time.sleep(Td)  # Initial delay
device_on = True

try:
    while device_on:
        # Generate exactly NUM_DAMPERS damper positions
        vav_dampers = [round(random.uniform(0.3, 0.95), 2) for _ in range(NUM_DAMPERS)]

        # Calculate the number of requests
        num_requests = calculate_requests(vav_dampers)

        # Adjust static pressure and determine adjustment type
        previous_pressure = current_static_pressure
        current_static_pressure, adjustment, adjustment_type = adjust_static_pressure(
            current_static_pressure, num_requests
        )

        # Print the results for this time step
        print(f"Previous Static Pressure Setpoint: {previous_pressure:.2f}” WC")
        print(
            f"Current Static Pressure Setpoint: {current_static_pressure:.2f}” WC ({adjustment_type})\n"
        )

        # Wait for the next time step
        time.sleep(T)
except KeyboardInterrupt:
    print("Simulation stopped.")
