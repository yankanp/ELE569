use rand::rngs::ThreadRng;
use rand::{Rng, thread_rng};
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::mem;

const NUM_NODES: usize = 1000;
const MAX_WEIGHT: i32 = 10;
const EDGE_PROBABILITY: f64 = 0.5;

#[derive(Copy, Clone, Eq, PartialEq)]
struct Edge {
    node: usize,
    weight: i32,
}

struct AdjacencyList {
    edges: Vec<Edge>,
}

struct Graph {
    adj_list: Vec<AdjacencyList>,
}

impl Graph {
    fn new() -> Graph {
        let mut adj_list = Vec::with_capacity(NUM_NODES);
        for _ in 0..NUM_NODES {
            adj_list.push(AdjacencyList { edges: Vec::new() });
        }
        Graph { adj_list }
    }

    fn add_edge(&mut self, from: usize, to: usize, weight: i32) {
        self.adj_list[from].edges.push(Edge { node: to, weight });
        self.adj_list[to].edges.push(Edge { node: from, weight });
    }
}

fn generate_large_graph(rng: &mut ThreadRng) -> Graph {
    let mut graph = Graph::new();
    for i in 0..NUM_NODES {
        for j in i + 1..NUM_NODES {
            if rng.gen::<f64>() < EDGE_PROBABILITY {
                let weight = rng.gen_range(1..=MAX_WEIGHT);
                graph.add_edge(i, j, weight);
            }
        }
    }
    graph
}



#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: i32,
    position: usize,
}

impl Ord for State {
    fn cmp(&self, other: &State) -> Ordering {
        other.cost.cmp(&self.cost).reverse()
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &State) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn dijkstra(graph: &Graph, start: usize) -> Vec<i32> {
    let mut dist: Vec<_> = (0..NUM_NODES).map(|_| i32::MAX).collect();
    let mut heap = BinaryHeap::new();

    dist[start] = 0;
    heap.push(State { cost: 0, position: start });

    while let Some(State { cost, position }) = heap.pop() {
        if cost > dist[position] { continue; }

        for edge in &graph.adj_list[position].edges {
            let next = State { cost: cost + edge.weight, position: edge.node };

            if next.cost < dist[next.position] {
                heap.push(next);
                dist[next.position] = next.cost;
            }
        }
    }
    dist
}

fn estimate_memory_usage(graph: &Graph) -> usize {
    let mut total_size = 0;

    // Size of the adjacency list vector itself
    total_size += mem::size_of::<Vec<AdjacencyList>>();

    for adj_list in &graph.adj_list {
        // Size of each adjacency list
        total_size += mem::size_of::<AdjacencyList>();
        // Size of the edges vector in each adjacency list
        total_size += mem::size_of::<Vec<Edge>>();
        // Size of the edges in each adjacency list
        total_size += adj_list.edges.capacity() * mem::size_of::<Edge>();
    }

    total_size
}

fn main() {
    let mut rng = thread_rng();
    let graph = generate_large_graph(&mut rng);

    let start_time = std::time::Instant::now();
    let distances = dijkstra(&graph, 0);
    let end_time = std::time::Instant::now();

    println!("Execution Time: {:?}", end_time.duration_since(start_time));

    // Example usage of distances
    // for (i, &dist) in distances.iter().enumerate() {
    //     println!("Distance from node 0 to node {}: {}", i, dist);
    // }
    let memory_usage = estimate_memory_usage(&graph);
    println!("Estimated Memory Usage: {} M", memory_usage/(1024*1024));
}
//https://play.rust-lang.org/?version=stable&mode=debug&edition=2021
