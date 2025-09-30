import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from typing import List, Tuple


def read_atoms_from_txt(filename: str) -> np.ndarray:
    atoms = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    if len(lines) < 3:
        return np.empty((0,3))
    for line in lines[2:]:
        parts = line.strip().split()
        if len(parts) >= 4:
            _, x, y, z = parts[:4]
            atoms.append((float(x), float(y), float(z)))
    return np.array(atoms, dtype=float)


def compute_rdf(atoms: np.ndarray, r_max: float = 20.0, dr: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
    N = atoms.shape[0]
    if N < 2:
        return np.array([]), np.array([])

    mins = atoms.min(axis=0)
    maxs = atoms.max(axis=0)
    V = np.prod(maxs - mins)
    if V == 0:
        V = 1.0

    rho = N / V

    bins = np.arange(0.0, r_max + dr, dr)
    counts = np.zeros(len(bins) - 1, dtype=float)

    block = 512
    for i0 in range(0, N, block):
        i1 = min(N, i0 + block)
        A = atoms[i0:i1]
        B = atoms[i1:]
        if B.shape[0] > 0:
            diff = A[:, None, :] - B[None, :, :]
            dists = np.linalg.norm(diff, axis=2).ravel()
            hist, _ = np.histogram(dists, bins=bins)
            counts += hist
        if A.shape[0] > 1:
            dists_block = []
            for ii in range(A.shape[0]):
                d = np.linalg.norm(A[ii+1:] - A[ii], axis=1)
                if d.size:
                    dists_block.append(d)
            if dists_block:
                dists_block = np.concatenate(dists_block)
                hist, _ = np.histogram(dists_block, bins=bins)
                counts += hist

    r_centers = 0.5 * (bins[:-1] + bins[1:])
    shell_volumes = 4.0 * np.pi * r_centers**2 * dr

    expected_pairs = N * rho * shell_volumes
    expected_pairs_half = 0.5 * expected_pairs

    mask = expected_pairs_half > 0
    g_r = np.zeros_like(r_centers)
    g_r[mask] = counts[mask] / expected_pairs_half[mask]

    return r_centers, g_r


def find_peaks_simple(y: np.ndarray, threshold: float = 0.05, min_dist_bins: int = 2) -> np.ndarray:
    if y.size == 0:
        return np.array([], dtype=int)
    ymax = np.max(y)
    thr = ymax * threshold
    peaks = []
    N = len(y)
    i = 1
    while i < N - 1:
        if y[i] > y[i-1] and y[i] > y[i+1] and y[i] >= thr:
            peaks.append(i)
            i += min_dist_bins
        else:
            i += 1
    return np.array(peaks, dtype=int)


def theoretical_peak_factors(lattice: str) -> List[float]:
    lattice = lattice.lower()
    if lattice == 'fcc':
        return [
            np.sqrt(2)/2,
            1.0,
            np.sqrt(3/2),
            np.sqrt(2.0),
            np.sqrt(5/2),
            np.sqrt(3.0)
        ]
    elif lattice == 'bcc':
        return [
            np.sqrt(3)/2,
            1.0,
            np.sqrt(2.0),
            np.sqrt(11/4),
            np.sqrt(3.0),
            np.sqrt(19/4)
        ]
    elif lattice == 'hcp':
        return [
            1.0,
            np.sqrt(8/3),
            np.sqrt(3),
            2.0,
            np.sqrt(11/3),
            np.sqrt(3*2)
        ]
    else:
        raise ValueError(f"Неизвестная решетка: {lattice}")


def analyze_lattice_from_peaks(r: np.ndarray, g_r: np.ndarray, peaks_idx: np.ndarray, max_peaks_to_use: int = 4) -> Tuple[str, float, dict]:
    details = {}
    if peaks_idx.size == 0:
        return "Не найдено пиков", float('nan'), details

    peak_positions = r[peaks_idx]
    peak_positions = np.sort(peak_positions)
    if peak_positions.size > max_peaks_to_use:
        peak_positions = peak_positions[:max_peaks_to_use]

    details['observed_peaks'] = peak_positions.tolist()

    r0 = peak_positions[0]
    if r0 <= 0:
        return "Не найдено пика 1", float('nan'), details
    obs_ratios = peak_positions / r0

    candidates = {}
    for lattice in ('fcc', 'bcc', 'hcp'):
        theory = np.array(theoretical_peak_factors(lattice))
        theory_ratios = theory[:len(obs_ratios)] / theory[0]
        mse = np.mean((obs_ratios - theory_ratios)**2)
        candidates[lattice] = float(mse)

    details['mse_candidates'] = candidates

    best = min(candidates, key=candidates.get)
    best_mse = candidates[best]

    theory_first = theoretical_peak_factors(best)[0]
    a_est = r0 / theory_first

    details['best'] = best
    details['best_mse'] = best_mse
    details['a_estimate'] = float(a_est)

    theory_positions = (np.array(theoretical_peak_factors(best)) * a_est)[:len(peak_positions)]
    details['theory_positions_for_best'] = theory_positions.tolist()
    details['residuals'] = (peak_positions - theory_positions).tolist()

    pretty = best.upper()
    return pretty, float(a_est), details


class RDFAnalyzer:
    def __init__(self, r_max: float = 15.0, dr: float = 0.02):
        self.r_max = r_max
        self.dr = dr
        self.results = {}

    def select_files_dialog(self) -> List[str]:
        root = tk.Tk()
        root.withdraw()
        filenames = filedialog.askopenfilenames(
            title="Выберите txt-файлы с координатами",
            filetypes=[("Text files", "*.txt")]
        )
        return list(filenames)

    def process_files(self, filenames: List[str]):
        for fn in filenames:
            atoms = read_atoms_from_txt(fn)
            r, g = compute_rdf(atoms, r_max=self.r_max, dr=self.dr)
            peaks_idx = find_peaks_simple(g, threshold=0.08, min_dist_bins=max(1, int(0.02/self.dr)))
            lattice_type, a_est, details = analyze_lattice_from_peaks(r, g, peaks_idx)
            self.results[fn] = {
                'r': r, 'g': g,
                'peaks_idx': peaks_idx,
                'peaks_r': r[peaks_idx].tolist(),
                'lattice_guess': lattice_type,
                'a_est': a_est,
                'analysis': details
            }

    def plot_all(self, show=True, savefig: str = None):
        plt.figure(figsize=(9,6))
        cmap = plt.get_cmap('tab10')
        for i, (fn, data) in enumerate(self.results.items()):
            label = f"{os.path.basename(fn)} — {data['lattice_guess']} a≈{data['a_est']:.3f}"
            plt.plot(data['r'], data['g'], label=label, color=cmap(i%10))
            peaks = data['peaks_r']
            if peaks:
                g_at_peaks = np.interp(peaks, data['r'], data['g'])
                plt.scatter(peaks, g_at_peaks, color=cmap(i%10), marker='x')

        plt.xlabel("r")
        plt.ylabel("g(r)")
        plt.title("Радиальная функция распределения (g(r))")
        plt.legend()
        plt.grid(True)
        if savefig:
            plt.savefig(savefig, dpi=300)
            print(f"Сохранён рисунок: {savefig}")
        if show:
            plt.show()

    def run_dialog_and_process(self):
        files = self.select_files_dialog()
        if not files:
            print("Файлы не выбраны.")
            return
        print("Выбрано файлов:", len(files))
        self.process_files(files)
        for fn, d in self.results.items():
            print(f"Файл: {os.path.basename(fn)} -> {d['lattice_guess']}, a≈{d['a_est']:.4f}")
        self.plot_all()


if __name__ == "__main__":
    analyzer = RDFAnalyzer(r_max=15.0, dr=0.02)
    analyzer.run_dialog_and_process()