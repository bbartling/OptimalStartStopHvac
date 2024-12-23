const readline = require("readline");

// Configuration Parameters
const SP0 = 0.5; // Initial static pressure setpoint in inches WC
const SPmin = 0.50; // Minimum allowable static pressure
const SPmax = 1.5; // Maximum allowable static pressure
const Td = 5000; // Delay timer in milliseconds for simulation
const T = 2000; // Time step in milliseconds for simulation
const I = 2; // Number of ignored requests (top I dampers excluded)
const SPtrim = -0.02; // Trim adjustment in inches WC
const SPres = 0.06; // Response adjustment in inches WC
const HighDamperSpt = 0.85;
const NUM_DAMPERS = 10; // Fixed number of VAV box dampers for the simulation only

// Current System State
let currentStaticPressure = SP0;
let deviceOn = false;

// Helper Functions
function calculateRequests(vavDampers) {
  /**
   * Calculate requests based on VAV damper positions being greater than or equal to HighDamperSpt.
   * Also, print the ignored damper positions (top I) and the max position after excluding the top I dampers.
   */
  const sortedDampers = vavDampers.sort((a, b) => b - a); // Sort descending
  const ignoredDampers = sortedDampers.slice(0, I); // Top I dampers
  const remainingDampers = sortedDampers.slice(I); // Dampers after ignoring top I
  const maxRemainingDamper =
    remainingDampers.length > 0 ? Math.max(...remainingDampers) : null;

  // Use a simple for loop to count requests
  let numRequests = 0;
  for (const pos of remainingDampers) {
    if (pos >= HighDamperSpt) {
      numRequests++;
    }
  }

  // Print results
  console.log(`Ignored Damper Positions: ${ignoredDampers}`);
  if (maxRemainingDamper !== null) {
    console.log(
      `Max Damper Position (After Excluding Top ${I}): ${maxRemainingDamper.toFixed(
        2
      )}`
    );
  } else {
    console.log(`No remaining dampers to evaluate after excluding the top ${I}.`);
  }
  console.log(`Net Requests (Factoring Ignored Dampers): ${numRequests}`);

  return numRequests;
}

function adjustStaticPressure(currentPressure, numRequests) {
  /**
   * Adjust the static pressure based on the number of requests.
   * Trim if no requests, respond if requests exist.
   */
  let adjustment = 0;
  if (numRequests === 0) {
    // Trim static pressure
    adjustment = SPtrim;
    currentPressure = Math.max(SPmin, currentPressure + adjustment);
    console.log("We need less static!...");
  } else {
    // Respond by increasing static pressure
    adjustment = SPres;
    currentPressure = Math.min(SPmax, currentPressure + adjustment);
    console.log("We need more static!...");
  }
  return { currentPressure, adjustment };
}

// Simulation
console.log("Starting AHU Static Pressure Simulation...");
console.log(`Ignore Var Set to ${I} for the simulation...`);

setTimeout(() => {
  deviceOn = true;

  const simulationInterval = setInterval(() => {
    if (!deviceOn) {
      clearInterval(simulationInterval);
      return;
    }

    // Generate exactly NUM_DAMPERS damper positions
    const vavDampers = Array.from({ length: NUM_DAMPERS }, () =>
      parseFloat((Math.random() * (0.95 - 0.3) + 0.3).toFixed(2))
    );

    // Calculate the number of requests
    const numRequests = calculateRequests(vavDampers);

    // Adjust static pressure and determine adjustment type
    const previousPressure = currentStaticPressure;
    const { currentPressure, adjustment } = adjustStaticPressure(
      currentStaticPressure,
      numRequests
    );
    currentStaticPressure = currentPressure;
    const adjustmentType = adjustment > 0 ? "increased" : "decreased";

    // Print the results for this time step
    console.log(`Previous Static Pressure Setpoint: ${previousPressure.toFixed(2)}” WC`);
    console.log(`Current Static Pressure Setpoint: ${currentStaticPressure.toFixed(2)}” WC (${adjustmentType})\n`);
  }, T);
}, Td);
