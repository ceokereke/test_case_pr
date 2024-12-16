import main_cso_cov_branches
import obj_fxn

iter = 1

for i in obj_fxn.myDict:
    print(i)
    for j in range(iter):
        main_cso_cov_branches.main(i,j)
