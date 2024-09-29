import numpy as np
import random
import math

# Generate test cases
def generate_test_cases(n_tests):
    test_cases = []
    for i in range(n_tests):
        execution_time = random.uniform(0.1, 10.0)  # Execution time in seconds
        fault_detection_probability = random.uniform(0.1, 1.0)
        code_coverage = random.uniform(0.1, 1.0)
        test_cases.append({
            'id': f'TC{i+1}',
            'execution_time': execution_time,
            'fault_detection_probability': fault_detection_probability,
            'code_coverage': code_coverage
        })
    return test_cases

# Objective function for test case prioritization
def objective_function(solution, test_cases):
    prioritized_tests = [test_cases[i] for i in solution]
    total_time = sum(test['execution_time'] for test in prioritized_tests)
    avg_fault_detection = sum(test['fault_detection_probability'] for test in prioritized_tests) / len(prioritized_tests)
    avg_code_coverage = sum(test['code_coverage'] for test in prioritized_tests) / len(prioritized_tests)
    
    # We want to minimize execution time and maximize fault detection and code coverage
    return total_time - (avg_fault_detection + avg_code_coverage)

def generate_new_solution(x, bounds, best_solution):
    beta = 3/2
    sigma = 0.6966  # Precomputed value for beta = 3/2
    u = np.random.randn(len(x)) * sigma
    v = np.random.randn(len(x))
    step = u / np.power(np.abs(v), 1 / beta)
    stepsize = 0.01 * step * (x - best_solution)
    new_solution = x + stepsize * np.random.randn(len(x))
    return np.clip(np.round(new_solution).astype(int), bounds[:, 0], bounds[:, 1])

def cuckoo_search(test_cases, n_nests, n_iterations, pa=0.25, n_cuckoos=5):
    n_tests = len(test_cases)
    bounds = np.array([[0, n_tests-1]] * n_tests)
    
    # Initialize nests (solutions)
    nests = np.array([np.random.permutation(n_tests) for _ in range(n_nests)])
    fitness = np.array([objective_function(nest, test_cases) for nest in nests])
    best_nest = nests[np.argmin(fitness)]
    best_fitness = np.min(fitness)
    
    for _ in range(n_iterations):
        # Generate new solutions (cuckoo eggs)
        cuckoos = np.array([generate_new_solution(nests[random.randint(0, n_nests-1)], bounds, best_nest) for _ in range(n_cuckoos)])
        cuckoos = np.array([np.unique(cuckoo, return_inverse=True)[1] for cuckoo in cuckoos])  # Ensure valid permutations
        f_cuckoos = np.array([objective_function(cuckoo, test_cases) for cuckoo in cuckoos])
        
        # Update nests
        for cuckoo, f_cuckoo in zip(cuckoos, f_cuckoos):
            j = random.randint(0, n_nests-1)
            if f_cuckoo < fitness[j]:
                nests[j] = cuckoo
                fitness[j] = f_cuckoo
        
        # Abandon worst nests
        worst = np.argsort(fitness)[:int(n_nests*pa)]
        for i in worst:
            nests[i] = np.random.permutation(n_tests)
            fitness[i] = objective_function(nests[i], test_cases)
        
        # Update best solution
        best_index = np.argmin(fitness)
        if fitness[best_index] < best_fitness:
            best_fitness = fitness[best_index]
            best_nest = nests[best_index]
    
    return best_nest, best_fitness

# Generate test cases
n_tests = 20
test_cases = generate_test_cases(n_tests)

# Run Cuckoo Search
n_nests = 25
n_iterations = 1000
best_solution, best_fitness = cuckoo_search(test_cases, n_nests, n_iterations)

# Print results
print("Optimized Test Case Order:")
for i, test_index in enumerate(best_solution):
    test = test_cases[test_index]
    print(f"{i+1}. {test['id']} - Execution Time: {test['execution_time']:.2f}s, "
          f"Fault Detection Probability: {test['fault_detection_probability']:.2f}, "
          f"Code Coverage: {test['code_coverage']:.2f}")

print(f"\nBest Fitness Score: {best_fitness}")