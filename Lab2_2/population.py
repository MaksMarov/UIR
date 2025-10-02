import numpy as np
from member import FitType, Member

class Population:
    def __init__(self, pop_size=100, gabsrange=10, tournament_k=3, mut_p=0.3, mut_scale=0.05, per_gene_p=0.3, elite_count=2, fit_type=FitType.MSE):
        self.pop_size = int(pop_size)
        self.gabsrange = gabsrange
        self.tournament_k = tournament_k
        self.mut_p = mut_p
        self.mut_scale = mut_scale
        self.per_gene_p = per_gene_p
        self.elite_count = elite_count
        self.fit_type = fit_type

        self.fit_story = []

        self.members = [Member(gabsrange=self.gabsrange, fit_type=self.fit_type)
                        for _ in range(self.pop_size)]
        self.best_member = None
        self.update_fitness()

    def update_fitness(self):
        for m in self.members:
            m.fitness()
        self.sort_by_fitness()
        self.best_member = self.members[0]
        return self.best_member.fit

    def sort_by_fitness(self):
        self.members.sort(key=lambda m: m.fit)

    def fitness(self):
        return self.best_member.fit

    def tournament_select(self, k=None, pool=None):
        if pool is None:
            pool = self.members
        if k is None:
            k = self.tournament_k
        idxs = np.random.choice(len(pool), min(k, len(pool)), replace=False)
        candidates = [pool[i] for i in idxs]
        return min(candidates, key=lambda m: m.fit)

    def crossover(self):
        children = []
        num_to_create = self.pop_size - self.elite_count
        parent_pool = self.members
        for _ in range(num_to_create):
            p1 = self.tournament_select(pool=parent_pool)
            p2 = self.tournament_select(pool=parent_pool)
            child = p1.crossover_uniform(p2)
            children.append(child)
        return children

    def mutate(self, population_subset):
        if len(population_subset) == 0:
            return
        num_to_mutate = max(1, int(len(population_subset) * self.mut_p))
        to_mutate = np.random.choice(population_subset, num_to_mutate, replace=False)
        for member in to_mutate:
            member.mutate(mut_scale=self.mut_scale, per_gene_p=self.per_gene_p)

    def evolve(self):
        self.sort_by_fitness()
        elite = self.members[:self.elite_count]

        children = self.crossover()

        self.mutate(children)

        self.members = elite + children

        best = self.update_fitness()
        self.fit_story.append(best)
        return best