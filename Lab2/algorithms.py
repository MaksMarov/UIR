import numpy as np
from benchmark import benchmark

@benchmark
def dijkstra_all_pairs(matrix):
    n = len(matrix)
    dist = np.full((n, n), np.inf)
    
    for i in range(n):
        dist[i] = dijkstra_single_source(matrix, i)
    
    return dist

def dijkstra_single_source(matrix, src):
    n = len(matrix)
    dist = np.full(n, np.inf)
    dist[src] = 0
    visited = [False] * n
    
    for _ in range(n):
        u = min_distance(dist, visited)
        visited[u] = True
        
        for v in range(n):
            if (not visited[v] and matrix[u][v] != float('inf') and 
                dist[u] != float('inf') and dist[u] + matrix[u][v] < dist[v]):
                dist[v] = dist[u] + matrix[u][v]
    
    return dist

def min_distance(dist, visited):
    min_val = float('inf')
    min_index = -1
    for i in range(len(dist)):
        if not visited[i] and dist[i] < min_val:
            min_val = dist[i]
            min_index = i
    return min_index

@benchmark
def floyd_warshall(matrix):
    n = len(matrix)
    dist = matrix.copy()
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist