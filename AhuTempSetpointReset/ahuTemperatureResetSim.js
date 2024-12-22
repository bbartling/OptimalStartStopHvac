// Configuration Parameters
const SP0 = 60; // Initial SAT setpoint in °F
const SPmin = 55; // Minimum SAT setpoint in °F
const SPmax = 65; // Maximum SAT setpoint in °F
const OATmin = 60; // Minimum outside air temperature in °F
const OATmax = 70; // Maximum outside air temperature in °F
const Td = 10 * 60 * 1000; // Delay timer in milliseconds (10 minutes)
const T = 2 * 60 * 1000; // Time step in milliseconds (2 minutes)

// Current System State
let currentSAT = SP0;
let deviceOn = false;

// Helper Function
function calculateSAT(OAT) {
  // Calculate SAT setpoint based on OAT
  if (OAT <= OATmin) {
    return SPmin;
  } else if (OAT >= OATmax) {
    return SPmax;
  } else {
    // Linear interpolation between SPmin and SPmax
    return SPmin + (SPmax - SPmin) * ((OAT - OATmin) / (OATmax - OATmin));
  }
}

// Simulation
console.log("Starting AHU Temperature Reset Simulation...");
setTimeout(() => {
  deviceOn = true;

  const interval = setInterval(() => {
    if (!deviceOn) clearInterval(interval);

    // Simulate fluctuating outside air temperature
    const currentOAT = Math.random() * (75 - 55) + 55;

    // Calculate the new SAT setpoint
    currentSAT = calculateSAT(currentOAT);
    console.log(`Current OAT: ${currentOAT.toFixed(2)}°F, Adjusted SAT: ${currentSAT.toFixed(2)}°F`);
  }, T);
}, Td);
