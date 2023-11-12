import time

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_primes(limit):
    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == "__main__":
    limit = 1000000  # Adjust the limit to control the resource usage

    start_time = time.time()
    print(f"Calculating prime numbers up to {limit}...")
    prime_numbers = find_primes(limit)
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Found {len(prime_numbers)} prime numbers.")
    print(f"Time taken: {elapsed_time:.2f} seconds")

