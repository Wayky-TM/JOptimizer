# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 21:13:55 2021

@author: Wayky
"""

import sys
sys.path.append(r"../.")

import copy
import random
import math
import time

from enum import Enum
from abc import *
import cProfile

import tkinter as tk

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import jmetal.operator.crossover as jcross
import jmetal.operator.mutation as jmut
import jmetal.algorithm.multiobjective as jalg
import jmetal.util.termination_criterion as jterm

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from core.evaluator import Evaluator
from core.variable import FloatVariable, IntegerVariable, DiscretizedFloatVariable
from core.constant import FloatConstant, IntegerConstant
# from core.composite_problem import CompositeProblem
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters

from evaluators.DebEtAl import Test3Evaluator

from interface.popups.algorithm_parameters_popup import algorithm_parameters_popup


class EvaluatorPrueba(Evaluator):
    
    def __init__(self):
        super( EvaluatorPrueba, self ).__init__()
        self.number_of_variables = 4
        self.number_of_objectives = 2
    
    def evaluate(self, x, y, z, t):
        f1 = x
        g = 1.0 + 9.0*(y+z+float(t)/1000.0)/3.0
        h = 1 - math.sqrt(f1/g)
        return [x, g*h]
    



# variables_float = [FloatVariable( keyword='x', lower_bound=0.0, upper_bound=1.0 )]
# variables_int = [IntegerVariable( keyword='t', lower_bound=0, upper_bound=1000 )]
# variables_int = []
# variables_discretized = [DiscretizedFloatVariable( keyword='z', lower_bound=0.0, upper_bound=1.0, step=0.1 ), DiscretizedFloatVariable( keyword='t', lower_bound=0.0, upper_bound=1.0, step=0.1 )]
# constants = [ FloatConstant( keyword='y', value=0.5 ) ]

# problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=EvaluatorPrueba(), constants=constants )
# problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=Test3Evaluator(4), constants=constants )

""" Alg. configuration """

frame_widget = tk.Tk()

algorithm_parameters = AlgorithmParameters()
problem_parameters = ProblemParameters()

problem_parameters.variables = [FloatVariable( keyword='x', lower_bound=0.0, upper_bound=1.0 ),
                                DiscretizedFloatVariable( keyword='z', lower_bound=0.0, upper_bound=1.0, step=0.1 ),
                                DiscretizedFloatVariable( keyword='t', lower_bound=0.0, upper_bound=1.0, step=0.05 )]

problem_parameters.constants = [ FloatConstant( keyword='y', value=0.5 ) ]

problem_parameters.options["template"] = ProblemParameters.PROBLEM_TEMPLATES.UNIVERSAL
problem_parameters.options["evaluator_path"] = "test_multitipo"
problem_parameters.options["evaluator_classname"] = "EvaluatorPrueba"
problem = problem_parameters.CompileProblem()

algorithm_parameters_popup( frame_widget, algorithm_parameters, problem_parameters )

# algorithm_parameters.choice = AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII
# algorithm_parameters.general_parameters["population_size"] = "100"
# algorithm_parameters.general_parameters["offspring_size"] = "100"

# algorithm_parameters.float_crossover_choice = AlgorithmParameters.FLOAT_CROSSOVER.SBX
# algorithm_parameters.float_crossover_parameters["probability"] = "0.9"
# algorithm_parameters.float_crossover_parameters["distribution_index"] = "20.0"
# algorithm_parameters.float_mutation_choice = AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL
# algorithm_parameters.float_mutation_parameters["probability"] = "0.1"
# algorithm_parameters.float_mutation_parameters["distribution_index"] = "20.0"

# algorithm_parameters.int_crossover_choice = AlgorithmParameters.INT_CROSSOVER.INT_SBX
# algorithm_parameters.int_crossover_parameters["probability"] = "0.9"
# algorithm_parameters.int_crossover_parameters["distribution_index"] = "20.0"
# algorithm_parameters.int_mutation_choice = AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL
# algorithm_parameters.int_mutation_parameters["probability"] = "0.1"
# algorithm_parameters.int_mutation_parameters["distribution_index"] = "20.0"

# algorithm_parameters.selection_choice = AlgorithmParameters.SELECTION.BINARY_TOURNAMENT

algorithm = algorithm_parameters.compile_algorithm( problem )




algorithm.solutions = algorithm.create_initial_solutions()
algorithm.solutions = algorithm.evaluate(algorithm.solutions)


def run():
    # nonlocal algorithm
    
    algorithm.init_progress()
    
    time1 = time.time()
    
    for i in range(1000):
        algorithm.step()
        algorithm.update_progress()
        
    total_time = time.time() - time1
    
    print(total_time)

cProfile.run( 'run()' )

# run()

solutions = algorithm.get_result()

front = get_non_dominated_solutions(solutions)

plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y'])
plot_front.plot(front, label='NSGAII-%s' % problem.get_name())

# class AlgorithmCompiler:
        
        
#     class NullCrossover(Crossover):
        
#         def execute( self, empty_solution: List ):
#             return empty_solution[0]
        
#     class NullMutation(Mutation)
        
#         def execute( self, empty_solution ):
#             return empty_solution
        
    
#     def __init__( self,
#                   float_vars : List[FloatVariable] = [],
#                   int_vars : List[IntegerVariable] = [],
#                   discretized_vars : List[DiscretizedFloatVariable] = [],
#                   evaluator: Evaluator,
                  
#                   ):
        
        
#     def Compile():
#         pass
        
        










