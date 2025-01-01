import os
import pandas as pd
import matplotlib.pyplot as plt

# Days to exclude from calculations
# when building is unoccupied
EXCLUDE_DAYTYPES = ["Saturday", "Sunday", "Monday"]

# Degrees F closest to occupied setpoint or "occupied_threshold" calc
# to know when warmup is completed and stop calculating data
OCC_ZONE_TEMP_PROX_THRES = 0.5

# For each time step its a delta temp in Degrees F to flag
# when the heating system started based on sharp rises
# from the "unoccupied_threshold" calc
STEEP_INCREASE_THRES = 0.5

# Rolling window size for ignoring outliers
ROLLING_WINDOW_SIZE = 3

# Minutes per time step in dataset
DATASET_MIN_PER_TIME_STEP = 5
OUTPUT_DIR = "Analysis_Results"


def analyze_warm_up(data, start_date, end_date, output_subdir):
    os.makedirs(output_subdir, exist_ok=True)
    subset_data = data.loc[start_date:end_date].copy()  # Use .copy() to ensure it's a new DataFrame

    # Exclude specified day types
    subset_data.loc[:, "day_of_week"] = subset_data.index.day_name()  # Explicit assignment to avoid warnings
    subset_data = subset_data[~subset_data["day_of_week"].isin(EXCLUDE_DAYTYPES)]

    # Calculate daily thresholds
    daily_stats = subset_data["SpaceTemp"].resample("D").agg(["min", "max", "mean"])
    occupied_threshold = daily_stats["max"].mean()
    unoccupied_threshold = daily_stats["min"].mean()

    print(
        f"Occupied threshold: {occupied_threshold} \n",
        f"Unoccupied threshold: {unoccupied_threshold} \n",
    )

    # Identify steep increases and proximity to setpoint
    subset_data.loc[:, "temp_steep_increase"] = (
        subset_data["SpaceTemp"].diff() > STEEP_INCREASE_THRES
    )
    subset_data.loc[:, "near_occupied_threshold"] = (
        (subset_data["SpaceTemp"] >= (occupied_threshold - OCC_ZONE_TEMP_PROX_THRES))
        & (subset_data["SpaceTemp"] <= (occupied_threshold + OCC_ZONE_TEMP_PROX_THRES))
    )

    # Warm-up phase detection
    subset_data.loc[:, "in_warm_up_phase"] = False
    warm_up_active = False
    for i in range(len(subset_data)):
        if subset_data["temp_steep_increase"].iloc[i]:
            warm_up_active = True
        if subset_data["near_occupied_threshold"].iloc[i]:
            warm_up_active = False
        subset_data.loc[subset_data.index[i], "in_warm_up_phase"] = warm_up_active

    subset_data["Warm_Up_Active"] = subset_data["in_warm_up_phase"].astype(int)

    # Smoothing Warm-Up Active
    subset_data["Warm_Up_Active_Smoothed"] = (
        subset_data["Warm_Up_Active"]
        .rolling(window=ROLLING_WINDOW_SIZE, center=True)
        .sum()
    )
    subset_data["Warm_Up_Active"] = (
        (subset_data["Warm_Up_Active"] == 1)
        & (subset_data["Warm_Up_Active_Smoothed"] > 1)
    ).astype(int)
    subset_data.drop(columns=["Warm_Up_Active_Smoothed"], inplace=True)

    # Calculate daily warm-up duration
    daily_warm_up_duration = subset_data["Warm_Up_Active"].resample("D").sum()
    daily_warm_up_duration_minutes = daily_warm_up_duration * DATASET_MIN_PER_TIME_STEP

    # Extract 4AM SpaceTemp and OaTemp
    daily_4am_values = subset_data.between_time("04:00", "04:00").resample("D").first()
    results = pd.DataFrame(
        {
            "Warm_Up_Duration (minutes)": daily_warm_up_duration_minutes,
            "4AM SpaceTemp": daily_4am_values["SpaceTemp"],
            "4AM OaTemp": daily_4am_values["OaTemp"],
        }
    )

    # Filter out rows with zero or missing values
    results = results.dropna().query("`Warm_Up_Duration (minutes)` > 0")

    # Save results to CSV
    csv_output_path = os.path.join(output_subdir, "daily_results.csv")
    results.to_csv(csv_output_path)
    print(f"Results saved to {csv_output_path}")

    # Save plots
    # Line Plot
    line_plot_path = os.path.join(output_subdir, "SpaceTemp_Plot.png")
    plt.figure(figsize=(15, 7))
    plt.plot(
        subset_data.index,
        subset_data["SpaceTemp"],
        label="SpaceTemp",
        color="blue",
        linewidth=1,
    )
    plt.scatter(
        subset_data[subset_data["Warm_Up_Active"] == 1].index,
        subset_data[subset_data["Warm_Up_Active"] == 1]["SpaceTemp"],
        color="red",
        label="Warm_Up_Active",
        zorder=5,
    )
    plt.axhline(
        occupied_threshold, color="purple", linestyle="--", label="Occupied Threshold"
    )
    plt.axhline(
        unoccupied_threshold, color="gray", linestyle="--", label="Unoccupied Threshold"
    )
    plt.fill_between(
        subset_data.index,
        unoccupied_threshold - 1,
        unoccupied_threshold + 1,
        color="gray",
        alpha=0.2,
        label="±1°F Unoccupied Range",
    )
    plt.fill_between(
        subset_data.index,
        occupied_threshold - 1,
        occupied_threshold + 1,
        color="purple",
        alpha=0.2,
        label="±1°F Occupied Range",
    )
    plt.title(
        f"SpaceTemp with Warm_Up_Active ({start_date} to {end_date})", fontsize=16
    )
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Temperature (°F)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(line_plot_path)
    print(f"Line plot saved to {line_plot_path}")

    return results



# Main script
if __name__ == "__main__":
    # Load dataset
    cold_snap_data = pd.read_csv("Jan_data.csv")
    cold_snap_data["timestamp"] = pd.to_datetime(cold_snap_data["timestamp"])
    cold_snap_data.set_index("timestamp", inplace=True)

    # Perform analyses for different time ranges
    time_ranges = {
        "Four_Days": ("2024-01-14", "2024-01-18"),
        "One_week": ("2024-01-10", "2024-01-18"),
        "Two_weeks": ("2024-01-01", "2024-01-18"),
    }
    for label, (start, end) in time_ranges.items():
        print(f"\nAnalyzing: {label}")
        output_subdir = os.path.join(OUTPUT_DIR, label)
        analyze_warm_up(cold_snap_data, start, end, output_subdir)
