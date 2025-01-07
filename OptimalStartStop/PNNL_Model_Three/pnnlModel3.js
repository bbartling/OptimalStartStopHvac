// Configuration Parameters
const earlyStartLimit = 180; // Maximum early start time in minutes
const lateStartLimit = 10; // Minimum pre-start time in minutes

// Initialize Parameters
let alpha3a = 10; // Default time to change indoor temp by 1 degree
let alpha3b = 5; // Time interval for outdoor temp influence
let alpha3d = 0; // Dynamic adjustment for start time

// Historical data
const historicalData = [
  { zoneTemp: 64.79, outdoorTemp: 41.4, warmupTimeMinutesHistory: 230 },
  { zoneTemp: 65.36, outdoorTemp: 34.07, warmupTimeMinutesHistory: 185 },
  { zoneTemp: 64.55, outdoorTemp: 31.82, warmupTimeMinutesHistory: 230 },
  { zoneTemp: 64.96, outdoorTemp: 32.45, warmupTimeMinutesHistory: 180 },
  { zoneTemp: 64.42, outdoorTemp: 16.45, warmupTimeMinutesHistory: 115 },
  { zoneTemp: 64.98, outdoorTemp: 31.13, warmupTimeMinutesHistory: 120 },
  { zoneTemp: 64.65, outdoorTemp: 18.08, warmupTimeMinutesHistory: 80 },
  { zoneTemp: 65.0, outdoorTemp: 21.57, warmupTimeMinutesHistory: 100 },
  { zoneTemp: 64.04, outdoorTemp: 22.76, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 65.06, outdoorTemp: 34.21, warmupTimeMinutesHistory: 105 },
  { zoneTemp: 64.53, outdoorTemp: 28.86, warmupTimeMinutesHistory: 105 },
  { zoneTemp: 65.46, outdoorTemp: 24.96, warmupTimeMinutesHistory: 105 },
  { zoneTemp: 65.32, outdoorTemp: 24.47, warmupTimeMinutesHistory: 105 },
  { zoneTemp: 64.01, outdoorTemp: -19.69, warmupTimeMinutesHistory: 100 },
  { zoneTemp: 64.18, outdoorTemp: -12.15, warmupTimeMinutesHistory: 70 },
  { zoneTemp: 63.92, outdoorTemp: -1.38, warmupTimeMinutesHistory: 55 },
  { zoneTemp: 63.86, outdoorTemp: -6.38, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 64.13, outdoorTemp: 15.82, warmupTimeMinutesHistory: 70 },
  { zoneTemp: 65.23, outdoorTemp: 33.14, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 65.39, outdoorTemp: 35.38, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 65.49, outdoorTemp: 36.19, warmupTimeMinutesHistory: 85 },
  { zoneTemp: 65.54, outdoorTemp: 36.33, warmupTimeMinutesHistory: 100 },
  { zoneTemp: 63.67, outdoorTemp: 25.75, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 65.44, outdoorTemp: 38.1, warmupTimeMinutesHistory: 150 },
  { zoneTemp: 65.44, outdoorTemp: 35.64, warmupTimeMinutesHistory: 140 },
  { zoneTemp: 65.59, outdoorTemp: 34.44, warmupTimeMinutesHistory: 115 },
  { zoneTemp: 65.09, outdoorTemp: 29.85, warmupTimeMinutesHistory: 145 },
  { zoneTemp: 63.98, outdoorTemp: 20.11, warmupTimeMinutesHistory: 100 },
  { zoneTemp: 64.94, outdoorTemp: 24.85, warmupTimeMinutesHistory: 75 },
  { zoneTemp: 65.34, outdoorTemp: 31.96, warmupTimeMinutesHistory: 90 },
  { zoneTemp: 65.99, outdoorTemp: 42.64, warmupTimeMinutesHistory: 110 },
  { zoneTemp: 66.23, outdoorTemp: 38.37, warmupTimeMinutesHistory: 205 },
  { zoneTemp: 64.44, outdoorTemp: 18.89, warmupTimeMinutesHistory: 45 },
  { zoneTemp: 64.51, outdoorTemp: 25.65, warmupTimeMinutesHistory: 40 },
  { zoneTemp: 64.42, outdoorTemp: 20.19, warmupTimeMinutesHistory: 30 },
  { zoneTemp: 64.98, outdoorTemp: 35.78, warmupTimeMinutesHistory: 45 },
  { zoneTemp: 64.14, outdoorTemp: 20.22, warmupTimeMinutesHistory: 60 },
  { zoneTemp: 64.26, outdoorTemp: 15.92, warmupTimeMinutesHistory: 25 },
  { zoneTemp: 64.71, outdoorTemp: 27.0, warmupTimeMinutesHistory: 55 },
  { zoneTemp: 65.0, outdoorTemp: 45.58, warmupTimeMinutesHistory: 70 },
  { zoneTemp: 64.96, outdoorTemp: 38.37, warmupTimeMinutesHistory: 45 },
  { zoneTemp: 64.77, outdoorTemp: 37.15, warmupTimeMinutesHistory: 50 },
  { zoneTemp: 64.08, outdoorTemp: 34.15, warmupTimeMinutesHistory: 50 },
  { zoneTemp: 64.81, outdoorTemp: 50.33, warmupTimeMinutesHistory: 60 },
  { zoneTemp: 64.56, outdoorTemp: 9.1, warmupTimeMinutesHistory: 230 },
  { zoneTemp: 64.12, outdoorTemp: 7.42, warmupTimeMinutesHistory: 45 },
  { zoneTemp: 65.11, outdoorTemp: 35.16, warmupTimeMinutesHistory: 55 },
];


// Current Conditions
const currentConditions = {
  zoneTemp: 48, // Current indoor temperature
  outdoorTemp: 12, // Current outdoor temperature
  occupiedSetPoint: 70, // Occupied temperature setpoint
};

// VOLTTRON-style EMA function
function ema(lst) {
  const smoothingConstant = lst.length
    ? Math.min(2.0 / (lst.length + 1.0) * 2.0, 1.0)
    : 1.0;
  let emaValue = 0;

  for (let n = 0; n < lst.length; n++) {
    const value = lst[lst.length - n - 1];
    emaValue += value * smoothingConstant * Math.pow(1.0 - smoothingConstant, n);
  }

  if (lst.length) {
    emaValue += lst[0] * Math.pow(1.0 - smoothingConstant, lst.length);
  }

  return emaValue;
}

// Calculate optimal start time
function calculateOptimalStart(currentConditions, alpha3a, alpha3b, alpha3d) {
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

// Update parameters using EMA
function updateParameters(historicalData) {
  const alpha3aList = [];
  const alpha3bList = [];
  const alpha3dList = [];

  for (const data of historicalData) {
    const Tsp = currentConditions.occupiedSetPoint;
    const Tz = data.zoneTemp;
    const To = data.outdoorTemp;
    const tActual = data.warmupTimeMinutesHistory;

    // Calculate new alpha values
    const alpha3aNew = Math.abs(tActual / (Tsp - Tz));
    const alpha3bNew = Math.abs(tActual / ((Tsp - Tz) * (Tsp - To)));
    const alpha3dNew =
      tActual -
      (alpha3aNew * (Tsp - Tz) +
        (alpha3bNew * (Tsp - Tz) * (Tsp - To)) / alpha3bNew);

    // Append new values to lists
    alpha3aList.push(alpha3aNew);
    alpha3bList.push(alpha3bNew);
    alpha3dList.push(alpha3dNew);
  }

  // Apply EMA to update parameters
  alpha3a = ema(alpha3aList);
  alpha3b = ema(alpha3bList);
  alpha3d = ema(alpha3dList);
}

// Update parameters based on historical data
updateParameters(historicalData);

// Calculate optimal start time for current conditions
const optimalStartTime = calculateOptimalStart(
  currentConditions,
  alpha3a,
  alpha3b,
  alpha3d
);

// Log the results
console.log(`Optimal Start Time in Minutes: ${optimalStartTime}`);
console.log(
  `Parameters: alpha3a=${alpha3a.toFixed(2)}, alpha3b=${alpha3b.toFixed(2)}, alpha3d=${alpha3d.toFixed(2)}`
);
