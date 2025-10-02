import tkinter as tk
from tkinter import filedialog
import numpy as np

class Task():
    def __init__(self):
        self.x = np.arange(50, 101)
        self.y_ref = self.load_function_data()

    def load_function_data(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(
            title="Выбор файла",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filename:
            print("Файл не выбран.")
            return None

        try:
            y = np.loadtxt(filename)
            if len(y) != len(self.x):
                print(f"Внимание: в файле {len(y)} точек, ожидается {len(self.x)}.")

            return np.array(y)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def evaluate(self, params: np.ndarray) -> np.ndarray:
        a, b, c, d = params
        if abs(b) < 0.1:
            b = 0.1 if b >= 0 else -0.1

        y_values = np.array([a * xi + c * np.cos(xi / b) + c / xi + d for xi in self.x])
        return y_values

    def try_solve(self, params: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        y_pred = self.evaluate(params)
        return y_pred, self.y_ref

class TaskFixed(Task):
    def __init__(self):
        self.x = np.arange(50, 101)
        # Задаем эталонные коэффициенты: a, b, c, d
        self.true_params = np.array([5, 10, 15, 20])
        self.y_ref = self.evaluate(self.true_params)


task = Task()