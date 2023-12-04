"""
Requirements
- Implement a genetic algorithm solving the F18 and F19 problems
- Implement an evolution strategy solving the F18 and F19 problems
- Submit at least two files 'studentnumber1_studentnumber2_GA.py' and 'studentnumber1_studentnumber2_ES.py'.
- Additional files of other functions are allowed. Please make sure we can get results by running 'python *_GA.py' and 'python *_ES.py' without additional arguments.
- Submit a report introducing your algorithms and presenting the experimental results. 

Task 1: Genetic Algorithm
Some hints:
- Which variators (i.e., mutation and crossover) and selection operators will you use?
- What's your suggestion for the parameter settings (e.g., population size, mutation rate, etc.)?
""" 

import numpy as np
import random
from ioh import get_problem, logger, ProblemClass

budget = 5000
dimension = 50
np.random.seed(42)


# 1-point crossover
def one_point_crossover(population, problem, population_size):

    crossover_pop = []
    random_generator = np.random.default_rng()

    while len(crossover_pop) < population_size:
        p1_idx = random_generator.integers(low = 0, high = len(population))
        p2_idx = random_generator.integers(low = 0, high = len(population))
        while p1_idx == p2_idx:
            p2_idx = random_generator.integers(low = 0, high = len(population))
        parent1 = population[p1_idx]
        parent2 = population[p2_idx]

        crossover_idx = random_generator.integers(low = 1, high = problem.meta_data.n_variables)
        child1 = parent1[:crossover_idx] + parent2[crossover_idx:]
        child2 = parent2[:crossover_idx] + parent1[crossover_idx:]
        crossover_pop.extend([child1, child2])

    return crossover_pop

# Bitflip mutation
def bitflip_mutation(crossover_pop, problem, mutation_rate=0.01):  # TODO: mutation rate used to be 0.1, might be a bit high
    mutated_pop = []
    for i in range(len(crossover_pop)):
        for j in range(len(crossover_pop[i])):
            if random.random() < mutation_rate:
                crossover_pop[i][j] = random.choice(range(0, 2))
        mutated_pop.append(crossover_pop[i])
    return mutated_pop

def adaptive_bitflip(crossover_pop, problem, mutation_rate = 0.01, mutation_decrease = 0.005):
    mutated_offspring = list()
    evaluated_offspring = tuple([problem(x), x] for x in crossover_pop)
    sorted_offspring = sorted(evaluated_offspring, reverse=True)
    for fitness, individual in sorted_offspring:
        mutation_rate = mutation_rate - mutation_decrease
        child = individual
        for j, gene in enumerate(individual):
            if random.random() <= mutation_rate:
                # flip
                if gene == 1:
                    child[j] = 0
                elif gene == 0:
                    child[j] = 1
        mutated_offspring.append(child)

    return mutated_offspring

# Tournament selection
def tournament_selection(pop, f_pop, problem, tournament_size):
    selected_parents = []
    tournament_candidates = list(zip(pop, f_pop))
    for _ in range(len(pop)):
        tournament_candidates = random.sample(tournament_candidates, tournament_size)
        best_candidate = sorted(tournament_candidates, key=lambda ind: ind[-1], reverse=True)[0]
        selected_parents.append(best_candidate[0])
    return selected_parents

def studentnumber1_studentnumber2_GA(problem):
    population_size = 20

    # Initialize random population
    initial_pop = [np.random.randint(0, 2, problem.meta_data.n_variables).tolist() for _ in range(population_size)]

    # Sort the population based on the calculated fitness values in descending order
    # offspring_pop_sorted = sorted(initial_pop, key=lambda i: problem(i), reverse=True)
    offspring_pop_sorted = initial_pop
    generation = 0

    while problem.state.evaluations < budget:
        # Crossover
        crossover_pop = one_point_crossover(offspring_pop_sorted, problem, population_size)
        # Mutation
        mutation_pop = bitflip_mutation(crossover_pop, problem)
        # mutation_pop = adaptive_bitflip(crossover_pop, problem)
        # Selection
        # Sort the population based on the calculated fitness values in descending order
        f_pop = [problem(x) for x in mutation_pop]
        # pop_sorted = sorted(mutation_pop, key=lambda i: problem(i), reverse=True)
        offspring_pop_sorted = tournament_selection(mutation_pop, f_pop, problem, tournament_size=10)
        assert len(offspring_pop_sorted) == population_size
        generation += 1
    print(generation)
    print(f"{problem.state.evaluations}")
    print(f"current best after using whole budget {problem.state.current_best} with fitness {problem.state.current_best.y}")


def create_problem(fid: int):
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name="genetic_algorithm",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l

if __name__ == "__main__":
    # this how you run your algorithm with 20 repetitions/independent run
    F18, _logger = create_problem(18)
    for run in range(20): 
        print('f18')
        studentnumber1_studentnumber2_GA(F18)
        F18.reset() # it is necessary to reset the problem after each independent run
    _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    F19, _logger = create_problem(19)
    for run in range(20): 
        print('f19')
        studentnumber1_studentnumber2_GA(F19)
        F19.reset()
    _logger.close()