'''  
================================================================
	@author   Chinonso Okereke
	@title    Test Case Prioritization 


	Main module.
=================================================================
'''

import subprocess
import testset_parse_copy
import rand_pri
import cuckoo_search_tcp_tbs
import ga_test_tcp_read_tbs
import cso_ga_tcp_claude_okay_copy_tbs
import pickle as pick


'''
Initializations
'''
pname=str(str(subprocess.check_output("pwd",shell=True).decode('utf-8')).split('/')[-1].strip())

location=""


test_var = 1

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
    testset,tot_statements,No_of_tests=testset_parse_copy.parse(pname,location)
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
no_tcp = No_of_tests # len(test_cases)  #CHange value to suit your needs
print ("################################\nEntered Random prioritization\n################################\n")
shuffled_test, best_test_rand=rand_pri.pri(testset)
# print(best_test_rand)
# print(shuffled_test)
print("Reading Test cases file")
file_path = "output_file_or.txt"
test_cases = {}
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            test_id = parts[0]
            test_data = eval(parts[1])
            if len(test_data) >= 2:
                # percentage_coverage = float(test_data[1])
                total_branch = float(test_data[4])
                # test_cases[test_id] = {'id': test_id, 'percentage_coverage': percentage_coverage}
                test_cases[test_id] = {'id': test_id, 'total_branch': total_branch}


print ("################################\nEntered CSO prioritization\n################################\n")
#No of Priority cases should be considered
population_size = 100 # number of nests

generations = 300 #generations or iterations
best_test_cso =cuckoo_search_tcp_tbs.cuckoo_search(test_cases, population_size,generations)


# print(best_test_cso)
# for index, test_id in enumerate(best_test_cso, 1):
#     test = test_cases[test_id]
#     # print(f"{index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")
#     print(f"{index}. {test['id']} - Total Branches and Statements: {test['total_branch']:.2f}")
# print(f" Fitness is: {best_test_cso_fitness}")
print ("################################\nEntered GA prioritization\n################################\n")
#No of Priority cases should be considered
mutation_rate = 0.2

best_test_ga = ga_test_tcp_read_tbs.genetic_algorithm(test_cases, population_size, generations, mutation_rate)
# print(best_test_ga)
# for index, test_id in enumerate(best_test_ga, 1):
#     test = test_cases[test_id]
#     print(f"{index}. {test['id']} - Total Branches and Statements: {test['total_branch']:.2f}")
#     # print(f"{index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")
# print(f" Fitness is: {best_test_ga_fitness}")

print ("################################\nEntered CSO+GA prioritization\n################################\n")

# best_test_cso_ga, all_tests = cso_ga_tcp_claude.hybrid_ga_search_ga(test_cases, population_size,no_tcp, generations, mutation_rate)

best_test_cso_ga, all_tests,best_test_cso_ga_fitness = cso_ga_tcp_claude_okay_copy_tbs.hybrid_ga_search_ga(test_cases, population_size, generations, mutation_rate)
# print(best_test_cso_ga)
# for index, test_id in enumerate(best_test_cso_ga, 1):
#     test = test_cases[test_id]
#     print(f"{index}. {test['id']} - Total Branches and Statements: {test['total_branch']:.2f}")
#     # print(f"{index}. {test['id']} - Percentage Coverage: {test['percentage_coverage']:.2f}%")
# print(f" Fitness is: {best_test_cso_ga_fitness}")

print ("################################\nResult Section\n################################\n")


print ("Total number of test cases=",No_of_tests)

'''Restoring environment'''
subprocess.call("rm tempfile",shell=True)
subprocess.call("cp selected tempfile",shell=True)
subprocess.call("cp selected "+pname+".gcda",shell=True)

'''Storing Results'''

subprocess.call("rm -r results",shell=True)

subprocess.call("mkdir results",shell=True)

with open('results/cso_4', 'wb') as test_file:
    pick.dump(best_test_cso, test_file)
    test_file.close()
with open('results/rand', 'wb') as test_file:
    pick.dump(best_test_rand, test_file)
    test_file.close()
with open('results/ga_4', 'wb') as test_file:
    pick.dump(best_test_ga, test_file)
    test_file.close()
with open('results/ga_cso', 'wb') as test_file:
    pick.dump(best_test_cso_ga, test_file)
    test_file.close()
with open('results/all_tests', 'wb') as test_file:
    pick.dump(all_tests, test_file)
    test_file.close()
with open('alltestcases', 'wb') as outp1:
	pick.dump(testset, outp1, pick.HIGHEST_PROTOCOL)
     
    
print ("Task Complete.Thank you.")



