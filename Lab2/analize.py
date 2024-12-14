import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime

def load_results(filename):
    results = defaultdict(lambda: {"dijkstra_all_pairs": [], "floyd_warshall": []})
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            _, size, algorithm, time_taken = row
            size = int(size)
            time_taken = float(time_taken)

            if algorithm in results[size]:
                results[size][algorithm].append(time_taken)

    formatted_results = [
        (size, results[size]["dijkstra_all_pairs"], results[size]["floyd_warshall"])
        for size in sorted(results.keys())
    ]
    
    return formatted_results

def calculate_average_results(results):
    averaged_results = []
    
    for size, dijkstra_results, floyd_results in results:
        dijkstra_filtered = [time for time in dijkstra_results if time >= 0]
        floyd_filtered = [time for time in floyd_results if time >= 0]

        avg_dijkstra = sum(dijkstra_filtered) / len(dijkstra_filtered) if dijkstra_filtered else 0
        avg_floyd = sum(floyd_filtered) / len(floyd_filtered) if floyd_filtered else 0

        averaged_results.append([size, avg_dijkstra, avg_floyd])
    
    return averaged_results

def find_efficiency_change_points(averaged_results):
    change_points = []
    
    prev_algorithm = None

    for i in range(len(averaged_results) - 1):
        size1, avg_dijkstra1, avg_floyd1 = averaged_results[i]
        size2, avg_dijkstra2, avg_floyd2 = averaged_results[i + 1]

        if avg_dijkstra1 < avg_floyd1:
            current_algorithm = 'Dijkstra'
        else:
            current_algorithm = 'Floyd-Warshall'

        if prev_algorithm is not None and current_algorithm != prev_algorithm:
            change_points.append((size1, current_algorithm))

        prev_algorithm = current_algorithm

    return change_points

def visualize_performance(averaged_results, change_points):
    sizes = [result[0] for result in averaged_results]
    avg_dijkstra = [result[1] for result in averaged_results]
    avg_floyd = [result[2] for result in averaged_results]

    output_dir = 'Lab2/data/analyses'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"analyse_{timestamp}.png")

    plt.figure(figsize=(12, 6))

    plt.plot(sizes, avg_dijkstra, marker='o', label='Dijkstra Algorithm', color='blue')
    plt.plot(sizes, avg_floyd, marker='o', label='Floyd-Warshall Algorithm', color='orange')

    for size, ratio in change_points:
        plt.axvline(x=size, linestyle='--', color='red', alpha=0.5)
        plt.text(size, max(max(avg_dijkstra), max(avg_floyd)), f'Switch at {size}', color='red', ha='center')

    plt.title('Performance Comparison of Dijkstra and Floyd-Warshall Algorithms')
    plt.xlabel('Matrix Size')
    plt.ylabel('Average Calculation Time (seconds)')
    plt.xticks(sizes)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()

def analise(filename):
    results = load_results(filename)
    average_results = calculate_average_results(results)
    points = find_efficiency_change_points(average_results)
    visualize_performance(average_results, points)
