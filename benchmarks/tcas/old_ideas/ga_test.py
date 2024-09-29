import random

class TestCase:
    def __init__(self, id, execution_time, priority):
        self.id = id
        self.execution_time = execution_time
        self.priority = priority

def initialize_population(test_cases, population_size):
    
    return [random.sample(test_cases, len(test_cases)) for _ in range(population_size)]

def fitness(individual, max_time):
    total_time = 0
    total_priority = 0
    for test in individual:
        if total_time + test.execution_time <= max_time:
            total_time += test.execution_time
            total_priority += test.priority
        else:
            break
    return total_priority

def select_parents(population, fitness_scores):
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + [test for test in parent2 if test not in parent1[:crossover_point]]
    return child

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def genetic_algorithm(test_cases, population_size, generations, mutation_rate, max_time):
    population = initialize_population(test_cases, population_size)
    print (population)
    input("wait")
    
    for _ in range(generations):
        fitness_scores = [fitness(ind, max_time) for ind in population]
        new_population = []
        
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            print("parent 1")
            print(parent1)
            print("parent 2")
            print(parent2)
            
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_individual = max(population, key=lambda x: fitness(x, max_time))
    return best_individual

# Example usage
test_cases = [
    TestCase(1, 10, 5),
    TestCase(2, 5, 3),
    TestCase(3, 8, 4),
    TestCase(4, 12, 7),
    TestCase(5, 6, 2),
]

population_size = 50
generations = 5
mutation_rate = 0.1
max_time = 30

best_order = genetic_algorithm(test_cases, population_size, generations, mutation_rate, max_time)
print("Best test case order:")
for test in best_order:
    print(f"Test {test.id}: Execution Time = {test.execution_time}, Priority = {test.priority}")