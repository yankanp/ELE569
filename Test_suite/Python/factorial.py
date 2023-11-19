import time
import resource

def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def get_memory_usage():
    # Get the current memory usage in kilobytes
    memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Convert kilobytes to megabytes
    memory_mb = memory_kb / 1024.0
    return memory_mb

def main():
    number = 100000  # You can adjust this number
    start_time = time.time()
    result = factorial_iterative(number)
    end_time = time.time()

    print(f"The factorial of {number} is calculated.")
    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    before_memory = get_memory_usage()
    main()
    after_memory = get_memory_usage()

    # Calculate peak memory usage during the execution
    peak_memory = max(before_memory, after_memory)
    print(f"Peak Memory Usage: {peak_memory} MiB")
