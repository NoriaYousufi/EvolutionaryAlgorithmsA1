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
# you need to install this package `ioh`. Please see documentations here: 
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
from ioh import get_problem, logger, ProblemClass

budget = 5000
dimension = 50

# To make your results reproducible (not required by the assignment), you could set the random seed by
# `np.random.seed(some integer, e.g., 42)`
np.random.seed(42)


# k-point crossover
def crossover(population, problem, population_size):
    crossover_pop = []
    crossover_points = 2
    # TODO check is the first for loop is correct
    for _ in range(int(population_size/2)):#offspring size can not exceet original population size?
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        for _ in range(crossover_points):
            point = random.randint(1, problem.meta_data.n_variables-1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            parent1 = child1
            parent2 = child2
        crossover_pop += [child1, child2]
    return crossover_pop

# TODO check mutation
# Bitflip mutation
def mutation(crossover_pop, problem, mutation_rate=0.2):
    mutated_pop = []
    for i in range(len(crossover_pop)):
        for j in range(len(crossover_pop[i])):
            if random.random() < mutation_rate:
                crossover_pop[i][j] = random.choice(range(0, 2))
    mutated_pop = crossover_pop
    return mutated_pop

# Tournament selection
def trounament_selection(pop_sorted, problem, tournament_size):
    selected_parents = []
    for _ in range(len(pop_sorted)):
        tournament_candidates = random.sample(pop_sorted, tournament_size)
        # print(f"candidates{tournament_candidates}")
        best_candidate = sorted(tournament_candidates, key=lambda ind: problem(ind), reverse=True)[0]
        # print(f"best {best_candidate}")
        selected_parents.append(best_candidate)
        # print(f"selected {selected_parents}")
        # break
    return selected_parents


    pass

def studentnumber1_studentnumber2_GA(problem):
    # initial_pop = ... make sure you randomly create the first population
    population_size = 20
    max_dim = problem.meta_data.n_variables

    # Initialize random populations
    initial_pop = [np.random.randint(0, 2, max_dim).tolist() for _ in range(population_size)]

    # Calculate fitness values for each individual
    fitness_values = [problem(individual) for individual in initial_pop]

    # Sort the population based on the pre-calculated fitness values in descending order
    offspring_pop_sorted = [x for value, x in sorted(zip(fitness_values, initial_pop), reverse=True)]

    # `problem.state.evaluations` counts the number of function evaluation automatically,
    # which is incremented by 1 whenever you call `problem(x)`.
    # You could also maintain a counter of function evaluations if you prefer.
    while problem.state.evaluations < budget:
        # please implement the mutation, crossover, selection here
        # .....
        # this is how you evaluate one solution `x`
        # f = problem(x)
        # Crossover
        crossover_pop = crossover(offspring_pop_sorted, problem, population_size)
        # Mutation
        mutation_pop = mutation(crossover_pop, problem)

        # Selection
        # Calculate fitness values for each individual
        fitness_values = [problem(individual) for individual in mutation_pop]

        # Sort the population based on the pre-calculated fitness values in descending order
        pop_sorted = [x for value, x in sorted(zip(fitness_values, mutation_pop), reverse=True)]

        # if problem(pop_sorted[0]) == max_dim:
        #     print(f'problem solved in {problem.state.evaluations} evaluations')
        #     return problem.state.current_best

        offspring_pop_sorted = trounament_selection(pop_sorted, problem, tournament_size=5)

    print(f"current best after using whole budget {problem.state.current_best}")
    return problem.state.current_best
    # no return value needed 


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

    # F19, _logger = create_problem(19)
    # for run in range(20): 
    #     print('f19')
    #     studentnumber1_studentnumber2_GA(F19)
    #     F19.reset()
    # _logger.close()