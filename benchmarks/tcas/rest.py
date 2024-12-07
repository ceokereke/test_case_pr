import random

# Sample implementation of test case prioritization based on execution time
def prioritize_test_cases(test_cases):
    """
    Prioritize test cases based on their execution time.

    Args:
        test_cases (list of tuples): A list where each tuple represents a test case as (test_case_id, execution_time).

    Returns:
        list: A sorted list of test case IDs prioritized by execution time in descending order.
    """
    # Sort the test cases by execution time (descending order)
    sorted_test_cases = sorted(test_cases, key=lambda x: x[1], reverse=True)

    # Extract and return the test case IDs in the prioritized order
    return [test_case[0] for test_case in sorted_test_cases]

def evaluate_test_suite_ranking(prioritized_test_cases, test_case_data):
    """
    Evaluate the test suite by calculating a rank-based score weighted by execution time.

    Args:
        prioritized_test_cases (list): A list of test case IDs in prioritized order.
        test_case_data (dict): A dictionary mapping test case IDs to their execution times.

    Returns:
        float: A score representing the quality of the prioritization.
    """
    # Calculate the rank-based weighted score
    score = sum((rank + 1) * test_case_data[test_case] for rank, test_case in enumerate(prioritized_test_cases))
    return score / len(test_cases)

# Example test cases with their execution times (in seconds)
test_cases = [
    ("TC1", 3.5),
    ("TC2", 1.2),
    ("TC3", 4.0),
    ("TC4", 2.8)
]

# Create a mapping of test case IDs to their execution times
test_case_data = {tc[0]: tc[1] for tc in test_cases}

# Correctly prioritized suite
correct_suite = prioritize_test_cases(test_cases)

# Generate 4 random test suites with different rankings
random_suites = []
for _ in range(9):
    shuffled_suite = test_cases.copy()
    random.shuffle(shuffled_suite)
    random_suites.append([tc[0] for tc in shuffled_suite])

# Evaluate each test suite and determine the best one
best_score = float('-inf')
best_suite = None

print(f"Correctly Prioritized Suite: {correct_suite}")
correct_score = evaluate_test_suite_ranking(correct_suite, test_case_data)
print(f"Correct Suite Evaluation Score: {correct_score}\n")

for idx, suite in enumerate(random_suites, start=1):
    score = evaluate_test_suite_ranking(suite, test_case_data)
    print(f"Test Suite {idx}: {suite}, Evaluation Score: {score}")
    if score > best_score:
        best_score = score
        best_suite = (idx, suite)

if best_suite:
    print(f"\nBest Random Suite: Test Suite {best_suite[0]} with Score: {best_score} and Ranking: {best_suite[1]}")
