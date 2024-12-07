
# Sample implementation of test case prioritization based on execution time
def prioritize_test_cases(test_cases,some_criterium):
    """
    Prioritize test cases based on their execution time.

    Args:
        test_cases (list of tuples): A list where each tuple represents a test case as (test_case_id, execution_time).

    Returns:
        list: A sorted list of test case IDs prioritized by execution time in descending order.
    """
    # Sort the test cases by execution time (descending order)
    sorted_test_cases = sorted(test_cases, key=lambda x: x[some_criterium], reverse=True)

    # Extract and return the test case IDs in the prioritized order
    return [test_case[0] for test_case in sorted_test_cases]

def f1(nest, test_cases):

    return sum(test_cases[test_id][1] for test_id in nest) / len(nest)

def f2(nest, test_cases):
    return sum(test_cases[test_id]['percentage_coverage'] for test_id in nest) / len(nest)

def f3(nest, test_cases):
    return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

def f4(nest, test_cases):
    return print(nest, test_cases)


myDict = {

            1 : f1,
            2 : f2,
            3 : f3,
            4 : f4

        }  

def myMain(name, nest, test_cases):

    myDict[name](nest, test_cases)


myMain(4, 6726732,"test")       