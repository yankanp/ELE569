#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

bool isPrime(int n) {
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

int* findPrimes(int limit, int* size) {
    int* primes = malloc(sizeof(int) * limit);
    *size = 0;
    for (int num = 2; num < limit; num++) {
        if (isPrime(num)) {
            primes[*size] = num;
            (*size)++;
        }
    }
    return primes;
}

int main() {
    int limit = 1000000; // Adjust the limit to control the resource usage

    clock_t startTime = clock();
    printf("Calculating prime numbers up to %d...\n", limit);
    
    int size;
    int* primeNumbers = findPrimes(limit, &size);
    
    clock_t endTime = clock();
    double elapsedTime = (double)(endTime - startTime) / CLOCKS_PER_SEC;

    printf("Found %d prime numbers.\n", size);
    printf("Time taken: %.2f seconds\n", elapsedTime);
    
    free(primeNumbers); // Free dynamically allocated memory
    return 0;
}
