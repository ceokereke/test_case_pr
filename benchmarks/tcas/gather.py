
'''  
=================================================================
	@version  3.0
	@author   Ashwin Ramadevanahalli
	@title    Testing.


	fault_analysis Helper module.
=================================================================
'''


import subprocess



tlist=["ga_cso","ga_4","cso_4","rand"]

for prior in tlist:
		subprocess.call("python3 fault_analysis_extra.py "+prior,shell=True)




