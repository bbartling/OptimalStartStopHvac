## Night Heat or Cycling in Full Recirculation Air Mode Algorithm

This repository provides a tutorial on implementing the **Night Heat or Cycling in Full Recirculation Air Mode Algorithm** for HVAC systems. The algorithm ensures energy efficiency by monitoring AHU (Air Handling Unit) operations during night-time heating or cooling calls and overriding dampers to operate in full recirculation air mode.

---

### Key Insights
- **Energy Efficiency**: Ensures AHU dampers are closed during unoccupied hours to prevent outdoor air intake and conserve energy.
- **Optimized Control**: Overrides AHU dampers to full recirculation mode during night-time heating or cooling.
- **Flexible Scheduling**: Integrates with BAS schedules via BACnet or similar protocols, a calendar widget in IoT, or hardcoded start/stop times and days of operation.

---

### Overview of the Algorithm
The algorithm monitors AHU operations and building schedules to determine the need for overrides:
- **AHU Active During Unoccupied Hours**: If the AHU wakes up on a heating or cooling call outside the occupied schedule, override the air dampers to full recirculation mode.
- **Occupied Hours**: Dampers are controlled by the building automation system (BAS) and operate normally.

#### Requirements:
1. **Schedule Input**: The building occupancy schedule can come from:
   - **Building Automation System (BAS)**: Utilizing BACnet or similar communication protocols.
   - **IoT Calendar Widget**: Allows dynamic scheduling through a user interface.
   - **Hardcoded Values**: Start and stop times, as well as occupied days, are defined directly in the configuration.

2. **AHU System**: The air handling unit must support damper control for recirculation mode.

---

### Adjustable Algorithm Variables

| Variable              | Description                                                    | Default Value         |
|------------------------|----------------------------------------------------------------|-----------------------|
| **Building Start Time**| The time when the building becomes occupied.                  | `7:00 AM`            |
| **Building End Time**  | The time when the building becomes unoccupied.                | `6:00 PM`            |
| **Days of Week**       | Days when the building is occupied.                           | `Monday-Friday`      |
| **Override Command**   | Command to close AHU dampers for recirculation mode.          | `Dampers_Closed`     |
| **Release Command**    | Command to release damper control to BAS during occupied hours.| `Release_Control`   |

---

### How the Algorithm Works
1. **Check Current Time**:
   - Compare the current time against the building schedule sourced from:
     - BAS via BACnet or similar protocol.
     - IoT calendar widget.
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

### Adjustable Algorithm Variables
- **Building Start Time**: Defines when occupancy begins.
- **Building End Time**: Defines when occupancy ends.
- **Days of Week**: Specifies occupied days.
- **Override Command**: Command to close AHU dampers.
- **Release Command**: Command to allow normal BAS operation.

---

### Notes
This algorithm ensures energy savings by preventing unnecessary outdoor air intake during night-time heating or cooling calls. It is ideal for AHUs operating in systems where energy conservation during unoccupied hours is critical.

</details>