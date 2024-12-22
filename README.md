## aso-pseudo-code
This repository explores versatile algorithms for Automated Supervisory Optimization (ASO), designed for implementation through IoT to enhance HVAC system performance in smart building environments.

- [ ] **[Optimal Start/Stop](https://github.com/bbartling/aso-pseudo-code/tree/develop/OptimalStartStop)**
   - Based on PNNL research.
   - Requires calendar input for building start times.

- [ ] **[VAV AHU Supply Air Duct Static Pressure Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuPressureSetpointReset)**
   - Based on GL36.

- [ ] **[VAV AHU Supply Air Temperature Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuTempSetpointReset)**
   - Based on GL36.

- [ ] **[DOAS Unit Start and Stop](https://github.com/bbartling/aso-pseudo-code/tree/develop/DoasStartStop)**
   - Simple algorithm to start and stop equipment only when people are present.
   - Dedicated outside air system for heat pump and VRF systems providing ventilation only.
   - Requires calendar input for building start times.

- [ ] **[AHU Night Heat or Cycling in Full Recirculation Air Mode](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuNightHeatCyclingInFullRecircMode)**
   - ASO monitors zone temperatures.
   - If the AHU wakes up, ensure it operates in full recirculation air mode:
     - If not, override AHU air dampers to full recirculation air mode.

- [ ] **Cold or Warm Weather AHU Overventilation Protection**
   - ASO monitors the calculated percentage of outside air:
     - If AHU is overventilating, ASO overrides the MIN OA ventilation setpoint.
   - Inspired by ASHRAE GL36 fault rule 6 for AHUs.
   - Requires design documentation or mechanical schedules to verify last ventilation design for the AHU.
   - Requires totalized VAV system airflow or a supply fan AHU AFMS.
   - Requires AHU outside air AFMS or calculation of ventilation air via outside air fraction method.
   - Requires an engineer's judgment to verify airflow values and sensor calibration.
   - Recommended: Conduct spot measurements of building CO₂ levels to ensure adequate ventilation and proper building pressurization.

- [ ] **Boiler Plant Optimization**

- [ ] **Chiller Plant Optimization**

- [ ] **Brainstorm further ideas or improvements.** 🤔
   * Start a git discussion or git issue!