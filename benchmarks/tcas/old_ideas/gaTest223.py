import random
import numpy as np

def initialize_population(test_cases, population_size, subset_size=5):
    test_ids = list(test_cases.keys())
    return [random.sample(test_ids, subset_size) for _ in range(population_size)]

def fitness(individual, test_cases):
    return sum(test_cases[test_id]['priority'] for test_id in individual)

def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [test_id for test_id in parent2 if test_id not in parent1[:crossover_point]]
    return child[:5]  # Ensure we keep only 5 test cases

def mutate(individual, test_cases, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(individual) - 1)
        new_test_id = random.choice([t for t in test_cases.keys() if t not in individual])
        individual[index] = new_test_id
    return individual

def genetic_algorithm(test_cases, population_size, generations, mutation_rate):
    population = initialize_population(test_cases, population_size)
    
    for _ in range(generations):
        fitness_scores = [fitness(ind, test_cases) for ind in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, test_cases, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = max(population, key=lambda x: fitness(x, test_cases))
    return best_individual

# Generate 100+ test cases as a dictionary
test_cases = {
    f"TC{i}": {
        'execution_time': random.randint(1, 20),
        'priority': random.randint(1, 10)
    } for i in range(150)
}

with open('output_file_ga.txt', 'w') as f:
     for key, value in test_cases.items():
         f.write(f"{key}:{value}\n")

population_size = 50
generations = 100
mutation_rate = 0.2

best_subset = genetic_algorithm(test_cases, population_size, generations, mutation_rate)

print("Top 5 prioritized test cases:")
for test_id in best_subset:
    test = test_cases[test_id]
    print(f"Test {test_id}: Execution Time = {test['execution_time']}, Priority = {test['priority']}")