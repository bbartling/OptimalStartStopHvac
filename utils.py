import datetime
import numpy as np  # For interpolation


class Schedule:
    def __init__(self, start_time_hour=8, earliest_start_offset_minutes=180):
        self.start_time = datetime.datetime.now().replace(hour=start_time_hour, minute=0, second=0, microsecond=0)
        self.earliest_start_offset_minutes = earliest_start_offset_minutes

    @property
    def earliest_start_time(self):
        return self.start_time - datetime.timedelta(minutes=self.earliest_start_offset_minutes)

    def get_next_event(self, current_time):
        if current_time < self.start_time:
            return self.start_time, True
        else:
            return self.start_time + datetime.timedelta(days=1), True

    def is_time_for_action(self):
        return True

    def current_action(self):
        now = datetime.datetime.now()
        if self.earliest_start_time <= now < self.start_time:
            return "active"
        else:
            return "inactive"


class TemperatureSensor:
    def __init__(self):
        self.temperature = None

    def update_temperature(self, new_temp):
        self.temperature = new_temp

    def read(self):
        return self.temperature


class FanStatus:
    def __init__(self):
        self.is_running = False
        self.start_cache = []  # Cache will store tuples: (outside_air_temp, temp_change_rate)

    def update_status(self, status, outside_air_temp=None, temp_change_rate=None):
        if status and not self.is_running:
            # Add a temperature change rate data point to the cache if provided
            if outside_air_temp is not None and temp_change_rate is not None:
                self.start_cache.append((outside_air_temp, temp_change_rate))
        self.is_running = status

    def status(self):
        return self.is_running

    def get_start_cache(self):
        return self.start_cache


class OptimalStartStop:
    def __init__(self, comfort_limits, schedule, outside_temp_sensor, space_temp_sensor, fan_status):
        self.comfort_limits = comfort_limits
        self.schedule = schedule
        self.outside_temp_sensor = outside_temp_sensor
        self.space_temp_sensor = space_temp_sensor
        self.fan_status = fan_status
        self.calculated_start_time = None

    def calculate_start_time(self):
        current_time = datetime.datetime.now()
        next_event_time, next_event_value = self.schedule.get_next_event(current_time)
        if not next_event_value:
            return

        # If the cache is empty, default to the earliest start time
        if not self.fan_status.get_start_cache():
            self.calculated_start_time = self.schedule.earliest_start_time
            print("Calculated Start Time (No Cache):", self.calculated_start_time)
            return self.calculated_start_time

        # Use cached data to estimate warm-up time
        current_outside_temp = self.outside_temp_sensor.read()
        estimated_temp_change_rate = self._estimate_temp_change_rate(current_outside_temp)
        if estimated_temp_change_rate == 0:  # Avoid division by zero
            estimated_temp_change_rate = 1

        space_temp = self.space_temp_sensor.read()
        temp_diff = self._calculate_temperature_difference(space_temp)

        required_runtime_minutes = temp_diff / estimated_temp_change_rate

        lead_time = datetime.timedelta(minutes=required_runtime_minutes)
        optimal_start_time = next_event_time - lead_time

        # Ensure the optimal start time does not go before the earliest start time
        if optimal_start_time < self.schedule.earliest_start_time:
            optimal_start_time = self.schedule.earliest_start_time

        self.calculated_start_time = optimal_start_time
        print("Calculated Start Time:", self.calculated_start_time)
        return self.calculated_start_time

    def _estimate_temp_change_rate(self, outside_temp):
        cache = self.fan_status.get_start_cache()
        if not cache:
            return 0  # Default rate if no data is available

        # Extract outdoor temperatures and change rates from the cache
        temps = [entry[0] for entry in cache]
        rates = [entry[1] for entry in cache]

        # Use interpolation to estimate the change rate for the current outdoor temp
        return np.interp(outside_temp, temps, rates)

    def _calculate_temperature_difference(self, space_temp):
        lower_limit, upper_limit, _ = self.comfort_limits
        if space_temp < lower_limit:
            return lower_limit - space_temp
        elif space_temp > upper_limit:
            return space_temp - upper_limit
        return 0

    def execute_optimal_start_stop(self):
        if self.schedule.is_time_for_action() and not self.fan_status.status():
            if self.schedule.current_action() == "active":
                start_time = self.calculate_start_time()
                if start_time and datetime.datetime.now() >= start_time:
                    self.start_equipment()

    def start_equipment(self):
        print("Starting equipment at", datetime.datetime.now())

        # Simulate logging a warm-up rate
        outside_temp = self.outside_temp_sensor.read()
        initial_temp = self.space_temp_sensor.read()
        final_temp = self.comfort_limits[0]  # Assume reaching the lower comfort limit
        warmup_minutes = 60  # Example warm-up time
        temp_change_rate = (final_temp - initial_temp) / warmup_minutes

        # Update the fan status with the new data
        self.fan_status.update_status(True, outside_air_temp=outside_temp, temp_change_rate=temp_change_rate)
