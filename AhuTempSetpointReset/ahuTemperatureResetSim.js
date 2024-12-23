const readline = require("readline");

// Configuration Parameters
const SP0 = 60; // Initial SAT setpoint in °F
const SPmin = 55; // Minimum SAT setpoint in °F
const SPmaxDefault = 65; // Default maximum SAT setpoint in °F
const highOatSPmax = 60; // Maximum SAT setpoint at high OAT
const OATmin = 60; // Minimum outside air temperature in °F
const OATmax = 70; // Maximum outside air temperature in °F
const HighZoneTempSpt = 75; // Zone temperature threshold to generate cooling requests in °F

const Td = 5; // Delay timer in seconds for simulation
const T = 5; // Time step in seconds for simulation
const I = 2; // Number of ignored requests (top I zones excluded)

const SPtrim = +0.2; // Trim adjustment in °F
const SPres = -0.3; // Response adjustment in °F

const NUM_ZONES = 10; // Fixed number of zones for simulation
let currentSAT = SP0;

// Helper Functions
function calculateDynamicSPmax(OAT) {
  /**
   * Calculate the dynamic maximum SAT setpoint (SPmax) based on the OAT.
   * Linearly decreases SPmax from SPmaxDefault to highOatSPmax as OAT rises from OATmin to OATmax.
   */
  if (OAT <= OATmin) {
    return SPmaxDefault;
  } else if (OAT >= OATmax) {
    return highOatSPmax;
  } else {
    return (
      SPmaxDefault -
      (SPmaxDefault - highOatSPmax) * ((OAT - OATmin) / (OATmax - OATmin))
    );
  }
}

function calculateRequests(zoneTemps) {
  /**
   * Calculate requests based on zone temperatures being greater than or equal to HighZoneTempSpt.
   * Also, print the ignored zone temperatures (top I) and the max zone temperature after excluding the top I.
   */
  const sortedTemps = [...zoneTemps].sort((a, b) => b - a); // Sort descending
  const ignoredTemps = sortedTemps.slice(0, I); // Top I temperatures
  const remainingTemps = sortedTemps.slice(I); // Temperatures after ignoring top I
  const maxRemainingTemp = remainingTemps.length > 0 ? Math.max(...remainingTemps) : null;

  // Count requests
  let numRequests = 0;
  for (const temp of remainingTemps) {
    if (temp >= HighZoneTempSpt) {
      numRequests++;
    }
  }

  // Print results
  console.log(`Ignored Zone Temperatures: ${ignoredTemps.map(t => t.toFixed(2)).join(", ")}`);
  if (maxRemainingTemp !== null) {
    console.log(`Max Zone Temperature (After Excluding Top ${I}): ${maxRemainingTemp.toFixed(2)}°F`);
  } else {
    console.log(`No remaining zones to evaluate after excluding the top ${I}.`);
  }
  console.log(`Net Requests (Factoring Ignored Zones): ${numRequests}`);
  return numRequests;
}

function adjustSAT(currentSAT, numRequests, dynamicSPmax) {
  /**
   * Adjust the SAT based on the number of requests.
   * Trim if no requests, respond if requests exist.
   */
  let adjustment;
  if (numRequests === 0) {
    adjustment = SPtrim;
    currentSAT = Math.min(dynamicSPmax, currentSAT + adjustment); // Ensure SAT trim stays within dynamicSPmax
    console.log("We need less cooling!...");
  } else {
    adjustment = SPres;
    currentSAT = Math.max(SPmin, currentSAT + adjustment); // Ensure SAT does not go below SPmin
    console.log("We need more cooling!...");
  }
  return { currentSAT, adjustment };
}

// Simulation
console.log("Starting AHU Temperature Reset Simulation...");
console.log(`High Zone Temperature Threshold: ${HighZoneTempSpt}°F`);
console.log(`Ignore Var Set to ${I} for the simulation...`);

setTimeout(() => {
  let deviceOn = true;

  function simulate() {
    if (!deviceOn) return;

    // Simulate a fluctuating outside air temperature
    const currentOAT = Math.random() * 20 + 55; // Random OAT between 55°F and 75°F
    const dynamicSPmax = calculateDynamicSPmax(currentOAT);

    // Simulate zone temperatures
    const zoneTemps = Array.from({ length: NUM_ZONES }, () => Math.random() * 15 + 65); // Random temps between 65°F and 80°F
    const numRequests = calculateRequests(zoneTemps);

    // Adjust SAT based on cooling requests
    const previousSAT = currentSAT;
    const result = adjustSAT(currentSAT, numRequests, dynamicSPmax);
    currentSAT = result.currentSAT;
    const adjustmentType = result.adjustment > 0 ? "increased" : "decreased";

    // Print the results for this time step
    console.log(`Current OAT: ${currentOAT.toFixed(2)}°F`);
    console.log(`Dynamic SPmax: ${dynamicSPmax.toFixed(2)}°F`);
    console.log(`Previous SAT Setpoint: ${previousSAT.toFixed(2)}°F`);
    console.log(`Current SAT Setpoint: ${currentSAT.toFixed(2)}°F (${adjustmentType})\n`);

    // Schedule next simulation step
    setTimeout(simulate, T * 1000);
  }

  simulate();
}, Td * 1000);
