import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
import numpy as np
from population import Population
from task import task


def plot_function_comparison(task, best_member, pop_size, save=False):
    """Сравнение эталонной функции и предсказанной."""
    y_pred, y_ref = task.try_solve(best_member.genotype)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(task.x, y_ref, label="Reference", color="blue")
    ax.plot(task.x, y_pred, label="Predicted", color="red", linestyle="--")
    ax.set_title(f"Function Comparison (Pop size={pop_size})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    if save:
        root = Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Сохранить график функции как..."
        )
        if save_path:
            fig.savefig(save_path)
            print(f"График сохранён: {save_path}")
        else:
            print("Сохранение отменено.")
    plt.show()

def plot_fitness_history(results, save=False):
    """Эволюция fitness по шагам для разных размеров популяций."""
    fig, ax = plt.subplots(figsize=(10, 6))
    for res in results:
        steps = np.arange(1, len(res['fitness_history']) + 1)
        ax.plot(steps, res['fitness_history'], label=f"Pop size {res['pop_size']}")

    ax.set_xlabel("Поколение")
    ax.set_ylabel("Fitness")
    ax.set_title("Эволюция fitness для разных размеров популяций")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    if save:
        root = Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Сохранить график fitness как..."
        )
        if save_path:
            fig.savefig(save_path)
            print(f"График сохранён: {save_path}")
        else:
            print("Сохранение отменено.")
    plt.show()


def run_experiment(task, pop_sizes=[50, 40, 30, 20, 10], max_generations=100, target_fitness=2):
    results = []

    for pop_size in pop_sizes:
        for _ in range(5):
            print(f"\n=== Популяция размером {pop_size} ===")
            pop = Population(pop_size=pop_size, gabsrange=50)

            for gen in range(max_generations):
                best_fit = pop.evolve()
                print(f"Поколение {gen+1}: fitness = {best_fit:.6f}", end="\r")
                if best_fit <= target_fitness:
                    print(f"\nДостигнут порог точности в поколении {gen+1}")
                    break

            print("Лучшие коэффициенты:", pop.best_member.genotype, "; fitness:", pop.best_member.fit)

            results.append({
                "pop_size": pop_size,
                "best_member": pop.best_member,
                "fitness_history": pop.fit_story
            })

    return results


if __name__ == "__main__":
    results = run_experiment(task)

    for res in results:
        plot_function_comparison(task, res['best_member'], res['pop_size'])

    plot_fitness_history(results)