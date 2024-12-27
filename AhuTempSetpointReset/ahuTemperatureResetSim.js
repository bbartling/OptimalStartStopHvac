// Configuration Parameters
const SP0 = 60; // Initial SAT setpoint in °F
const SPmin = 55; // Minimum SAT setpoint in °F
const SPmaxDefault = 65; // Default maximum SAT setpoint in °F
const highOatSPmax = 60; // Maximum SAT setpoint at high OAT
const OATmin = 60; // Minimum outside air temperature in °F
const OATmax = 70; // Maximum outside air temperature in °F
const HighZoneTempSpt = 75; // Zone temperature threshold to generate cooling requests in °F

const Td = 5000; // Delay timer in milliseconds for simulation
const T = 5000; // Time step in milliseconds for simulation
const I = 2; // Number of ignored requests (top I zones excluded)

const SPtrim = 0.2; // Trim adjustment in °F
const SPres = -0.3; // Response adjustment in °F
const SPresMax = 1.0; // Maximum allowable response adjustment (in °F)

const NUM_ZONES = 40; // Fixed number of zones for simulation
let currentSAT = SP0;
let deviceOn = false;

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
    // Linear interpolation
    return (
      SPmaxDefault -
      ((SPmaxDefault - highOatSPmax) * ((OAT - OATmin) / (OATmax - OATmin)))
    );
  }
}

function calculateRequests(zoneTemps) {
  /**
   * Calculate requests based on zone temperatures being greater than or equal to HighZoneTempSpt.
   */
  const sortedTemps = [...zoneTemps].sort((a, b) => b - a); // Sort descending
  const ignoredTemps = sortedTemps.slice(0, I); // Top I temperatures
  const remainingTemps = sortedTemps.slice(I); // Temperatures after ignoring top I
  const maxRemainingTemp = remainingTemps.length > 0 ? Math.max(...remainingTemps) : null;

  const numRequests = remainingTemps.filter((temp) => temp >= HighZoneTempSpt).length;

  // Print results
  console.log(`Ignored Zone Temperatures: ${ignoredTemps.map((temp) => temp.toFixed(2)).join(", ")}`);
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
   * Limit adjustment to SPresMax.
   */
  let totalAdjustment = 0;
  if (numRequests === 0) {
    // Trim SAT
    totalAdjustment = SPtrim;
  } else {
    // Respond by decreasing SAT
    totalAdjustment = SPres * numRequests;
  }

  // Cap the adjustment to SPresMax
  if (totalAdjustment > 0) {
    totalAdjustment = Math.min(totalAdjustment, SPresMax);
  } else if (totalAdjustment < 0) {
    totalAdjustment = Math.max(totalAdjustment, -SPresMax);
  }

  console.log(`Total Adjustment is ${totalAdjustment.toFixed(2)}°F`);

  // Update the current SAT with capped adjustment
  currentSAT = Math.max(SPmin, Math.min(dynamicSPmax, currentSAT + totalAdjustment));

  const adjustmentType = totalAdjustment > 0 ? "increased" : "decreased";
  console.log(`We need ${totalAdjustment > 0 ? "less" : "more"} cooling!...`);

  return { currentSAT, totalAdjustment, adjustmentType };
}

// Simulation
console.log("Starting AHU Temperature Reset Simulation...");
console.log(`High Zone Temperature Threshold: ${HighZoneTempSpt}°F`);
console.log(`Ignore Var Set to ${I} for the simulation...`);

setTimeout(() => {
  deviceOn = true;

  const simulationInterval = setInterval(() => {
    if (!deviceOn) {
      clearInterval(simulationInterval);
      return;
    }

    // Simulate a fluctuating outside air temperature
    const currentOAT = Math.random() * (75 - 55) + 55;
    const dynamicSPmax = calculateDynamicSPmax(currentOAT);

    // Simulate zone temperatures
    // zoneTemps can be a fixed number to simulate increase or decrease logic
    const zoneTemps = Array.from({ length: NUM_ZONES }, () => Math.random() * (80 - 65) + 65);  
    const numRequests = calculateRequests(zoneTemps);

    // Adjust SAT based on cooling requests
    const previousSAT = currentSAT;
    const { currentSAT: newSAT, totalAdjustment, adjustmentType } = adjustSAT(currentSAT, numRequests, dynamicSPmax);
    currentSAT = newSAT;

    // Print the results for this time step
    console.log(`Current OAT: ${currentOAT.toFixed(2)}°F`);
    console.log(`Dynamic SPmax: ${dynamicSPmax.toFixed(2)}°F`);
    console.log(`Previous SAT Setpoint: ${previousSAT.toFixed(2)}°F`);
    console.log(`Current SAT Setpoint: ${currentSAT.toFixed(2)}°F (${adjustmentType})\n`);
  }, T);
}, Td);
