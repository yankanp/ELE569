import time
import resource

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

def get_memory_usage():
    # Get the current memory usage in kilobytes
    memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Convert kilobytes to megabytes
    memory_mb = memory_kb / 1024.0
    return memory_mb

def find_primes(limit):
    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == "__main__":
    limit = 1000000  # Adjust the limit to control the resource usage
    before_memory = get_memory_usage()
    start_time = time.time()
    print(f"Calculating prime numbers up to {limit}...")
    prime_numbers = find_primes(limit)
    end_time = time.time()

    elapsed_time = end_time - start_time
    after_memory = get_memory_usage()
    print(f"Found {len(prime_numbers)} prime numbers.")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    peak_memory = max(before_memory, after_memory)
    print(f"Peak Memory Usage: {peak_memory} MiB")
