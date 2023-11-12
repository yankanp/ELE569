use std::time::{SystemTime, Duration};

fn is_prime(n: u64) -> bool {
    if n <= 1 {
        return false;
    }
    if n <= 3 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}

fn find_primes(limit: u64) -> Vec<u64> {
    let mut primes = Vec::new();
    for num in 2..limit {
        if is_prime(num) {
            primes.push(num);
        }
    }
    primes
}

fn main() {
    let limit: u64 = 1000000; // Adjust the limit to control the resource usage

    let start_time = SystemTime::now();
    println!("Calculating prime numbers up to {}...", limit);
    let prime_numbers = find_primes(limit);
    let end_time = SystemTime::now();

    let elapsed_time = end_time.duration_since(start_time).expect("Time went backwards");
    
    println!("Found {} prime numbers.", prime_numbers.len());
    if let Ok(elapsed) = elapsed_time.as_secs_f64() {
        println!("Time taken: {:.2} seconds", elapsed);
    }
}
