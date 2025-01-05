import numpy as np

# Configuration Parameters
learning_rate = 0.01  # Learning rate for gradient descent
n_iterations = 1000  # Number of iterations for optimization
tolerance = 1e-6  # Convergence tolerance

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

# 4AM Conditions Check
current_conditions = {
    "zone_temp": 61.,  # Current indoor temperature
    "outdoor_temp": 1.,  # Current outdoor temperature
    "occupied_set_point": 70.,  # Occupied temperature setpoint
}

# Convert historical data to numpy arrays
T_sp = current_conditions["occupied_set_point"]
T_z = np.array([data["zone_temp"] for data in historical_data])
T_o = np.array([data["outdoor_temp"] for data in historical_data])
t_actual = np.array([data["warmup_time_minutes_history"] for data in historical_data])

# Gradient Descent for Parameter Updates
for iteration in range(n_iterations):
    # Predicted warmup time
    t_pred = (
        alpha_3a * (T_sp - T_z)
        + alpha_3b * (T_sp - T_z) * (T_sp - T_o) / alpha_3b
        + alpha_3d
    )

    # Compute the loss (Mean Squared Error)
    loss = np.mean((t_actual - t_pred) ** 2)

    # Compute gradients
    grad_alpha_3a = -2 * np.mean((t_actual - t_pred) * (T_sp - T_z))
    grad_alpha_3b = -2 * np.mean((t_actual - t_pred) * (T_sp - T_z) * (T_sp - T_o))
    grad_alpha_3d = -2 * np.mean(t_actual - t_pred)

    # Update parameters
    alpha_3a -= learning_rate * grad_alpha_3a
    alpha_3b -= learning_rate * grad_alpha_3b
    alpha_3d -= learning_rate * grad_alpha_3d

    # Monitor progress
    if iteration % 100 == 0 or iteration < 10:
        print(f"Iteration {iteration}: Loss = {loss:.6f}, alpha_3a = {alpha_3a:.4f}, alpha_3b = {alpha_3b:.4f}, alpha_3d = {alpha_3d:.4f}")

    # Check for convergence
    if loss < tolerance:
        print(f"Converged at iteration {iteration}: Loss = {loss:.6f}")
        break

# Output optimized parameters
print(f"Optimized Parameters: alpha_3a = {alpha_3a:.4f}, alpha_3b = {alpha_3b:.4f}, alpha_3d = {alpha_3d:.4f}")

# Function to calculate the optimal start time
def calculate_optimal_start_time(current_conditions, alpha_3a, alpha_3b, alpha_3d):
    T_sp = current_conditions["occupied_set_point"]
    T_z = current_conditions["zone_temp"]
    T_o = current_conditions["outdoor_temp"]

    # Optimal start time formula
    t_opt = (
        alpha_3a * (T_sp - T_z)
        + alpha_3b * (T_sp - T_z) * (T_sp - T_o) / alpha_3b
        + alpha_3d
    )
    return t_opt

# Calculate optimal start time using the optimized parameters
optimal_start_time = calculate_optimal_start_time(current_conditions, alpha_3a, alpha_3b, alpha_3d)

# Output the calculated optimal start time
print(f"Optimal Start Time for Current Conditions: {optimal_start_time:.2f} minutes")
