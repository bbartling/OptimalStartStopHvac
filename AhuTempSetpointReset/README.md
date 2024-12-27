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
| `zone_temps`    | FLOAT     | Zone air temperatures in °F.                     |
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
| **SPres-max**            | Maximum amount of change allowed per time step  | `1°F`           |
| **HighZoneTempSpt**  | High Zone threshold to generate requests (znt > 75°F)          | `75.0°F`              |

---

## Implementation

#### Python
```bash
$ python ahu_temperature_reset_sim.py
```

#### JavaScript
```bash
$ node ahuTemperatureResetSim.js
```

#### Java
```bash
# compile
$ javac AHUTemperatureResetSim.java

# run
$ java AHUTemperatureResetSim
```

#### Example Output Per Timestep
```
Ignored Zone Temperatures: 79.95, 79.11
Max Zone Temperature (After Excluding Top 2): 78.82°F
Net Requests (Factoring Ignored Zones): 10
Total Adjustment is -1.00°F
We need more cooling!...
Current OAT: 71.99°F
Dynamic SPmax: 60.00°F
Previous SAT Setpoint: 55.00°F
Current SAT Setpoint: 55.00°F (decreased)

Ignored Zone Temperatures: 79.50, 79.00
Max Zone Temperature (After Excluding Top 2): 78.96°F
Net Requests (Factoring Ignored Zones): 11
Total Adjustment is -1.00°F
We need more cooling!...
Current OAT: 69.02°F
Dynamic SPmax: 60.49°F
Previous SAT Setpoint: 55.00°F
Current SAT Setpoint: 55.00°F (decreased)

Ignored Zone Temperatures: 79.76, 79.21
Max Zone Temperature (After Excluding Top 2): 78.95°F
Net Requests (Factoring Ignored Zones): 10
Total Adjustment is -1.00°F
We need more cooling!...
Current OAT: 63.96°F
Dynamic SPmax: 63.02°F
Previous SAT Setpoint: 55.00°F
Current SAT Setpoint: 55.00°F (decreased)
...
```

---


---

## Trim & Respond Logic Details


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
| **Outside Air Temperature**              | `outsideAirTemp`        | `outside`, `air`, `temp`, `sensor`             |


### Notes

This algorithm is designed for occupied buildings and should be carefully tuned, particularly the ignore variable (`I`), to ensure occupant comfort is maintained. It is also recommended to follow up with an occupant comfort survey to confirm that zones do not feel too hot, cold, muggy, dry, or experience any other occupant comfort issues.