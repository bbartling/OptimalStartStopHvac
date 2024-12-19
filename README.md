## Model 3 Optimal Start Strategy for HVAC Systems

This repository provides a tutorial on implementing the **Model 3 Optimal Start Strategy** for HVAC systems, inspired by the work of the Pacific Northwest National Laboratory (PNNL). The strategy determines the best preconditioning time to warm or cool a building before occupancy, based on historical data and dynamic parameter tuning. The algorithm is designed for skilled professionals in HVAC, Building Automation Systems (BAS), Automated Supervisory Optimization (ASO), and IoT who wish to learn the mechanics of this algorithm.

## Key Insights
- **Dynamic Tuning**: Parameters adapt over time, using a week's worth of historical data for proper tuning.
- **Inputs from BAS Telemetry**: Outdoor air temperature and zone temperature data are expected to come from sensors ingested into a local BAS system and stored in an SQL database.
- **Citing PNNL**: This work builds on concepts developed by PNNL for advancing energy-efficient and grid-interactive buildings. Visit the [PNNL VOLTTRON documentation](https://volttron.readthedocs.io/en/main/) for more insights.

## Overview of Model 3
The Model 3 algorithm calculates the optimal start time for HVAC systems by leveraging the following inputs:
- **Outdoor Air Temperature**: Current temperature outside the building.
- **Zone Air Temperature**: Current indoor temperature.
- **Occupied Setpoint Temperature**: Desired indoor temperature by occupancy time.

The algorithm dynamically tunes three key parameters:
- **`alpha_3a`**: Time required to change the indoor temperature by 1 degree (**measured in minutes**).
- **`alpha_3b`**: Influence of outdoor temperature on the indoor temperature change (**measured in degrees Fahrenheit**).
- **`alpha_3d`**: Dynamic offset for start time adjustments (**measured in minutes**).

These parameters are updated using exponential smoothing based on the historical data.

## Required Inputs
### SQL Database Schema
The algorithm assumes an SQL database containing the following table:

| Column Name            | Data Type | Description                                      |
|-------------------------|-----------|--------------------------------------------------|
| `outdoor_temp`          | FLOAT     | Outdoor air temperature in degrees Fahrenheit.   |
| `zone_temp`             | FLOAT     | Zone air temperature in degrees Fahrenheit.      |
| `warmup_time_minutes`   | INT       | Captured preconditioning duration in minutes.    |
| `timestamp`             | DATETIME  | Timestamp of the recorded data.                  |

### Example SQL Query
```sql
SELECT outdoor_temp, zone_temp, warmup_time_minutes
FROM hvac_historical_data
WHERE timestamp >= NOW() - INTERVAL 7 DAY;
```
This query retrieves a week's worth of historical data required for proper parameter tuning.

## How the Algorithm Works
1. **Historical Data Retrieval**:
   - The algorithm queries the SQL database to fetch the historical data.
   - At least one week's worth of data is needed for effective parameter tuning.

2. **Parameter Tuning**:
   - The algorithm dynamically updates the parameters `alpha_3a`, `alpha_3b`, and `alpha_3d` using exponential smoothing.
   - Historical warm-up times (`warmup_time_minutes`) are compared with the differences in outdoor and indoor temperatures to refine the parameters.

3. **Optimal Start Time Calculation**:
   - The tuned parameters are applied to calculate the required preconditioning time.
   - The algorithm ensures the calculated time stays within defined bounds (e.g., no earlier than 180 minutes before occupancy).

## Python Implementation

### Running the Script
```bash
$ python pnnl_model3_method.py
```

### Example Py Output
```
Optimal Start Time (in minutes before occupancy): 180.00
HVAC Start Timestamp: 2024-12-19 08:31:26.524257
HVAC Start Time has already passed!
Parameters: alpha_3a=7.76, alpha_3b=2.44, alpha_3d=-628.77
```

## JavaScript Implementation

### Running the Script
```bash
$ node pnnlModel3.js 
```

### Example Js Output
```
Optimal Start Time: Thu Dec 19 2024 08:32:47 GMT-0600 (Central Standard Time)
Parameters: alpha3a=7.76, alpha3b=2.44, alpha3d=-628.77
```

