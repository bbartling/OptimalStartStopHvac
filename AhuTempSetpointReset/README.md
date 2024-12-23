## AHU Supply Air Temperature Reset Algorithm

This repository provides a tutorial on implementing the **Supply Air Temperature Reset Algorithm** for HVAC systems. The strategy dynamically adjusts supply air temperature (SAT) setpoints based on outside air temperature (OAT) to optimize energy use while maintaining occupant comfort.

---

### Key Insights
- **Energy Optimization**: Balances chiller energy consumption with maintaining appropriate cooling.
- **Inputs from BAS Telemetry**: Outdoor air temperature (OAT) data is expected to come from sensors ingested into a local BAS system.
- **Humidity Control**: Ensures latent cooling loads are met by limiting SAT increases in humid conditions.

---

### Overview of the Algorithm
The SAT reset algorithm calculates the optimal SAT setpoint based on OAT:
- **Warmer Outdoor Air**: Decrease SAT to increase cooling capacity.
- **Cooler Outdoor Air**: Increase SAT to reduce chiller energy consumption.
- **Linear Reset**: Adjust SAT proportionally between defined limits (SPmin and SPmax) based on OAT.

---

### Required Inputs
#### SQL Database Schema
The algorithm assumes an SQL database containing the following table:

| Column Name     | Data Type | Description                                      |
|-----------------|-----------|--------------------------------------------------|
| `outside_temp`  | FLOAT     | Current outside air temperature in °F.           |
| `sat_setpoint`  | FLOAT     | Current SAT setpoint in °F.                      |
| `device_status` | BOOLEAN   | Status of the AHU (on/off).                      |
| `timestamp`     | DATETIME  | Timestamp of the recorded data.                  |

#### Example SQL Query
```sql
SELECT outside_temp, sat_setpoint, device_status
FROM ahu_temperature_data
WHERE timestamp >= NOW() - INTERVAL 7 DAY;
```
This query retrieves historical data required for analyzing SAT adjustments.

---

### Adjustable Algorithm Variables

| Variable             | Description                                                    | Default Value         |
|-----------------------|----------------------------------------------------------------|-----------------------|
| **SP0**              | Initial SAT setpoint.                                          | `60°F`               |
| **SPmin**            | Minimum allowable SAT setpoint.                                | `55°F`               |
| **SPmax**            | Maximum allowable SAT setpoint.                                | `65°F`               |
| **OATmin**           | Minimum outside air temperature for reset control.             | `60°F`               |
| **OATmax**           | Maximum outside air temperature for reset control.             | `70°F`               |
| **Td**               | Delay timer before logic activates.                            | `10 minutes`         |
| **T**                | Time step for evaluating SAT reset logic.                      | `2 minutes`          |

---

## Python Implementation

#### Running the Script
```bash
$ python ahu_temperature_reset_sim.py
```

#### Example Py Output
```
Starting AHU Temperature Reset Simulation...
Current OAT: 65.30°F, Adjusted SAT: 60.30°F
...
```

---

## JavaScript Implementation

#### Running the Script
```bash
$ node ahuTemperatureResetSim.js
```

#### Example Js Output
```
Starting AHU Temperature Reset Simulation...
Current OAT: 65.30°F, Adjusted SAT: 60.30°F
...
```

---

## Trim & Respond Logic Details

<details>
  <summary>Algorithm Details</summary>

### Aim
Prevent excessive chiller energy consumption while maintaining proper dehumidification in humid climates.

---

### Level of Complexity
Low

---

### Potential Savings
Low

---

### Process
The algorithm adjusts the SAT setpoint dynamically based on the following rules:
- **Warmer Outdoor Air**: Decrease SAT to increase cooling capacity.
- **Cooler Outdoor Air**: Increase SAT to reduce chiller energy consumption.
- **Linear Reset**: Use a linear interpolation between **OATmin** and **OATmax** to determine the SAT setpoint.

---

## Data Model in Haystack

**Note:** The algorithm requires proper Haystack markers and tags for AHU leaving air temperature, outside air temperature, and **ALL** associated space air temperature sensors to generate requests for SAT adjustments.

| **Point Name**                           | **navName**             | **Marker Tags in Haystack**                     |
|------------------------------------------|-------------------------|------------------------------------------------|
| **AHU Leaving Air Temperature**          | `ahuLeavingAirTemp`     | `ahu`, `leaving`, `air`, `temp`, `sensor`      |
| **AHU Leaving Air Temperature Setpoint** | `ahuLeavingAirTempSp`   | `ahu`, `leaving`, `air`, `temp`, `sp`          |
| **Space Air Temperature**                | `spaceAirTemp`          | `space`, `air`, `temp`, `sensor`               |
| **Space Air Temperature Cooling Setpoint** | `spaceAirTempCoolSp`   | `space`, `air`, `temp`, `cooling`, `sp`        |
| **Space Air Temperature Heating Setpoint** | `spaceAirTempHeatSp`   | `space`, `air`, `temp`, `heating`, `sp`        |
| **Outside Air Temperature**              | `outsideAirTemp`        | `outside`, `air`, `temp`, `sensor`             |

</details>