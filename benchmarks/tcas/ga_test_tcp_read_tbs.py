import random
import numpy as np
import obj_fxn

def initialize_population(test_cases, population_size):
    test_ids = list(test_cases.keys())
    return [random.sample(test_ids, len(test_ids)) for _ in range(population_size)]

def fitness(individual, test_cases):
    return sum(test_cases[test_id]['total_branch'] for test_id in individual) / len(individual)

def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point]
    for test_id in parent2:
        if test_id not in child:
            child.append(test_id)
    return child

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual



def genetic_algorithm(test_cases, population_size, generations, mutation_rate):
    population = initialize_population(test_cases, population_size)
    
    for _ in range(generations):
        fitness_scores = [fitness(ind, test_cases) for ind in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = max(population, key=lambda x: fitness(x, test_cases))
    best_fitness = fitness(best_individual, test_cases)
    
    return best_individual
