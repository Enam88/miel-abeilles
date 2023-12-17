import random
import numpy as np

class Bee:
    def __init__(self, flower_coordinates):
        self.genes = []
        self.performance_score = 0
        self.flower_coordinates = flower_coordinates

    def set_genes(self):
        flower_coordinates_list = list(zip(self.flower_coordinates['x'], self.flower_coordinates['y']))
        self.genes = random.sample(flower_coordinates_list, len(flower_coordinates_list))


    def calculate_performance(self):
        genes_np = np.array(self.genes)
        distances = np.sum(np.abs(genes_np[:-1] - genes_np[1:]), axis=1)
        self.performance_score = np.sum(distances)

    def reproduce(self, parent1, parent2):
        child1 = Bee(self.flower_coordinates)
        child2 = Bee(self.flower_coordinates)
        crossover_point = random.randint(1, len(self.genes) - 1)
        child1_genes = parent1.genes[:crossover_point]
        child2_genes = parent2.genes[:crossover_point]
        missing_coords_child1 = [coord for coord in parent2.genes if coord not in child1_genes]
        missing_coords_child2 = [coord for coord in parent1.genes if coord not in child2_genes]
        child1_genes += missing_coords_child1
        child2_genes += missing_coords_child2
        child1.genes = child1_genes
        child2.genes = child2_genes
        return child1, child2


class Beehive:
    def __init__(self, num_bees, flower_coordinates):
        self.bees = [Bee(flower_coordinates) for _ in range(num_bees)]
        self.generation = 0
        self.best_bee = None
        self.best_score = float('inf')
        self.all_bees_scores = []

    def initialize_bees(self):
        for bee in self.bees:
            bee.set_genes()
            bee.calculate_performance()

    def evolve_generation(self):
        self.bees.sort(key=lambda bee: bee.performance_score)
        best_bees = self.bees[:50]
        new_bees = []

        while len(new_bees) < len(self.bees):
            parent1, parent2 = random.sample(best_bees, 2)
            child1, child2 = parent1.reproduce(parent1, parent2)
            child1.calculate_performance()
            child2.calculate_performance()
            new_bees.extend([child1, child2])
        
        self.bees = new_bees

        # Update best bee and score
        current_best_bee = min(self.bees, key=lambda bee: bee.performance_score)
        if current_best_bee.performance_score < self.best_score:
            self.best_bee = current_best_bee
            self.best_score = current_best_bee.performance_score

        # Collect scores for visualization
        all_scores = [bee.performance_score for bee in self.bees]
        self.all_bees_scores.append(all_scores)
