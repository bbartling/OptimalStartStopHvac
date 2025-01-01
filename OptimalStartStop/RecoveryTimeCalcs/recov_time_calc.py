import pandas as pd
import matplotlib.pyplot as plt

# Degrees to indicate temp has warmed up close enough to setpoint
OCC_ZONE_TEMP_PROX_THRES = 0.5

# Detect steep increases like when the heat comes on
STEEP_INCREASE_THRES = 0.5

# Rolling window to attempt to exclude outliers
ROLLING_WINDOW_SIZE = 3

# Data set time interval
DATASET_MIN_PER_TIME_STEP = 5

# Load the data
cold_snap_data = pd.read_csv("Cold_Snap_Data.csv")

# Convert timestamp to datetime for easier manipulation
cold_snap_data["timestamp"] = pd.to_datetime(cold_snap_data["timestamp"])

# Set the timestamp as the index for resampling purposes
cold_snap_data.set_index("timestamp", inplace=True)

# Calculate daily occupied and unoccupied setpoints
daily_stats = cold_snap_data["SpaceTemp"].resample("D").agg(["min", "max", "mean"])

# Define thresholds
occupied_threshold = daily_stats[
    "max"
].mean()  # Assume max temps represent occupied periods
unoccupied_threshold = daily_stats[
    "min"
].mean()  # Assume min temps represent unoccupied periods

print("occupied_threshold: ", occupied_threshold)
print("unoccupied_threshold: ", unoccupied_threshold)
print()

# Identify steep increases
cold_snap_data["temp_steep_increase"] = (
    cold_snap_data["SpaceTemp"].diff() > STEEP_INCREASE_THRES
)

# Identify points near the occupied threshold
cold_snap_data["near_occupied_threshold"] = (
    cold_snap_data["SpaceTemp"] >= (occupied_threshold - OCC_ZONE_TEMP_PROX_THRES)
) & (cold_snap_data["SpaceTemp"] <= (occupied_threshold + OCC_ZONE_TEMP_PROX_THRES))

# Initialize a column to track the warm-up phase
cold_snap_data["in_warm_up_phase"] = False

# Use a loop to track warm-up phases and turn off once stabilized
warm_up_active = False
for i in range(len(cold_snap_data)):
    if cold_snap_data["temp_steep_increase"].iloc[i]:
        warm_up_active = True  # Warm-up begins when there's a steep increase
    if cold_snap_data["near_occupied_threshold"].iloc[i]:
        warm_up_active = False  # Warm-up ends when close to the occupied threshold
    # Use .loc to avoid chained assignment warnings
    cold_snap_data.loc[cold_snap_data.index[i], "in_warm_up_phase"] = warm_up_active

# Set Warm_Up_Active based on the tracked warm-up phase
cold_snap_data["Warm_Up_Active"] = cold_snap_data["in_warm_up_phase"].astype(int)

# Create a rolling window to check for isolated True values
# Adjust based on the expected duration of a warm-up phase
cold_snap_data["Warm_Up_Active_Smoothed"] = (
    cold_snap_data["Warm_Up_Active"]
    .rolling(window=ROLLING_WINDOW_SIZE, center=True)
    .sum()
)

# Convert isolated True values (with fewer neighbors) to False
cold_snap_data["Warm_Up_Active"] = (
    (cold_snap_data["Warm_Up_Active"] == 1)
    & (
        cold_snap_data["Warm_Up_Active_Smoothed"] > 1
    )  # Keep points with at least one neighbor
).astype(int)

# Drop the intermediate smoothing column
cold_snap_data.drop(columns=["Warm_Up_Active_Smoothed"], inplace=True)

# Identify problematic points
problematic_points = cold_snap_data[
    (cold_snap_data["Warm_Up_Active"] == 1)
    & (cold_snap_data["Warm_Up_Active"].shift(1) == 0)
    & (cold_snap_data["Warm_Up_Active"].shift(-1) == 0)
]

# Print the number of problematic points
print(f"\nNumber of problematic points: {len(problematic_points)}")
if not problematic_points.empty:
    print(problematic_points[["SpaceTemp", "Warm_Up_Active"]])

# Plot SpaceTemp
plt.figure(figsize=(15, 7))
plt.plot(
    cold_snap_data.index,
    cold_snap_data["SpaceTemp"],
    label="SpaceTemp",
    color="blue",
    linewidth=1,
)

# Highlight Warm_Up_Active points
warm_up_points = cold_snap_data[cold_snap_data["Warm_Up_Active"] == 1]
plt.scatter(
    warm_up_points.index,
    warm_up_points["SpaceTemp"],
    color="red",
    label="Warm_Up_Active",
    zorder=5,
)

# Add threshold lines and shaded regions
plt.axhline(
    occupied_threshold, color="purple", linestyle="--", label="Occupied Threshold"
)
plt.axhline(
    unoccupied_threshold, color="gray", linestyle="--", label="Unoccupied Threshold"
)
plt.fill_between(
    cold_snap_data.index,
    unoccupied_threshold - 1,
    unoccupied_threshold + 1,
    color="gray",
    alpha=0.2,
    label="±1°F Unoccupied Range",
)
plt.fill_between(
    cold_snap_data.index,
    occupied_threshold - 1,
    occupied_threshold + 1,
    color="purple",
    alpha=0.2,
    label="±1°F Occupied Range",
)

# Add labels, legend, and grid
plt.title("SpaceTemp with Warm_Up_Active Stabilization", fontsize=16)
plt.xlabel("Timestamp", fontsize=12)
plt.ylabel("Temperature (°F)", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()

# ===============================
# Time Delta Calculation
# ===============================

# Resample to daily frequency and sum Warm_Up_Active
daily_warm_up_duration = cold_snap_data["Warm_Up_Active"].resample("D").sum()

# Convert duration from intervals to minutes (assuming 5-min intervals in data)
daily_warm_up_duration_minutes = daily_warm_up_duration * DATASET_MIN_PER_TIME_STEP

# Print daily warm-up durations
print("\nDaily Warm-Up Durations (minutes):")
print(daily_warm_up_duration_minutes)

# Plot the daily warm-up durations as a bar chart
plt.figure(figsize=(10, 6))
daily_warm_up_duration_minutes.plot(kind="bar", color="orange", alpha=0.7)
plt.title("Daily Warm-Up Duration", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Warm-Up Duration (minutes)", fontsize=12)
plt.grid(axis="y")
plt.tight_layout()

# Show the bar plot
plt.show()
