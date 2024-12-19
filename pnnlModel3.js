// Configuration Parameters
const forgettingFactor = 0.1; // Exponential smoothing factor
const earlyStartLimit = 180; // Maximum early start time in minutes
const lateStartLimit = 10; // Minimum pre-start time in minutes

// Initialize Parameters
let alpha3a = 10; // Default time to change indoor temp by 1 degree
let alpha3b = 5; // Time interval for outdoor temp influence
let alpha3d = 0; // Dynamic adjustment for start time

// Historical data (fake data for 7 days)
const historicalData = [
  { zoneTemp: 50, outdoorTemp: 10, warmupTimeMinutes: 120 },
  { zoneTemp: 48, outdoorTemp: 12, warmupTimeMinutes: 115 },
  { zoneTemp: 52, outdoorTemp: 8, warmupTimeMinutes: 125 },
  { zoneTemp: 50, outdoorTemp: 11, warmupTimeMinutes: 118 },
  { zoneTemp: 51, outdoorTemp: 9, warmupTimeMinutes: 122 },
  { zoneTemp: 49, outdoorTemp: 13, warmupTimeMinutes: 110 },
  { zoneTemp: 47, outdoorTemp: 14, warmupTimeMinutes: 108 },
];

// Current Conditions
const currentConditions = {
  zoneTemp: 48, // Current indoor temperature
  outdoorTemp: 12, // Current outdoor temperature
  occupiedSetPoint: 70, // Occupied temperature setpoint
};

function smoothParameters(alpha, alphaNew, forgettingFactor) {
  // Exponential smoothing for parameter updates
  return alpha + forgettingFactor * (alphaNew - alpha);
}

function calculateOptimalStart(currentConditions, alpha3a, alpha3b, alpha3d) {
  // Calculate optimal start time based on Model 3
  const Tsp = currentConditions.occupiedSetPoint;
  const Tz = currentConditions.zoneTemp;
  const To = currentConditions.outdoorTemp;

  let tOpt =
    alpha3a * (Tsp - Tz) +
    (alpha3b * (Tsp - Tz) * (Tsp - To)) / alpha3b +
    alpha3d;

  // Ensure tOpt is within configured bounds
  tOpt = Math.max(lateStartLimit, Math.min(tOpt, earlyStartLimit));
  return tOpt;
}

function updateParameters(historicalData, forgettingFactor) {
  // Update parameters alpha3a, alpha3b, and alpha3d using historical data
  for (const data of historicalData) {
    const Tsp = currentConditions.occupiedSetPoint;
    const Tz = data.zoneTemp;
    const To = data.outdoorTemp;
    const tActual = data.warmupTimeMinutes;

    // Calculate new alpha values based on historical data
    const alpha3aNew = Math.abs(tActual / (Tsp - Tz));
    const alpha3bNew = Math.abs(tActual / ((Tsp - Tz) * (Tsp - To)));
    const alpha3dNew =
      tActual -
      (alpha3aNew * (Tsp - Tz) +
        (alpha3bNew * (Tsp - Tz) * (Tsp - To)) / alpha3bNew);

    // Apply exponential smoothing
    alpha3a = smoothParameters(alpha3a, alpha3aNew, forgettingFactor);
    alpha3b = smoothParameters(alpha3b, alpha3bNew, forgettingFactor);
    alpha3d = smoothParameters(alpha3d, alpha3dNew, forgettingFactor);
  }
}

// Update parameters based on historical data
updateParameters(historicalData, forgettingFactor);

// Calculate optimal start time for current conditions
const optimalStartTime = calculateOptimalStart(
  currentConditions,
  alpha3a,
  alpha3b,
  alpha3d
);

// Display results
const currentTime = new Date();
const startTime = new Date(
  currentTime.getTime() - optimalStartTime * 60000
);
console.log(`Optimal Start Time: ${startTime}`);
console.log(
  `Parameters: alpha3a=${alpha3a.toFixed(2)}, alpha3b=${alpha3b.toFixed(2)}, alpha3d=${alpha3d.toFixed(2)}`
);
