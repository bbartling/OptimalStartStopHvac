# Model 3 Optimal Start Strategy for HVAC Systems

This repository provides a tutorial on implementing the **Model 3 Optimal Start Strategy** for HVAC systems, as inspired by the work of the Pacific Northwest National Laboratory (PNNL). The strategy determines the best preconditioning time to warm or cool a building before occupancy, based on historical data and dynamic parameter tuning. The algorithm is designed for skilled professionals in HVAC, Building Automation Systems (BAS), Automated Supervisory Optimization (ASO), and IoT who wish to learn the mechanics of this algorithm.


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
- **`alpha_3a`**: Time required to change the indoor temperature by 1 degree.
- **`alpha_3b`**: Influence of outdoor temperature on the indoor temperature change.
- **`alpha_3d`**: Dynamic offset for start time adjustments.

These parameters are updated using exponential smoothing based on the historical data.


## Required Inputs
### SQL Database Schema
The algorithm assumes an SQL database containing the following table:

| Column Name       | Data Type | Description                                      |
|-------------------|-----------|--------------------------------------------------|
| `outdoor_temp`    | FLOAT     | Outdoor air temperature in degrees Fahrenheit.  |
| `zone_temp`       | FLOAT     | Zone air temperature in degrees Fahrenheit.     |
| `start_minutes`   | INT       | Actual preconditioning start time in minutes.   |
| `timestamp`       | DATETIME  | Timestamp of the recorded data.                 |

### Example SQL Query
```sql
SELECT outdoor_temp, zone_temp, start_minutes
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
   - Historical start times (`start_minutes`) are compared with the differences in outdoor and indoor temperatures to refine the parameters.

3. **Optimal Start Time Calculation**:
   - The tuned parameters are applied to calculate the required preconditioning time.
   - The algorithm ensures the calculated time stays within defined bounds (e.g., no earlier than 180 minutes before occupancy).


## Python Implementation

```bash
$ python pnnl_model3_method.py
```
### Example Output
```
Optimal Start Time: 2024-12-19 05:45:46.237731
Parameters: alpha_3a=7.76, alpha_3b=2.44, alpha_3d=-628.77
```
### Key Steps in the Code
1. **Parameter Initialization**:
   ```python
   alpha_3a = 10  # Default time to change indoor temp by 1 degree
   alpha_3b = 5   # Time interval for outdoor temp influence
   alpha_3d = 0   # Dynamic adjustment for start time
   ```
2. **Exponential Smoothing**:
   Parameters are updated based on historical data using:
   ```python
   alpha = alpha + forgetting_factor * (alpha_new - alpha)
   ```
3. **Optimal Start Calculation**:
   ```python
   t_opt = (
       alpha_3a * (T_sp - T_z)
       + alpha_3b * (T_sp - T_z) * (T_sp - T_o) / alpha_3b
       + alpha_3d
   )
   ```


## JavaScript Implementation
There is also a JavaScript version of the algorithm that can be ran with `Node`.

### Running the Script
```bash
$ node pnnlModel3.js 
```

For further guidance, please refer to the [PNNL VOLTTRON AEMS](https://github.com/VOLTTRON/volttron-pnnl-aems) repository and white papers.
