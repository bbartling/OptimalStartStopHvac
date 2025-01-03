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
)

# Constants
EXCLUDE_DAYTYPES = ["Saturday", "Sunday", "Monday"]
ZONE_TEMP_PROX_THRES = 0.5  # °F
STEEP_INCREASE_THRES = 0.6  # °F
ROLLING_WINDOW_SIZE = 3
DATASET_MIN_PER_TIME_STEP = 5
OUTPUT_DIR = "Analysis_Results"

# Time ranges for analysis
time_ranges = {
    "Four_Days_V1": ("2024-01-14", "2024-01-18"),
    "Four_Days_V2": ("2024-01-01", "2024-01-04"),
    "One_week": ("2024-01-10", "2024-01-18"),
    "Two_weeks": ("2024-01-01", "2024-01-18"),
}

# Load data
cold_snap_data = pd.read_csv("Jan_data.csv")
cold_snap_data["timestamp"] = pd.to_datetime(cold_snap_data["timestamp"])
cold_snap_data.set_index("timestamp", inplace=True)

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
    )

    # Debug results
    if not results.empty:
        print("Results:")
        print(results)

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
    else:
        print(
            f"[ERROR!] Results are empty for time range {start} to {end}. \n",
            "SKIPPING ANY PLOTTING!!",
        )
