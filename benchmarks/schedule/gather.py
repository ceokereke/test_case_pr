
'''  
=================================================================
	@version  3.0
	@author   Ashwin Ramadevanahalli
	@title    Testing.


	fault_analysis Helper module.
=================================================================
'''


import subprocess
import fault_analysis_extra
import obj_fxn
import sys
import pickle



# tlist=["ga_cso"]
tlist=["ga_cso","ga","cso","rand"]
pname=str(str(subprocess.check_output("pwd",shell=True)).split('/')[-1].rstrip('\\n\''))
iter = 1

# #Read test case
# for prior in tlist:
# 	for i in obj_fxn.myDict:
# 		for j in range(iter):
# 			suite_name = prior +"_"+ str(i) + "_"+str(iter)
# 			for suite in [suite_name]:
# 				infile=open("results/"+suite,"rb")
# 				testcases=pickle.load(infile)
# 				print(testcases)
# 				print("#######################################################")
# sys.exit()
			


rep=open("Overall_Results_"+pname+".txt","w")
for prior in tlist:
	res=open("Results_"+pname+"_"+prior+".csv","w")
	rep.write(prior+" , \n")
	res.write(prior+" , \n")
	for i in obj_fxn.myDict:
		res.write("Objective fxn :" + str(i)+", \n")
		rep.write("Objective fxn, Ave AFPD,  Ave CE, \n")
		res.write("AFPD,CE, \n")
		total_afpd=0
		total_ce = 0
		for j in range(iter):
			j+1
			suite_name = prior +"_"+ str(i) + "_"+str(j)
			afpd, ce = fault_analysis_extra.main(suite_name)
			res.write(str(afpd)+","+str(ce)+", \n")
			total_afpd = total_afpd +afpd
			total_ce = total_ce + ce
		ave_afpd = total_afpd / iter
		ave_ce = total_ce / iter
		res.write("Average AFPD, Average CE, \n")
		res.write(str(ave_afpd)+","+str(ave_ce)+", \n")
		# rep.write("Average AFPD, Average CE, \n")
		rep.write(str(i)+", "+str(ave_afpd)+", "+str(ave_ce)+", \n")
		res.write("\n")
		rep.write("\n")




		




