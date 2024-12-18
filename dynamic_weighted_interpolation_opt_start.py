import datetime as dt


"""
"Dynamic Weighted Interpolation for Optimal Start" (DWIOS).

Dynamic: Adapts to changing conditions such as current outdoor and zone temperatures.
Weighted Interpolation: Uses a weighted calculation to interpolate between historical data points for accurate estimation.
Optimal Start: Clearly states the purpose of the strategy in the context of HVAC scheduling.

"""
# Configuration parameters
earliest_start_time = 180  # in minutes before occupancy
latest_start_time = 10  # in minutes before occupancy
default_minutes = 60  # Default pre-start time if no data exists


def interpolate_start_minutes(historical_data, current_outside_temp, current_zone_temp):
    """
    Interpolate start minutes based on historical data and current conditions.
    """
    if not historical_data:
        return default_minutes

    # Calculate distances to current conditions
    distances = []
    for outside_temp, zone_temp, minutes in historical_data:
        distance = abs(current_outside_temp - outside_temp) + abs(
            current_zone_temp - zone_temp
        )
        distances.append((distance, minutes))

    # Sort by distance and take the two closest points
    distances.sort()
    closest = distances[:2]

    # If only one point exists, return its minutes
    if len(closest) == 1:
        return closest[0][1]

    # Extract values for interpolation
    (distance1, minutes1), (distance2, minutes2) = closest

    # Weighted interpolation
    weight1 = 1 / distance1 if distance1 != 0 else 1
    weight2 = 1 / distance2 if distance2 != 0 else 1

    interpolated_minutes = (minutes1 * weight1 + minutes2 * weight2) / (
        weight1 + weight2
    )
    return round(interpolated_minutes)


def calculate_prestart(temperature_data, historical_data):
    """
    Calculate the required pre-start time using historical data for interpolation.
    """
    current_outside_temp = temperature_data["outdoor_temp"]
    current_zone_temp = temperature_data["zone_temp"]
    interpolated_minutes = interpolate_start_minutes(
        historical_data, current_outside_temp, current_zone_temp
    )

    # Ensure prestart time is within configured bounds
    prestart_time = max(
        latest_start_time, min(interpolated_minutes, earliest_start_time)
    )
    return prestart_time


def optimal_start(schedule, temperature_data, historical_data):
    """
    Determine optimal start time for HVAC equipment based on interpolated prestart time.
    """
    start_time = schedule["start"]
    prestart_minutes = calculate_prestart(temperature_data, historical_data)
    optimal_start_time = start_time - dt.timedelta(minutes=prestart_minutes)
    return optimal_start_time


# Historical Data Example
# (outdoorAirTemp, ZoneAirTemp, Minutes)
historical_data = [
    (5, 60, 111),
    (9, 61, 100),
    (15, 62, 90),
    (22, 63, 80),
    (25, 64, 70),
    (29, 65, 60),
    (34, 66, 50),
    (38, 67, 40),
    (40, 68, 30),
    (45, 65, 0),
    (50, 66, 0),
    (55, 67, 0),
    (60, 68, 0),
    (35, 60, 55),
    (30, 61, 66),
    (25, 62, 77),
    (22, 63, 88),
    (15, 65, 99),
    (10, 66, 111),
]

# Current Sensor Data
temperature_data = {
    "zone_temp": 50,  # Current space temperature
    "outdoor_temp": 11,  # Current outdoor temperature
}

# Schedule Example
schedule = {
    "start": dt.datetime.now().replace(hour=6, minute=30),  # Scheduled occupancy start
    "end": dt.datetime.now().replace(hour=18, minute=0),  # Scheduled occupancy end
}

# Calculate Optimal Start Time
optimal_time = optimal_start(schedule, temperature_data, historical_data)
print(f"Optimal Start Time: {optimal_time}")
