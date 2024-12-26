import java.util.*;

public class PnnlModel3 {
    // Configuration Parameters
    private static final double FORGETTING_FACTOR = 0.1; // Exponential smoothing factor
    private static final int EARLY_START_LIMIT = 180; // Maximum early start time in minutes
    private static final int LATE_START_LIMIT = 10; // Minimum pre-start time in minutes

    // Initialize Parameters
    private static double alpha3a = 10; // Default time to change indoor temp by 1 degree
    private static double alpha3b = 5; // Time interval for outdoor temp influence
    private static double alpha3d = 0; // Dynamic adjustment for start time

    // Historical data
    private static final List<Map<String, Object>> historicalData = Arrays.asList(
        Map.of("zoneTemp", 50, "outdoorTemp", 10, "warmupTimeMinutesHistory", 120),
        Map.of("zoneTemp", 48, "outdoorTemp", 12, "warmupTimeMinutesHistory", 115),
        Map.of("zoneTemp", 52, "outdoorTemp", 8, "warmupTimeMinutesHistory", 125),
        Map.of("zoneTemp", 50, "outdoorTemp", 11, "warmupTimeMinutesHistory", 118),
        Map.of("zoneTemp", 51, "outdoorTemp", 9, "warmupTimeMinutesHistory", 122),
        Map.of("zoneTemp", 49, "outdoorTemp", 13, "warmupTimeMinutesHistory", 110),
        Map.of("zoneTemp", 47, "outdoorTemp", 14, "warmupTimeMinutesHistory", 108)
    );

    // Current conditions
    private static final Map<String, Integer> currentConditions = Map.of(
        "zoneTemp", 48,
        "outdoorTemp", 12,
        "occupiedSetPoint", 70
    );

    public static void main(String[] args) {
        // Update parameters based on historical data
        updateParameters(historicalData);

        // Calculate optimal start time
        double optimalStartTime = calculateOptimalStart(currentConditions);
        System.out.printf("Optimal Start Time in Minutes: %.2f%n", optimalStartTime);

        // Print updated parameters
        System.out.printf("Parameters: alpha3a=%.2f, alpha3b=%.2f, alpha3d=%.2f%n", alpha3a, alpha3b, alpha3d);
    }

    private static double calculateOptimalStart(Map<String, Integer> conditions) {
        int Tsp = conditions.get("occupiedSetPoint");
        int Tz = conditions.get("zoneTemp");
        int To = conditions.get("outdoorTemp");

        double tOpt = alpha3a * (Tsp - Tz) +
                      (alpha3b * (Tsp - Tz) * (Tsp - To)) / alpha3b +
                      alpha3d;

        // Clamp tOpt within bounds
        tOpt = Math.max(LATE_START_LIMIT, Math.min(tOpt, EARLY_START_LIMIT));
        return tOpt;
    }

    private static void updateParameters(List<Map<String, Object>> historicalData) {
        for (Map<String, Object> data : historicalData) {
            int Tsp = currentConditions.get("occupiedSetPoint");
            int Tz = (int) data.get("zoneTemp");
            int To = (int) data.get("outdoorTemp");
            int tActual = (int) data.get("warmupTimeMinutesHistory");

            double alpha3aNew = Math.abs(tActual / (double) (Tsp - Tz));
            double alpha3bNew = Math.abs(tActual / ((double) (Tsp - Tz) * (Tsp - To)));
            double alpha3dNew = tActual - (alpha3aNew * (Tsp - Tz) +
                                           (alpha3bNew * (Tsp - Tz) * (Tsp - To)) / alpha3bNew);

            alpha3a = smoothParameters(alpha3a, alpha3aNew);
            alpha3b = smoothParameters(alpha3b, alpha3bNew);
            alpha3d = smoothParameters(alpha3d, alpha3dNew);
        }
    }

    private static double smoothParameters(double alpha, double alphaNew) {
        return alpha + FORGETTING_FACTOR * (alphaNew - alpha);
    }
}
