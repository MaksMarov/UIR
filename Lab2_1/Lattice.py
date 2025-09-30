from enum import Enum
import tkinter as tk
from tkinter import filedialog
import math

class LatticeType(Enum):
    FCC = 'fcc'
    BCC = 'bcc'
    HCP = 'hcp'

class Lattice:
    def __init__(self, lattice_type: LatticeType, n: int, a: float, c: float = None):
        """
        lattice_type: LatticeType.FCC, LatticeType.BCC или LatticeType.HCP
        n: количество ячеек вдоль каждой оси
        a: длина ребра элементарной ячейки (для HCP — a)
        c: высота ячейки по z (только для HCP). Если None, c = 1.633*a
        """
        self.lattice_type = lattice_type
        self.n = n
        self.a = a
        self.c = c if c is not None else 1.633 * a
        self.atoms = []

    def generate(self):
        """Генерация координат атомов"""
        self.atoms.clear()

        if self.lattice_type == LatticeType.BCC:
            basis = [(0, 0, 0), (0.5, 0.5, 0.5)]
            scale = (self.a, self.a, self.a)
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        for b in basis:
                            x = (i + b[0]) * scale[0]
                            y = (j + b[1]) * scale[1]
                            z = (k + b[2]) * scale[2]
                            self.atoms.append((x, y, z))

        elif self.lattice_type == LatticeType.FCC:
            basis = [(0, 0, 0), (0.5, 0.5, 0), (0, 0.5, 0.5), (0.5, 0, 0.5)]
            scale = (self.a, self.a, self.a)
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        for b in basis:
                            x = (i + b[0]) * scale[0]
                            y = (j + b[1]) * scale[1]
                            z = (k + b[2]) * scale[2]
                            self.atoms.append((x, y, z))

        elif self.lattice_type == LatticeType.HCP:
            sqrt3 = math.sqrt(3)
            a1 = (self.a, 0, 0)
            a2 = (-self.a / 2, self.a * sqrt3 / 2, 0)
            a3 = (0, 0, self.c)

            basis = [(0, 0, 0), (2/3, 1/3, 0.5)]

            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        for b in basis:
                            x = i*a1[0] + j*a2[0] + k*a3[0] + b[0]*a1[0] + b[1]*a2[0] + b[2]*a3[0]
                            y = i*a1[1] + j*a2[1] + k*a3[1] + b[0]*a1[1] + b[1]*a2[1] + b[2]*a3[1]
                            z = i*a1[2] + j*a2[2] + k*a3[2] + b[0]*a1[2] + b[1]*a2[2] + b[2]*a3[2]
                            self.atoms.append((x, y, z))

        else:
            raise ValueError("Неверный тип решетки")

    def save_to_file(self, filename=None):
        """Сохраняем координаты в файл"""
        if filename is None:
            root = tk.Tk()
            root.withdraw()
            filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt")])
            if not filename:
                print("Файл не выбран")
                return

        N = len(self.atoms)
        with open(filename, 'w') as f:
            f.write(f"{N}\n\n")
            for idx, (x, y, z) in enumerate(self.atoms, start=1):
                f.write(f"{idx} {x} {y} {z}\n")
        print(f"Файл сохранён: {filename}")


if __name__ == "__main__":
    lattice_fcc = Lattice(LatticeType.FCC, n=10, a=5)
    lattice_fcc.generate()
    lattice_fcc.save_to_file("fcc_generated.txt")

    lattice_bcc = Lattice(LatticeType.BCC, n=10, a=3)
    lattice_bcc.generate()
    lattice_bcc.save_to_file("bcc_generated.txt")

    lattice_hcp = Lattice(LatticeType.HCP, n=10, a=2)
    lattice_hcp.generate()
    lattice_hcp.save_to_file("hcp_generated.txt")