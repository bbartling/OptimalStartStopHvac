## DOAS Unit Start and Stop Algorithm

This repository provides a tutorial on implementing the **Dedicated Outside Air System (DOAS) Start and Stop Algorithm** for HVAC systems. The algorithm ensures that the DOAS unit operates only when the building is occupied, improving energy efficiency while maintaining ventilation requirements.

---

### Key Insights
- **Simple Control Logic**: Ensures DOAS units operate only when people are present.
- **Optimized Ventilation**: Specifically for heat pump and VRF systems to provide ventilation without unnecessary runtime.
- **Flexible Scheduling**: Integrates with BAS schedules via BACnet or similar protocols, a calendar widget in IoT, or hardcoded start/stop times and days of operation.

---

### Overview of the Algorithm
The DOAS Start and Stop Algorithm determines the occupancy status of the building and adjusts the DOAS unit control accordingly:
- **Building Unoccupied**: Overrides the occupancy command to keep the DOAS unit off.
- **Building Occupied**: Releases the control back to the building automation system (BAS), allowing normal operation.

#### Requirements:
1. **Schedule Input**: The building occupancy schedule can come from:
   - **Building Automation System (BAS)**: Utilizing BACnet or similar communication protocols.
   - **IoT Calendar Widget**: Allows dynamic scheduling through a user interface.
   - **Hardcoded Values**: Start and stop times, as well as occupied days, are defined directly in the configuration.

2. **DOAS System**: A dedicated outside air system for heat pump and VRF systems to provide ventilation.

---

### Adjustable Algorithm Variables

| Variable              | Description                                                    | Default Value         |
|------------------------|----------------------------------------------------------------|-----------------------|
| **Building Start Time**| The time when the building becomes occupied.                  | `7:00 AM`            |
| **Building End Time**  | The time when the building becomes unoccupied.                | `6:00 PM`            |
| **Days of Week**       | Days when the building is occupied.                           | `Monday-Friday`      |
| **Override Command**   | Command to turn off the DOAS unit during unoccupied hours.    | `DOAS_Off`           |
| **Release Command**    | Command to release control to the BAS during occupied hours.  | `Release_Control`    |

---

### How the Algorithm Works
1. **Check Current Time**:
   - Compare the current time against the building schedule sourced from:
     - BAS via BACnet or similar protocol.
     - IoT calendar widget.
     - Hardcoded values.

2. **Apply Overrides**:
   - **If Unoccupied**: Issue an override command (`DOAS_Off`) to keep the DOAS unit off.
   - **If Occupied**: Issue a release command (`Release_Control`) to allow BAS control.

3. **Schedule Inputs**:
   - Schedules can be updated dynamically through the BAS or IoT interface.
   - Hardcoded schedules can be used for simple and consistent control.

---

## Python Implementation

#### Running the Script
```bash
$ python doas_unit_control.py
```

#### Example Py Output
```
Current Time: 5:30 PM
Building Status: Occupied
DOAS Status: Released to BAS Control
...
```

---

## JavaScript Implementation

#### Running the Script
```bash
$ node doasUnitControl.js
```

#### Example Js Output
```
Current Time: 5:30 PM
Building Status: Occupied
DOAS Status: Released to BAS Control
...
```

---

## Control Logic Details

<details>
  <summary>Algorithm Details</summary>

### Aim
Ensure the DOAS unit operates only when the building is occupied to minimize energy use while maintaining ventilation requirements.

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
2. If the time is outside the occupied hours:
   - Override the occupancy command to turn the DOAS unit off.
3. If the time is within the occupied hours:
   - Release the control back to the BAS to operate normally.

---

## Data Model in Haystack

**Note:** The algorithm requires proper Haystack markers and tags for the building schedule and occupancy commands to manage the DOAS unit operation effectively.

| **Point Name**                        | **navName**             | **Marker Tags in Haystack**               |
|---------------------------------------|-------------------------|--------------------------------------------|
| **Building Occupancy Schedule**       | `buildingOccSchedule`   | `schedule`, `building`, `occ`             |
| **DOAS Occupancy Command**            | `doasOccCmd`            | `doas`, `occ`, `cmd`                      |
| **DOAS Status**                       | `doasStatus`            | `doas`, `status`                          |

---

### Adjustable Algorithm Variables
- **Building Start Time**: Defines when occupancy begins.
- **Building End Time**: Defines when occupancy ends.
- **Days of Week**: Specifies occupied days.
- **Override Command**: Command to turn off the DOAS unit.
- **Release Command**: Command to allow normal BAS operation.

---

### Notes
This algorithm is ideal for standalone DOAS units in systems using heat pumps or VRF technologies. The scheduling flexibility ensures efficient operation tailored to the building's occupancy patterns.

</details>
