"""
Requirements
- Implement a genetic algorithm solving the F18 and F19 problems
- Implement an evolution strategy solving the F18 and F19 problems
- Submit at least two files 'studentnumber1_studentnumber2_GA.py' and 'studentnumber1_studentnumber2_ES.py'.
- Additional files of other functions are allowed. Please make sure we can get results by running 'python *_GA.py' and 'python *_ES.py' without additional arguments.
- Submit a report introducing your algorithms and presenting the experimental results. 
"""

"""
Task 1: Genetic Algorithm
Some hints:
- Which variators (i.e., mutation and crossover) and selection operators will you use?
- What's your suggestion for the parameter settings (e.g., population size, mutation rate, etc.)?
"""

import random
import shutil
from typing import List
import ioh 
from ioh import problem
from ioh import get_problem, ProblemClass

# F18: Low Autocorrelation Binary Sequence (LABS)
f18 = get_problem("LABS", 1, 30, ProblemClass.PBO)
print(f18)
print(f18.meta_data)
print(f18.bounds)
print(f18.state)

# F19-F21: The Ising Model
f19 = get_problem("IsingRing", 1, 100, ProblemClass.PBO)
f20 = get_problem("IsingTorus", 1, 100, ProblemClass.PBO)
f21 = get_problem("IsingTriangular", 1, 100, ProblemClass.PBO)

# help(problem)