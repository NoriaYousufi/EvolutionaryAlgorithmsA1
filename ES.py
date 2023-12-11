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
        mutation_rates.append(random_generator.random())

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

def studentnumber1_studentnumber2_ES(problem, mu_, lambda_):

    # mu_ = 5  # TODO: Tune?
    # lambda_ = 7 * mu_  # TODO: Tune?

    global_tau = 1.0 / np.sqrt(2 * problem.meta_data.n_variables)
    tau = 1.0 / np.sqrt(2 * np.sqrt(problem.meta_data.n_variables))

    population, sigma = initialization(problem, mu_)
    generation = 0
 
    while problem.state.evaluations < BUDGET:
        offspring = recombine(population, lambda_, problem)
        sigma = adept_step_size(sigma, global_tau, tau, problem)
        mutated_offspring = mutate(offspring, sigma, problem)
        f_offspring = [problem(array_to_bitstring(np.array(x))) for x in mutated_offspring]
        population = select(mutated_offspring, f_offspring, mu_, problem)
        generation += 1

    # print(f"Problem: {problem.meta_data.name}. Found an objective value of {problem.state.current_best.y} in {generation} generations.")
    return problem.state.current_best.y

def create_problem(fid: int):

    problem = get_problem(fid, dimension = DIMENSION, instance=1, problem_class=ProblemClass.PBO)
    l = logger.Analyzer(
        root="data",
        folder_name="run",
        algorithm_name="evolution_strategies",
        algorithm_info="Practical assignment of the EA course",
    )
    problem.attach_logger(l)

    return problem, l

if __name__ == "__main__":

    BUDGET = 5000
    DIMENSION = 50
    TUNING = False

    np.random.seed(42)
    random_generator = np.random.default_rng()

    if not TUNING:
        F18, _logger = create_problem(18)
        for run in range(20): 
            studentnumber1_studentnumber2_ES(F18, mu_ = 15, lambda_= 121)
            F18.reset()
        _logger.close()

        F19, _logger = create_problem(19)
        for run in range(20): 
            studentnumber1_studentnumber2_ES(F19, mu_= 5, lambda_= 98)
            F19.reset()
        _logger.close()
    else:
        for p in [19]:
            problem, _logger = create_problem(p)
            for population_size in range(2, 16):
                for offspring_size in range(population_size, 130):
                        mean = np.array([])
                        for run in range(20):
                            best = studentnumber1_studentnumber2_ES(problem, population_size, offspring_size)
                            mean = np.append(mean, best)
                            problem.reset()
                        with open("./es-optimization.txt", "a") as fo:
                            fo.write(f"{problem.meta_data.name}, {population_size}, {offspring_size}, {np.mean(mean)}\n")
