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
	random.shuffle(tests)
	subprocess.call(["rm",pname+".gcno"])
	subprocess.call(["rm","-r",pname+".dsYM"])
	subprocess.call(["rm",pname])
	subprocess.call(["rm",pname+".c.gcov"])
	subprocess.call(["rm",pname+".gcda"])
	subprocess.call("gcc -fprofile-arcs -ftest-coverage -g -o "+pname+" "+location+pname+".c",shell=True)
	for test in tests:

		if sflag==True:
			s_adeq_suite.append(test)
		if bflag==True:
			b_adeq_suite.append(test)
		sb_adeq_suite.append(test)

		subprocess.call("./"+pname+" "+test,shell=True)
		temp_out=subprocess.check_output("gcov -b -c "+pname,shell=True)
		if  float(maxlim[pname])==float(temp_out.split(b'\n')[1].split(b':')[-1].split()[0].strip(b'%')):
			sflag=False

		if 100==float(temp_out.split(b'\n')[2].split(b':')[-1].split()[0].strip(b'%')):
			bflag=False

		if not(sflag) and not(bflag):
			return s_adeq_suite,b_adeq_suite,sb_adeq_suite

	sys.exit("Adequate test not found(random)")





