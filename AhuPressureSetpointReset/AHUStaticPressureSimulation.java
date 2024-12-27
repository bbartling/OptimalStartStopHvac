import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

public class AHUStaticPressureSimulation {

    // Configuration Parameters
    private static final double SP0 = 0.5; // Initial static pressure setpoint in inches WC
    private static final double SPmin = 0.50; // Minimum allowable static pressure
    private static final double SPmax = 1.5; // Maximum allowable static pressure
    private static final int Td = 5000; // Delay timer in milliseconds for simulation
    private static final int T = 2000; // Time step in milliseconds for simulation
    private static final int I = 2; // Number of ignored requests (top I dampers excluded)
    private static final double SPtrim = -0.02; // Trim adjustment in inches WC
    private static final double SPres = 0.06; // Response adjustment in inches WC
    private static final double SPresMax = 0.15; // Maximum allowable response adjustment (inches WC)
    private static final double HighDamperSpt = 0.85;
    private static final int NUM_DAMPERS = 40; // Fixed number of VAV box dampers for the simulation only

    // Current System State
    private double currentStaticPressure = SP0;
    private boolean deviceOn = false;

    public static void main(String[] args) {
        AHUStaticPressureSimulation simulation = new AHUStaticPressureSimulation();
        simulation.runSimulation();
    }

    public void runSimulation() {
        System.out.println("Starting AHU Static Pressure Simulation...");
        System.out.println("Ignore Var Set to " + I + " for the simulation...");

        try {
            Thread.sleep(Td);
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

                List<Double> vavDampers = generateRandomDamperPositions();
                int numRequests = calculateRequests(vavDampers);

                double previousPressure = currentStaticPressure;
                AdjustmentResult adjustmentResult = adjustStaticPressure(currentStaticPressure, numRequests);
                currentStaticPressure = adjustmentResult.currentPressure;

                System.out.printf("Previous Static Pressure Setpoint: %.2f\" WC%n", previousPressure);
                System.out.printf("Current Static Pressure Setpoint: %.2f\" WC (%s)%n%n", currentStaticPressure, adjustmentResult.adjustmentType);
            }
        }, 0, T);
    }

    private List<Double> generateRandomDamperPositions() {
        List<Double> vavDampers = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < NUM_DAMPERS; i++) {
            vavDampers.add(0.3 + (0.95 - 0.3) * random.nextDouble());
        }
        return vavDampers;
    }

    private int calculateRequests(List<Double> vavDampers) {
        Collections.sort(vavDampers, Collections.reverseOrder());
        List<Double> ignoredDampers = vavDampers.subList(0, Math.min(I, vavDampers.size()));
        List<Double> remainingDampers = vavDampers.subList(Math.min(I, vavDampers.size()), vavDampers.size());
        Double maxRemainingDamper = remainingDampers.isEmpty() ? null : Collections.max(remainingDampers);

        long numRequests = remainingDampers.stream().filter(pos -> pos >= HighDamperSpt).count();

        System.out.println("Ignored Damper Positions: " + ignoredDampers);
        if (maxRemainingDamper != null) {
            System.out.printf("Max Damper Position (After Excluding Top %d): %.2f%n", I, maxRemainingDamper);
        } else {
            System.out.printf("No remaining dampers to evaluate after excluding the top %d.%n", I);
        }
        System.out.println("Net Requests (Factoring Ignored Dampers): " + numRequests);

        return (int) numRequests;
    }

    private AdjustmentResult adjustStaticPressure(double currentPressure, int numRequests) {
        double totalAdjustment;
        if (numRequests == 0) {
            totalAdjustment = SPtrim;
        } else {
            totalAdjustment = SPres * numRequests;
        }

        if (totalAdjustment > 0) {
            totalAdjustment = Math.min(totalAdjustment, SPresMax);
        } else if (totalAdjustment < 0) {
            totalAdjustment = Math.max(totalAdjustment, -SPresMax);
        }

        System.out.printf("Total Adjustment is %.2f Inch WC%n", totalAdjustment);

        currentPressure = Math.max(SPmin, Math.min(SPmax, currentPressure + totalAdjustment));
        String adjustmentType = totalAdjustment > 0 ? "increased" : "decreased";
        System.out.println("We need " + (totalAdjustment > 0 ? "more" : "less") + " static!...");

        return new AdjustmentResult(currentPressure, adjustmentType);
    }

    private static class AdjustmentResult {
        double currentPressure;
        String adjustmentType;

        AdjustmentResult(double currentPressure, String adjustmentType) {
            this.currentPressure = currentPressure;
            this.adjustmentType = adjustmentType;
        }
    }
}
