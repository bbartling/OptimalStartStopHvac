// Configuration Parameters
const BUILDING_START_TIME = "07:00"; // Building start time (24-hour format)
const BUILDING_END_TIME = "18:00";   // Building end time (24-hour format)
const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]; // Occupied days
const OVERRIDE_COMMAND = "Dampers_Closed";
const RELEASE_COMMAND = "Release_Control";

// Current System State
let AHU_ACTIVE = false; // Simulate the AHU's activity status

// Helper Functions
function isBuildingOccupied(currentTime) {
  const options = { weekday: "long", hour: "2-digit", minute: "2-digit", hour12: false };
  const formattedTime = new Intl.DateTimeFormat("en-US", options).format(currentTime);
  const [currentDay, currentHourMinute] = formattedTime.split(", ");

  if (DAYS_OF_WEEK.includes(currentDay)) {
    return BUILDING_START_TIME <= currentHourMinute && currentHourMinute <= BUILDING_END_TIME;
  }
  return false;
}

// Main Logic
function controlAHUDampers() {
  console.log("Starting Night Recirculation Mode Control...");
  setInterval(() => {
    const currentTime = new Date();
    const occupied = isBuildingOccupied(currentTime);

    if (!occupied && AHU_ACTIVE) {
      console.log(`${currentTime}: Building is unoccupied. AHU is active. ${OVERRIDE_COMMAND}`);
    } else if (occupied) {
      console.log(`${currentTime}: Building is occupied. ${RELEASE_COMMAND}`);
    } else {
      console.log(`${currentTime}: Building is unoccupied. AHU is inactive. No action required.`);
    }
  }, 60000); // Check every minute
}

// Start the control process
controlAHUDampers();
