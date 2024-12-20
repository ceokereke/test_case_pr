'''  
=================================================================
	@version  1.0
	@author   CHinonso OKereke
	@title    Testing.


	Main module.
=================================================================
'''

import pickle 
import subprocess
import time
import sys


def main(prior):

	
	meganame=prior

	pname=str(str(subprocess.check_output("pwd",shell=True)).split('/')[-1].rstrip('\\n\''))
	print (pname)
	num_faults=int(subprocess.check_output("ls | grep -c ^v",shell=True))

	subprocess.call("rm -r safe",shell=True)
	subprocess.call("rm -r V0outouts",shell=True)
	# subprocess.call("rm FResults_"+pname+"_"+meganame,shell=True)



	subprocess.call("mkdir safe",shell=True)
	subprocess.call("mkdir V0outouts",shell=True)

	subprocess.call("cp *.c safe/",shell=True)
	subprocess.call("cp *.h safe/",shell=True)

	real_outputs=[]


	# res=open("FResults_"+pname+"_"+meganame,"w")
	# res.write("0 Fault analysis of "+pname+"\n0 Total number of faults: "+str(num_faults)+"\n")


	print("####################")
	print("Enetring loop Pass")
	print("####################")

	with open('alltestcases', 'rb') as inp1:
		alltestcases = pickle.load(inp1)
	print(alltestcases)
	# input("all")

	for suite in [meganame]:
		infile=open("results/"+suite,"rb")
		testcases=pickle.load(infile)
		# print(testcases)
		print("####################")
		print("After Pickle")
		print("####################")

		out=open("V0outouts/Vmainoutputs_rt"+suite,"w")
		
		subprocess.call(["rm",pname])
		subprocess.call("gcc -o "+pname+" "+pname+".c",shell=True)

		print("####################")
		print("After Gcc")
		print("####################")

		for test in testcases:
			# print(test)
			
			test_content = alltestcases.get(int(test))[0]
			# print(test)
			# input("test")
			try:

				temp=subprocess.run("timeout 1 ./"+pname+" "+test_content,shell=True,stdout=subprocess.PIPE,universal_newlines=True)
				# print(temp)
				pout=str(temp.stdout)
				# print(pout)
				
				# pout=str(subprocess.check_output(["./"+pname,test_content],timeout=5))
			except subprocess.CalledProcessError as e:
				print("Exception occured XXXXXXXXXXXXX",str(e))
				real_outputs.append(str(e))
				input('XXXXXXXXXXXXXXXXX')
				out.write(str(e))
			except subprocess.TimeoutExpired as e:
				print("Exception occured XXXXXXXXXXXXX",str(e))
				real_outputs.append(str(e))
				input('XXXXXXXXXXXXXXXXX')
				out.write(str(e))
			except Exception as e:
				print ("Doesnt Run.......")
				print (str(e))
				real_outputs.append(str(e))
				input('XXXXXXXXXXXXXXXXX')
				out.write(str(e))

			else:
				real_outputs.append(pout)
				print("Exception did not occured XXXXXXXXXXXXX")
				out.write(pout)



			
		print("####################")
		print("After load zone")
		print("####################")
		# to calculate apfd
		n = len(testcases)
		m = num_faults
		tf_sum = 0 
		jmax = 1
		for i in range(num_faults):
			i+=1
			print("runnning version:",i)
			subprocess.call("cp v"+str(i)+"/* .",shell=True)
			subprocess.call("gcc -o "+pname+" "+pname+".c",shell=True)
			c=0
			fflag=False
			tested = 0  # to calculate apfd
			for j,test in enumerate(testcases):
				# print(test)
				test_content = alltestcases.get(int(test))[0]
				try:
					temp=subprocess.run("timeout 1 ./"+pname+" "+test_content,shell=True,stdout=subprocess.PIPE, universal_newlines=True)
					temp_out=str(temp.stdout)
				except subprocess.CalledProcessError as e:
					print("Exception occured XXXXXXXXXXXXX",str(e))
					temp_out=str(e)
				except subprocess.TimeoutExpired as e:
					print("Exception occured XXXXXXXXXXXXX",str(e))
					temp_out=str(e)
				except Exception as e:
					print ("Doesnt Run.......")
					temp_out=str(e)
					# real_outputs.append(str(e))
					# out.write(str(e))
				print("####\nfisrt one:",real_outputs[c],"\nSecond one:",temp_out,"\n####")
				if not(real_outputs[c]==temp_out):
					# res.write(str(j)+": "+str(test)+" in "+suite+" reveals fault	 in v"+str(i)+"\n")
					fflag=True
					print("####\nfisrt one:",real_outputs[c],"\nSecond one:",temp_out,"\n####")
					print("####################")
					print(i,"\t",suite,"\tPass")
					print("####################")
					if jmax <= j+1:
						jmax = j+1

					if tested < 1:
						tf_sum += j + 1
						tested +=1
						# res.write(str(j+1)+" testcase:"+str(tf_sum)+" "+str(tested)+"\n")
					break
				c+=1
			
			if fflag==False:
					# res.write(suite +" does not reveal fault in v"+str(i)+"\n")
					print("####################")
					print(i,"\t",suite,"\Fail")
					print("####################")

			
			subprocess.call("cp safe/* .",shell=True)
		infile.close()

		apfd = 1 - (tf_sum / (n * m)) + (1 / (2 * n))

		ce = 1-(jmax/n)

		# res.write("APFD is "+str(apfd))
	# res.close()
	out.close()


	print("Total number of faults: ",num_faults,"\n")
	print("HIghest suite used",jmax)
	return apfd, ce,












