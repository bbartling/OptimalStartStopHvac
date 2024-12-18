# Dynamic Weighted Interpolation for Optimal Start (DWIOS)

Dynamic Weighted Interpolation for Optimal Start (DWIOS) is a robust strategy for determining the preconditioning time needed to warm or cool HVAC zones before occupancy. The algorithm adapts to varying outdoor and indoor conditions using historical data and dynamically adjusts the start time based on current temperature readings. The method ensures optimal HVAC system operation, improving efficiency and maintaining comfort.

This code base is inspired by the work of the Pacific Northwest National Laboratory (PNNL) and specifically their VOLTTRON team, which creates open-source software and leads research efforts in making buildings not only energy-efficient but also advancing the future of Grid-Interactive Efficient Buildings (GEB).

For more information on VOLTTRON, visit their [documentation](https://volttron.readthedocs.io/en/main/).



## Overview
The DWIOS algorithm calculates the optimal pre-start time by comparing current outdoor and zone temperatures to historical conditions. Using **weighted interpolation**, it predicts how long it will take to reach desired temperatures. The algorithm dynamically adjusts for varying weather conditions and can be implemented on any IoT platform that supports historical data retrieval.

## Key Features
- **Dynamic Adaptation**: Adjusts based on outdoor and zone air temperatures.
- **Weighted Interpolation**: Prioritizes closer historical conditions for accurate predictions.
- **Cross-Platform Compatibility**: Can be implemented in any programming language with database access.
- **Python Demo**: Includes a Python implementation for proof-of-concept and simulation.



## How It Works
### 1. Historical Data Retrieval
DWIOS requires historical data containing:
- **Outdoor Air Temperature**
- **Zone Air Temperature**
- **Start Times (in minutes)**

### 2. Calculation Workflow
1. **Data Query**: Historical data is retrieved from an SQL database.
2. **Distance Calculation**: The algorithm calculates the "distance" between current conditions and historical records based on temperature differences.
3. **Weighted Interpolation**: Two closest historical points are used to interpolate the required pre-start time.
4. **Bounds Enforcement**: Ensures calculated times respect configured limits (e.g., earliest and latest start times).



## Function: `interpolate_start_minutes`
This function is the core of the DWIOS algorithm, performing weighted interpolation to calculate start times.

### **Logic:**
- **Inputs**: Current outdoor and zone temperatures, historical data.
- **Outputs**: Interpolated pre-start time in minutes.
- **Steps**:
  1. Calculate distances between current conditions and historical data.
  2. Sort distances and select the two closest points.
  3. Perform weighted interpolation using the inverse of distances.
  4. Return the rounded interpolated start time.



## Python Implementation
The Python implementation simulates DWIOS with sample data. Running the script outputs an **optimal start time** as a Python `datetime` object.

### Example:
```bash
$ python dynamic_weighted_interpolation_opt_start.py
Optimal Start Time: 2024-12-18 04:54:19.641972
```

The script ensures:
- Integration with SQL for historical data retrieval.
- Flexible, modular design for deployment on IoT platforms.



## SQL for Historical Data Retrieval
DWIOS retrieves historical data from an SQL database. Here's a generic SQL query:

### Example SQL Query:
```sql
SELECT outdoor_temp, zone_temp, start_minutes
FROM hvac_historical_data
WHERE date >= CURDATE() - INTERVAL 15 DAY;
```
### Notes:
1. The query fetches 15 days of historical data.
2. The IoT platform can cache this data for the algorithm to use.



## Generic Pseudocode for IoT Platforms
DWIOS can be implemented on any IoT platform. Here's a generic approach:

### Pseudocode:
```pseudo
FUNCTION get_optimal_start_time(current_outdoor_temp, current_zone_temp):
    historical_data = query_sql_database()
    IF historical_data IS EMPTY:
        RETURN default_start_time

    distances = []
    FOR each record IN historical_data:
        distance = ABS(current_outdoor_temp - record.outdoor_temp) + 
                   ABS(current_zone_temp - record.zone_temp)
        APPEND (distance, record.start_minutes) TO distances

    SORT distances BY distance ASCENDING
    closest = GET first TWO distances

    IF closest HAS ONE record:
        RETURN closest[0].start_minutes

    weight1 = 1 / closest[0].distance
    weight2 = 1 / closest[1].distance
    interpolated_minutes = (closest[0].start_minutes * weight1 + 
                            closest[1].start_minutes * weight2) / (weight1 + weight2)

    RETURN ROUND(interpolated_minutes)
```



## IoT Platform Integration
DWIOS can integrate with IoT platforms by:
1. **Database Setup**: Store historical data in a time-series database.
2. **Data Access**: Query historical data at runtime.
3. **Cross-Language Implementation**: Translate the provided pseudocode into the platform's native programming language.



## Advantages
- **Scalable**: Supports large datasets and dynamic conditions.
- **Accurate**: Uses precise weighted interpolation for predictions.
- **Flexible**: Deployable on various platforms and architectures.
