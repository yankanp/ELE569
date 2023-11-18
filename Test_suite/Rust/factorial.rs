use std::time::Instant;
use std::mem::size_of;

fn factorial_iterative(n: u64) -> u128 {
    let mut result: u128 = 1;
    for i in 2..=n {
        result *= i as u128;
    }
    result
}

fn main() {
    let number = 34; // Adjust this number to a value that fits within u128

    let start_time = Instant::now();
    let result = factorial_iterative(number);
    let end_time = Instant::now();

    let result_size = size_of::<u128>();

    println!("The factorial of {} is {}.", number, result);
    println!("Execution Time: {:?}", end_time.duration_since(start_time));
    println!("Estimated Memory Usage for Result: {} bytes", result_size);

    // Note: This is a very basic estimation and does not reflect the actual memory usage of the program.
}
//https://play.rust-lang.org/?version=stable&mode=debug&edition=2021
