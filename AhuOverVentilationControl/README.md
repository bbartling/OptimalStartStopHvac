## AHU Over-Ventilation Control Algorithm

### Overview
This algorithm requires evaluating existing HVAC design records in mechanical schedules to determine the design percentage of outside air (OA) in an AHU system. It operates during extreme outdoor air conditions (hot or cold) when the AHU is set to minimum outside air ventilation. Similar to ASHRAE G36 Fault Rule 6, this algorithm assesses the design OA percentage and reduces the `MIN OA` damper position setpoint incrementally if the actual OA percentage exceeds the design level.

### Activation Criteria
- The temperature delta between return and outside air must be at least **10°F** for the algorithm to engage.
- The supply fan must have run for at least **30 minutes** to ensure thermal stabilization before calculations begin.
- Consideration of exhaust systems is essential to maintain proper ventilation balance.
- The most ideal scenario would involve using AHU return air **CO₂ sensor data** to determine if the building is at design occupancy and receiving adequate ventilation.
- An engineer should review ventilation records, evaluate changes in space utilization from the previous design, and assess exhaust systems within the building.
- If **CO₂ levels indicate high occupancy**, the AHU should operate at **design ventilation levels**, ensuring proper indoor air quality.
- Part of this implementation could involve updating the **ventilation design** if necessary to align with current occupancy and building usage patterns which typical to RCx efforts.


### Control Strategy
1. **Rolling Average Calculation:**
   - Ideally the algorithm computes a rolling average of the outside air percentage.
   - If the **calculated OA percentage exceeds the design level**, the `MIN OA` damper position is reduced by **1% every 5 minutes** until the average aligns with the design target.
   - If the **calculated OA percentage falls below the design level**, the `MIN OA` damper position is increased by **1% every 5 minutes**—but never exceeding the existing BAS setpoint.

2. **Algorithm Deactivation:**
   - The algorithm releases control back to the BAS if:
     - The **return and outside air temperature delta drops below 10°F**.
     - The **supply fan turns OFF**.

### Cold Weather Considerations
- Zone-level data should be monitored to prevent excessive economizer operation in cold weather.
- AHU discharge air temperature reset strategies should be evaluated to avoid unnecessary reheat energy waste.
- Preventing economization in cold conditions due to rogue zones ensures energy-efficient operation.

### Design Awareness
- Typical AHU systems operate at **10-15% outdoor air**.
- If an AHU has a **30% minimum outside air design**, investigate whether this is due to **makeup air for exhaust systems or high occupancy levels**.
- Understanding these design choices prevents unnecessary adjustments that could compromise ventilation effectiveness.
