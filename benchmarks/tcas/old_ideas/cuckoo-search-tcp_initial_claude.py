import numpy as np
import random
import math

def read_test_cases(file_path):
    test_cases = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                test_id = parts[0]
                code_coverage = float(parts[1])
                test_cases.append({'id': test_id, 'code_coverage': code_coverage})
    return test_cases

def objective_function(solution, test_cases):
    prioritized_tests = [test_cases[i] for i in solution]
    total_coverage = sum(test['code_coverage'] for test in prioritized_tests)
    average_coverage = total_coverage / len(prioritized_tests)
    return average_coverage

def levy_flight(n):
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step

def generate_new_solution(current_solution, n_tests):
    new_solution = current_solution.copy()
    step = int(abs(levy_flight(1)[0]))
    
    if step > 0:
        start = random.randint(0, n_tests - 1)
        end = (start + step) % n_tests
        
        if start < end:
            element = new_solution[start]
            new_solution[start:end] = new_solution[start+1:end+1]
            new_solution[end-1] = element
        else:
            element = new_solution[start]
            new_solution[start:] = new_solution[start+1:]
            new_solution[:end] = new_solution[1:end+1]
            new_solution[end-1] = element
    
    return new_solution
def cuckoo_search(test_cases, n_nests, n_eggs, n_iterations, pa=0.25):
    n_tests = len(test_cases)
    
    nests = [[np.random.permutation(n_tests) for _ in range(n_eggs)] for _ in range(n_nests)]
    fitness = [[objective_function(egg, test_cases) for egg in nest] for nest in nests]
    
    # best_solution = max(egg for nest in nests for egg in nest, key=lambda egg: objective_function(egg, test_cases))
    best_solution = max((egg for nest in nests for egg in nest), key=lambda egg: objective_function(egg, test_cases))
    best_fitness = objective_function(best_solution, test_cases)
    
    for _ in range(n_iterations):
        # Generate one cuckoo per nest
        for i in range(n_nests):
            j = random.randint(0, n_eggs - 1)
            cuckoo = generate_new_solution(nests[i][j], n_tests)
            f_cuckoo = objective_function(cuckoo, test_cases)
            
            k = random.randint(0, n_nests - 1)
            l = random.randint(0, n_eggs - 1)
            
            if f_cuckoo > fitness[k][l]:
                nests[k][l] = cuckoo
                fitness[k][l] = f_cuckoo
            
            if f_cuckoo > best_fitness:
                best_solution = cuckoo
                best_fitness = f_cuckoo
        
        # Abandon worst nests
        worst_nests = sorted(range(n_nests), key=lambda i: max(fitness[i]))[:int(pa * n_nests)]
        for i in worst_nests:
            nests[i] = [np.random.permutation(n_tests) for _ in range(n_eggs)]
            fitness[i] = [objective_function(egg, test_cases) for egg in nests[i]]
'''           
def cuckoo_search(test_cases, n_nests, n_eggs, n_iterations):
    n_tests = len(test_cases)
    
    nests = [[np.random.permutation(n_tests) for _ in range(n_eggs)] for _ in range(n_nests)]
    fitness = [[objective_function(egg, test_cases) for egg in nest] for nest in nests]
    
    best_solution = max(egg for nest in nests for egg in nest, key=lambda egg: objective_function(egg, test_cases))
    best_fitness = objective_function(best_solution, test_cases)
    
    for _ in range(n_iterations):
        # Generate one cuckoo per nest
        for i in range(n_nests):
            j = random.randint(0, n_eggs - 1)
            cuckoo = generate_new_solution(nests[i][j], n_tests)
            f_cuckoo = objective_function(cuckoo, test_cases)
            
            k = random.randint(0, n_nests - 1)
            l = random.randint(0, n_eggs - 1)
            
            if f_cuckoo > fitness[k][l]:
                nests[k][l] = cuckoo
                fitness[k][l] = f_cuckoo
            
            if f_cuckoo > best_fitness:
                best_solution = cuckoo
                best_fitness = f_cuckoo
        
        # Abandon worst nest
        worst_nest_idx = min(range(n_nests), key=lambda i: max(fitness[i]))
        nests[worst_nest_idx] = [np.random.permutation(n_tests) for _ in range(n_eggs)]
        fitness[worst_nest_idx] = [objective_function(egg, test_cases) for egg in nests[worst_nest_idx]]
    
    return best_solution, best_fitness
    '''

# Main execution
if __name__ == "__main__":
    file_path = "path_to_your_test_cases_file.txt"  # Replace with your actual file path
    test_cases = read_test_cases(file_path)

    n_nests = 5
    n_eggs = 5
    n_iterations = 1000
    best_solution, best_fitness = cuckoo_search(test_cases, n_nests, n_eggs, n_iterations)

    print(f"Total number of test cases: {len(test_cases)}")
    print("\nTop 10 Test Cases in the Best Prioritization:")
    cumulative_coverage = 0
    for i, test_index in enumerate(best_solution[:10], 1):
        test = test_cases[test_index]
        cumulative_coverage += test['code_coverage']
        average_coverage = cumulative_coverage / i
        print(f"{i}. {test['id']} - Code Coverage: {test['code_coverage']:.4f}, "
              f"Average Coverage: {average_coverage:.4f}")

    print(f"\nBest Fitness Score (Average Coverage): {best_fitness:.4f}")
