import numpy as np
import os

MATRICES_DIR = 'Lab2/data/matrices'

import numpy as np

def generate_adjacency_matrix(size):
    matrix = np.full((size, size), np.inf)

    for i in range(size):
        matrix[i][i] = 0
    for i in range(size):
        for j in range(i + 1, size):
            if np.random.rand() > 0.5:
                weight = np.random.randint(1, 10)
                matrix[i][j] = matrix[j][i] = weight
                
    return matrix

def load_adjacency_matrix(filename):
    filepath = os.path.join(MATRICES_DIR, filename)
    with open(filepath, 'r') as f:
        matrix = []
        for line in f:
            matrix.append([float(x) if x != 'inf' else np.inf for x in line.split()])
        return np.array(matrix)

def save_adjacency_matrix(matrix, filename):
    filepath = os.path.join(MATRICES_DIR, filename)
    with open(filepath, 'w') as f:
        for row in matrix:
            f.write(' '.join(str(x) if x != np.inf else 'inf' for x in row) + '\n')
