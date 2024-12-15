import pandas as pd
from utils import Schedule, TemperatureSensor, FanStatus, OptimalStartStop


def simulate_optimal_start_stop(csv_file):
    # Load the CSV file
    data = pd.read_csv(csv_file, skiprows=1)
    data.columns = ["timestamp", "SpaceTemp", "OutsideAirTemp", "FanStatus"]
    data = data[~data["timestamp"].str.contains("timestamp", na=False)]
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data = data.dropna(subset=["timestamp"])
    data = data.reset_index(drop=True)

    # Instantiate classes
    schedule = Schedule()
    outside_temp_sensor = TemperatureSensor()
    space_temp_sensor = TemperatureSensor()
    fan_status = FanStatus()
    oss = OptimalStartStop(
        comfort_limits=(68, 74, 71),  # Example comfort limits
        schedule=schedule,
        outside_temp_sensor=outside_temp_sensor,
        space_temp_sensor=space_temp_sensor,
        fan_status=fan_status,
    )

    # Simulate equipment startup
    for _, row in data.iterrows():
        # Update sensor data
        outside_temp_sensor.update_temperature(row["OutsideAirTemp"])
        space_temp_sensor.update_temperature(row["SpaceTemp"])
        fan_status.update_status(row["FanStatus"] == 1)

        # Simulate equipment start in the "active" block
        if schedule.current_action() == "active":
            # Trigger the optimal start logic
            oss.execute_optimal_start_stop()

    # Print cached warm-up data
    print("Fan Start Cache:", fan_status.get_start_cache())


# Run the simulation with the CSV file
simulate_optimal_start_stop("Cold_Snap_Data.csv")
