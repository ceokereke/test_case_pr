import numpy as np
import random
from math import gamma

def objective_fun(test,pname):

    return cov_test


#Initialize population test_values
def initial_population(source,pop_size):

    idx = np.random.random_integers(0,len(source)-1,pop_size)
    population = source[idx]
    return population, idx


def initialize_population(test_cases, population_size, subset_size):
    return [random.sample(test_cases, subset_size) for _ in range(population_size)]

def fitness(individual):
    return sum(test.priority for test in individual)

def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2,sub_size):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [test for test in parent2 if test not in parent1[:crossover_point]]
    return child[:sub_size]  # Ensure we keep only sub_size test cases

def mutate(individual, test_cases, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(individual) - 1)
        new_test = random.choice([t for t in test_cases if t not in individual])
        individual[index] = new_test
    return individual

def genetic_algorithm(test_cases, population_size, generations, mutation_rate, no_tcp):
    population = initialize_population(test_cases, population_size, no_tcp)
    
    for _ in range(generations):
        fitness_scores = [fitness(ind) for ind in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2, no_tcp)
            child = mutate(child, test_cases, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = max(population, key=fitness)
    return best_individual

