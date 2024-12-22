// Configuration Parameters
const SP0 = 0.5; // Initial static pressure setpoint in inches WC
const SPmin = 0.15; // Minimum allowable static pressure
const SPmax = 1.5; // Maximum allowable static pressure
const Td = 5 * 60 * 1000; // Delay timer in milliseconds (5 minutes)
const T = 2 * 60 * 1000; // Time step in milliseconds (2 minutes)
const I = 2; // Number of ignored requests (top 2 VAV boxes)
const SPtrim = -0.02; // Trim adjustment in inches WC
const SPres = 0.04; // Response adjustment in inches WC
const SPresMax = 0.06; // Max allowable response adjustment

// Current System State
let currentStaticPressure = SP0;
let deviceOn = false;

// Helper Functions
function calculateRequests(vavDampers) {
  // Calculate requests based on damper positions
  const requests = vavDampers.filter(pos => pos > 0.75 || pos < 0.5);
  return { requestCount: requests.length, requests };
}

function adjustStaticPressure(currentPressure, R) {
  // Adjust static pressure based on the number of requests
  if (R <= 1) {
    currentPressure = Math.max(SPmin, currentPressure + SPtrim);
  } else {
    const adjustment = Math.min(SPres * (R - I), SPresMax);
    currentPressure = Math.min(SPmax, currentPressure + adjustment);
  }
  return currentPressure;
}

// Simulation
console.log("Starting AHU Static Pressure Simulation...");
setTimeout(() => {
  deviceOn = true;

  const interval = setInterval(() => {
    if (!deviceOn) clearInterval(interval);

    // Simulate VAV damper positions (random for demonstration)
    const vavDampers = Array.from({ length: 10 }, () =>
      Math.random() * (0.9 - 0.3) + 0.3
    );
    const { requestCount } = calculateRequests(vavDampers);

    // Adjust static pressure
    currentStaticPressure = adjustStaticPressure(currentStaticPressure, requestCount);
    console.log(`Current Static Pressure: ${currentStaticPressure.toFixed(2)}” WC`);
  }, T);
}, Td);
