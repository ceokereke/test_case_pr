'''  
=================================================================
	@version  2.0
	@author   Ashwin Ramadevanahalli
	@title    Testing.


	Random Priorization module.
=================================================================
'''
import random
import subprocess
import sys

'''Intializations'''


def pri(tests,pname,location,maxlim):
	s_adeq_suite=[]
	b_adeq_suite=[]
	sb_adeq_suite=[]
	sflag=True
	bflag=True

	#random.shuffle(tests) python2 code

	#python3 code
	# Convert the dictionary values to a list
	values = list(tests.values())

	# Shuffle the list of values
	random.shuffle(values)

	# If you need to maintain the keys and shuffle the values, you can create a new dictionary
	shuffled_tests = dict(zip(tests.keys(), values))

	# Get the dict_values object from the shuffled dictionary
	shuffled_tests_values = shuffled_tests.values()

	#print(shuffled_tests_values)  # This will output the dict_values object


	subprocess.call(["rm",pname+".gcno"])
	subprocess.call(["rm","-r",pname+".dsYM"])
	subprocess.call(["rm",pname])
	subprocess.call(["rm",pname+".c.gcov"])
	subprocess.call(["rm",pname+".gcda"])
	subprocess.call("gcc -fprofile-arcs -ftest-coverage -g -o "+pname+" "+location+pname+".c",shell=True)
	
	for test in shuffled_tests_values:
		print("see",sflag,bflag)
		if sflag==True:
			s_adeq_suite.append(test)
		if bflag==True:
			b_adeq_suite.append(test)
		sb_adeq_suite.append(test)

		subprocess.call("./"+pname+" "+test,shell=True)
		temp_out=subprocess.check_output("gcov -b -c "+pname,shell=True).decode('utf-8')
		if  float(maxlim[pname])>=float(temp_out.split('\n')[1].split(':')[-1].split()[0].strip('%')):
			sflag=False

		if 100==float(temp_out.split('\n')[2].split(':')[-1].split()[0].strip('%')):
			bflag=False

		if not(sflag) and not(bflag):
			return s_adeq_suite,b_adeq_suite,sb_adeq_suite

	sys.exit("Adequate test not found(random)")





