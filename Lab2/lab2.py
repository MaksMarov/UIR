import datetime
from lib2to3.fixes.fix_print import parend_expr
import os
import csv
import numpy as np
from adjacency_matrix import generate_adjacency_matrix, save_adjacency_matrix, load_adjacency_matrix
from algorithms import dijkstra_all_pairs, floyd_warshall
from visualization import create_visualization
from benchmark import benchmark_results
from analize import analise
import math

def log_results(file_writer, matrix_size, benchmark_results):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for algorithm, time_taken in benchmark_results.items():
        file_writer.writerow([timestamp, matrix_size, algorithm, f"{time_taken:.10f}"])

def run_multiple_start(min_size, max_size, steps, repetitions=3):
    print("Prepare")
    step_size = max(1, math.floor((max_size - min_size) / steps))

    sizes = list(range(min_size, max_size + 1, step_size))
    if sizes[-1] > max_size:
        sizes = sizes[:-1]

    results_dir = "Lab2/data"
    os.makedirs(results_dir, exist_ok=True)
    results_filename = os.path.join(results_dir, f"results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    with open(results_filename, 'w', newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(['Timestamp', 'Matrix Size', 'Algorithm', 'Time Taken (s)'])
        print("Start calculation")
        for size in sizes:
            for i in range(repetitions):
                print("Calculation for: size = ", size, " , ", i, " of ", repetitions)
                if start(size, False):
                    log_results(file_writer, size, benchmark_results)
                    print("Succes. Result was saved")
                else:
                    print("Skip step")
        print("Finish")
    analise(results_filename)

def start(n, save_matrix = True, create_visual = False):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    matrix = generate_adjacency_matrix(n)
    if save_matrix:
        matrix_filename = f"matrix_{timestamp}.txt"
        save_adjacency_matrix(matrix, matrix_filename)
    # loaded_matrix = load_adjacency_matrix(matrix_filename)

    shortest_paths_dijkstra = dijkstra_all_pairs(matrix)
    shortest_paths_floyd = floyd_warshall(matrix)

    if np.array_equal(shortest_paths_dijkstra, shortest_paths_floyd):
        print("The result matched")
        if create_visual:
            visualization_filename = f"visual_{timestamp}.png" 
            create_visualization(matrix, shortest_paths_dijkstra, benchmark_results, visualization_filename)
        return True
    else:
        print("Bad result")
        return False

# start(30, create_visual=True)
# run_multiple_start(3, 30, 10, 3)
analise("Lab2/data/results_20241027_160048.csv")