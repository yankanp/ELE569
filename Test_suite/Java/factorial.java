import java.math.BigInteger;

public class FactorialCalculator {

    public static BigInteger factorialIterative(int n) {
        BigInteger result = BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            result = result.multiply(BigInteger.valueOf(i));
        }
        return result;
    }

    public static void main(String[] args) {
        int number = 100000; // You can adjust this number

        // Memory usage estimation
        long beforeUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long startTime = System.currentTimeMillis();
        BigInteger result = factorialIterative(number);
        long endTime = System.currentTimeMillis();
        // Execute your code (already done above)
        long afterUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long actualMemUsed = afterUsedMem - beforeUsedMem;
        long actualMemUsedMB = actualMemUsed / ( 1024 * 1024 );

        System.out.println("The factorial of " + number + " is calculated.");
        System.out.println("Execution Time: " + (endTime - startTime) + " milliseconds");

        System.out.println("Estimated Memory Usage: " + actualMemUsedMB + " bytes");
    }
}
