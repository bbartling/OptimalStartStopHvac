# Define constants
PERCENT_OA = 0.2  # Design outside air percentage (20%)
MIN_RETURN_OA_DELTA = 10  # Minimum temperature difference between return and outside air to calculate OA fraction

# Define data structures to simulate telemetry data
fault_data = {
    "vav_total_air_flow": [10000, 10050, 10025, 10075, 10030, 10020],
    "mix_air_temp": [30, 29.5, 30.5, 29.8, 30.2, 29.6],
    "out_air_temp": [10, 10.5, 10.2, 10.8, 10.3, 10.1],
    "return_air_temp": [72, 72.5, 72.2, 72.8, 72.3, 72.1],
    "fan_vfd_speed_col": [0.66, 0.67, 0.65, 0.66, 0.68, 0.67],
    "economizer_sig_col": [0.2] * 6,
}


# Define the function to calculate the outside air fraction
def calculate_oa_fraction(mix_air_temp, out_air_temp, return_air_temp):
    if abs(out_air_temp - return_air_temp) >= MIN_RETURN_OA_DELTA:
        return (return_air_temp - mix_air_temp) / (return_air_temp - out_air_temp)
    else:
        return None  # Condition false equivalent in Python


# Function to calculate and print outside air fraction and CFM
def calculate_ventilation(fault_data):
    for minute in range(len(fault_data["vav_total_air_flow"])):
        vav_total_air_flow = fault_data["vav_total_air_flow"][minute]
        mix_air_temp = fault_data["mix_air_temp"][minute]
        out_air_temp = fault_data["out_air_temp"][minute]
        return_air_temp = fault_data["return_air_temp"][minute]
        fan_vfd_speed = fault_data["fan_vfd_speed_col"][minute]

        if (
            fan_vfd_speed == 0.0
            or abs(out_air_temp - return_air_temp) < MIN_RETURN_OA_DELTA
        ):
            oa_fraction = None
            calculated_oa_cfm = None
        else:
            oa_fraction = calculate_oa_fraction(
                mix_air_temp, out_air_temp, return_air_temp
            )
            calculated_oa_cfm = (
                oa_fraction * vav_total_air_flow if oa_fraction is not None else None
            )
            design_oa_cfm = PERCENT_OA * vav_total_air_flow

        print(
            f"Minute {minute}: OA Fraction = {oa_fraction}, Calculated OA CFM = {calculated_oa_cfm}, Design OA CFM = {design_oa_cfm}"
        )


# Run the calculation
calculate_ventilation(fault_data)
