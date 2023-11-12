public class PrimeNumbers {

    public static boolean isPrime(int n) {
        if (n <= 1) {
            return false;
        }
        if (n <= 3) {
            return true;
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;
        }
        int i = 5;
        while (i * i <= n) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
            i += 6;
        }
        return true;
    }

    public static List<Integer> findPrimes(int limit) {
        List<Integer> primes = new ArrayList<>();
        for (int num = 2; num < limit; num++) {
            if (isPrime(num)) {
                primes.add(num);
            }
        }
        return primes;
    }

    public static void main(String[] args) {
        int limit = 1000000; // Adjust the limit to control the resource usage

        long startTime = System.currentTimeMillis();
        System.out.println("Calculating prime numbers up to " + limit + "...");
        List<Integer> primeNumbers = findPrimes(limit);
        long endTime = System.currentTimeMillis();

        double elapsedTime = (endTime - startTime) / 1000.0;

        System.out.println("Found " + primeNumbers.size() + " prime numbers.");
        System.out.printf("Time taken: %.2f seconds%n", elapsedTime);
    }
}
