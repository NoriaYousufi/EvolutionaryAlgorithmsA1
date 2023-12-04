import numpy as np
from ioh import get_problem, logger, ProblemClass
import random


# 1-point crossover
def one_point_crossover(population, problem, population_size):

    crossover_pop = []

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

def bitflip_mutation(crossover_pop, problem, mutation_rate=0.01):  # TODO: Tune mutation rate

    mutated_pop = []

    for i in range(len(crossover_pop)):
        for j in range(problem.meta_data.n_variables):
            if random_generator.random() < mutation_rate:
                crossover_pop[i][j] = (crossover_pop[i][j] + 1) % 2
        mutated_pop.append(crossover_pop[i])

    return mutated_pop

def tournament_selection(pop, f_pop, problem, tournament_size):  # TODO: Tune tournament size

    selected_parents = []
    tournament_candidates = list(zip(pop, f_pop))

    for _ in range(len(pop)):
        tournament_candidates = random.sample(tournament_candidates, tournament_size)
        best_candidate = sorted(tournament_candidates, key=lambda ind: ind[-1], reverse=True)[0]
        selected_parents.append(best_candidate[0])

    return selected_parents

def studentnumber1_studentnumber2_GA(problem):

    population_size = 20
    population = [random_generator.integers(low = 0, high = 2, size = problem.meta_data.n_variables).tolist() for _ in range(population_size)]
    # population = [np.random.randint(0, 2, problem.meta_data.n_variables).tolist() for _ in range(population_size)]
    generation = 0

    while problem.state.evaluations < BUDGET:
        # Crossover
        crossover_pop = one_point_crossover(population, problem, population_size)
        # Mutation
        mutation_pop = bitflip_mutation(crossover_pop, problem)
        # Selection
        f_pop = [problem(x) for x in mutation_pop]
        population = tournament_selection(mutation_pop, f_pop, problem, tournament_size=10)
        generation += 1

    print(f"Problem: {problem.meta_data.name}. Found an objective value of {problem.state.current_best.y} in {generation} generations.")

def create_problem(fid: int):

    problem = get_problem(fid, dimension=DIMENSION, instance=1, problem_class=ProblemClass.PBO)
    l = logger.Analyzer(
        root="data",
        folder_name="run",
        algorithm_name="genetic_algorithm",
        algorithm_info="Practical assignment of the EA course",
    )
    problem.attach_logger(l)

    return problem, l

if __name__ == "__main__":

    BUDGET = 5000
    DIMENSION = 50

    np.random.seed(42)
    random_generator = np.random.default_rng()

    F18, _logger = create_problem(18)
    for run in range(20): 
        studentnumber1_studentnumber2_GA(F18)
        F18.reset()
    _logger.close()

    F19, _logger = create_problem(19)
    for run in range(20): 
        studentnumber1_studentnumber2_GA(F19)
        F19.reset()
    _logger.close()