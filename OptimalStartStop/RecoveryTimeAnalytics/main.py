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
EXCLUDE_DAYTYPES = [] # ["Saturday", "Sunday", "Monday"]
WARMUP_WINDOWS_HOURS = [4,6,7,8,9,10]
ZONE_TEMP_PROX_THRES = 0.5  # °F
STEEP_INCREASE_THRES = 0.6  # °F
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
    subset_data = cold_snap_data.loc[start:end].copy()  # Original data retained for plotting

    # Create filtered data for calculations
    print("Step 1.1: Filtering data for warm-up window hours")
    filtered_data = subset_data[subset_data.index.hour.isin(WARMUP_WINDOWS_HOURS)].copy()
    if filtered_data.empty:
        print(f"[WARNING!] Filtered data is empty for time range {start} to {end}. Skipping analysis.")
        continue

    print("Step 2: Calculating daily setpoints...")
    daily_setpoints = calculate_daily_setpoints(filtered_data, EXCLUDE_DAYTYPES)
    print(daily_setpoints[["occupied_threshold", "unoccupied_threshold"]])

    print("Step 3: Processing data with daily setpoints...")
    filtered_data = process_data_with_daily_setpoints(
        filtered_data,
        daily_setpoints,
        ZONE_TEMP_PROX_THRES,
        STEEP_INCREASE_THRES,
        WARMUP_WINDOWS_HOURS,
    )

    print("Step 4: Analyzing warm-up data...")
    _, _, results = analyze_warm_up(
        filtered_data,  # Use filtered data for calculations
        start,
        end,
        EXCLUDE_DAYTYPES,
        ZONE_TEMP_PROX_THRES,
        STEEP_INCREASE_THRES,
        DATASET_MIN_PER_TIME_STEP,
        MAX_WARMUP_TIME_MINUTES,
        WARMUP_WINDOWS_HOURS,
    )

    # Merge Warm_Up_Active column back into subset_data for plotting
    print("Step 5: Merging Warm_Up_Active column back into subset_data for plotting...")
    subset_data = subset_data.merge(
        filtered_data[["Warm_Up_Active"]], how="left", left_index=True, right_index=True
    )
    subset_data["Warm_Up_Active"].fillna(0, inplace=True)  # Fill missing values with 0

    # Debug results
    if not results.empty:
        print("Results:")
        print(results.describe())

        # Ensure the output directory exists
        os.makedirs(output_subdir, exist_ok=True)

        # Save the results to the corresponding directory
        save_results_to_csv(results, output_subdir)

        # Generate plots using the full dataset (subset_data)
        print("Generating plots...")
        plot_line_chart(
            subset_data,  # Full data for plotting, now with Warm_Up_Active column
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
