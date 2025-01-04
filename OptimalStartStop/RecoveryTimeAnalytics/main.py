import os
import pandas as pd
from helpers import (
    calculate_daily_setpoints,
    process_data_with_daily_setpoints,
    analyze_warm_up,
    save_results_to_csv,
)
from plotting_utils import (
    plot_line_chart,
    plot_bar_chart,
    plot_temperature_distribution,
    plot_degrees_per_hour,
    plot_relationship_matrix
)

# Constants
EXCLUDE_DAYTYPES = ["Saturday", "Sunday", "Monday"]
ZONE_TEMP_PROX_THRES = 0.5  # °F
STEEP_INCREASE_THRES = 0.6  # °F
ROLLING_WINDOW_SIZE = 3
DATASET_MIN_PER_TIME_STEP = 5
MAX_WARMUP_TIME_MINUTES = 230
OUTPUT_DIR = "Analysis_Results"

time_ranges = {
    "Four_Days_Jan_Cold_Snap": ("2024-01-14", "2024-01-18"),
    "Dec_Xmas_Break": ("2023-12-24", "2023-12-31"),
    "Four_Days_Jan_1": ("2024-01-01", "2024-01-04"),
    "One_Week_Jan": ("2024-01-10", "2024-01-18"),
    "Two_Weeks_Jan": ("2024-01-01", "2024-01-18"),
    "Xmas_Thru_March": ("2023-12-24", "2024-03-01"),
}

# Load data
cold_snap_data = pd.read_csv("AllData.csv")
cold_snap_data["timestamp"] = pd.to_datetime(cold_snap_data["timestamp"])
cold_snap_data.set_index("timestamp", inplace=True)

# Remove rows where SpaceTemp is 0
cold_snap_data = cold_snap_data[cold_snap_data["SpaceTemp"] != 0]

# Analyze each time range and generate plots
for label, (start, end) in time_ranges.items():
    print(f"\nAnalyzing: {label}")
    output_subdir = os.path.join(OUTPUT_DIR, label)

    # Step-by-step troubleshooting: Call functions explicitly
    print(f"Step 1: Filtering data for time range {start} to {end}")
    subset_data = cold_snap_data.loc[start:end].copy()

    print("Step 2: Calculating daily setpoints...")
    daily_setpoints = calculate_daily_setpoints(subset_data, EXCLUDE_DAYTYPES)
    print(daily_setpoints[["occupied_threshold", "unoccupied_threshold"]])

    print("Step 3: Processing data with daily setpoints...")
    subset_data = process_data_with_daily_setpoints(
        subset_data,
        daily_setpoints,
        ZONE_TEMP_PROX_THRES,
        STEEP_INCREASE_THRES,
        ROLLING_WINDOW_SIZE,
    )

    print("Step 4: Analyzing warm-up data...")
    subset_data, daily_setpoints, results = analyze_warm_up(
        cold_snap_data,
        start,
        end,
        EXCLUDE_DAYTYPES,
        ZONE_TEMP_PROX_THRES,
        STEEP_INCREASE_THRES,
        ROLLING_WINDOW_SIZE,
        DATASET_MIN_PER_TIME_STEP,
        MAX_WARMUP_TIME_MINUTES, 
    )

    # Debug results
    if not results.empty:
        print("Results:")
        print(results.describe())

        # Ensure the output directory exists
        os.makedirs(output_subdir, exist_ok=True)

        # Save the results to the corresponding directory
        save_results_to_csv(results, output_subdir)

        # Generate plots
        plot_line_chart(
            subset_data,
            daily_setpoints["occupied_threshold"].mean(),
            daily_setpoints["unoccupied_threshold"].mean(),
            output_subdir,
        )
        plot_bar_chart(results, output_subdir)
        plot_temperature_distribution(subset_data, output_subdir, f"{start}_to_{end}")
        plot_degrees_per_hour(results, output_subdir)
        plot_relationship_matrix(results, output_subdir)
    else:
        print(
            f"[ERROR!] Results are empty for time range {start} to {end}. \n",
            "SKIPPING ANY PLOTTING!!",
        )
