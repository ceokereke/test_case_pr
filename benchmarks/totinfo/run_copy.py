import multiprocessing
import obj_fxn
import main_cso_cov_branches

def run_iteration(item_and_iter):
    """
    Function to run a single iteration for a specific item
    
    :param item_and_iter: Tuple containing (item, iteration number)
    """
    item, j = item_and_iter
    print(f"Processing {item}, iteration {j}")
    main_cso_cov_branches.main(item, j)

def parallel_execute(iter=30):
    """
    Execute iterations in parallel
    
    :param iter: Number of iterations
    """
    # Prepare parameters for parallel execution
    all_params = []
    for i in obj_fxn.myDict:
        print(i)  # Keeping the original print statement
        for j in range(iter):
            all_params.append((i, j))
    
    # Determine the number of cores to use
    num_cores = multiprocessing.cpu_count()
    print('num?',num_cores)

    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_cores) as pool:
        # Map the run_iteration function to all parameter combinations
        pool.map(run_iteration, all_params)

if __name__ == '__main__':
    parallel_execute(iter=30)