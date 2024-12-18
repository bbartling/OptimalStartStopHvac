def interpolate_start_minutes(
    historical_data, current_outside_temp, current_zone_temp, default_minutes=60
):
    if not historical_data:
        return default_minutes

    print("current_outside_temp: ", current_outside_temp)
    print("current_zone_temp: ", current_zone_temp)

    # Calculate distances and sort by closeness to current conditions
    distances = []
    for outside_temp, zone_temp, minutes in historical_data:
        distance = abs(current_outside_temp - outside_temp) + abs(
            current_zone_temp - zone_temp
        )
        distances.append((distance, minutes))

    print(
        "Distances are the \n (current_outside_temp - outside_temp) + (current_zone_temp - zone_temp)"
    )
    print("Boiled into a Tuple of (distance, minutes) for each optimal start")

    # Sort distances and take the two closest data points
    distances.sort()
    print("distances \n", distances)

    closest = distances[:2]  # Take top 2 points
    print("closest: ", closest)

    # If only one data point is available
    if len(closest) == 1:
        return closest[0][1]

    # Extract values for interpolation
    (distance1, minutes1), (distance2, minutes2) = closest
    print("distance1: ", distance1)
    print("minutes1: ", minutes1)
    print("distance2: ", distance2)
    print("minutes2: ", minutes2)

    # Weighted interpolation
    weight1 = 1 / distance1 if distance1 != 0 else 1
    print("weight1: ", weight1)

    weight2 = 1 / distance2 if distance2 != 0 else 1
    print("weight2: ", weight2)

    interpolated_minutes = (minutes1 * weight1 + minutes2 * weight2) / (
        weight1 + weight2
    )
    return round(interpolated_minutes)


# Made Up Data
# (outdoorAirTemp, ZoneAirTemp, Minutes)
historical_data = [
    (5, 60, 111),  # outside air temp starts cold and goes warmer
    (9, 61, 100),
    (15, 62, 90),
    (22, 63, 80),
    (25, 64, 70),
    (29, 65, 60),
    (34, 66, 50),
    (38, 67, 40),
    (40, 68, 30),
    (45, 65, 0),  # warm weather 0 minutes
    (50, 66, 0),  # warm weather 0 minutes
    (55, 67, 0),  # warm weather 0 minutes
    (60, 68, 0),  # warm weather 0 minutes
    (35, 60, 55),  # cold weather front came and getting colder!
    (30, 61, 66),
    (25, 62, 77),
    (22, 63, 88),
    (20, 64, 77),
    (15, 65, 99),
    (10, 66, 111),
]

# Sensor values at Optimal start IE., 5AM or so...
current_outside_temp = 11
current_zone_temp = 50

start_minutes = interpolate_start_minutes(
    historical_data, current_outside_temp, current_zone_temp
)
print("Interpolated Start Minutes:", start_minutes)
