import datetime


class OptimizedStart:
    def __init__(self):
        # Default configuration values
        self.upper_comfort_limit = 77.0  # Upper temperature threshold (°F)
        self.lower_comfort_limit = 68.0  # Lower temperature threshold (°F)
        self.runtime_per_degree_cooling = 10.0  # Minutes to cool by 1°F
        self.runtime_per_degree_heating = 10.0  # Minutes to heat by 1°F
        self.earliest_start_time = datetime.time(6, 0)  #  6:00 AM

        # Input variables
        self.next_event_time = datetime.datetime.now().replace(hour=8, minute=0)
        self.space_temp = 60.0  # Current space temperature

    def calculate_lead_time(self):
        """Calculate the lead time for the start event."""
        if self.space_temp > self.upper_comfort_limit:
            return int(
                (self.space_temp - self.upper_comfort_limit)
                * self.runtime_per_degree_cooling
            )
        elif self.space_temp < self.lower_comfort_limit:
            return int(
                (self.lower_comfort_limit - self.space_temp)
                * self.runtime_per_degree_heating
            )
        else:
            return 0

    def update(self):
        """Calculate and display the optimized start time."""
        print("BAS schedule starts at: ", self.next_event_time)
        lead_time = self.calculate_lead_time()
        command_time = self.next_event_time - datetime.timedelta(minutes=lead_time)

        # Ensure the command time respects earliest constraints
        if command_time.time() < self.earliest_start_time:
            command_time = datetime.datetime.combine(
                command_time.date(), self.earliest_start_time
            )
            print("Optimized Start Calc is too early.")
            print("Resorting back to earliest start config.", self.earliest_start_time)

        # Display the calculated start time
        print(f"Optimized Start Command Time: {command_time}")


if __name__ == "__main__":
    # Simulate running the script at 5:00 AM
    print("Simulation: Running the Optimized Start Algorithm\n")

    # Initialize the optimized start system
    system = OptimizedStart()

    # Calculate and display the result
    system.update()
