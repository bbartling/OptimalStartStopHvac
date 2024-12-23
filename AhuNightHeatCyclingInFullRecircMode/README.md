## Night Heat or Cycling in Full Recirculation Air Mode Algorithm

This repository provides a tutorial on implementing the **Night Heat or Cycling in Full Recirculation Air Mode Algorithm** for HVAC systems. The algorithm ensures energy efficiency by monitoring AHU (Air Handling Unit) operations during night-time heating or cooling calls and overriding dampers to operate in full recirculation air mode.

### Notes

This algorithm can be further enhanced (A future TODO?) by monitoring zone air temperature values to optimize AHU operation. If there are no active heating or cooling calls, the AHU can be overridden to remain OFF, running only when an actual unoccupied heating or cooling demand is detected. Energy code standards recommend unoccupied cooling setpoints of 90°F and unoccupied heating setpoints of 55°F, though these are often not implemented in Building Automation Systems (BAS). Integrating these setpoints can help ensure compliance while reducing energy consumption. ***For now please exclude this thought!***

---

### Key Insights
- **Energy Efficiency**: Ensures AHU dampers remain closed during unoccupied hours, preventing unnecessary outdoor air intake and conserving energy when the building is not actively in use. For school districts, this should align with the district's defined schedule, including start and end times for regular school hours. It should exclude minimally occupied after-hours periods, such as school activities or custodial overnight cleaning. Events with large gatherings, such as sports games in gymnasiums or theater performances, should follow full occupancy ventilation requirements to maintain adequate air exchange. Conversely, activities with minimal occupancy, like sports practices, may operate with reduced ventilation, as design ventilation rates typically account for the maximum occupancy in terms of CFM/person. Always communicate to client conditions of when areas would be at designed ventilation or maximum. ASHRAE 62.1's latest revision supports `occupied-standby` which could also be used to verify if the type of zone can go below designed ventilation.
- **Optimized Control**: Overrides AHU dampers to full recirculation mode during night-time heating or cooling if the AHU cycles during the night.
- **Flexible Scheduling**: Integrates with BAS schedules via BACnet or similar protocols, a calendar widget in IoT, or hardcoded start/stop times and days of operation.

---

### Overview of the Algorithm
The algorithm monitors AHU operations and building schedules to determine the need for overrides:
- **AHU Active During Unoccupied Hours**: If the AHU wakes up on a heating or cooling call outside the occupied schedule, override the air dampers to full recirculation mode.
- **Occupied Hours**: Dampers are controlled by the building automation system (BAS) and operate normally. The algorithm or IoT operating ASO shall release any overrides back to the BAS.

#### Requirements:
1. **Schedule Input**: The building occupancy schedule can come from:
   - **Building Automation System (BAS)**: Utilizing BACnet or similar communication protocols.
   - **IoT Calendar Widget**: Allows dynamic scheduling through a user interface or **Hardcoded Values** for the start and stop times, as well as occupied days, are defined directly in the configuration.

2. **AHU System**: The air handling unit must support damper control for recirculation mode.

---

### Adjustable Algorithm Variables

| **Variable**                            | **Description**                                              | **Default Value**      |
|-----------------------------------------|--------------------------------------------------------------|------------------------|
| **Building Start Time**                 | The time when the building becomes occupied.                 | `7:00 AM`             |
| **Building End Time**                   | The time when the building becomes unoccupied.               | `6:00 PM`             |
| **Days of Week**                        | Days when the building is occupied.                          | `Monday-Friday`       |
| **Economizer High Limit Temperature**   | The maximum outdoor air temperature for enabling free cooling.| `60°F`                |
| **Economizer Low Limit Temperature**    | The minimum outdoor air temperature for enabling free cooling.| `50°F`                |

---

### How the Algorithm Works
1. **Check Current Time**:
   - Compare the current time against the building schedule sourced from:
     - BAS via BACnet or similar protocol.
     - IoT calendar widget. (preferred)
     - Hardcoded values.

2. **Monitor AHU Activity**:
   - If the AHU wakes up during unoccupied hours due to a heating or cooling call, override the air dampers to **closed** for full recirculation mode.

3. **Occupied Schedule**:
   - During occupied hours, release control of the dampers back to the BAS for normal operation.

---

## Python Implementation

#### Running the Script
```bash
$ python night_recirc_mode.py
```

#### Example Py Output
```
Current Time: 3:00 AM
Building Status: Unoccupied
AHU Status: Active
Damper Override: Dampers Closed for Full Recirculation Mode
...
```

---

## JavaScript Implementation

#### Running the Script
```bash
$ node nightRecircMode.js
```

#### Example Js Output
```
Current Time: 3:00 AM
Building Status: Unoccupied
AHU Status: Active
Damper Override: Dampers Closed for Full Recirculation Mode
...
```

---

## Control Logic Details

<details>
  <summary>Algorithm Details</summary>

### Aim
Ensure AHUs operate in full recirculation air mode during unoccupied hours to conserve energy.

---

### Level of Complexity
Low

---

### Potential Savings
Moderate

---

### Process
1. Check the current time and compare it against the building schedule sourced from:
   - **BAS**: Using BACnet or similar protocols.
   - **IoT Calendar Widget**: For user-configurable schedules.
   - **Hardcoded Values**: Directly set start/stop times and occupied days.
2. If the time is outside the occupied hours and the AHU is active:
   - Override the dampers to **closed** for full recirculation mode.
3. During occupied hours:
   - Release damper control back to the BAS for normal operation.

---

## Data Model in Haystack

**Note:** Haystack does not appear to have a `schedule` tag but documentation states to use a `sp` tag for this purposes. See [link](https://project-haystack.org/forum/topic/656) for more info. The `occ` tag or reference to equiment being occupied could potentially be used if it perfectly mirrors the BAS schedule calendar.

| **Point Name**                               | **navName**               | **Marker Tags in Haystack**                     |
|----------------------------------------------|---------------------------|------------------------------------------------|
| **Building Occupancy Schedule**              | `buildingOccSchedule`     | `sp`                                          |
| **AHU/RTU Operating Status**                 | `ahuRtuStatus`            | `ahu`, `rtu`, `status`, `cmd`                 |
| **Minimum Outdoor Air Damper Setpoint**      | `minOaDamperSp`           | `ahu`, `rtu`, `damper`, `outdoor`, `sp`       |
| **Outdoor Air Damper Command**               | `oaDamperCmd`             | `ahu`, `rtu`, `damper`, `outdoor`, `cmd`      |
| **Outside Air Temperature**                  | `outsideAirTemp`          | `outside`, `air`, `temp`, `sensor`            |
| **Economizer High Limit Temperature**        | `economizerHighLimitTemp` | `ahu`, `economizer`, `temp`, `high`, `limit`  |
| **Economizer Low Limit Temperature**         | `economizerLowLimitTemp`  | `ahu`, `economizer`, `temp`, `low`, `limit`   |



</details>