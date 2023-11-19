import time
import heapq
import random
import resource

def generate_large_graph(num_nodes, edge_probability, max_weight=10):
    graph = {i: {} for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                graph[i][j] = weight
                graph[j][i] = weight
    return graph

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def get_memory_usage():
    # Get the current memory usage in kilobytes
    memory_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Convert kilobytes to megabytes
    memory_mb = memory_kb / 1024.0
    return memory_mb

def main():
    num_nodes = 3000  # Number of nodes in the graph
    edge_probability = 0.5  # Probability of an edge between two nodes

    graph = generate_large_graph(num_nodes, edge_probability)

    start_node = 0
    start_time = time.time()
    distances = dijkstra(graph, start_node)
    end_time = time.time()

    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    before_memory = get_memory_usage()
    main()
    after_memory = get_memory_usage()

    # Calculate peak memory usage during the execution
    peak_memory = max(before_memory, after_memory)
    print(f"Peak Memory Usage: {peak_memory} MiB")
