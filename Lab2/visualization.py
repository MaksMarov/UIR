import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os

VISUALIZATIONS_DIR = 'Lab2/data/visualisations'

def create_visualization(adjacency_matrix, shortest_paths, benchmark_results, filename='visualization.png'):
    if not os.path.exists(VISUALIZATIONS_DIR):
        os.makedirs(VISUALIZATIONS_DIR)

    filepath = os.path.join(VISUALIZATIONS_DIR, filename)
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    axs[0, 0].imshow(adjacency_matrix, cmap='viridis', aspect='auto')
    axs[0, 0].set_title('Adjacency Matrix')
    axs[0, 0].set_xlabel('Vertices')
    axs[0, 0].set_ylabel('Vertices')
    for (i, j), val in np.ndenumerate(adjacency_matrix):
        axs[0, 0].text(j, i, 'inf' if val == np.inf else val, ha='center', va='center', color='white')

    cleaned_matrix = np.where(adjacency_matrix == np.inf, 0, adjacency_matrix)
    G = nx.from_numpy_array(cleaned_matrix)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, ax=axs[0, 1], node_color='skyblue', node_size=700, font_size=10, font_color='black', edge_color='gray')
    axs[0, 1].set_title('Graph from Adjacency Matrix')

    axs[1, 0].imshow(shortest_paths, cmap='viridis', aspect='auto')
    axs[1, 0].set_title('Shortest Paths Matrix')
    axs[1, 0].set_xlabel('Vertices')
    axs[1, 0].set_ylabel('Vertices')
    for (i, j), val in np.ndenumerate(shortest_paths):
        axs[1, 0].text(j, i, 'inf' if val == np.inf else val, ha='center', va='center', color='white')

    axs[1, 1].axis('off')
    results_text = "\n".join([f"{func}: {time:.10f} sec." for func, time in benchmark_results.items()])
    axs[1, 1].text(0.5, 0.5, results_text, ha='center', va='center', fontsize=12)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust margins
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close(fig)