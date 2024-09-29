import numpy as np
import random
import math

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

def objective_function(nest, test_cases):
    return sum(test_cases[test_id]['percentage_coverage'] for test_id in nest) / len(nest)

def levy_flight(n):
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step

def generate_new_solution(current_solution, test_ids, n_eggs):
    new_solution = current_solution.copy()
    step = max(1, int(abs(levy_flight(1)[0])))
    for _ in range(step):
        i = random.randint(0, n_eggs - 1)
        new_test_id = random.choice([t for t in test_ids if t not in new_solution])
        new_solution[i] = new_test_id
    return new_solution

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [test_id for test_id in parent2 if test_id not in parent1[:crossover_point]]
    return child[:len(parent1)]

def mutation(solution, test_ids, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(solution) - 1)
        new_test_id = random.choice([t for t in test_ids if t not in solution])
        solution[index] = new_test_id
    return solution

def hybrid_cuckoo_search_ga(test_cases, n_nests, n_eggs, n_iterations,mutation_rate, pa=0.25, crossover_rate=0.6, ):
    test_ids = list(test_cases.keys())
    
    # Initialize nests
    nests = [random.sample(test_ids, n_eggs) for _ in range(n_nests)]
    fitness = [objective_function(nest, test_cases) for nest in nests]
    
    best_nest = max(nests, key=lambda nest: objective_function(nest, test_cases))
    best_fitness = max(fitness)
    
    for _ in range(n_iterations):
        # Cuckoo Search phase
        for i in range(n_nests):
            new_nest = generate_new_solution(nests[i], test_ids, n_eggs)
            new_fitness = objective_function(new_nest, test_cases)
            
            if new_fitness > fitness[i]:
                nests[i] = new_nest
                fitness[i] = new_fitness
                
                if new_fitness > best_fitness:
                    best_nest = new_nest
                    best_fitness = new_fitness
        
        # Genetic Algorithm phase
        for i in range(n_nests):
            if random.random() < crossover_rate:
                partner = random.choice(nests)
                child = crossover(nests[i], partner)
                child_fitness = objective_function(child, test_cases)
                
                if child_fitness > fitness[i]:
                    nests[i] = child
                    fitness[i] = child_fitness
                    
                    if child_fitness > best_fitness:
                        best_nest = child
                        best_fitness = child_fitness
            
            nests[i] = mutation(nests[i], test_ids, mutation_rate)
            fitness[i] = objective_function(nests[i], test_cases)
        
        # Abandon worst nests and build new ones
        worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        for i in worst_nests:
            nests[i] = random.sample(test_ids, n_eggs)
            fitness[i] = objective_function(nests[i], test_cases)
    
    return best_nest, test_ids
