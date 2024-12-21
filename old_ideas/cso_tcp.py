#Cuckoo Search ALgorithm via Levy Flight

import numpy as np
from math import gamma
import sys
import subprocess

#Define Objective Function

def objective_fun(test,pname):
    subprocess.call("./"+pname+" "+test,shell=True)
    temp_out=subprocess.check_output("gcov -b -c "+pname,shell=True)
    cov_test = float(temp_out.split(b'\n')[1].split(b':')[-1].split()[0].strip(b'%'))
    return cov_test

#Initialize Population
def initial_population(Pop_Size):
    return np.random.uniform(0,len(Pop_Size),(Pop_Size))

#Calculate Levy flight
def Levy_flight(beta):
    num = gamma(1+beta)*np.sin(np.pi*beta/2 )/gamma((1+beta)/2)*beta*(2**((beta-1)/2))
    sigma = num**(1/beta)
    u = np.random.normal(0,sigma)
    v = np.random.normal(0,1)
    step = u / abs(v)**(1/beta)
    return step

#Apply Cuckoo Search Algorithm
def CS (test_cases, no_priority_cases,pname,location,  MaxT = 100, pa = 0.25):

    
    best_solution = np.zeros(no_priority_cases)
    best_fitness = np.matrix(np.ones((no_priority_cases)) * np.inf)

    subprocess.call(["rm",pname+".gcno"])
    subprocess.call(["rm","-r",pname+".dsYM"])
    subprocess.call(["rm",pname])
    subprocess.call(["rm",pname+".c.gcov"])
    subprocess.call(["rm",pname+".gcda"])
    subprocess.call("gcc -fprofile-arcs -ftest-coverage -g -o "+pname+" "+location+pname+".c",shell=True)

    fitness = np.array([objective_fun(nest,pname) for nest in population])

    #CSA Main Loop Start
    for i in range(MaxT):
        #Generate New Solutoion by Levy Flight
        new_population = np.empty_like(population)

        for j, nest in enumerate(population):
            Step_size = Levy_flight(1.5)
            Step_Direction = np.random.uniform(-1,1,size=Dim)
            new_nest = nest + Step_size * Step_Direction
            new_population[j] = new_nest

            #Check Bounds [-5,5]
            new_population[j] = np.clip(new_population[j], 0, len(test_cases))


        #Calculate New Solution Fitness
        new_fitness = np.array([objective_fun(nest,pname) for nest in new_population])

        #Compare and Replace Solutions
        all_replace_soln = np.where(new_fitness < fitness)
        print ("all replace solution", all_replace_soln)

        replace_soln = all_replace_soln[0]
        print("replace soln", replace_soln)

        population[replace_soln] = new_population[replace_soln]
        fitness[replace_soln] = new_fitness[replace_soln]

        #Sort Population 
        sorted_soln = np.argsort(fitness)
        population = population[sorted_soln]
        fitness = fitness[sorted_soln]

        #update Best Solution
        for k in range(len(best_fitness)): 
            
            if fitness[k] < best_fitness[k]:
                best_solution[k] = population[k]
                best_fitness[k] = fitness[k]

        #Abandon egg with probability (pa) and lay new eggs
        abandon_egg = int(pa*len(test_cases))
        abandon_soln = np.random.choice(len(test_cases),size=abandon_egg, replace=False)
        population[abandon_soln] = initial_population(len(test_cases),abandon_egg)
        fitness[abandon_soln] = np.array([objective_fun(nest,pname) for nest in population[abandon_soln]])
        print(f"Iteration {i+1}/{MaxT}: Best_fitness= {best_fitness}")

    return best_solution, best_fitness



# best_solution,best_fitness = CS(objective_fun, testset, no_of_cases)

# print("Best solution",best_solution)
# print("Best fitness",best_fitness)