'''  
=================================================================
	@version  2.0
	@author   Chinonso Okereke
	@title    Testing.


	Preprocessing and initial testing and Gcov output file parse module.
=================================================================
'''
import subprocess
import sys
import pickle

def parse(pname,location):
	
	'''Initializations and clean up'''

	testset={}
	uni=open(location+"universe.txt")
	i=0
	subprocess.call(["rm",pname+".gcno"])
	subprocess.call(["rm","-r",pname+".dsYM"])
	subprocess.call(["rm",pname])
	subprocess.call("gcc -fprofile-arcs -ftest-coverage -g -o "+pname+" "+location+pname+".c",shell=True)

	
	'''
	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	Parsing of statement coverage info
	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	'''

	'''Clean up of files generated after ./ and gcov'''
	subprocess.call(["rm",pname+".c.gcov"])
	subprocess.call(["rm",pname+".gcda"])
	

	'''Runnning each case and storing output'''
	tot_statements = 0
	for line in uni:

		i=i+1
		
		subprocess.call("./"+pname+" "+str(line),shell=True)
		# print(testset)

		temp_out=subprocess.check_output("gcov -b -c "+pname,shell=True).decode('utf-8')
		tot_statements=int(temp_out.split('\n')[1].split()[-1])
		fit=float(temp_out.split('\n')[1].split(':')[-1].split()[0].strip('%'))
		testset[i]=[str(line.strip('\n')),fit]

		try:
			check=subprocess.check_output("mv "+pname+".c.gcov"+" outputs/"+str(i),shell=True).decode('utf-8')
			subprocess.call(["rm",pname+".gcda"])
		except Exception as e:
			logging.error(traceback.format_exc())
			print ("\n Abrupt exit")
			sys.exit(0)
		# input("Enter")




	'''
	Clean up- Removing obj file, gcno and dsYM created after compiling.
	'''
	uni.close()
	subprocess.call(["rm",pname+".gcno"])
	subprocess.call(["rm","-r",pname+".dsYM"])
	subprocess.call(["rm",pname])
	

	for key in testset:
		total = tot_statements
		scount=0
		bcount=0
		Sout=open("outputs/"+str(key))
		for line in Sout.readlines():
			if line.split(':')[0]=="    #####":
				scount+=1

			ls=line.split()
			if ls[0]=="branch" and ls[2]=="taken" and int(ls[3])>0:
				bcount+=1

		Sout.close()

		testset[key].append(total-scount)

		testset[key].append(bcount)

		testset[key].append(bcount+total-scount)

		testset[key].append(scount)

	# print(testset)



	with open('output_file.txt', 'w') as f:
		for key, value in testset.items():
			f.write(f"{key}:{value}\n")

	return testset,tot_statements,i
