
def xt(nest, test_cases):
    return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

def xp(nest, test_cases):
    return sum(test_cases[test_id]['percentage_coverage'] for test_id in nest) / len(nest)

def fitness(nest, test_cases):
    return sum(test_cases[test_id]['total_branch'] for test_id in nest) / len(nest)

def testx(nest, test_cases):
    return print(nest, test_cases)


myDict = {

            1 : xt,
            2 : xp,
            3 : fitness,
            4 : testx

        }  

def myMain(name, nest, test_cases):

    myDict[name](nest, test_cases)


myMain(4, 6726732,"test")       