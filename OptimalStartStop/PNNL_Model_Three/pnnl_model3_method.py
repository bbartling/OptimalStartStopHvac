import datetime as dt
import matplotlib.pyplot as plt

# Configuration Parameters
learning_rate= 0.1  # What is an optimal learning rate???

# Initialize Parameters
alpha_3a = 10  # Default time to change indoor temp by 1 degree
alpha_3b = 5  # Time interval for outdoor temp influence
alpha_3d = 0  # Dynamic adjustment for start time

# Historical data with sensor values recorded at 4 AM
historical_data = [
    {"zone_temp": 50, "outdoor_temp": 10, "warmup_time_minutes_history": 120},
    {"zone_temp": 48, "outdoor_temp": 12, "warmup_time_minutes_history": 115},
    {"zone_temp": 52, "outdoor_temp": 8, "warmup_time_minutes_history": 125},
    {"zone_temp": 50, "outdoor_temp": 11, "warmup_time_minutes_history": 118},
    {"zone_temp": 51, "outdoor_temp": 9, "warmup_time_minutes_history": 122},
    {"zone_temp": 49, "outdoor_temp": 13, "warmup_time_minutes_history": 110},
    {"zone_temp": 47, "outdoor_temp": 14, "warmup_time_minutes_history": 108},
]

# 4AM Conditions Check
current_conditions = {
    "zone_temp": 48,  # Current indoor temperature
    "outdoor_temp": 12,  # Current outdoor temperature
    "occupied_set_point": 70,  # Occupied temperature setpoint
}


def compute_minutes(alpha, alpha_new, learning_rate):
    return alpha + learning_rate * (alpha_new - alpha)


def calculate_optimal_start(current_conditions, alpha_3a, alpha_3b, alpha_3d):
    """Calculate optimal start time based on Model 3."""
    T_sp = current_conditions["occupied_set_point"]
    T_z = current_conditions["zone_temp"]
    T_o = current_conditions["outdoor_temp"]

    t_opt = (
        alpha_3a * (T_sp - T_z)
        + alpha_3b * (T_sp - T_z) * (T_sp - T_o) / alpha_3b
        + alpha_3d
    )

    return t_opt


def update_parameters(historical_data, learning_rate):
    """Update parameters alpha_3a, alpha_3b, and alpha_3d using historical data."""
    global alpha_3a, alpha_3b, alpha_3d

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

        alpha_3a = compute_minutes(alpha_3a, alpha_3a_new, learning_rate)
        alpha_3b = compute_minutes(alpha_3b, alpha_3b_new, learning_rate)
        alpha_3d = compute_minutes(alpha_3d, alpha_3d_new, learning_rate)


# Update parameters based on historical data
update_parameters(historical_data, learning_rate)

# Calculate optimal start time for current conditions
optimal_start_time = calculate_optimal_start(
    current_conditions, alpha_3a, alpha_3b, alpha_3d
)

# Log the raw optimal start time in minutes
print(f"Optimal Start Time in Minutes: {optimal_start_time:.2f}")

# Log the tuned parameters
print(
    f"Parameters: alpha_3a={alpha_3a:.2f}, alpha_3b={alpha_3b:.2f}, alpha_3d={alpha_3d:.2f}"
)
