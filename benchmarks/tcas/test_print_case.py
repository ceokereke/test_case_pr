
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
                total_branch = float(test_data[4])
                # test_cases[test_id] = {'id': test_id, 'percentage_coverage': percentage_coverage}
                test_cases[test_id] = test_data
print (test_cases["1"])
