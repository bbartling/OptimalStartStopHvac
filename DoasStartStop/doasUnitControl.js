// Configuration Parameters
const BUILDING_START_TIME = "07:00"; // Building start time (24-hour format)
const BUILDING_END_TIME = "18:00";   // Building end time (24-hour format)
const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]; // Occupied days
const OVERRIDE_COMMAND = "Command_DOAS_Off";
const RELEASE_COMMAND = "Release_DOAS_Overrides";

// Helper Functions
function isBuildingOccupied(randomDay, randomTime) {
    /**
     * Check if the building is occupied based on the schedule.
     */
    if (DAYS_OF_WEEK.includes(randomDay)) {
        return BUILDING_START_TIME <= randomTime && randomTime <= BUILDING_END_TIME;
    }
    return false;
}

function generateRandomTimeAndDay() {
    /**
     * Generate a random day and time for simulation purposes.
     */
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const randomDay = days[Math.floor(Math.random() * days.length)];
    const randomHour = Math.floor(Math.random() * 24);
    const randomMinute = Math.floor(Math.random() * 60);
    const randomTime = `${randomHour.toString().padStart(2, "0")}:${randomMinute.toString().padStart(2, "0")}`;
    return { randomDay, randomTime };
}

// Main Logic
function controlDOAS() {
    /**
     * Control the DOAS unit based on the building occupancy schedule.
     */
    console.log("Starting DOAS Unit Control Simulation...");

    setInterval(() => {
        // Generate a random time and day for simulation
        const { randomDay, randomTime } = generateRandomTimeAndDay();

        // Check if the generated time and day are within the building's schedule
        const occupied = isBuildingOccupied(randomDay, randomTime);

        // Print whether the building is occupied or not
        if (occupied) {
            console.log(`${randomDay} ${randomTime}: Building is occupied. Release back to the BAS! ${RELEASE_COMMAND}`);
        } else {
            console.log(`${randomDay} ${randomTime}: Building is unoccupied. Override the BAS! ${OVERRIDE_COMMAND}`);
        }
    }, 2000); // Run every 2 seconds for simulation purposes
}

// Run the simulation
controlDOAS();
