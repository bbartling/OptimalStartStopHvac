// Configuration Parameters
const BUILDING_START_TIME = "07:00"; // Building start time (24-hour format)
const BUILDING_END_TIME = "18:00";   // Building end time (24-hour format)
const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]; // Occupied days
const OVERRIDE_COMMAND = "DOAS_Off";
const RELEASE_COMMAND = "Release_Control";

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
function controlDOAS() {
  console.log("Starting DOAS Unit Control...");
  setInterval(() => {
    const currentTime = new Date();
    const occupied = isBuildingOccupied(currentTime);

    if (occupied) {
      console.log(`${currentTime}: Building is occupied. ${RELEASE_COMMAND}`);
    } else {
      console.log(`${currentTime}: Building is unoccupied. ${OVERRIDE_COMMAND}`);
    }
  }, 60000); // Check every minute
}

// Start the control process
controlDOAS();
