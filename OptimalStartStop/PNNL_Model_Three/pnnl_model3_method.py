

# Import required libraries
import datetime as dt
import matplotlib.pyplot as plt

# VOLTTRON-style EMA function
def ema(lst):
    smoothing_constant = 2.0 / (len(lst) + 1.0) * 2.0 if lst else 1.0
    smoothing_constant = smoothing_constant if smoothing_constant <= 1.0 else 1.0
    _sort = lst[::-1]
    ema_value = 0
    _sort = [item[1] if isinstance(item, list) else item for item in _sort]
    for n in range(len(lst)):
        ema_value += _sort[n] * smoothing_constant * (1.0 - smoothing_constant) ** n
    if _sort:
        ema_value += _sort[-1] * (1.0 - smoothing_constant) ** len(lst)
    return ema_value

# Calculate optimal start time
def calculate_optimal_start(current_conditions, alpha_3a, alpha_3b, alpha_3d):
    T_sp = current_conditions["occupied_set_point"]
    T_z = current_conditions["zone_temp"]
    T_o = current_conditions["outdoor_temp"]

    t_opt = (
        alpha_3a * (T_sp - T_z)
        + alpha_3b * (T_sp - T_z) * (T_sp - T_o) / alpha_3b
        + alpha_3d
    )

    t_opt = max(late_start_limit, min(t_opt, early_start_limit))
    return t_opt

# Configuration Parameters
early_start_limit = 180  # Maximum early start time in minutes
late_start_limit = 10  # Minimum pre-start time in minutes
max_days_of_data = 10
monday_morning_extra_time = 30

# Initialize Parameters
alpha_3a = 10  # Default time to change indoor temp by 1 degree
alpha_3b = 5  # Time interval for outdoor temp influence
alpha_3d = 0  # Dynamic adjustment for start time

# Historical data with sensor values recorded at 4 AM from writeup
historical_data = [
    {"zone_temp": 64.79, "outdoor_temp": 41.4, "warmup_time_minutes_history": 230},
    {"zone_temp": 65.36, "outdoor_temp": 34.07, "warmup_time_minutes_history": 185},
    {"zone_temp": 64.55, "outdoor_temp": 31.82, "warmup_time_minutes_history": 230},
    {"zone_temp": 64.96, "outdoor_temp": 32.45, "warmup_time_minutes_history": 180},
    {"zone_temp": 64.42, "outdoor_temp": 16.45, "warmup_time_minutes_history": 115},
    {"zone_temp": 64.98, "outdoor_temp": 31.13, "warmup_time_minutes_history": 120},
    {"zone_temp": 64.65, "outdoor_temp": 18.08, "warmup_time_minutes_history": 80},
    {"zone_temp": 65.0, "outdoor_temp": 21.57, "warmup_time_minutes_history": 100},
    {"zone_temp": 64.04, "outdoor_temp": 22.76, "warmup_time_minutes_history": 90},
    {"zone_temp": 65.06, "outdoor_temp": 34.21, "warmup_time_minutes_history": 105},
    {"zone_temp": 64.53, "outdoor_temp": 28.86, "warmup_time_minutes_history": 105},
    {"zone_temp": 65.46, "outdoor_temp": 24.96, "warmup_time_minutes_history": 105},
    {"zone_temp": 65.32, "outdoor_temp": 24.47, "warmup_time_minutes_history": 105},
    {"zone_temp": 64.01, "outdoor_temp": -19.69, "warmup_time_minutes_history": 100},
    {"zone_temp": 64.18, "outdoor_temp": -12.15, "warmup_time_minutes_history": 70},
    {"zone_temp": 63.92, "outdoor_temp": -1.38, "warmup_time_minutes_history": 55},
    {"zone_temp": 63.86, "outdoor_temp": -6.38, "warmup_time_minutes_history": 90},
    {"zone_temp": 64.13, "outdoor_temp": 15.82, "warmup_time_minutes_history": 70},
    {"zone_temp": 65.23, "outdoor_temp": 33.14, "warmup_time_minutes_history": 90},
    {"zone_temp": 65.39, "outdoor_temp": 35.38, "warmup_time_minutes_history": 90},
    {"zone_temp": 65.49, "outdoor_temp": 36.19, "warmup_time_minutes_history": 85},
    {"zone_temp": 65.54, "outdoor_temp": 36.33, "warmup_time_minutes_history": 100},
    {"zone_temp": 63.67, "outdoor_temp": 25.75, "warmup_time_minutes_history": 90},
    {"zone_temp": 65.44, "outdoor_temp": 38.1, "warmup_time_minutes_history": 150},
    {"zone_temp": 65.44, "outdoor_temp": 35.64, "warmup_time_minutes_history": 140},
    {"zone_temp": 65.59, "outdoor_temp": 34.44, "warmup_time_minutes_history": 115},
    {"zone_temp": 65.09, "outdoor_temp": 29.85, "warmup_time_minutes_history": 145},
    {"zone_temp": 63.98, "outdoor_temp": 20.11, "warmup_time_minutes_history": 100},
    {"zone_temp": 64.94, "outdoor_temp": 24.85, "warmup_time_minutes_history": 75},
    {"zone_temp": 65.34, "outdoor_temp": 31.96, "warmup_time_minutes_history": 90},
    {"zone_temp": 65.99, "outdoor_temp": 42.64, "warmup_time_minutes_history": 110},
    {"zone_temp": 66.23, "outdoor_temp": 38.37, "warmup_time_minutes_history": 205},
    {"zone_temp": 64.44, "outdoor_temp": 18.89, "warmup_time_minutes_history": 45},
    {"zone_temp": 64.51, "outdoor_temp": 25.65, "warmup_time_minutes_history": 40},
    {"zone_temp": 64.42, "outdoor_temp": 20.19, "warmup_time_minutes_history": 30},
    {"zone_temp": 64.98, "outdoor_temp": 35.78, "warmup_time_minutes_history": 45},
    {"zone_temp": 64.14, "outdoor_temp": 20.22, "warmup_time_minutes_history": 60},
    {"zone_temp": 64.26, "outdoor_temp": 15.92, "warmup_time_minutes_history": 25},
    {"zone_temp": 64.71, "outdoor_temp": 27.0, "warmup_time_minutes_history": 55},
    {"zone_temp": 65.0, "outdoor_temp": 45.58, "warmup_time_minutes_history": 70},
    {"zone_temp": 64.96, "outdoor_temp": 38.37, "warmup_time_minutes_history": 45},
    {"zone_temp": 64.77, "outdoor_temp": 37.15, "warmup_time_minutes_history": 50},
    {"zone_temp": 64.08, "outdoor_temp": 34.15, "warmup_time_minutes_history": 50},
    {"zone_temp": 64.81, "outdoor_temp": 50.33, "warmup_time_minutes_history": 60},
    {"zone_temp": 64.56, "outdoor_temp": 9.1, "warmup_time_minutes_history": 230},
    {"zone_temp": 64.12, "outdoor_temp": 7.42, "warmup_time_minutes_history": 45},
    {"zone_temp": 65.11, "outdoor_temp": 35.16, "warmup_time_minutes_history": 55},
]

# Limit historical data to the last 10 entries
historical_data = historical_data[-max_days_of_data:]


# Current Conditions
current_conditions = {
    "zone_temp": 48,  # Current indoor temperature
    "outdoor_temp": 12,  # Current outdoor temperature
    "occupied_set_point": 70,  # Occupied temperature setpoint
}

# Update parameters with EMA
def update_parameters(historical_data):
    global alpha_3a, alpha_3b, alpha_3d

    alpha_3a_list = []
    alpha_3b_list = []
    alpha_3d_list = []

    for data in historical_data:
        T_sp = current_conditions["occupied_set_point"]
        T_z = data["zone_temp"]
        T_o = data["outdoor_temp"]
        t_actual = data["warmup_time_minutes_history"]

        alpha_3a_new = abs(t_actual / (T_sp - T_z))
        alpha_3b_new = abs(t_actual / ((T_sp - T_z) * (T_sp - T_o)))
        alpha_3d_new = t_actual - (
            alpha_3a_new * (T_sp - T_z)
            + alpha_3b_new * (T_sp - T_z) * (T_sp - T_o) / alpha_3b_new
        )

        # Append new values to lists
        alpha_3a_list.append(alpha_3a_new)
        alpha_3b_list.append(alpha_3b_new)
        alpha_3d_list.append(alpha_3d_new)

    # Use EMA to update parameters
    alpha_3a = ema(alpha_3a_list)
    alpha_3b = ema(alpha_3b_list)
    alpha_3d = ema(alpha_3d_list)

# Update parameters using historical data
update_parameters(historical_data)

# Calculate optimal start time
optimal_start_time = calculate_optimal_start(current_conditions, alpha_3a, alpha_3b, alpha_3d)

# Log the results
print(f"Optimal Start Time in Minutes: {optimal_start_time:.2f}")
print(f"Parameters: alpha_3a={alpha_3a:.2f}, alpha_3b={alpha_3b:.2f}, alpha_3d={alpha_3d:.2f}")
