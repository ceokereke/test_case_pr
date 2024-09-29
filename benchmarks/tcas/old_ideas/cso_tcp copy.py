#Cuckoo Search ALgorithm via Levy Flight

import numpy as np
from math import gamma
import random
import sys, os
import subprocess
import pickle as pick

#Define Objective Function

def objective_fun(test_cases, individual):

    return test_cases[test_id][1]

#Initialize population test_values
def initial_population(source,pop_size):

    idx = np.random.random_integers(0,len(source)-1,pop_size)
    # mask = np.ones(len(source), dtype=bool)
    # mask[idx] = False
    population = source[idx]
    return population, idx

#Calculate Levy flight
def Levy_flight(beta):
    num = gamma(1+beta)*np.sin(np.pi*beta/2 )
    den = gamma((1+beta)/2)*beta*(2**((beta-1)/2))
    sigma = (num/den)**(1/beta)
    u = np.random.normal(0,sigma)
    v = np.random.normal(0,1)
    step = u /(np.abs(v)**(1/beta))
    return step

#Apply Cuckoo Search Algorithm
def CS (test_cases, no_priority_cases, MaxT = 100, pa = 0.25):



    #Initialize population
    source_np = np.array(list(test_cases.items()))
    #Find fitness of population 

    fitness = np.array([objective_fun(nest) for nest in source_np])

    print(fitness)
    input("Fitness")
    source_np_ft = np.column_stack((source_np, fitness))
    print(source_np_ft)
    # input("load_ft.pkl")

    population, idx = initial_population(source_np_ft, no_priority_cases)

    #Remove test cases in initialized population from original population
    mask = np.zeros(len(test_cases), dtype=bool)
    mask[idx] = True

    # print(mask)
    # print(type(mask), type(source_np))
    # print(len(mask))
    source_np_ft = source_np_ft[mask]
    print(source_np_ft)
    # input("load_ft.pkl")




    
     #Initial BEst Solution
    best_solution = np.zeros(no_priority_cases)
    best_fitness = np.matrix(np.ones((no_priority_cases)) * 0)

    
   
    new_population = source_np
    #CSA Main Loop Start
    for i in range(MaxT):
        #Generate New Solution by Levy Flight

        j = np.random.random_integers(0,(new_population.size/2)-1)
        Step_size = Levy_flight(1.5)
        Step_Direction = random.uniform(-1,1)
        new_nest = j + round(Step_size * Step_Direction)

        # Clip Solution 
        if new_nest < 0:
            new_nest = 0
        if new_nest >= (new_population.size/2):
            print(new_nest)
            new_nest = (new_population.size/2)-1
            print(new_nest)
        

        #Calculate New Solution Fitness
        print("Cuckoo Solution")
        print(new_nest,new_population[new_nest])

        #print(new_population)
        new_fitness = objective_fun(new_population[new_nest])


        #Compare and Replace Solutions
        x = np.random.random_integers(0,no_priority_cases-1)
        
        fitnessX = objective_fun(population[x])
        print("before replacement")        
        print(population)
        print(fitnessX, new_fitness)

        if new_fitness > fitnessX:
            population[x] = new_population[new_nest]
        
        new_population = np.delete(new_population,new_nest)
        print(population)
        #Find fitness of population 
        fitness = np.array([objective_fun(nest) for nest in population])
        print(fitness)
        #Sort test_values population
        sorted_soln = np.flip(np.argsort(fitness))
        
        population = population[sorted_soln]
        print(population)
        fitness = fitness[sorted_soln]
        print(fitness)
        # print(sorted_soln)
        
        #update Best Solution
        best_solution = population
        best_fitness = fitness
        print(best_solution)
        input("enter")

        #Abandon egg with probability (pa) and lay new eggs
        if np.random.uniform(0,1) < pa:
           
            population[no_priority_cases-1], iidxx = initial_population(new_population,1)
            new_population = np.delete(new_population, iidxx)
        
        print(f"Iteration {i+1}/{MaxT}: Best_fitness= {best_fitness}")

    return best_solution, best_fitness
