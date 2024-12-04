import main_cso_cov_branches
import obj_fxn
amp = [0,10,15,20]
iter = 30

# LOAD  = 0 for new obstacle arrangement 
# LOAD = 1 to use previous/existing obstacle arrangement
LOAD = 1 
for i in obj_fxn.myDict:
    for _ in range(iter):
        main_cso_cov_branches.main(i)
