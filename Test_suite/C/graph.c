#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

#define NUM_NODES 1000
#define MAX_WEIGHT 10
#define EDGE_PROBABILITY 0.5

typedef struct {
    int node;
    int weight;
} Edge;

typedef struct {
    Edge edges[NUM_NODES];
    int numEdges;
} AdjacencyList;

typedef struct {
    AdjacencyList adjList[NUM_NODES];
} Graph;

void addEdge(Graph *graph, int from, int to, int weight) {
    int fromIndex = graph->adjList[from].numEdges++;
    graph->adjList[from].edges[fromIndex] = (Edge){to, weight};

    int toIndex = graph->adjList[to].numEdges++;
    graph->adjList[to].edges[toIndex] = (Edge){from, weight};
}

void generateLargeGraph(Graph *graph, int numNodes, double edgeProbability, int maxWeight) {
    srand(time(NULL));
    for (int i = 0; i < numNodes; i++) {
        for (int j = i + 1; j < numNodes; j++) {
            if ((double)rand() / RAND_MAX < edgeProbability) {
                int weight = rand() % maxWeight + 1;
                addEdge(graph, i, j, weight);
            }
        }
    }
}

// Simple priority queue (min heap) implementation
typedef struct {
    int node;
    int distance;
} QueueNode;

typedef struct {
    QueueNode nodes[NUM_NODES];
    int size;
} PriorityQueue;

void swap(QueueNode *a, QueueNode *b) {
    QueueNode temp = *a;
    *a = *b;
    *b = temp;
}

void heapify(PriorityQueue *pq, int index) {
    int smallest = index;
    int left = 2 * index + 1;
    int right = 2 * index + 2;

    if (left < pq->size && pq->nodes[left].distance < pq->nodes[smallest].distance)
        smallest = left;
    if (right < pq->size && pq->nodes[right].distance < pq->nodes[smallest].distance)
        smallest = right;

    if (smallest != index) {
        swap(&pq->nodes[index], &pq->nodes[smallest]);
        heapify(pq, smallest);
    }
}

void push(PriorityQueue *pq, QueueNode node) {
    pq->nodes[pq->size] = node;
    int i = pq->size;
    pq->size++;

    while (i != 0 && pq->nodes[(i - 1) / 2].distance > pq->nodes[i].distance) {
        swap(&pq->nodes[(i - 1) / 2], &pq->nodes[i]);
        i = (i - 1) / 2;
    }
}

QueueNode pop(PriorityQueue *pq) {
    if (pq->size <= 0) {
        return (QueueNode){-1, -1};
    }

    QueueNode root = pq->nodes[0];
    pq->nodes[0] = pq->nodes[--pq->size];
    heapify(pq, 0);

    return root;
}

// Dijkstra's algorithm
void dijkstra(Graph *graph, int start, int distances[NUM_NODES]) {
    for (int i = 0; i < NUM_NODES; i++) {
        distances[i] = INT_MAX;
    }
    distances[start] = 0;

    PriorityQueue pq = {0};
    push(&pq, (QueueNode){start, 0});

    while (pq.size > 0) {
        QueueNode minNode = pop(&pq);
        int u = minNode.node;

        for (int i = 0; i < graph->adjList[u].numEdges; i++) {
            Edge edge = graph->adjList[u].edges[i];
            int v = edge.node;
            int weight = edge.weight;

            if (distances[u] + weight < distances[v]) {
                distances[v] = distances[u] + weight;
                push(&pq, (QueueNode){v, distances[v]});
            }
        }
    }
}

int main() {
    Graph graph = {0};
    generateLargeGraph(&graph, NUM_NODES, EDGE_PROBABILITY, MAX_WEIGHT);

    int distances[NUM_NODES];

    clock_t start_time = clock();
    dijkstra(&graph, 0, distances);
    clock_t end_time = clock();

    double execution_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    // Estimate memory usage
    size_t graphMemory = NUM_NODES * (NUM_NODES - 1) * sizeof(Edge);
    size_t pqMemory = NUM_NODES * sizeof(QueueNode);
    size_t totalMemory = graphMemory + pqMemory; // Add more if needed for other variables

    printf("Execution Time: %f seconds\n", execution_time);
    printf("Estimated Memory Usage: %zu M\n", totalMemory/(1024*1024));

    return 0;
}

// https://www.onlinegdb.com/online_c_compiler
