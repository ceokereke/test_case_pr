import random
import numpy as np

def read_test_cases(file_path):
    test_cases = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                test_id = parts[0]
                test_data = eval(parts[1])
                if len(test_data) >= 2:
                    percentage_coverage = float(test_data[1])
                    test_cases[test_id] = {'id': test_id, 'percentage_coverage': percentage_coverage}
    return test_cases

def initialize_population(test_cases, population_size, no_tcp):
    test_ids = list(test_cases.keys())
    return [random.sample(test_ids, no_tcp) for _ in range(population_size)]

def fitness(individual, test_cases):
    return sum(test_cases[test_id]['percentage_coverage'] for test_id in individual) / len(individual)

def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2, no_tcp):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [test_id for test_id in parent2 if test_id not in parent1[:crossover_point]]
    return child[:no_tcp]  # Ensure we keep only no_tcp test cases

def mutate(individual, test_cases, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(individual) - 1)
        new_test_id = random.choice([t for t in test_cases.keys() if t not in individual])
        individual[index] = new_test_id
    return individual

def genetic_algorithm(test_cases, population_size, generations, mutation_rate, no_tcp):
    population = initialize_population(test_cases, population_size, no_tcp)
    
    for _ in range(generations):
        fitness_scores = [fitness(ind, test_cases) for ind in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2, no_tcp)
            child = mutate(child, test_cases, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = max(population, key=lambda x: fitness(x, test_cases))
    return best_individual

# Main execution
if __name__ == "__main__":
    file_path = "output_file.txt"  # Update this to the actual file path
    test_cases = read_test_cases(file_path)

    population_size = 50
    generations = 100
    mutation_rate = 0.2
    no_tcp = 5  # Number of test cases to select

    best_solution = genetic_algorithm(test_cases, population_size, generations, mutation_rate, no_tcp)

    print(f"Total number of test cases: {len(test_cases)}")
    print(f"\nBest Solution ({no_tcp} test cases):")
    for index, test_id in enumerate(best_solution, 1):
        test = test_cases[test_id]
        print(f"{index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")

    best_fitness = fitness(best_solution, test_cases)
    print(f"\nBest Fitness Score (Average Coverage): {best_fitness:.2f}%")

    # Add this to check individual test coverages
    print("\nIndividual test coverages in best solution:")
    for test_id in best_solution:
        print(f"{test_id}: {test_cases[test_id]['percentage_coverage']:.2f}%")