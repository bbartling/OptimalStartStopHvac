const readline = require('readline');

// Configuration Parameters
const BUILDING_START_TIME = "07:00"; // Building start time (24-hour format)
const BUILDING_END_TIME = "18:00";   // Building end time (24-hour format)
const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]; // Occupied days
const OVERRIDE_COMMAND = "Dampers_Closed";
const RELEASE_COMMAND = "Release_Control";
const ECON_HIGH_LIMIT_TEMP = 60; // Maximum outdoor air temperature for enabling free cooling (°F)
const ECON_LOW_LIMIT_TEMP = 50;  // Minimum outdoor air temperature for enabling free cooling (°F)

// Helper Functions
function isBuildingOccupied(randomDay, randomTime) {
    // Check if the building is occupied based on the schedule
    return DAYS_OF_WEEK.includes(randomDay) && randomTime >= BUILDING_START_TIME && randomTime <= BUILDING_END_TIME;
}

function isFreeCoolingEnabled(OAT) {
    // Check if the outdoor air temperature is within the free cooling range
    return OAT >= ECON_LOW_LIMIT_TEMP && OAT <= ECON_HIGH_LIMIT_TEMP;
}

function generateRandomTimeAndDay() {
    // Generate a random day and time for simulation purposes
    const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const randomDay = daysOfWeek[Math.floor(Math.random() * daysOfWeek.length)];
    const randomHour = String(Math.floor(Math.random() * 24)).padStart(2, '0');
    const randomMinute = String(Math.floor(Math.random() * 60)).padStart(2, '0');
    return { randomDay, randomTime: `${randomHour}:${randomMinute}` };
}

function controlAhuDampers() {
    console.log("Starting Night Recirculation Mode Control Simulation...");

    setInterval(() => {
        // Generate random day, time, and AHU status
        const { randomDay, randomTime } = generateRandomTimeAndDay();
        const AHU_ACTIVE = Math.random() < 0.5; // Randomly simulate AHU activity
        const currentOAT = (Math.random() * (70 - 40) + 40).toFixed(2); // Simulate fluctuating outdoor air temperature

        // Check if the building is occupied
        const occupied = isBuildingOccupied(randomDay, randomTime);

        if (!occupied) {
            if (AHU_ACTIVE) {
                if (isFreeCoolingEnabled(currentOAT)) {
                    console.log(`${randomDay} ${randomTime}: Building is unoccupied. AHU is active. Free cooling enabled (OAT: ${currentOAT}°F). ${RELEASE_COMMAND}`);
                } else {
                    console.log(`${randomDay} ${randomTime}: Building is unoccupied. AHU is active. Free cooling disabled (OAT: ${currentOAT}°F). ${OVERRIDE_COMMAND}`);
                }
            } else {
                console.log(`${randomDay} ${randomTime}: Building is unoccupied. AHU is inactive. No action required.`);
            }
        } else {
            console.log(`${randomDay} ${randomTime}: Building is occupied. ${RELEASE_COMMAND}`);
        }
    }, 2000); // Run every 2 seconds for simulation
}

// Start the simulation
controlAhuDampers();
