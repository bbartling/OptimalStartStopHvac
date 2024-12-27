import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class AHUTemperatureResetSim {

    // Configuration Parameters
    private final double SP0 = 60.0; // Initial SAT setpoint in °F
    private final double SPmin = 55.0; // Minimum SAT setpoint in °F
    private final double SPmaxDefault = 65.0; // Default maximum SAT setpoint in °F
    private final double highOatSPmax = 60.0; // Maximum SAT setpoint at high OAT
    private final double OATmin = 60.0; // Minimum outside air temperature in °F
    private final double OATmax = 70.0; // Maximum outside air temperature in °F
    private final double HighZoneTempSpt = 75.0; // Zone temperature threshold in °F

    private final int Td = 5000; // Delay timer in milliseconds
    private final int T = 5000; // Time step in milliseconds
    private final int I = 2; // Number of ignored requests (top I zones excluded)

    private final double SPtrim = 0.2; // Trim adjustment in °F
    private final double SPres = -0.3; // Response adjustment in °F
    private final double SPresMax = 1.0; // Maximum allowable response adjustment (in °F)

    private final int NUM_ZONES = 40; // Fixed number of zones for simulation

    // Current State
    private double currentSAT;
    private boolean deviceOn;

    public AHUTemperatureResetSim() {
        this.currentSAT = SP0;
        this.deviceOn = false;
    }

    public static void main(String[] args) {
        AHUTemperatureResetSim simulation = new AHUTemperatureResetSim();
        simulation.runSimulation();
    }

    public void runSimulation() {
        System.out.println("Starting AHU Temperature Reset Simulation...");
        System.out.printf("High Zone Temperature Threshold: %.2f°F%n", HighZoneTempSpt);
        System.out.printf("Ignore Var Set to %d for the simulation...%n", I);

        try {
            Thread.sleep(Td); // Wait for delay timer
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        deviceOn = true;

        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                if (!deviceOn) {
                    timer.cancel();
                    return;
                }

                Random random = new Random();

                // Simulate fluctuating outside air temperature
                double currentOAT = 55.0 + (75.0 - 55.0) * random.nextDouble();
                double dynamicSPmax = calculateDynamicSPmax(currentOAT);

                // Simulate zone temperatures
                List<Double> zoneTemps = generateRandomZoneTemps();

                int numRequests = calculateRequests(zoneTemps);

                // Adjust SAT based on cooling requests
                double previousSAT = currentSAT;
                AdjustmentResult result = adjustSAT(numRequests, dynamicSPmax);
                currentSAT = result.currentSAT;

                // Print results for this time step
                System.out.printf("Current OAT: %.2f°F%n", currentOAT);
                System.out.printf("Dynamic SPmax: %.2f°F%n", dynamicSPmax);
                System.out.printf("Previous SAT Setpoint: %.2f°F%n", previousSAT);
                System.out.printf("Current SAT Setpoint: %.2f°F (%s)%n%n", currentSAT, result.adjustmentType);
            }
        }, 0, T);
    }

    private double calculateDynamicSPmax(double OAT) {
        if (OAT <= OATmin) {
            return SPmaxDefault;
        } else if (OAT >= OATmax) {
            return highOatSPmax;
        } else {
            return SPmaxDefault - ((SPmaxDefault - highOatSPmax) * ((OAT - OATmin) / (OATmax - OATmin)));
        }
    }

    private List<Double> generateRandomZoneTemps() {
        List<Double> zoneTemps = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < NUM_ZONES; i++) {
            zoneTemps.add(65.0 + (80.0 - 65.0) * random.nextDouble());
        }
        return zoneTemps;
    }

    private int calculateRequests(List<Double> zoneTemps) {
        Collections.sort(zoneTemps, Collections.reverseOrder());
        List<Double> ignoredTemps = zoneTemps.subList(0, Math.min(I, zoneTemps.size()));
        List<Double> remainingTemps = zoneTemps.subList(Math.min(I, zoneTemps.size()), zoneTemps.size());

        long numRequests = remainingTemps.stream().filter(temp -> temp >= HighZoneTempSpt).count();

        // Print debug information
        System.out.print("Ignored Zone Temperatures: ");
        ignoredTemps.forEach(temp -> System.out.printf("%.2f, ", temp));
        System.out.println();

        if (!remainingTemps.isEmpty()) {
            System.out.printf("Max Zone Temperature (After Excluding Top %d): %.2f°F%n", I, Collections.max(remainingTemps));
        } else {
            System.out.printf("No remaining zones to evaluate after excluding the top %d.%n", I);
        }

        System.out.printf("Net Requests (Factoring Ignored Zones): %d%n", numRequests);

        return (int) numRequests;
    }

    private AdjustmentResult adjustSAT(int numRequests, double dynamicSPmax) {
        double totalAdjustment;

        if (numRequests == 0) {
            totalAdjustment = SPtrim;
        } else {
            totalAdjustment = SPres * numRequests;
        }

        // Cap the adjustment to SPresMax
        if (totalAdjustment > 0) {
            totalAdjustment = Math.min(totalAdjustment, SPresMax);
        } else if (totalAdjustment < 0) {
            totalAdjustment = Math.max(totalAdjustment, -SPresMax);
        }

        System.out.printf("Total Adjustment is %.2f°F%n", totalAdjustment);

        // Update SAT with capped adjustment
        currentSAT = Math.max(SPmin, Math.min(dynamicSPmax, currentSAT + totalAdjustment));

        String adjustmentType = totalAdjustment > 0 ? "increased" : "decreased";
        System.out.println("We need " + (totalAdjustment > 0 ? "less" : "more") + " cooling!...");

        return new AdjustmentResult(currentSAT, adjustmentType);
    }

    private static class AdjustmentResult {
        double currentSAT;
        String adjustmentType;

        AdjustmentResult(double currentSAT, String adjustmentType) {
            this.currentSAT = currentSAT;
            this.adjustmentType = adjustmentType;
        }
    }
}
