import numpy as np
from task import task
from enum import Enum

class FitType(Enum):
    L1 = 0
    L2 = 1
    MSE = 2
    LINF = 3

class Member:
    def __init__(self, genotype=None, gabsrange=100, fit_type=FitType.MSE):
        self.gabsrange = gabsrange
        self.fit_type = fit_type
        self.genotype = genotype if genotype is not None else np.random.uniform(0, self.gabsrange, size=4)
        self.size = len(self.genotype)
        self.fit = None
        self.fitness()

    def calc_fitness(self, y_pred, y_ref):
        diff = np.array(y_pred) - np.array(y_ref)
        if self.fit_type == FitType.L1:
            return float(np.mean(np.abs(diff)))
        elif self.fit_type == FitType.L2:
            return float(np.sqrt(np.sum(diff**2)))
        elif self.fit_type == FitType.MSE:
            return float(np.mean(diff**2))
        elif self.fit_type == FitType.LINF:
            return float(np.max(np.abs(diff)))
        else:
            return float(np.mean(diff**2))

    def fitness(self):
        y_pred, y_ref = task.try_solve(self.genotype)
        self.fit = self.calc_fitness(y_pred, y_ref)
        return self.fit

    def crossover_uniform(self, other, swap_p=0.5):
        mask = np.random.rand(self.size) < swap_p
        child_gen = np.where(mask, self.genotype, other.genotype)
        return Member(genotype=child_gen, gabsrange=self.gabsrange, fit_type=self.fit_type)

    def mutate(self, mut_scale=0.02, per_gene_p=0.2):
        for i in range(self.size):
            if np.random.rand() < per_gene_p:
                sigma = mut_scale * self.gabsrange
                self.genotype[i] += np.random.normal(0, sigma)
                self.genotype[i] = float(max(min(self.genotype[i], self.gabsrange), 0))
        self.fitness()
