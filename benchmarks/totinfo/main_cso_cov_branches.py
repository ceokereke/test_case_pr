'''  
================================================================
	@author   Chinonso Okereke
	@title    Test Case Prioritization 


	Main module.
=================================================================
'''

import subprocess
import sys
import testset_parse_copy
import rand_pri
import tcp_cuckoo_search as tcp_cuckoo_search
import tcp_ga_test as tcp_ga_test
import tcp_cso_ga as tcp_cso_ga
import pickle as pick



def main (fxn,iter):
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
                    if (fxn < 7):
                        # percentage_coverage = float(test_data[1])
                        data = float(test_data[fxn])
                        # test_cases[test_id] = {'id': test_id, 'percentage_coverage': percentage_coverage}
                        test_cases[test_id] = data
                    else:
                         data = test_data[1:7]
                         test_cases[test_id] = data


    print ("################################\nEntered CSO prioritization\n################################\n")
    #No of Priority cases should be considered
    population_size = 50 # number of nests

    generations = 300 #generations or iterations
    best_test_cso =tcp_cuckoo_search.cuckoo_search(test_cases,fxn, population_size,generations)
    # print(best_test_cso)
    best_cso_values = [test_cases[test_id] for test_id in best_test_cso]
    # print(best_cso_values)
    


    print ("################################\nEntered GA prioritization\n################################\n")
    #No of Priority cases should be considered
    mutation_rate = 0.2

    best_test_ga = tcp_ga_test.genetic_algorithm(test_cases,fxn, population_size, generations, mutation_rate)
    # print(best_test_ga)
    best_ga_values = [test_cases[test_id] for test_id in best_test_ga]
    # print(best_ga_values)
    


    print ("################################\nEntered CSO+GA prioritization\n################################\n")

    # best_test_cso_ga, all_tests = cso_ga_tcp_claude.hybrid_ga_search_ga(test_cases, population_size,no_tcp, generations, mutation_rate)

    best_test_cso_ga, all_tests = tcp_cso_ga.hybrid_ga_search_ga(test_cases,fxn, population_size, generations, mutation_rate)
    # print(best_test_cso_ga)
    best_cso_ga_values = [test_cases[test_id] for test_id in best_test_cso_ga]
    # print(best_cso_ga_values)
    # sys.exit()
    
    print ("################################\nResult Section\n################################\n")


    print ("Total number of test cases=",No_of_tests)

    '''Restoring environment'''
    subprocess.call("rm tempfile",shell=True)
    subprocess.call("cp selected tempfile",shell=True)
    subprocess.call("cp selected "+pname+".gcda",shell=True)

    '''Storing Results'''

    # subprocess.call("rm -r results",shell=True)

    # subprocess.call("mkdir results",shell=True)

    with open('results/cso'+'_'+str(fxn)+'_'+str(iter), 'wb') as test_file:
        pick.dump(best_test_cso, test_file)
        test_file.close()
    with open('results/rand'+'_'+str(fxn)+'_'+str(iter), 'wb') as test_file:
        pick.dump(best_test_rand, test_file)
        test_file.close()
    with open('results/ga'+'_'+str(fxn)+'_'+str(iter), 'wb') as test_file:
        pick.dump(best_test_ga, test_file)
        test_file.close()
    with open('results/ga_cso'+'_'+str(fxn)+'_'+str(iter), 'wb') as test_file:
        pick.dump(best_test_cso_ga, test_file)
        test_file.close()
    # with open('results/all_tests', 'wb') as test_file:
    #     pick.dump(all_tests, test_file)
    #     test_file.close()
    with open('alltestcases', 'wb') as outp1:
        pick.dump(testset, outp1, pick.HIGHEST_PROTOCOL)
        
        
    print ("Task Complete.Thank you.")



