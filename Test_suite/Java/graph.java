import java.util.*;

public class GraphDemo {

    static class Graph {
        private final Map<Integer, Map<Integer, Integer>> graph = new HashMap<>();

        public void addEdge(int from, int to, int weight) {
            graph.computeIfAbsent(from, k -> new HashMap<>()).put(to, weight);
            graph.computeIfAbsent(to, k -> new HashMap<>()).put(from, weight);
        }

        public Map<Integer, Integer> getNeighbors(int node) {
            return graph.getOrDefault(node, Collections.emptyMap());
        }
    }

    public static Graph generateLargeGraph(int numNodes, double edgeProbability, int maxWeight) {
        Graph graph = new Graph();
        Random random = new Random();

        for (int i = 0; i < numNodes; i++) {
            for (int j = i + 1; j < numNodes; j++) {
                if (random.nextDouble() < edgeProbability) {
                    int weight = random.nextInt(maxWeight) + 1;
                    graph.addEdge(i, j, weight);
                }
            }
        }
        return graph;
    }

    public static Map<Integer, Integer> dijkstra(Graph graph, int start) {
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        Map<Integer, Integer> distances = new HashMap<>();
        pq.offer(new int[]{start, 0});

        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int currentNode = current[0];
            int currentDistance = current[1];

            if (!distances.containsKey(currentNode)) {
                distances.put(currentNode, currentDistance);

                for (Map.Entry<Integer, Integer> entry : graph.getNeighbors(currentNode).entrySet()) {
                    int nextNode = entry.getKey();
                    int nextDistance = currentDistance + entry.getValue();

                    if (!distances.containsKey(nextNode)) {
                        pq.offer(new int[]{nextNode, nextDistance});
                    }
                }
            }
        }
        return distances;
    }

    public static void main(String[] args) {
        int numNodes = 1000;
        double edgeProbability = 0.5;
        int maxWeight = 10;

        long startTime = System.currentTimeMillis();
        long beforeUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory(); //memory calc start
        Graph graph = generateLargeGraph(numNodes, edgeProbability, maxWeight);
        Map<Integer, Integer> distances = dijkstra(graph, 0);
        long afterUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory(); //memory calc end
        long actualMemUsed = afterUsedMem - beforeUsedMem; // Total memory took
        long actualMemUsedInMB = actualMemUsed / (1024 * 1024);
        long endTime = System.currentTimeMillis();
        

        System.out.println("Execution Time: " + (endTime - startTime) + " milliseconds");
        System.out.println("Memory Used: " + actualMemUsedInMB + " M");

        // Memory usage measurement is not straightforward in Java as in Python.
        // Java does not have a direct equivalent to Python's memory_profiler.
    }
}
