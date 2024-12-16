import random
print("Reading Test cases file")
file_path = "output_file_or.txt"
test_cases = {}
n=1
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(':')
        if len(parts) == 2:
            test_id = parts[0]
            test_data = eval(parts[1])
            if len(test_data) >= 2:
                
                # percentage_coverage = float(test_data[1])
                data = float(test_data[1])
                data1 = test_data[1:7]
                # test_cases[test_id] = {'id': test_id, 'percentage_coverage': percentage_coverage}
                test_cases[test_id] = data1

# sort_1 = sorted(range(len(test_cases)), key=lambda x: test_cases[1][])
# print (sort_1)
print (test_cases["1"])
print (test_cases["1"][1])
test_ids = list(test_cases.keys())
    
# Initialize nests (each nest contains eggs)
nest = random.sample(test_ids, len(test_ids))
# print(nest,len(nest))

# cont_test_cases = [test_cases[test_id] for test_id in nest]
# print(cont_test_cases)
# sorted_test_cases = sorted(range(len(test_cases)), key=lambda x: cont_test_cases[x], reverse=True)
# print(sorted_test_cases)
# prioritize_test = [cont_test_cases[test_case] for test_case in sorted_test_cases]
# print(prioritize_test)
# score = sum((rank + 1) * cont_test_cases[prioritize_test.index(test_case)] for rank, test_case in enumerate(prioritize_test))
# testscore = score / len(test_cases)

