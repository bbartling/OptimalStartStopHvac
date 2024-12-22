import time
import random

# Configuration Parameters
SP0 = 0.5  # Initial static pressure setpoint in inches WC
SPmin = 0.15  # Minimum allowable static pressure
SPmax = 1.5  # Maximum allowable static pressure
Td = 5 * 60  # Delay timer in seconds (5 minutes)
T = 2 * 60  # Time step in seconds (2 minutes)
I = 2  # Number of ignored requests (top 2 VAV boxes)
SPtrim = -0.02  # Trim adjustment in inches WC
SPres = 0.04  # Response adjustment in inches WC
SPres_max = 0.06  # Max allowable response adjustment

# Current System State
current_static_pressure = SP0
device_on = False
requests = []

# Helper Functions
def calculate_requests(vav_dampers):
    """Simulate VAV damper positions and calculate requests."""
    requests = [pos for pos in vav_dampers if pos > 0.75 or pos < 0.5]
    return len(requests), requests

def adjust_static_pressure(current_pressure, R):
    """Adjust static pressure based on the number of requests."""
    if R <= 1:
        current_pressure = max(SPmin, current_pressure + SPtrim)
    else:
        adjustment = min(SPres * (R - I), SPres_max)
        current_pressure = min(SPmax, current_pressure + adjustment)
    return current_pressure

# Simulation
print("Starting AHU Static Pressure Simulation...")
time.sleep(Td)  # Wait for delay timer

device_on = True
while device_on:
    # Simulate VAV damper positions (random for demonstration)
    vav_dampers = [random.uniform(0.3, 0.9) for _ in range(10)]
    R, _ = calculate_requests(vav_dampers)
    
    # Adjust static pressure
    current_static_pressure = adjust_static_pressure(current_static_pressure, R)
    print(f"Current Static Pressure: {current_static_pressure:.2f}” WC")
    
    # Sleep for the time step
    time.sleep(T)
