import numpy as np
import random
import math

def read_test_cases(file_path):
    test_cases = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                test_id = parts[0]
                test_data = eval(parts[1])
                if len(test_data) >= 2:
                    percentage_coverage = float(test_data[1])
                    test_cases.append({'id': test_id, 'percentage_coverage': percentage_coverage})
    return test_cases

# def initialize_population(test_cases, population_size, subset_size=5):
#     test_ids_tst = test_cases[0]['id']
#     test_ids= test_cases[int(test_index) for test_index in test_cases]
#     print(test_ids)
#     return [random.sample(test_ids, subset_size) for _ in range(population_size)]

def objective_function(nest, test_cases):
    return sum(sum(test_cases[int(test_index)]['percentage_coverage'] for test_index in egg) for egg in nest) / (len(nest) * len(nest[0]))

def levy_flight(n):
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step

def generate_new_egg(current_egg, n_tests):
    new_egg = current_egg.copy()
    step = max(1, int(abs(levy_flight(1)[0])))
    start = random.randint(0, n_tests - 1)
    end = (start + step) % n_tests
    if start != end:
        new_egg = np.roll(new_egg, shift=(end - start))
        # testcase
    return new_egg

def cuckoo_search(test_cases, n_nests, n_eggs, n_iterations, pa=0.25):
    n_tests = len(test_cases)
    
    # Initialize nests (each nest contains 5 eggs)
    nests = [np.array([np.random.permutation(n_tests) for _ in range(n_eggs)]) for _ in range(n_nests)]
    # nests = initialize_population(test_cases, n_nests)
    # print(nests)
    print(len(nests))
    print(nests[0])
    print(len(nests[0]))
    print(nests[0][0])
    print(len(nests[0][0]))


    fitness = [objective_function(nest, test_cases) for nest in nests]
    
    best_nest = max(nests, key=lambda nest: objective_function(nest, test_cases)).copy()
    best_fitness = max(fitness)
    
    for _ in range(n_iterations):
        # Generate a new cuckoo egg
        i = random.randint(0, n_nests - 1)
        j = random.randint(0, n_eggs - 1)
        new_egg = generate_new_egg(nests[i][j], n_tests)
        
        # Choose a random nest
        k = random.randint(0, n_nests - 1)
        
        # Replace a random egg in the chosen nest if the new egg is better
        if objective_function(np.array([new_egg]), test_cases) > objective_function(np.array([nests[k][j]]), test_cases):
            nests[k][j] = new_egg
            fitness[k] = objective_function(nests[k], test_cases)
            
            # Update the best solution if needed
            if fitness[k] > best_fitness:
                best_nest = nests[k].copy()
                best_fitness = fitness[k]
        
        # Abandon worst nests and build new ones
        worst_nests = np.argsort(fitness)[:int(pa * n_nests)]
        for i in worst_nests:
            nests[i] = np.array([np.random.permutation(n_tests) for _ in range(n_eggs)])
            fitness[i] = objective_function(nests[i], test_cases)
    print(best_nest)
    return best_nest, best_fitness

# Main execution
if __name__ == "__main__":
    file_path = "output_file.txt"  # Update this to the actual file path
    test_cases = read_test_cases(file_path)

    n_nests = 25
    n_eggs = 5
    n_iterations = 1000
    best_solution, best_fitness = cuckoo_search(test_cases, n_nests, n_eggs, n_iterations)

    print(f"Total number of test cases: {len(test_cases)}")
    print(f"\nBest Nest (5 eggs):")
    for egg_index, egg in enumerate(best_solution, 1):
        print(f"\nEgg {egg_index}:")
        print("Top 5 Test Cases:")
        for i, test_index in enumerate(egg[:5], 1):
            test = test_cases[int(test_index)]
            print(f"{i}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")

    print(f"\nBest Fitness Score (Average Coverage): {best_fitness:.2f}%")