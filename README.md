## aso-pseudo-code
This repository explores versatile algorithms for Automated Supervisory Optimization (ASO), designed for implementation through IoT to enhance HVAC system performance in smart building environments. Each pseudo code folder has simulation to run in Python, JavaScript, and Java versions of the algorithm.

- [x] **[Optimal Start/Stop](https://github.com/bbartling/aso-pseudo-code/tree/develop/OptimalStartStop)**
   - Based on PNNL research.
   - Requires calendar input for building start times.

- [x] **[VAV AHU Supply Air Duct Static Pressure Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuPressureSetpointReset)**
   - Based on GL36.

- [x] **[VAV AHU Supply Air Temperature Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuTempSetpointReset)**
   - Based on GL36.

- [x] **[DOAS Unit Start and Stop](https://github.com/bbartling/aso-pseudo-code/tree/develop/DoasStartStop)**
   - Simple algorithm to start and stop equipment only when people are present.
   - Dedicated outside air system for heat pump and VRF systems providing ventilation only.
   - Requires calendar input for building start times.

- [x] **[AHU Night Heat or Cycling in Full Recirculation Air Mode](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuNightHeatCyclingInFullRecircMode)**
   - ASO monitors zone temperatures.
   - If the AHU wakes up, ensure it operates in full recirculation air mode:
     - If not, override AHU air dampers to full recirculation air mode.

- [ ] **DOAS Unit Temperature Reset**
   - Override BAS to design based temperature setpoints for DOAS units.
   - If the BAS has occupancy integration of zones (IE., zone level OCC sensors), revising ventilation control for demand-based ventilation based on real-time occupancy could be explored. This might involve assessing the availability of zone-level air flow volume measurements and DOAS supply fan controls, as well as evaluating the potential for integrating data from Air Flow Measurement Station (AFMS) to optimize ventilation rates based on actual occupancy levels.
   - If Dedicated Outdoor Air Systems (DOAS) units are equipped with a by-pass air damper across the heat exchangers, ensure that the heat exchangers are bypassed during economizer free cooling conditions to minimize energy consumption by reducing fan pressure drops resulting from overcoming heat exchanger resistance. Additionally, conduct efficiency calculations to determine the optimal conditions under which the heat exchangers should be utilized. Default energy recovery unit (ERV) heating efficiency could be 70 to 90% in a heating application and much lower in a cooling application around 45 to 60%. Use engineering knowledge to best know when to recover heat else bypass the wheel or ERV.

- [ ] **Geothermal Central Plant Optimization**
   - If the geothermal system has additional boiler or cooling capacity with a cooling tower or chiller, utilize Automated System Optimization (ASO) to ensure that extra energy-consuming capacity equipment only operates when conditions exist that the original HVAC design intended for auxiliary capacity equipment to run, specifically when the geothermal loop is not meeting the capacity of heating or cooling loads.

- [ ] **Boiler Plant Leaving Water Setpoint Optimization**
   - Based on GL36 for a "request" based T&R on central plant setpoints Vs outside air temperature central plant resets.

- [ ] **Cold or Warm Weather AHU Overventilation Protection**
   - ASO monitors the calculated percentage of outside air:
     - If AHU is overventilating, ASO overrides the MIN OA ventilation setpoint.
   - Inspired by ASHRAE GL36 fault rule 6 for AHUs.
   - Requires design documentation or mechanical schedules to verify last ventilation design for the AHU.
   - Requires totalized VAV system airflow or a supply fan AHU AFMS.
   - Requires AHU outside air AFMS or calculation of ventilation air via outside air fraction method.
   - Requires an engineer's judgment to verify airflow values and sensor calibration.
   - Recommended: Conduct spot measurements of building CO₂ levels to ensure adequate ventilation and proper building pressurization.

- [ ] **Chiller Plant Leaving Water Setpoint Optimization**
   - Based on GL36 for a "request" based T&R on central plant setpoints Vs outside air temperature central plant resets.
   - Chiller Plant Condensor Water Setpoint Optimization
   - Chiller Staging Optimization

- [ ] **Brainstorm further ideas or improvements.** 🤔
   * Start a git discussion or git issue!