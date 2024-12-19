import datetime as dt
import matplotlib.pyplot as plt

# Configuration Parameters
forgetting_factor = 0.1  # Exponential smoothing factor
early_start_limit = 180  # Maximum early start time in minutes
late_start_limit = 10  # Minimum pre-start time in minutes

monday_morning_extra_time = 30

# Initialize Parameters
alpha_3a = 10  # Default time to change indoor temp by 1 degree
alpha_3b = 5  # Time interval for outdoor temp influence
alpha_3d = 0  # Dynamic adjustment for start time

# Historical data (fake data for 7 days)
historical_data = [
    {"zone_temp": 50, "outdoor_temp": 10, "warmup_time_minutes": 120},
    {"zone_temp": 48, "outdoor_temp": 12, "warmup_time_minutes": 115},
    {"zone_temp": 52, "outdoor_temp": 8, "warmup_time_minutes": 125},
    {"zone_temp": 50, "outdoor_temp": 11, "warmup_time_minutes": 118},
    {"zone_temp": 51, "outdoor_temp": 9, "warmup_time_minutes": 122},
    {"zone_temp": 49, "outdoor_temp": 13, "warmup_time_minutes": 110},
    {"zone_temp": 47, "outdoor_temp": 14, "warmup_time_minutes": 108},
]

# Current Conditions
current_conditions = {
    "zone_temp": 48,  # Current indoor temperature
    "outdoor_temp": 12,  # Current outdoor temperature
    "occupied_set_point": 70,  # Occupied temperature setpoint
}

def smooth_parameters(alpha, alpha_new, forgetting_factor):
    """Exponential smoothing for parameter updates."""
    return alpha + forgetting_factor * (alpha_new - alpha)

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

    t_opt = max(late_start_limit, min(t_opt, early_start_limit))
    return t_opt

def update_parameters(historical_data, forgetting_factor):
    """Update parameters alpha_3a, alpha_3b, and alpha_3d using historical data."""
    global alpha_3a, alpha_3b, alpha_3d

    for data in historical_data:
        T_sp = current_conditions["occupied_set_point"]
        T_z = data["zone_temp"]
        T_o = data["outdoor_temp"]
        t_actual = data["warmup_time_minutes"]

        alpha_3a_new = abs(t_actual / (T_sp - T_z))
        alpha_3b_new = abs(t_actual / ((T_sp - T_z) * (T_sp - T_o)))
        alpha_3d_new = t_actual - (
            alpha_3a_new * (T_sp - T_z)
            + alpha_3b_new * (T_sp - T_z) * (T_sp - T_o) / alpha_3b_new
        )

        alpha_3a = smooth_parameters(alpha_3a, alpha_3a_new, forgetting_factor)
        alpha_3b = smooth_parameters(alpha_3b, alpha_3b_new, forgetting_factor)
        alpha_3d = smooth_parameters(alpha_3d, alpha_3d_new, forgetting_factor)

        parameter_history.append(
            {"alpha_3a": alpha_3a, "alpha_3b": alpha_3b, "alpha_3d": alpha_3d}
        )

def plot_tuned_parameters(parameter_history):
    """
    Plot the evolution of alpha parameters over time using subplots.
    """
    days = list(range(1, len(parameter_history) + 1))
    alpha_3a_values = [p["alpha_3a"] for p in parameter_history]
    alpha_3b_values = [p["alpha_3b"] for p in parameter_history]
    alpha_3d_values = [p["alpha_3d"] for p in parameter_history]

    plt.figure(figsize=(15, 10))

    # Plot alpha_3a
    plt.subplot(3, 1, 1)
    plt.plot(days, alpha_3a_values, label="alpha_3a (Time per degree)")
    plt.xlabel("Day")
    plt.ylabel("Value")
    plt.title("Evolution of alpha_3a: Default time to change indoor temp by 1 degree")
    plt.legend()
    plt.grid(True)

    # Plot alpha_3b
    plt.subplot(3, 1, 2)
    plt.plot(days, alpha_3b_values, label="alpha_3b (Outdoor influence)", color="orange")
    plt.xlabel("Day")
    plt.ylabel("Value")
    plt.title("Evolution of alpha_3b: Time interval for outdoor temp influence")
    plt.legend()
    plt.grid(True)

    # Plot alpha_3d
    plt.subplot(3, 1, 3)
    plt.plot(days, alpha_3d_values, label="alpha_3d (Dynamic offset)", color="green")
    plt.xlabel("Day")
    plt.ylabel("Value")
    plt.title("Evolution of alpha_3d: Dynamic adjustment for start time")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Track parameter history
parameter_history = []

# Update parameters based on historical data
update_parameters(historical_data, forgetting_factor)

# Calculate optimal start time for current conditions
optimal_start_time = calculate_optimal_start(current_conditions, alpha_3a, alpha_3b, alpha_3d)

# Log the raw optimal start time in minutes
print(f"Optimal Start Time (in minutes before occupancy): {optimal_start_time:.2f}")

# Calculate the exact start time as a timestamp
current_time = dt.datetime.now()
start_time = current_time - dt.timedelta(minutes=optimal_start_time)

# Log the exact timestamp for when the HVAC should start
print(f"HVAC Start Timestamp: {start_time}")

# Optionally, calculate the time delta until the start time
if start_time > current_time:
    time_until_start = (start_time - current_time).total_seconds() / 60  # in minutes
    print(f"Time until HVAC Start: {time_until_start:.2f} minutes")
else:
    print("HVAC Start Time has already passed!")

# Log the tuned parameters
print(f"Parameters: alpha_3a={alpha_3a:.2f}, alpha_3b={alpha_3b:.2f}, alpha_3d={alpha_3d:.2f}")

# Plot the tuned parameters
plot_tuned_parameters(parameter_history)
