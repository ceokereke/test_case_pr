import numpy as np
import random
import math
import obj_fxn

# def objective_function(nest, test_cases):
#     return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

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


def cuckoo_search(test_cases,fxn, n_nests, n_iterations, pa=0.25):
    test_ids = list(test_cases.keys())
    
    # Initialize nests (each nest contains eggs)
    nests = [random.sample(test_ids, len(test_ids)) for _ in range(n_nests)]
    # print(nests)

    sorted_test_cases = sorted(test_cases, key=lambda x: x[1], reverse=True)
    fitness = [obj_fxn.myDict[fxn](nest, test_cases) for nest in nests]
    # print(fitness)
    
    best_nest = max(nests, key=lambda nest: obj_fxn.myDict[fxn](nest, test_cases))
    best_fitness = max(fitness)
    # print(best_nest, best_fitness)
    
    for _ in range(n_iterations):
        # Generate a new cuckoo egg
        i = random.randint(0, n_nests - 1)
        j = random.randint(0, len(test_ids) - 1)
        new_egg = generate_new_egg(nests[i][j], test_ids)
        # new_egg = generate_new_egg(nests[i], test_ids)
        
        # Choose a random nest
        k = random.randint(0, n_nests - 1)
        
        # Replace the nest if the new egg is better
        # new_fitness = obj_fxn.myDict[fxn]([new_egg], test_cases)
        ind_fitness = test_cases[new_egg]['total_branch'] 
        old_ind_fitness = test_cases[nests[i][j]]['total_branch']

        # if new_fitness > fitness[k]:
        #     nests[k] = new_egg
        #     fitness[k] = new_fitness
            
        #     # Update the best solution if needed
        #     if new_fitness > best_fitness:
        #         best_nest = new_egg
        #         best_fitness = new_fitness

        if ind_fitness > old_ind_fitness:
            nests[i][j] = new_egg
            fitness[i] = obj_fxn.myDict[fxn](nests[i], test_cases)
        #     # Update the best solution if needed
        if fitness[i] > best_fitness:
            best_nest = nests[i]
            best_fitness = fitness[i]


        
        # Abandon worst nests and build new ones
        worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        for i in worst_nests:
            nests[i] = random.sample(test_ids, len(test_ids))
            fitness[i] = obj_fxn.myDict[fxn](nests[i], test_cases)
    
    return best_nest    

