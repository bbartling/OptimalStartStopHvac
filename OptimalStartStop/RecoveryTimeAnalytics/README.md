## Recovery Time Calcs

This Python script analyzes HVAC zone temperature data to identify and evaluate **warm-up phases**, during which the temperature rises to reach an occupied setpoint. The script processes time-series data by excluding specified days, calculating thresholds for occupied and unoccupied conditions, and detecting steep temperature increases and proximity to the occupied setpoint. Using this information, it determines whether the system is in a warm-up phase and calculates the total warm-up duration in minutes for each day. Additionally, the script extracts 4AM outdoor air and zone air temperatures for each day and records these along with the warm-up duration to a CSV file. It also generates visualizations, including line plots showing the warm-up phases and temperature thresholds, bar charts for daily warm-up durations, and histograms illustrating the distribution of zone temperatures over the analyzed period, providing comprehensive insights into the warm-up behavior of the HVAC system.

### Running the Py Script

```bash
python -m pip install pandas matplotlib
```

## SQL Commands for Filtering Time Series Data

### In the editing debug process if there is an existing view drop it
```sql
DROP VIEW IF EXISTS warm_up_analysis;
```

### Create a View
This command creates a view to filter data between `2023-12-24` and `2024-03-01` for specific time windows.

```sql
SELECT * FROM warm_up_analytics;

```

### Query the View

```sql
SELECT * FROM filtered_data;
```