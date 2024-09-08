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
    if not nest or not nest[0]:
        return 0
    
    total_coverage = 0
    unique_tests = set()
    for egg in nest:
        for test_id in egg:
            if test_id in test_cases and test_id not in unique_tests:
                total_coverage += test_cases[test_id]['percentage_coverage']
                unique_tests.add(test_id)
    
    return total_coverage / len(unique_tests) if unique_tests else 0

def levy_flight(n):
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step

# def generate_new_egg(current_egg, test_ids):
#     new_egg = current_egg.copy()
#     step = max(1, int(abs(levy_flight(1)[0])))
#     for i in range(len(new_egg)):
#         current_index = test_ids.index(new_egg[i])
#         new_index = (current_index + step) % len(test_ids)
#         new_egg[i] = test_ids[new_index]
#     return new_egg

def generate_new_egg(current_egg, test_ids):
    new_egg = current_egg
    step = max(1, int(abs(levy_flight(1)[0])))
    # for i in range(len(new_egg)):
    current_index = test_ids.index(new_egg)
    new_index = (current_index + step) % len(test_ids)
    new_egg = test_ids[new_index]
    return new_egg


def cuckoo_search(test_cases, n_nests, n_eggs, n_iterations, pa=0.25):
    test_ids = list(test_cases.keys())
    
    # Initialize nests (each nest contains n_eggs eggs)
    nests = [random.sample(test_ids, n_eggs) for _ in range(n_nests)]
    # print(nests)
    fitness = [objective_function(nest, test_cases) for nest in nests]
    print(fitness)
    
    best_nest = max(nests, key=lambda nest: objective_function([nest], test_cases))
    best_fitness = max(fitness)
    print(best_nest, best_fitness)
    
    for _ in range(n_iterations):
        # Generate a new cuckoo egg
        i = random.randint(0, n_nests - 1)
        j = random.randint(0, n_eggs - 1)
        new_egg = generate_new_egg(nests[i][j], test_ids)
        # new_egg = generate_new_egg(nests[i], test_ids)
        
        # Choose a random nest
        k = random.randint(0, n_nests - 1)
        
        # Replace the nest if the new egg is better
        # new_fitness = objective_function([new_egg], test_cases)
        ind_fitness = test_cases[new_egg]['percentage_coverage']
        old_ind_fitness = test_cases[nests[i][j]]['percentage_coverage']

        # if new_fitness > fitness[k]:
        #     nests[k] = new_egg
        #     fitness[k] = new_fitness
            
        #     # Update the best solution if needed
        #     if new_fitness > best_fitness:
        #         best_nest = new_egg
        #         best_fitness = new_fitness

        if ind_fitness > old_ind_fitness:
            nests[i][j] = new_egg
            fitness[i] = objective_function(nests[i], test_cases)
        #     # Update the best solution if needed
        if fitness[i] > best_fitness:
            best_nest = nests[i]
            best_fitness = fitness[i]


        
        # Abandon worst nests and build new ones
        worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        for i in worst_nests:
            nests[i] = random.sample(test_ids, n_eggs)
            fitness[i] = objective_function([nests[i]], test_cases)
        print(best_nest,best_fitness)
        print(nests[i],fitness[i])
    
    return best_nest, best_fitness

# Main execution
if __name__ == "__main__":
    file_path = "output_file.txt"  # Update this to the actual file path
    test_cases = read_test_cases(file_path)

    n_nests = 25
    n_eggs = 5
    n_iterations = 10
    best_solution, best_fitness = cuckoo_search(test_cases, n_nests, n_eggs, n_iterations)

    print(f"Total number of test cases: {len(test_cases)}")
    print(f"\nBest Nest ({n_eggs} eggs):")
    for egg_index, test_id in enumerate(best_solution, 1):
        test = test_cases[test_id]
        print(f"{egg_index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")

    print(f"\nBest Fitness Score (Average Coverage): {best_fitness:.2f}%")

    # Add this to check individual test coverages
    print("\nIndividual test coverages in best solution:")
    for test_id in best_solution:
        print(f"{test_id}: {test_cases[test_id]['percentage_coverage']:.2f}%")