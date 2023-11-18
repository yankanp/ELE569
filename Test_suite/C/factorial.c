#include <stdio.h>
#include <gmp.h>
#include <math.h>
#include <sys/time.h>

void factorial(mpz_t result, unsigned long int n) {
    mpz_set_ui(result, 1); // Initialize result to 1

    for (unsigned long int i = 2; i <= n; i++) {
        mpz_mul_ui(result, result, i); // result *= i
    }
}

int main() {
    unsigned long int number = 100000; // You can adjust this number

    // Initialize the big integer for factorial
    mpz_t factorialResult;
    mpz_init(factorialResult);

    // Start time
    struct timeval start, end;
    gettimeofday(&start, NULL);

    factorial(factorialResult, number);

    // End time
    gettimeofday(&end, NULL);
    long seconds = end.tv_sec - start.tv_sec;
    long microseconds = end.tv_usec - start.tv_usec;
    double elapsed = seconds + microseconds*1e-6;

    // Estimate memory usage
    double numDigits = (log(sqrt(2 * M_PI * number)) / log(10)) + (number * log(number / M_E) / log(10));
    double numBits = numDigits * log(10) / log(2);
    double memoryUsageBytes = numBits / 8;

    printf("The factorial of %lu is calculated.\n", number);
    printf("Execution Time: %f seconds\n", elapsed);
    printf("Estimated Memory Usage: %f M\n", memoryUsageBytes/(1024*1024));

    mpz_clear(factorialResult); // Free the memory occupied by factorialResult
    return 0;
}
