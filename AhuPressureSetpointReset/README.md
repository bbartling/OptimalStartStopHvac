## Duct Static Pressure Reset Algorithm for HVAC Systems

This repository provides a tutorial on implementing the **Duct Static Pressure Reset Algorithm** for HVAC systems, inspired by industry best practices and ASHRAE Guideline 36. The strategy dynamically adjusts supply air static pressure to optimize energy consumption while maintaining zone comfort. This documentation is designed for skilled professionals in HVAC, Building Automation Systems (BAS), Automated Supervisory Optimization (ASO), and IoT who wish to learn the mechanics of this algorithm.

## Key Insights
- **Energy Efficiency**: Reduces fan energy consumption while ensuring sufficient airflow to VAV zones.
- **Inputs from BAS Telemetry**: Zone damper positions and static pressure data are expected to come from sensors ingested into a local BAS system and stored in an SQL database.
- **Compliance with Standards**: Inspired by ASHRAE Guideline 36 for advanced HVAC optimization strategies.

## Overview of the Algorithm
The Duct Static Pressure Reset Algorithm calculates the optimal setpoint for supply air duct static pressure by leveraging the following inputs:
- **Zone Damper Positions**: Average or worst-case scenario for VAV box dampers.
- **Static Pressure Limits**: Defined minimum and maximum setpoints to maintain system safety and performance.
- **Device Status**: Ensures adjustments are only made when the associated fan or pump is active.

The algorithm dynamically trims or responds to requests from zones, ensuring most dampers operate within an optimal range of 50-75% open.

## Required Inputs
### SQL Database Schema
The algorithm assumes an SQL database containing the following table:

| Column Name           | Data Type | Description                                              |
|-----------------------|-----------|----------------------------------------------------------|
| `damper_position`     | FLOAT     | Current VAV damper position as a percentage (0-1).       |
| `static_pressure`     | FLOAT     | Current duct static pressure in inches WC.              |
| `device_status`       | BOOLEAN   | Status of the associated device (on/off).               |
| `timestamp`           | DATETIME  | Timestamp of the recorded data.                         |

### Example SQL Query
```sql
SELECT damper_position, static_pressure, device_status
FROM duct_static_pressure_data
WHERE timestamp >= NOW() - INTERVAL 7 DAY;
```
This query retrieves a week's worth of historical data required for proper parameter tuning.

## How the Algorithm Works
1. **Historical Data Retrieval**:
   - The algorithm queries the SQL database to fetch the historical data.
   - At least one week's worth of data is needed for effective parameter tuning.

2. **Dynamic Adjustment**:
   - The algorithm monitors damper positions across zones. If the average damper position is below 50%, the static pressure setpoint is decreased. If the average is above 75%, the setpoint is increased.
   - Trimming and responding logic ensures changes occur incrementally to maintain stability.

3. **Limits Enforcement**:
   - The adjusted static pressure is clamped within defined limits (e.g., SPmin and SPmax).

## Adjustable Algorithm Variables

| Variable             | Description                                                    | Default Value         |
|-----------------------|----------------------------------------------------------------|-----------------------|
| **SP0**              | Initial static pressure setpoint                               | `0.5” WC`            |
| **SPmin**            | Minimum allowable static pressure                              | `0.15” WC`           |
| **SPmax**            | Maximum allowable static pressure                              | `1.5” WC`            |
| **Td**               | Delay timer before logic activates                             | `5 minutes`          |
| **T**                | Time step for evaluating trim and respond logic                | `2 minutes`          |
| **I**                | Number of ignored requests (highest damper positions)          | `2`                  |
| **SPtrim**           | Amount by which the setpoint is trimmed if below thresholds    | `-0.02” WC`          |
| **SPres**            | Amount by which the setpoint is increased if above thresholds  | `0.04” WC`           |
| **SPres-max**        | Maximum allowable response adjustment per time interval        | `0.06” WC`           |

## Python Implementation

### Running the Script
```bash
$ python ahu_static_pressure_sim.py
```

### Example Py Output
```
Starting AHU Static Pressure Simulation...
Current Static Pressure: 0.48” WC
Current Static Pressure: 0.46” WC
...
```

## JavaScript Implementation

### Running the Script
```bash
$ node ahuStaticPressureSim.js 
```

### Example Js Output
```
Starting AHU Static Pressure Simulation...
Current Static Pressure: 0.48” WC
Current Static Pressure: 0.46” WC
...
```

---

## Trim & Respond Logic Details

<details>
  <summary>Algorithm Details</summary>

### Aim
Reduce fan energy consumption by dynamically adjusting duct static pressure setpoints.

### Level of Complexity
(High)

### Potential Savings
(High)

### Process
The algorithm evaluates VAV box damper positions across zones. If the average damper position is:
- **Below 50%**: Decrease static pressure setpoint.
- **Above 75%**: Increase static pressure setpoint.

Adjustments occur incrementally to maintain system stability, with limits enforced to prevent excessive changes.

---

### Adjustable Algorithm Variables
- **SP0**: Initial setpoint for static pressure.
- **SPmin**: Minimum allowable static pressure.
- **SPmax**: Maximum allowable static pressure.
- **SPtrim**: Amount by which the setpoint is trimmed if below thresholds.
- **SPres**: Amount by which the setpoint is increased if above thresholds.
- **SPres-max**: Maximum allowable response adjustment per time interval.

---

### Data Retrieval
- Historical data is retrieved from an SQL database, including:
  - Damper positions
  - Static pressure
  - Device status

This data is used to refine the algorithm’s dynamic adjustments.

</details>
