
import pandas as pd
import matplotlib.pyplot as plt
from beehive import Beehive
import numpy as np

def main():
    # Constants
    NUM_BEES = 100
    NUM_GENERATIONS = 100

    # Load flower coordinates using Pandas
    file_path = "flowers.csv"
    flower_coordinates = pd.read_csv(file_path, delimiter="\t")

    # Create beehive
    beehive = Beehive(NUM_BEES, flower_coordinates)

    # Initialize bees
    beehive.initialize_bees()

    # Variables for visualization
    best_bee = None
    best_score = float('inf')
    best_bee_scores = []
    all_bees_avg_scores = []  # New list for average scores of all bees

    # Evolution loop
    for _ in range(NUM_GENERATIONS):
        beehive.evolve_generation()

        # Update best bee and score
        current_best_bee = beehive.best_bee
        if current_best_bee.performance_score < best_score:
            best_bee = current_best_bee
            best_score = current_best_bee.performance_score

        # Collect scores for visualization
        best_bee_scores.append(current_best_bee.performance_score)

        # Calculate and store average performance score of all bees
        avg_score = np.mean([bee.performance_score for bee in beehive.bees])
        all_bees_avg_scores.append(avg_score)

    # Visualize results
    visualize_results(best_bee, best_bee_scores, all_bees_avg_scores, flower_coordinates, NUM_GENERATIONS)

def visualize_results(best_bee, best_bee_scores, all_bees_avg_scores, flower_coordinates, num_generations):
    # Set a larger square figure size
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Visualize best bee's path
    axes[0].plot(*zip(*best_bee.genes), marker='o')
    axes[0].set_xlabel('X Coordinate')
    axes[0].set_ylabel('Y Coordinate')
    axes[0].set_title("Best Bee's Path")
    axes[0].grid(True)

    # Visualize evolution of best bee's performance score
    axes[1].plot(range(num_generations), best_bee_scores, color='blue', label="Best Bee's Score")
    axes[1].set_xlabel('Generation')
    axes[1].set_ylabel("Performance Score")
    axes[1].set_title("Evolution of Best Bee's Performance Score")
    axes[1].legend()
    axes[1].grid(True)

    # Visualize average performance score of all bees
    axes[2].plot(range(num_generations), all_bees_avg_scores, color='green', label='Average Score')
    axes[2].set_xlabel('Generation')
    axes[2].set_ylabel('Average Performance Score')
    axes[2].set_title('Average Performance Score of All Bees')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig('bee_path_visualization.png')  # Save the plot as an image
    plt.show()

if __name__ == '__main__':
    main()
