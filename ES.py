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
# you need to install this package `ioh`. Please see documentations here: 
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
from ioh import get_problem, logger, ProblemClass

budget = 5000
dimension = 50

# To make your results reproducible (not required by the assignment), you could set the random seed by
# `np.random.seed(some integer, e.g., 42)`
np.random.seed(42)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def array_to_bitstring(array):
    # Apply the sigmoid function to each element in the array
    sigmoid_values = sigmoid(array)
    
    # Map sigmoid values to binary (0 or 1)
    bitstring = np.round(sigmoid_values).astype(int)
    
    return bitstring


def initialization(mu, dimension, lowerbound=-5.0, upperbound=5.0):
    parent = []
    parent_sigma = []

    for i in range(mu):
        individual = np.random.uniform(low=lowerbound, high=upperbound, size=dimension)
        # Convert the real-valued array to a bitstring using sigmoid
        bitstring = array_to_bitstring(individual)
        parent.append(bitstring)
        parent_sigma.append(0.05 * (upperbound - lowerbound))

    return parent, parent_sigma

def recombination(parent, parent_sigma):
    p1, p2 = np.random.choice(len(parent), 2, replace=False)
    print(f"p1 {p1}")
    print(f"p2 {p2}")
    pass
    # offspring = (parent[p1] + parent[p2]) / 2
    # sigma = (parent_sigma[p1] + parent_sigma[p2]) / 2

    # return offspring, sigma

def studentnumber1_studentnumber2_ES(problem):
    # hint: F18 and F19 are Boolean problems. Consider how to present bitstrings as real-valued vectors in ES
    # initial_pop = ... make sure you randomly create the first population
    mu_ = 5  # population size
    lambda_ = 10  # offspring size
    tau = 1.0 / np.sqrt(problem.meta_data.n_variables)  # step size adjustment parameter

    # Initialize population and strategy parameters
    parent, parent_sigma = initialization(mu_, problem.meta_data.n_variables)
    print(f"parent {parent}")
    print(f"parent_sigma {parent_sigma}")
    parent = [ind.tolist() for ind in parent]
    print(f"list parent {parent}")
 
    # `problem.state.evaluations` counts the number of function evaluation automatically,
    # which is incremented by 1 whenever you call `problem(x)`.
    # You could also maintain a counter of function evaluations if you prefer.
    while problem.state.evaluations < budget:
        # please implement the mutation, crossover, selection here
        # .....
        # this is how you evaluate one solution `x`
        # f = problem(x)
        # Evaluate parent solutions
        parent_f = [problem(x) for x in parent]
        print(f"parent_f {parent_f}")

        # Recombination 
        offspring = []
        offspring_sigma = []
        offspring_f = []

        for i in range(lambda_):
            o, s = recombination(parent, parent_sigma)
            offspring.append(o)
            offspring_sigma.append(s)

        print(f"Offspring {offspring}")
        print(f"offsprong sigma {offspring_sigma}")
        break
        pass
        
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
        print("F18")
        studentnumber1_studentnumber2_ES(F18)
        F18.reset() # it is necessary to reset the problem after each independent run
    _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    F19, _logger = create_problem(19)
    for run in range(20): 
        print("F19")
        studentnumber1_studentnumber2_ES(F19)
        F19.reset()
    _logger.close()


