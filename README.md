## aso-pseudo-code
This repository explores versatile algorithms for Automated Supervisory Optimization (ASO), designed for implementation through IoT to enhance HVAC system performance in smart building environments. Each pseudo code folder has simulation to run in Python and JavaScript versions of the algorithm.

## Implement on the BAS
- Reduce equipment runtime via BAS schedules
- PID tuning or hunting issues found in controls


## ASO

- [ ] **[Optimal Start/Stop](https://github.com/bbartling/aso-pseudo-code/tree/develop/OptimalStartStop)**
   [x] Based on PNNL research Model 3 from paper.
      - Work in progress.
      - Adaptive `learning-algorithm` that tunes itself. 
   - Recovery Time Analytics:
      - A script designed to calculate the time (in minutes) required for a temperature sensor to reach the zone temperature setpoint. This metric is integral to Optimal Start calculations.
      - Status:
         - [x] Winter time morning warm up in Python version completed.
         - [ ] Winter time morning warm up in SQL version for Grafana pending.
         - [x] Summertime time morning cooldown in Python version completed.
         - [ ] Summertime time morning cooldown in SQL version for Grafana pending.
   [x] Recovery Time Per Degree.
      - Traditional Non-Adaptive Optimal Start or Stop.
      - Requires manual set of degree per hour of temperature recovery rates.

- [x] **[VAV AHU Supply Air Duct Static Pressure Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuPressureSetpointReset)**
   - Based on GL36.

- [x] **[VAV AHU Supply Air Temperature Setpoint Reset](https://github.com/bbartling/aso-pseudo-code/tree/develop/AhuTempSetpointReset)**
   - Based on GL36.

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