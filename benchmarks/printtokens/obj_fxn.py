
import numpy as np

def fx(nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values = [test_cases[test_id] for test_id in nest]
    
    # weights = np.exp(-np.arange(n))  # Exponential decay for weights
    # score = sum(weight * value for weight, value in zip(weights, values))
    
    
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # # Calculate the weighted sum
    score = sum(weight * value for weight, value in zip(weights, values))
    # # print(score, score/100000)
    return score / 10000

def f1( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][1] for test_id in nest]
    values_2 = [test_cases[test_id][2] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 10000

def f2( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][2] for test_id in nest]
    values_2 = [test_cases[test_id][1] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 50000
def f3( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][1] for test_id in nest]
    values_2 = [test_cases[test_id][5] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 10000

def f4( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][5] for test_id in nest]
    values_2 = [test_cases[test_id][1] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 10000

def f5( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][5] for test_id in nest]
    values_2 = [test_cases[test_id][2] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 10000

def f6( nest, test_cases):
    # Assign weights to prioritize larger values first
    n = len(test_cases)
    values_1 = [test_cases[test_id][2] for test_id in nest]
    values_2 = [test_cases[test_id][5] for test_id in nest]
    weights = [n - i for i in range(n)]  # Higher weights for earlier values
    
    # Calculate the weighted sum
    score = sum(weight * (value1*0.6 + value2*0.4) for weight, value1,value2 in zip(weights, values_1, values_2))
    return score / 10000



myDict = {

            #1 : fx,
            2 : fx,
            3 : fx,
            4 : fx,
            6 : fx,
            7 : f1,
            8 : f2,
            9 : f3,
            10 : f4,
            11 : f5,
            12 : f6
        }  

def myMain(name, nest, test_cases):
    myDict[name](nest, test_cases)
      