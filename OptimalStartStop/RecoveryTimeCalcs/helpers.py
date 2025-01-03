import pandas as pd
import os


def save_results_to_csv(results, output_dir):
    """
    Save the results DataFrame as a CSV file in the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    csv_output_path = os.path.join(output_dir, "daily_results.csv")
    results.to_csv(csv_output_path, index=True)
    print(f"Results saved to {csv_output_path}")


def calculate_daily_setpoints(data, exclude_daytypes):
    """
    Calculate daily occupied and unoccupied thresholds for each day.
    """
    daily_stats = data.resample("D").agg({"SpaceTemp": ["min", "max", "mean"]})
    daily_stats.columns = ["min", "max", "mean"]

    thresholds = daily_stats[
        ~daily_stats.index.day_name().isin(exclude_daytypes)
    ].copy()
    thresholds["occupied_threshold"] = thresholds["max"]
    thresholds["unoccupied_threshold"] = thresholds["min"]
    return thresholds


def process_data_with_daily_setpoints(
    data,
    daily_setpoints,
    zone_temp_prox_thres,
    steep_increase_thres,
    rolling_window_size,
):
    """
    Process the data using daily thresholds for warm-up calculations.
    """
    # Ensure the day column is of the same type as the daily_setpoints index
    data["day"] = pd.to_datetime(data.index.date)

    for day, thresholds in daily_setpoints.iterrows():
        # Convert 'day' to the same type as 'data["day"]'
        day = pd.to_datetime(day)
        day_data = data[data["day"] == day].copy()  # Explicit copy to avoid warning
        if day_data.empty:
            print(f"No data for day: {day}. Skipping...")
            continue

        occupied_threshold = thresholds["occupied_threshold"]
        unoccupied_threshold = thresholds["unoccupied_threshold"]

        # Explicit use of .loc for assignments
        day_data.loc[:, "temp_steep_increase"] = (
            day_data["SpaceTemp"].diff() > steep_increase_thres
        ) & (day_data["SpaceTemp"] >= (unoccupied_threshold + zone_temp_prox_thres))
        day_data.loc[:, "near_occupied_threshold"] = (
            day_data["SpaceTemp"] >= (occupied_threshold - zone_temp_prox_thres)
        ) & (day_data["SpaceTemp"] <= (occupied_threshold + zone_temp_prox_thres))

        warm_up_active = False
        for row in day_data.itertuples():
            if row.temp_steep_increase:
                warm_up_active = True
            if row.near_occupied_threshold:
                warm_up_active = False
            data.loc[row.Index, "Warm_Up_Active"] = int(warm_up_active)

    data["Warm_Up_Active_Smoothed"] = (
        data["Warm_Up_Active"].rolling(window=rolling_window_size, center=True).sum()
    )
    data["Warm_Up_Active"] = (
        (data["Warm_Up_Active"] == 1) & (data["Warm_Up_Active_Smoothed"] > 1)
    ).astype(int)
    data.drop(columns=["Warm_Up_Active_Smoothed"], inplace=True)

    return data


def analyze_warm_up(
    data,
    start_date,
    end_date,
    exclude_daytypes,
    zone_temp_prox_thres,
    steep_increase_thres,
    rolling_window_size,
    dataset_min_per_time_step,
):
    """
    Analyze warm-up data for the specified date range.
    """
    print(f"\nAnalyzing warm-up for {start_date} to {end_date}...")
    subset_data = data.loc[start_date:end_date].copy()

    print("Step 1: Calculating daily setpoints...")
    daily_setpoints = calculate_daily_setpoints(subset_data, exclude_daytypes)

    print("Step 2: Processing data with daily setpoints...")
    subset_data = process_data_with_daily_setpoints(
        subset_data,
        daily_setpoints,
        zone_temp_prox_thres,
        steep_increase_thres,
        rolling_window_size,
    )

    print("Step 3: Calculating warm-up durations and results...")
    daily_warm_up_duration = subset_data["Warm_Up_Active"].resample("D").sum()
    daily_warm_up_duration_minutes = daily_warm_up_duration * dataset_min_per_time_step
    daily_4am_values = subset_data.between_time("04:00", "04:00").resample("D").first()

    results = pd.DataFrame(
        {
            "Warm_Up_Duration (minutes)": daily_warm_up_duration_minutes,
            "4AM SpaceTemp": daily_4am_values["SpaceTemp"],
            "4AM OaTemp": daily_4am_values["OaTemp"],
        }
    ).dropna()

    return subset_data, daily_setpoints, results
