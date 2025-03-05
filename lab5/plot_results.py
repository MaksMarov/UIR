import os
import numpy as np
import matplotlib.pyplot as plt
from data_tool import load_simulation_data

def calculate_statistics(data):
    return {
        "Average": np.mean(data),
        "Median": np.median(data),
        "Standard deviation": np.std(data, ddof=1)
    }

def plot_and_save(file_path, dead_counts, survived_counts, evacuation_times):
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    fig.suptitle("Simulations results")

    datasets = [("Dead", dead_counts), ("Survived", survived_counts), ("Evacuation times", evacuation_times)]
    
    for i, (title, data) in enumerate(datasets):
        axs[i].plot(data, marker="o", linestyle="-")
        axs[i].set_title(title)
        axs[i].set_xlabel("Sumulation number")
        axs[i].set_ylabel(title)

        stats = calculate_statistics(data)
        textstr = '\n'.join([f"{k}: {v:.2f}" for k, v in stats.items()])
        axs[i].text(0.02, 0.85, textstr, transform=axs[i].transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    save_path = os.path.splitext(file_path)[0] + ".png"
    plt.savefig(save_path)
    plt.show()

    print(f"Plot is saved as {save_path}")

if __name__ == "__main__":
    file_path, dead_counts, survived_counts, evacuation_times = load_simulation_data()
    if file_path:
        plot_and_save(file_path, dead_counts, survived_counts, evacuation_times)