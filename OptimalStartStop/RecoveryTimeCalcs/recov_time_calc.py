import os
import pandas as pd
import matplotlib.pyplot as plt

# Exclude days of the week when the building is unoccupied control
EXCLUDE_DAYTYPES = ["Saturday", "Sunday", "Monday"]

# Threshold for rule based logic to start or stop when temperature
# is within this parameter of the calculated unocc or occ zone
# temperature setpoint
ZONE_TEMP_PROX_THRES = 0.5 # °F

# Steep increases in temp when the heat turns on
# Calculated from a delta temp for each time step
STEEP_INCREASE_THRES = 0.5 # °F

# Attempt to rule out outliers or false calculations
ROLLING_WINDOW_SIZE = 3

# Dataset time interval
DATASET_MIN_PER_TIME_STEP = 5

# Directory to save plots and CSV data
OUTPUT_DIR = "Analysis_Results"

def wrangle_data(data, start_date, end_date):
    subset_data = data.loc[start_date:end_date].copy()
    subset_data.loc[:, "day_of_week"] = subset_data.index.day_name()
    subset_data = subset_data[~subset_data["day_of_week"].isin(EXCLUDE_DAYTYPES)]
    daily_stats = subset_data["SpaceTemp"].resample("D").agg(["min", "max", "mean"])

    print()
    print("Calculated Zone Temperature Setpoints...")
    occupied_threshold = daily_stats["max"].mean()
    print(f"occupied_threshold: {occupied_threshold:.2f}") 
    unoccupied_threshold = daily_stats["min"].mean()
    print(f"unoccupied_threshold: {unoccupied_threshold:.2f}") 

    # Start of the heating increase
    subset_data.loc[:, "temp_steep_increase"] = (
        (subset_data["SpaceTemp"].diff() > STEEP_INCREASE_THRES)
        &  (subset_data["SpaceTemp"] >= (unoccupied_threshold + ZONE_TEMP_PROX_THRES))
    )
    # Stop of the heating increase
    subset_data.loc[:, "near_occupied_threshold"] = (
        (subset_data["SpaceTemp"] >= (occupied_threshold - ZONE_TEMP_PROX_THRES))
        & (subset_data["SpaceTemp"] <= (occupied_threshold + ZONE_TEMP_PROX_THRES))
    )

    subset_data.loc[:, "in_warm_up_phase"] = False
    warm_up_active = False
    for row in subset_data.itertuples():
        if row.temp_steep_increase:
            warm_up_active = True
        if row.near_occupied_threshold:
            warm_up_active = False
        subset_data.loc[row.Index, "in_warm_up_phase"] = warm_up_active

    subset_data["Warm_Up_Active"] = subset_data["in_warm_up_phase"].astype(int)

    # attempt to remove false data
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

    return subset_data, occupied_threshold, unoccupied_threshold


def save_results_to_csv(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    csv_output_path = os.path.join(output_dir, "daily_results.csv")
    results.to_csv(csv_output_path)
    print(f"Results saved to {csv_output_path}")


def plot_line_chart(subset_data, occupied_threshold, unoccupied_threshold, output_dir):
    line_plot_path = os.path.join(output_dir, "SpaceTemp_Plot.png")
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
    plt.title("SpaceTemp with Warm_Up_Active", fontsize=16)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Temperature (°F)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(line_plot_path)
    plt.close()
    print(f"Line plot saved to {line_plot_path}")

def plot_bar_chart(results, output_dir):
    bar_plot_path = os.path.join(output_dir, "Warm_Up_Bar_Plot.png")
    fig, ax1 = plt.subplots(figsize=(15, 7))

    ax1.bar(
        results.index,
        results["Warm_Up_Duration (minutes)"],
        color="skyblue",
        label="Warm-Up Duration (minutes)",
        alpha=0.8,
    )
    ax1.set_ylabel("Warm-Up Duration (minutes)", fontsize=12)
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_title("Warm-Up Duration with 4AM Temperatures", fontsize=16)
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.scatter(
        results.index,
        results["4AM OaTemp"],
        color="red",
        label="4AM OaTemp",
        zorder=5,
    )
    ax2.scatter(
        results.index,
        results["4AM SpaceTemp"],
        color="green",
        label="4AM SpaceTemp",
        zorder=5,
    )
    ax2.set_ylabel("Temperature (°F)", fontsize=12)

    fig.legend(loc="upper right", bbox_to_anchor=(1, 0.95), bbox_transform=ax1.transAxes)
    plt.tight_layout()
    plt.savefig(bar_plot_path)
    plt.close()
    print(f"Bar plot with additional data saved to {bar_plot_path}")

def plot_temperature_distribution(subset_data, output_dir, label):
    # Simple Histogram Plot
    simple_hist_path = os.path.join(output_dir, f"Histogram.png")
    plt.figure(figsize=(12, 6))
    subset_data["SpaceTemp"].plot(kind="hist", bins=30, alpha=0.8, color="blue")
    plt.title(f"Temperature Histogram ({label})", fontsize=16)
    plt.xlabel("Space Temperature (°F)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(simple_hist_path)
    plt.close()
    print(f"Simple histogram plot saved to {simple_hist_path}")

def analyze_warm_up(data, start_date, end_date, output_subdir):
    subset_data, occupied_threshold, unoccupied_threshold = wrangle_data(
        data, start_date, end_date
    )

    daily_warm_up_duration = subset_data["Warm_Up_Active"].resample("D").sum()
    daily_warm_up_duration_minutes = daily_warm_up_duration * DATASET_MIN_PER_TIME_STEP

    daily_4am_values = subset_data.between_time("04:00", "04:00").resample("D").first()
    results = pd.DataFrame(
        {
            "Warm_Up_Duration (minutes)": daily_warm_up_duration_minutes,
            "4AM SpaceTemp": daily_4am_values["SpaceTemp"],
            "4AM OaTemp": daily_4am_values["OaTemp"],
        }
    ).dropna().query("`Warm_Up_Duration (minutes)` > 0")

    print()
    print(results)
    print()

    save_results_to_csv(results, output_subdir)
    plot_line_chart(subset_data, occupied_threshold, unoccupied_threshold, output_subdir)
    plot_bar_chart(results, output_subdir)
    plot_temperature_distribution(subset_data, output_subdir, f"{start_date}_to_{end_date}")


if __name__ == "__main__":
    cold_snap_data = pd.read_csv("Jan_data.csv")
    cold_snap_data["timestamp"] = pd.to_datetime(cold_snap_data["timestamp"])
    cold_snap_data.set_index("timestamp", inplace=True)

    time_ranges = {
        "Four_Days_V1": ("2024-01-14", "2024-01-18"),
        "Four_Days_V2": ("2024-01-01", "2024-01-04"),
        "One_week": ("2024-01-10", "2024-01-18"),
        "Two_weeks": ("2024-01-01", "2024-01-18"),
    }
    for label, (start, end) in time_ranges.items():
        print(f"\nAnalyzing: {label}")
        output_subdir = os.path.join(OUTPUT_DIR, label)
        analyze_warm_up(cold_snap_data, start, end, output_subdir)
