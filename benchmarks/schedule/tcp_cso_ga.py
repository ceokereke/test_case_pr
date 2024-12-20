import numpy as np
import random
import math
import obj_fxn
import sys

# def objective_function(nest, test_cases):
#     return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

def initialize_population(test_cases, population_size):
    test_ids = list(test_cases.keys())
    # original_list_copy = test_ids[:]
    # shuffled_list = random.sample(original_list_copy, len(original_list_copy))
    return [random.sample(test_ids, len(test_ids)) for _ in range(population_size)]
    
def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

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
    # for i in range(len(new_egg)):
    current_index = test_ids.index(new_egg)
    new_index = (current_index + step*20) % len(test_ids)
    new_egg = test_ids[new_index]
    return new_egg,current_index,new_index

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point]
    for test_id in parent2:
        if test_id not in child:
            child.append(test_id)
    # print("child len",len(child))
    return child
    # child = parent1[:crossover_point] + [test_id for test_id in parent2 if test_id not in parent1[:crossover_point]]
    # return child[:len(parent1)]

def mutation(solution, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(solution)), 2)
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
    # print(len(solution))
    return solution

def check_lists(lists, min_length):
    if any(len(lst) < min_length for lst in lists):
        print("At least one list does not meet the requirement. Stopping.")
        sys.exit()
        return False
    print("All lists meet the requirement.")
    
    return True

# def correct_list(current, original):
#     """
#     Adjusts `current` list to match `original` list:
#       - Removes duplicates.
#       - Ensures completeness by adding missing elements to the end.

#     Args:
#         current (list): The list to be corrected.
#         original (list): The reference list with the desired elements (no duplicates).

#     Returns:
#         list: Corrected list matching the `original` composition.
#     """
#     # Remove duplicates from current
#     current = list(set(current))
#     print("current",current[1:5])

#     # Find missing elements (present in original but not in current)
#     missing_elements = [item for item in original if item not in current]
#     print("missing",missing_elements)

#     # Add missing elements to the end of the current list
#     current.extend(missing_elements)

def correct_list(current, original):
    """
    Adjusts `current` list to match `original` list:
      - Removes duplicates while preserving order.
      - Ensures completeness by adding missing elements to the end.

    Args:
        current (list): The list to be corrected.
        original (list): The reference list with the desired elements.

    Returns:
        list: Corrected list matching the `original` composition.
    """
    # Use a dictionary to remove duplicates while preserving order
    seen = {}
    for item in current:
        if item not in seen:
            seen[item] = True

    # Convert back to list to keep only unique items
    corrected = list(seen.keys())

    # Add missing elements from original that are not in corrected
    for item in original:
        if item not in corrected:
            corrected.append(item)

    return corrected

    return current
def are_elements_swapped(original, swapped):
    if sorted(original) != sorted(swapped):  # Check if they contain the same elements
        return False
    
    # Find indices where elements differ
    differences = [(i, original[i], swapped[i]) for i in range(len(original)) if original[i] != swapped[i]]
    
    # There should be exactly two differences, and swapping them should make the lists identical
    if len(differences) == 2:
        (i1, o1, s1), (i2, o2, s2) = differences
        return o1 == s2 and o2 == s1
    
    return False
def find_swapped_elements(original, swapped):
    if sorted(original) != sorted(swapped):  # Ensure the lists have the same elements
        return None  # Lists do not contain the same elements

    # Identify the mismatched indices and elements
    mismatches = [(i, original[i], swapped[i]) for i in range(len(original)) if original[i] != swapped[i]]

    if len(mismatches) == 2:
        # Return the mismatched elements
        return mismatches
    return None  # No swaps or more than two elements differ

# Example usage
original_list = [1, 2, 3, 4]
swapped_list = [1, 4, 3, 2]


def hybrid_ga_search_ga(test_cases,fxn, n_nests, n_iterations, mutation_rate, pa=0.25,crossover_rate=0.6 ):
    nests = initialize_population(test_cases, n_nests)
    # lengths = [len(inner_list) for inner_list in nests]
    # print(lengths)
    test_ids = list(test_cases.keys())
    # # Initialize nests
    # nests = [random.sample(test_ids, n_eggs) for _ in range(n_nests)]
    
    
    for _ in range(int(n_iterations)):
        fitness = [obj_fxn.myDict[fxn](nest, test_cases) for nest in nests]
        best_nest = max(nests, key=lambda nest: obj_fxn.myDict[fxn](nest, test_cases))
        best_fitness = max(fitness)
        new_population = []
        # print(fg)
        # check_lists(nests,len(test_ids))
            
            # Cuckoo Search phase

        # Generate a new cuckoo egg
        for _ in range(n_nests):
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
            # print(len(nests[i]),len(new_soln),new_ix,i,j)
            # new_soln[new_ix] = nests[i][j]
            # print(are_elements_swapped(new_soln,nests[i]))

            # swapped_elements = find_swapped_elements(nests[i],new_soln)
            # if swapped_elements:
            #     print("Swapped elements:")
            #     for mismatch in swapped_elements:
            #         print(f"Index {mismatch[0]}: {mismatch[1]} -> {mismatch[2]}")
            # else:
            #         print("No swaps detected or lists are invalid.")

            # print(j,new_ix, old_ix,new_soln[j],new_soln[new_ix])
            fitness_new = obj_fxn.myDict[fxn](new_soln,test_cases)
            fitness_old = obj_fxn.myDict[fxn](nests[i],test_cases)
            # print(new_soln)
            # print(nests[i])
            
            # print(new_soln[old_ix], new_soln[new_ix],old_ix,new_ix,fitness_new,fitness_old)
            # sys.exit()
            # ind_fitness = test_cases[new_egg]['total_branch'] 
            # old_ind_fitness = test_cases[nests[i][j]]['total_branch']



            if fitness_new > fitness_old:
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
            # print("worst", len(nests[i]))
            fitness[i] = obj_fxn.myDict[fxn](nests[i], test_cases)
        # lengths = [len(inner_list) for inner_list in worst_nests]
        # print(lengths)

        # check_lists(nests,len(test_ids))
        # Genetic Algorithm phase
        for _ in range(n_nests):

            # if random.random() < crossover_rate:
            parent1, parent2 = select_parents(nests, fitness)
            # print(len(parent1),len(parent2))
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            # Remove duplicates from current
            child = correct_list(child,test_ids)
            # print(child[1:5])

            new_population.append(child)
            # partner = random.choice(nests)
            # child = crossover(nests[i], partner)
            # child_fitness = obj_fxn.myDict[fxn](child, test_cases)
            
            # if child_fitness > fitness[i]:
            #     nests[i] = child
            #     fitness[i] = child_fitness
                
            #     if child_fitness > best_fitness:
            #         best_nest = child
            #         best_fitness = child_fitness
    
            # nests[i] = mutation(nests[i], mutation_rate)
            # fitness[i] = obj_fxn.myDict[fxn](nests[i], test_cases)
            # # lengths = [len(inner_list) for inner_list in nests]
            # # print(lengths)
        nests = new_population
        # check_lists(nests,len(test_ids))
                    # Abandon worst nests and build new ones
        # worst_nests = sorted(range(len(fitness)), key=lambda i: fitness[i])[:int(pa * n_nests)]
        # for k in worst_nests:
        #     nests[k] = random.sample(test_ids, len(test_ids))
        #     fitness[k] = obj_fxn.myDict[fxn](nests[k], test_cases)
    best_nest = max(nests, key=lambda nest: obj_fxn.myDict[fxn](nest, test_cases))
    # best_fitness = max(fitness)
    # print(best_fitness,best_nest)
    return best_nest, test_ids
