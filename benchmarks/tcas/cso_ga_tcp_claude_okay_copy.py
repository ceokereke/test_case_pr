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

def initialize_population(test_cases, population_size):
    test_ids = list(test_cases.keys())
    return [random.sample(test_ids, len(test_ids)) for _ in range(population_size)]


def levy_flight(n):
    beta = 3 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step
def generate_new_egg(current_egg, test_ids):
    new_egg = current_egg
    step = max(1, int(abs(levy_flight(1)[0])))
    # for i in range(len(new_egg)):
    current_index = test_ids.index(new_egg)
    new_index = (current_index + step) % len(test_ids)
    new_egg = test_ids[new_index]
    return new_egg

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
        idx1, idx2 = random.sample(range(len(solution)), 2)
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

    return solution

def hybrid_ga_search_ga(test_cases, n_nests, n_iterations, mutation_rate, pa=0.25,crossover_rate=0.6 ):
    nests = initialize_population(test_cases, n_nests)
    test_ids = list(test_cases.keys())

    # Initialize nests
    #nests = [random.sample(test_ids, n_eggs) for _ in range(n_nests)]
    fitness = [objective_function(nest, test_cases) for nest in nests]
    
    best_nest = max(nests, key=lambda nest: objective_function(nest, test_cases))
    best_fitness = max(fitness)
    print(best_fitness,best_nest)
    
    for _ in range(int(n_iterations)):
        # Cuckoo Search phase

        # Generate a new cuckoo egg
        for i in range(n_nests):
        # i = random.randint(0, n_nests - 1)
            j = random.randint(0, len(nests[i]) - 1)
            new_egg = generate_new_egg(nests[i][j], test_ids)
            # new_egg = generate_new_egg(nests[i], test_ids)
            
            # Choose a random nest
            k = random.randint(0, n_nests - 1)
            
            # Replace the nest if the new egg is better
            # new_fitness = objective_function([new_egg], test_cases)
            ind_fitness = test_cases[new_egg]['percentage_coverage']
            old_ind_fitness = test_cases[nests[i][j]]['percentage_coverage']



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
            nests[i] = random.sample(test_ids, len(test_cases))
            fitness[i] = objective_function(nests[i], test_cases)

        
        # Genetic Algorithm phase

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
        # worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        # for i in worst_nests:
        #     nests[i] = random.sample(test_ids, n_eggs)
        #     fitness[i] = objective_function(nests[i], test_cases)
    return best_nest, best_fitness

# Main execution
if __name__ == "__main__":
    file_path = "output_file.txt"  # Update this to the actual file path
    test_cases = read_test_cases(file_path)

    n_nests = 25
    n_eggs = 5
    n_iterations = 10
    pa = 0.25
    crossover_rate = 0.6
    mutation_rate = 0.1

    best_solution,best_fitness = hybrid_ga_search_ga(test_cases, n_nests, n_eggs, n_iterations, mutation_rate, pa, crossover_rate)

    print(f"Total number of test cases: {len(test_cases)}")
    print(f"\nBest Solution ({n_eggs} test cases):")
    for index, test_id in enumerate(best_solution, 1):
        test = test_cases[test_id]
        print(f"{index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")

    print("\nIndividual test coverages in best solution:")
    for test_id in best_solution:
        print(f"{test_id}: {test_cases[test_id]['percentage_coverage']:.2f}%")