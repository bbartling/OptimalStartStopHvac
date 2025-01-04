## Recovery Time Calcs

This Python script analyzes HVAC zone temperature data to identify and evaluate **warm-up phases**, during which the temperature rises to reach an occupied setpoint. The script processes time-series data by excluding specified days, calculating thresholds for occupied and unoccupied conditions, and detecting steep temperature increases and proximity to the occupied setpoint. Using this information, it determines whether the system is in a warm-up phase and calculates the total warm-up duration in minutes for each day. Additionally, the script extracts 4AM outdoor air and zone air temperatures for each day and records these along with the warm-up duration to a CSV file. It also generates visualizations, including line plots showing the warm-up phases and temperature thresholds, bar charts for daily warm-up durations, and histograms illustrating the distribution of zone temperatures over the analyzed period, providing comprehensive insights into the warm-up behavior of the HVAC system.

### Running the Py Script

```bash
python -m pip install pandas matplotlib
```

## SQL Instructions instead of Python to Extract Warm-Up Data for a Generic Time Range

The following steps **attempts** to outline how to ***(mimic the same process as in the Py script)*** to extract the required HVAC zone temperature and outdoor air temperature data from a PostgreSQL time-series database for a single, configurable time range. The goal is to analyze warm-up durations and capture the 4AM temperature readings for outdoor air and zone air temperatures.

#### Input Requirements:
- **Time Range**: Defined by `time_ranges = {"range": ("2024-01-14", "2024-01-18")}`. Replace the start and end dates as needed.
- **Table Schema**:
  - `timestamp` (datetime): The timestamp for each data point.
  - `zone_temp` (float): The zone air temperature.
  - `outdoor_temp` (float): The outdoor air temperature.

---

### Steps to Extract Data:

1. **Filter Data by Time Range**:
   - Retrieve all rows from the database where the `timestamp` column falls within the specified time range (`start_date` to `end_date`).

2. **Aggregate Data for Daily Warm-Up Analysis**:
   - Group the filtered data by day (using `DATE_TRUNC` on the `timestamp`).
   - Calculate the daily warm-up duration (`warm_up_duration_minutes`) by:
     - Summing time intervals where the `zone_temp` exceeds a threshold (`minimum zone_temp + 0.5°F`).
     - Multiply the count of such intervals by the time interval duration (e.g., 5 minutes).

3. **Extract 4AM Temperature Values**:
   - Identify rows where the `timestamp` corresponds to exactly 4AM.
   - Extract the `zone_temp` (zone air temperature) and `outdoor_temp` (outdoor air temperature) for each day.

4. **Combine Daily Warm-Up Durations with 4AM Temperatures**:
   - Join the aggregated daily warm-up data with the 4AM temperature values.
   - Ensure the data is aligned by day.

5. **Output Results**:
   - Return the combined dataset containing:
     - `day`: The date for each row.
     - `warm_up_duration_minutes`: Total calculated warm-up duration for the day in minutes.
     - `zone_temp_at_4am`: The zone air temperature recorded at 4AM.
     - `outdoor_temp_at_4am`: The outdoor air temperature recorded at 4AM.

---

### Key Notes:
- The query will only return data for the days included in the specified time range.
- The data is returned as a table (or query result) that can be visualized or processed further.
- The calculation assumes regular intervals between temperature readings (e.g., 5 minutes).
- The thresholds for warm-up detection (`zone_temp > min(zone_temp) + 0.5°F`) can be adjusted as needed.
