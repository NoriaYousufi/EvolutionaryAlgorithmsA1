"""
Requirements
- Implement a genetic algorithm solving the F18 and F19 problems
- Implement an evolution strategy solving the F18 and F19 problems
- Submit at least two files 'studentnumber1_studentnumber2_GA.py' and 'studentnumber1_studentnumber2_ES.py'.
- Additional files of other functions are allowed. Please make sure we can get results by running 'python *_GA.py' and 'python *_ES.py' without additional arguments.
- Submit a report introducing your algorithms and presenting the experimental results. 

Task 2: Evolution Strategy
- How to handle the representation of binary/discrete variables while applying evolution strategies?
- What encoding and decoding methods will you use?
- Which variators (e.g., one-� mutation, correlated mutation, discrete recombination, etc) and selectionmoperators will you use?
- What’s your suggestion for the parameter settings (e.g., population size, step size, etc.)?
"""

import numpy as np
from ioh import get_problem, logger, ProblemClass


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def array_to_bitstring(array):

    sigmoid_values = sigmoid(array)
    bitstring = np.round(sigmoid_values).astype(int)

    return bitstring

def initialization(problem, n_individuals):

    population, mutation_rates = list(), list()

    for individual in range(n_individuals):
        indiv = random_generator.uniform(size = problem.meta_data.n_variables, low = -1, high = 1)
        population.append(array_to_bitstring(indiv))

    for param in range(problem.meta_data.n_variables):
        mutation_rates.append(0.05)  # TODO: mutation rate initialization?

    return population, mutation_rates

def discrete_recombination(r1, r2, problem):

    individual = np.full((50), -1)

    for idx in range(problem.meta_data.n_variables):
        individual[[idx]] = np.random.choice([r1[idx], r2[idx]])

    return individual.tolist()

def recombine(population, n_offspring, problem):

    offspring = list()
    for i in range(n_offspring):
        idx_r1 = random_generator.integers(low = 0, high = len(population))
        idx_r2 = idx_r1
        while idx_r1 == idx_r2:
            idx_r2 = random_generator.integers(low = 0, high = len(population))
        r1 = population[idx_r1]
        r2 = population[idx_r2]
        offspring.append(discrete_recombination(r1, r2, problem))

    return offspring

def adept_step_size(sigma, global_tau, tau, problem):

    g = random_generator.normal(0, 1)
    sigma_prime = np.full((50), 0)

    for idx in range(problem.meta_data.n_variables):
        sigma_prime[idx] = sigma[idx] * np.exp(global_tau * g + tau * random_generator.normal(0, 1))

    return sigma_prime

def mutate(offspring, sigma, problem):

    offspring_prime = list()

    for idx in range(len(offspring)):
        offspring_prime.append(offspring[idx] + sigma * random_generator.normal(0, 1, size = problem.meta_data.n_variables))

    return offspring

def select(offspring, f_offspring, n_individuals, problem):

    f_offspring_mapping = {tuple(offspring[idx]) : f_offspring[idx] for idx in range(len(offspring))}
    sorted_offspring = sorted(offspring, key=lambda x: f_offspring_mapping[tuple(x)], reverse=True)

    return [array_to_bitstring(np.array(x)) for x in sorted_offspring[:n_individuals]]


def studentnumber1_studentnumber2_ES(problem):

    mu_ = 5  # population size
    lambda_ = 10  # offspring size
    global_tau = 1.0 / np.sqrt(2 * problem.meta_data.n_variables)
    tau = 1.0 / np.sqrt(2 * np.sqrt(problem.meta_data.n_variables))
    generation = 0

    population, sigma = initialization(problem, mu_)
    f_population = [problem(x) for x in population]
 
    while problem.state.evaluations < BUDGET:
        offspring = recombine(population, lambda_, problem)
        sigma = adept_step_size(sigma, global_tau, tau, problem)
        mutated_offspring = mutate(offspring, sigma, problem)
        f_offspring = [problem(array_to_bitstring(np.array(x))) for x in mutated_offspring]
        population = select(mutated_offspring, f_offspring, mu_, problem)
        generation += 1

    print(f"Problem {problem.meta_data.name} yielded an objective value of {problem.state.current_best.y} in {generation} generations.")

def create_problem(fid: int):

    problem = get_problem(fid, dimension = DIMENSION, instance=1, problem_class=ProblemClass.PBO)
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name="genetic_algorithm",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    problem.attach_logger(l)

    return problem, l


if __name__ == "__main__":

    BUDGET = 5000
    DIMENSION = 50

    np.random.seed(42)
    random_generator = np.random.default_rng()

    TESTING = True
    if not TESTING:
        F18, _logger = create_problem(18)
        for run in range(20): 
            studentnumber1_studentnumber2_ES(F18)
            F18.reset()
        _logger.close()

        F19, _logger = create_problem(19)
        for run in range(20): 
            studentnumber1_studentnumber2_ES(F19)
            F19.reset()
        _logger.close()

    elif TESTING:
        F18, _ = create_problem(18)
        studentnumber1_studentnumber2_ES(F18)
        F19, _ = create_problem(19)
        studentnumber1_studentnumber2_ES(F19)
