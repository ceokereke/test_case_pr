import numpy as np
import random
import math
import obj_fxn

# def objective_function(nest, test_cases):
#     return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

def levy_flight(n):
    beta = 1 / 2
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
    u = np.random.randn(n) * sigma
    v = np.random.randn(n)
    step = u / np.abs(v)**(1 / beta)
    return step

def generate_new_egg(current_egg, test_ids):
    new_egg = current_egg
    step = max(1, int(abs(levy_flight(1)[0])))
    # print(step)
    # for i in range(len(new_egg)):
    current_index = test_ids.index(new_egg)
    new_index = (current_index + step*20) % len(test_ids)
    new_egg = test_ids[new_index]
    # print(type(current_egg),type(new_egg),type(current_index),type(new_index))
    # print(current_egg,new_egg,current_index,new_index)
    return new_egg,current_index,new_index


def cuckoo_search(test_cases,fxn, n_nests, n_iterations, pa=0.25):
    test_ids = list(test_cases.keys())
    
    # Initialize nests (each nest contains eggs)
    nests = [random.sample(test_ids, len(test_ids)) for _ in range(n_nests)]
    # print(nests)

    fitness = [obj_fxn.myDict[fxn](nest, test_cases) for nest in nests]
    # print(fitness)
    
    best_nest = max(nests, key=lambda nest: obj_fxn.myDict[fxn](nest, test_cases))
    best_fitness = max(fitness)
    # print(best_nest, best_fitness)
    
    for _ in range(n_iterations):
        # Generate a new cuckoo egg
        i = random.randint(0, n_nests - 1)
        j = random.randint(0, len(test_ids) - 1)
        new_egg, old_ix, new_ix = generate_new_egg(nests[i][j], test_ids)
        # new_egg = generate_new_egg(nests[i], test_ids)
        
        # Choose a random nest
        # k = random.randint(0, n_nests - 1)
        
        # Replace the nest if the new egg is better
        new_soln = nests[i].copy()
        # new_fitness = obj_fxn.myDict[fxn]([new_egg], test_cases)
        new_soln[old_ix], new_soln[new_ix] = new_soln[new_ix], new_soln[old_ix]
        # new_soln[j] = new_egg
        
        # new_soln[new_ix] = nests[i][j]
        # print(len(nests[i]),len(new_soln),new_ix,i,j)
        # print(j,new_ix, old_ix,new_soln[j],new_soln[new_ix])
        fitness_new = obj_fxn.myDict[fxn](new_soln,test_cases)
        fitness_old = obj_fxn.myDict[fxn](nests[i],test_cases)
        # ind_fitness = test_cases[new_egg]['total_branch'] 
        # old_ind_fitness = test_cases[nests[i][j]]['total_branch']



        if fitness_new > fitness_old:
            nests[i][j] = new_egg
            fitness[i] = obj_fxn.myDict[fxn](nests[i], test_cases)
        #     # Update the best solution if needed
        if fitness[i] > best_fitness:
            best_nest = nests[i]
            best_fitness = fitness[i]
            # print(best_fitness,best_nest)


        
        # Abandon worst nests and build new ones
        worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        for k in worst_nests:
            nests[k] = random.sample(test_ids, len(test_ids))
            fitness[k] = obj_fxn.myDict[fxn](nests[k], test_cases)
    #print(fitness)
    return best_nest    

