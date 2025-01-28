# Define constants
MIN_TEMP_DELTA = 10  # Temperature delta threshold (in °F) for mild economizer operation
FAULT_THRESHOLD = .20  # Fault condition time threshold (in minutes)
SETPOINT_ADJUST_INTERVAL = .5  # Time interval for setpoint adjustments (in minutes)
MIN_OA_SETPOINT_STEP = 1  # Increment percentage for decreasing minimum outside air setpoint
MAX_OA_SETPOINT = 100  # Upper limit for outside air setpoint (100%)
MIN_OA_SETPOINT = 0    # Lower limit for outside air setpoint (0%)
ALARM_THRESHOLD = 0.75 # Fraction of supply air that should be outside air for it to be flagged as over-ventilation

# Define data structures to simulate telemetry data
fault_data = {
    "vav_total_air_flow": [10000, 10050, 10025, 10075, 10030, 10020],
    "mix_air_temp": [30, 29.5, 30.5, 29.8, 30.2, 29.6],
    "out_air_temp": [10, 10.5, 10.2, 10.8, 10.3, 10.1],
    "return_air_temp": [72, 72.5, 72.2, 72.8, 72.3, 72.1],
    "fan_vfd_speed_col": [0.66, 0.67, 0.65, 0.66, 0.68, 0.67],
    "economizer_sig_col": [0.2] * 6,
}

# Simulation of the AHU's outside air damper setpoint
outside_air_setpoint = 50  # Start with a 50% outside air setpoint

# Define the function to calculate the outside air fraction
def calculate_oa_fraction(mix_air_temp, out_air_temp, return_air_temp):
    # Estimate outside air fraction using the temperature difference method
    return (return_air_temp - mix_air_temp) / (return_air_temp - out_air_temp)

# Define the function to detect over-ventilation based on outside air fraction
def detect_over_ventilation(oa_fraction, alarm_threshold=ALARM_THRESHOLD):
    return oa_fraction > alarm_threshold

# Function to adjust the minimum outside air setpoint downward
def adjust_oa_setpoint(current_setpoint, increment=MIN_OA_SETPOINT_STEP):
    # Ensure setpoint is within allowed limits
    new_setpoint = max(current_setpoint - increment, MIN_OA_SETPOINT)
    return new_setpoint

# Updated optimize_ahu_ventilation function
def optimize_ahu_ventilation(
    fault_data,
    fault_threshold=FAULT_THRESHOLD,
    adjust_interval=SETPOINT_ADJUST_INTERVAL,
    initial_setpoint=50  # Added parameter to pass the initial setpoint
):
    outside_air_setpoint = initial_setpoint  # Explicitly initialize the setpoint
    over_ventilation_start_time = None  # To track the start time of over-ventilation
    last_adjust_time = None  # To track the last time the setpoint was adjusted
    elapsed_time = 0  # Tracks the total time the fault condition has been active

    # Loop through each data point (assuming 1-minute intervals)
    for minute in range(len(fault_data["vav_total_air_flow"])):
        # Extract telemetry data for the current minute
        vav_total_air_flow = fault_data["vav_total_air_flow"][minute]
        mix_air_temp = fault_data["mix_air_temp"][minute]
        out_air_temp = fault_data["out_air_temp"][minute]
        return_air_temp = fault_data["return_air_temp"][minute]
        fan_vfd_speed = fault_data["fan_vfd_speed_col"][minute]

        # Calculate the outside air fraction
        oa_fraction = calculate_oa_fraction(mix_air_temp, out_air_temp, return_air_temp)

        # Check if economizer weather conditions are met (fan running and temperature delta less than threshold)
        if abs(out_air_temp - return_air_temp) < MIN_TEMP_DELTA:
            # Economizer mode: do not optimize ventilation
            print("Economizer weather detected, optimization turned off.")
            over_ventilation_start_time = None  # Reset fault condition tracking
            continue

        if fan_vfd_speed > 0:  # Fan is running
            if detect_over_ventilation(oa_fraction):
                if over_ventilation_start_time is None:
                    # Start tracking the fault condition time
                    over_ventilation_start_time = minute
                    last_adjust_time = None  # Reset last adjustment time

                # Calculate elapsed time since the fault condition started
                elapsed_time = minute - over_ventilation_start_time

                if elapsed_time > fault_threshold:
                    print(f"Fault condition active for {elapsed_time} minutes.")

                    # Check if it's time to adjust the setpoint
                    if last_adjust_time is None or (minute - last_adjust_time) >= adjust_interval:
                        # Adjust the setpoint and log the time
                        outside_air_setpoint = adjust_oa_setpoint(outside_air_setpoint)
                        last_adjust_time = minute
                        print(f"Adjusted outside air setpoint to {outside_air_setpoint}% at minute {minute}.")
                else:
                    print(f"Fault detected but below threshold time. Elapsed time: {elapsed_time} minutes.")
            else:
                # Reset fault tracking if no over-ventilation is detected
                over_ventilation_start_time = None
                elapsed_time = 0
                print("No over-ventilation detected. Reset fault condition tracking.")
        else:
            # Fan is off, reset fault tracking
            print("Fan is off. Optimization turned off.")
            over_ventilation_start_time = None
            elapsed_time = 0

    # Ensure the setpoint is returned even if the loop skips the adjustment path
    return outside_air_setpoint


# Run the optimization loop
final_setpoint = optimize_ahu_ventilation(fault_data, initial_setpoint=outside_air_setpoint)
print(f"Final outside air damper setpoint: {final_setpoint}%")

