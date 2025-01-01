## Recovery Time Calcs

This Python script analyzes HVAC zone temperature data to identify and evaluate **warm-up phases**, where the temperature rises to reach an occupied setpoint. It uses configurable parameters to tailor the analysis for different data sets and operational scenarios. 

### Key Steps in the Analysis:
1. **Loading and Preprocessing Data**:
   - The script loads zone temperature data from a CSV file, converts timestamps for time-based operations, and sets the index for resampling and filtering.

2. **Daily Setpoint Calculation**:
   - **Occupied threshold (`occupied_threshold`)**: Calculated as the mean of the maximum daily temperatures, representing periods when the building is occupied.
   - **Unoccupied threshold (`unoccupied_threshold`)**: Calculated as the mean of the minimum daily temperatures, representing periods when the building is unoccupied.

3. **Warm-Up Phase Identification**:
   - **Steep Increases**: The script detects sharp temperature rises (greater than `STEEP_INCREASE_THRES` degrees) to flag the start of a warm-up phase.
   - **Proximity to Setpoint**: The script marks the warm-up phase as complete when the temperature approaches the `occupied_threshold` within `OCC_ZONE_TEMP_PROX_THRES` degrees.

4. **Smoothing and Refinement**:
   - A rolling window (`ROLLING_WINDOW_SIZE`) smooths the `Warm_Up_Active` column to remove isolated values that might be outliers or noise, ensuring only meaningful warm-up phases are considered.

5. **Daily Duration Calculation**:
   - The total warm-up duration for each day is calculated by summing intervals where warm-up is active and converting counts to minutes (`DATASET_MIN_PER_TIME_STEP`).

6. **Exclusions**:
   - Days specified in `EXCLUDE_DAYTYPES` (e.g., weekends and Mondays) are excluded from the analysis to focus on occupied building days.

7. **Visualization and Output**:
   - A bar chart summarizes daily warm-up durations, while a time-series plot highlights warm-up phases alongside the temperature profile.
   - Results, including daily durations and 4 AM temperature readings for `SpaceTemp` and `OaTemp`, are saved to a structured output directory (`OUTPUT_DIR`).

---

### Parameter Descriptions:
- **`EXCLUDE_DAYTYPES`**:
  - Days to exclude from calculations, typically when the building is unoccupied (e.g., weekends or Mondays).

- **`OCC_ZONE_TEMP_PROX_THRES`**:
  - The tolerance in degrees Fahrenheit to determine when the temperature is "close enough" to the `occupied_threshold`. This helps flag when the warm-up phase is complete.

- **`STEEP_INCREASE_THRES`**:
  - The minimum temperature increase in degrees Fahrenheit between time steps to detect the start of a warm-up phase from the `unoccupied_threshold`.

- **`ROLLING_WINDOW_SIZE`**:
  - The size of the rolling window (in data points) used to smooth the `Warm_Up_Active` column. Helps ignore outliers by requiring nearby supporting data.

- **`DATASET_MIN_PER_TIME_STEP`**:
  - The time resolution of the dataset in minutes. Used to convert counts of active intervals into total durations in minutes.

- **`OUTPUT_DIR`**:
  - The directory where results (CSV files and plots) are saved. Ensures organized output for multiple time ranges.

---

### Getting Setup

```bash
python -m pip install pandas matplotlib
```