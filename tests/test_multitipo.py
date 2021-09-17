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

from enum import Enum
from abc import *

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
from core.composite_problem import CompositeProblem

from evaluators.DebEtAl import Test3Evaluator


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
    



variables_float = [FloatVariable( keyword='x', lower_bound=0.0, upper_bound=1.0 )]
# variables_int = [IntegerVariable( keyword='t', lower_bound=0, upper_bound=1000 )]
variables_int = []
variables_discretized = [DiscretizedFloatVariable( keyword='z', lower_bound=0.0, upper_bound=1.0, step=0.1 ), DiscretizedFloatVariable( keyword='t', lower_bound=0.0, upper_bound=1.0, step=0.1 )]
constants = [ FloatConstant( keyword='y', value=0.5 ) ]

# problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=EvaluatorPrueba(), constants=constants )
problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=Test3Evaluator(4), constants=constants )

crossover = jcross.CompositeCrossover( [ jcross.SBXCrossover( probability=0.9 ), jcross.IntegerSBXCrossover( probability=0.9 ), jcross.IntegerSBXCrossover( probability=0.9 ) ] )

mutation = jmut.CompositeMutation( [ jmut.PolynomialMutation( probability=0.1 ), jmut.IntegerPolynomialMutation( probability=0.1 ), jmut.IntegerPolynomialMutation( probability=0.1 )] )

algorithm = jalg.NSGAII(problem, population_size=100, offspring_population_size=100, mutation=mutation, crossover=crossover, termination_criterion=jterm.StoppingByEvaluations(1000))

algorithm.run()

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
        
        










