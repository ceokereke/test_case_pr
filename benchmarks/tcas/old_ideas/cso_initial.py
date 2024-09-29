#Cuckoo Search ALgorithm via Levy Flight

import numpy as np
from math import gamma

#Define Objective Function

def objective_fun(x):
    # print(" objective")
    # print(x)
    return np.sum(x**2)


#Initialize Population
def initial_population(Pop_Size,Dim):
    return np.random.uniform(-5,5,(Pop_Size,Dim))

#Calculate Levy flight
def Levy_flight(beta):
    num = gamma(1+beta)*np.sin(np.pi*beta/2 )/gamma((1+beta)/2)*beta*(2**((beta-1)/2))
    sigma = num**(1/beta)
    u = np.random.normal(0,sigma)
    v = np.random.normal(0,1)
    step = u / abs(v)**(1/beta)
    return step

#Apply Cuckoo Search Algorithm
def CS (obj_fun,pop_size = 50, Dim = 2, MaxT = 100, pa = 0.25):
    population = initial_population(pop_size, Dim)
    fitness = np.array([obj_fun(nest) for nest in population])
    best_solution = None
    best_fitness = np.inf 

    #CSA Main Loop Start
    for i in range(MaxT):
        #Generate New Solutoion by Levy Flight
        new_population = np.empty_like(population)
        #print(new_population)

        for j, nest in enumerate(population):
            #print (j,nest)
            Step_size = Levy_flight(1.5)
            Step_Direction = np.random.uniform(-1,1,size=Dim)
            new_nest = nest + Step_size * Step_Direction
            new_population[j] = new_nest
            #print(j,new_population[j])

            #Check Bounds [-5,5]
            new_population[j] = np.clip(new_population[j],-5,5)
            #print(j,new_population[j])



        #Calculate New Solution Fitness
        new_fitness = np.array([obj_fun(nest) for nest in new_population])

        #Compare and Replace Solutions
        replace_soln = np.where(new_fitness < fitness)[0]
        print(replace_soln)
        population[replace_soln] = new_population[replace_soln]
        fitness[replace_soln] = new_fitness[replace_soln]

        #Sort Population 
        sorted_soln = np.argsort(fitness)
        #print(sorted_soln)
        population = population[sorted_soln]
        fitness = fitness[sorted_soln]

        #update Best Solution
        if fitness[0] < best_fitness:
            best_solution = population[0]
            best_fitness = fitness[0]

        #Abandon egg with probability (pa) and lay new eggs
        abandon_egg = int(pa*pop_size)
        abandon_soln = np.random.choice(pop_size,size=abandon_egg, replace=False)
        population[abandon_soln] = initial_population(abandon_egg,Dim)
        # print ("abodan solon")
        # print (population[abandon_soln])
        fitness[abandon_soln] = np.array([obj_fun(nest) for nest in population[abandon_soln]])
        print(f"Iteration {i+1}/{MaxT}: Best_fitness= {best_fitness}")

    return best_solution, best_fitness



best_solution,best_fitness = CS(objective_fun)
print("Best solution",best_solution)
print("Best fitness",best_fitness)