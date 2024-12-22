import time
import random

# Configuration Parameters
SP0 = 60  # Initial SAT setpoint in °F
SPmin = 55  # Minimum SAT setpoint in °F
SPmax = 65  # Maximum SAT setpoint in °F
OATmin = 60  # Minimum outside air temperature in °F
OATmax = 70  # Maximum outside air temperature in °F
Td = 10 * 60  # Delay timer in seconds (10 minutes)
T = 2 * 60  # Time step in seconds (2 minutes)

# Current System State
current_SAT = SP0
device_on = False
current_OAT = random.uniform(55, 75)  # Simulate current outside air temperature

# Helper Functions
def calculate_SAT(OAT):
    """Calculate SAT setpoint based on OAT."""
    if OAT <= OATmin:
        return SPmin
    elif OAT >= OATmax:
        return SPmax
    else:
        # Linear interpolation between SPmin and SPmax
        return SPmin + (SPmax - SPmin) * ((OAT - OATmin) / (OATmax - OATmin))

# Simulation
print("Starting AHU Temperature Reset Simulation...")
time.sleep(Td)  # Wait for delay timer

device_on = True
while device_on:
    # Simulate a fluctuating outside air temperature
    current_OAT = random.uniform(55, 75)
    
    # Calculate the new SAT setpoint
    current_SAT = calculate_SAT(current_OAT)
    print(f"Current OAT: {current_OAT:.2f}°F, Adjusted SAT: {current_SAT:.2f}°F")
    
    # Sleep for the time step
    time.sleep(T)
