'''  
================================================================
	@author   Chinonso Okereke
	@title    Test Case Prioritization 


	Main module.
=================================================================
'''

import os
import sys
import subprocess
import testset_parse
import rand_pri
import cuckoo_search_tcp
import ga_test_tcp_read
import pickle as pick


'''
Initializations
'''
pname=str(str(subprocess.check_output("pwd",shell=True).decode('utf-8')).split('/')[-1].strip())

location=""


test_var = 0

if test_var < 1:

    '''
    Cleaning
    '''
    print ("################################\nEntered Cleaning\n################################\n")
    subprocess.call("rm -r outputs",shell=True)
    subprocess.call("mkdir outputs",shell=True)
    '''
    Testset parse module 
    returns: 	A dictionary with Key in range '1 to No_of_tests' and value as the testcases and total number of statements in program.
    returns:	state_testset=list of <No of statements it covers,testcase> and Brances_testset=list of <No of brances it covers,testcase> and both.
    input: 		program name, location of program.
    '''
    print ("################################\nEntered Testset parse module\n################################\n")
    testset,tot_statements,No_of_tests=testset_parse.parse(pname,location)
    print (testset)

    print (tot_statements)

    test_load = [testset, tot_statements, No_of_tests]
    with open('load_test.pkl', 'wb') as outp1:
            pick.dump(test_load, outp1, pick.HIGHEST_PROTOCOL)

else:
    with open('load_test.pkl', 'rb') as inp1:
                setup = pick.load(inp1)
                testset = setup[0]
                tot_statements = setup[1]
                No_of_tests = setup[2]
    pass

'''
Random prioritization
returns:	Random prioritizated testsets for statement, branch and both coverage.
input:		testset

'''
#No of Priority cases should be considered
no_tcp = 5 #CHange value to suit your needs
print ("################################\nEntered Random prioritization\n################################\n")
shuffled_test, best_test_rand=rand_pri.pri(testset,no_tcp)
print(best_test_rand)
input("Random")
print(shuffled_test)
print("Reading Test cases file")
file_path = "output_file.txt"
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

print ("################################\nEntered CSO prioritization\n################################\n")
#No of Priority cases should be considered
population_size = 50 # number of nests

generations = 100 #generations or iterations
best_test_cso =cuckoo_search_tcp.cuckoo_search(test_cases, population_size, no_tcp, generations)


print(best_test_cso)

print ("################################\nEntered GA prioritization\n################################\n")
#No of Priority cases should be considered
mutation_rate = 0.2

best_test_ga = ga_test_tcp_read.genetic_algorithm(test_cases, population_size, generations, mutation_rate,no_tcp)
print("Top 5 prioritized test cases for GA:")
for test in best_test_ga:
    print(f"Test {test}: Content = {test[0]} Coverage = {test[1]}")


print ("################################\nResult Section\n################################\n")



print ("Total number of test cases=",No_of_tests)

'''Restoring environment'''
subprocess.call("rm tempfile",shell=True)
subprocess.call("cp selected tempfile",shell=True)
subprocess.call("cp selected "+pname+".gcda",shell=True)

'''Storing Results'''

subprocess.call("rm -r results",shell=True)

subprocess.call("mkdir results",shell=True)

with open('results/cso', 'wb') as test_file:
    pick.dump(best_test_cso, test_file)
    test_file.close()
with open('results/ga', 'wb') as test_file:
    pick.dump(best_test_ga, test_file)
    test_file.close()
with open('results/rand', 'wb') as test_file:
    pick.dump(best_test_rand, test_file)
    test_file.close()
with open('alltestcases', 'wb') as outp1:
	pick.dump(testset, outp1, pick.HIGHEST_PROTOCOL)
    
print ("Task Complete.Thank you.")



