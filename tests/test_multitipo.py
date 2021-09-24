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
from core.engine import OptimizationEngine

from evaluators.DebEtAl import Test3Evaluator

from interface.popups.algorithm_parameters_popup import algorithm_parameters_popup


# variables_float = [FloatVariable( keyword='x', lower_bound=0.0, upper_bound=1.0 )]
# variables_int = [IntegerVariable( keyword='t', lower_bound=0, upper_bound=1000 )]
# variables_int = []
# variables_discretized = [DiscretizedFloatVariable( keyword='z', lower_bound=0.0, upper_bound=1.0, step=0.1 ), DiscretizedFloatVariable( keyword='t', lower_bound=0.0, upper_bound=1.0, step=0.1 )]
# constants = [ FloatConstant( keyword='y', value=0.5 ) ]

# problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=EvaluatorPrueba(), constants=constants )
# problem = CompositeProblem( float_vars=variables_float, discretized_vars=variables_discretized, int_vars=variables_int, evaluator=Test3Evaluator(4), constants=constants )

""" Alg. configuration """

class App(tk.Tk):
    
    def __init__(self, algorithm_parameters: AlgorithmParameters, problem_parameters: ProblemParameters):
        super( App, self ).__init__()
        

        self.geometry("100x100")
        button1=tk.Button(self, text="Algoritmo", command=lambda: algorithm_parameters_popup( self, algorithm_parameters, problem_parameters ))
        button1.place(x=0, y=0)
        

algorithm_parameters = AlgorithmParameters()
problem_parameters = ProblemParameters()

problem_parameters.variables = [FloatVariable( keyword='x', lower_bound=0.0, upper_bound=1.0 ),
                                FloatVariable( keyword='y', lower_bound=0.0, upper_bound=1.0 ),
                                DiscretizedFloatVariable( keyword='z', lower_bound=0.0, upper_bound=1.0, step=0.1 ),
                                DiscretizedFloatVariable( keyword='t', lower_bound=0.0, upper_bound=1.0, step=0.1 )]

# problem_parameters.constants = [ FloatConstant( keyword='y', value=0.5 ) ]

problem_parameters.options["template"] = ProblemParameters.PROBLEM_TEMPLATES.UNIVERSAL
problem_parameters.options["evaluator_path"] = r"C:\Users\Álvaro\Documents\GitHub\JOptimizer\tests\evaluator_4var.py"
problem_parameters.options["evaluator_classname"] = "EvaluatorPrueba"

app = App(algorithm_parameters, problem_parameters)
app.mainloop()

problem = problem_parameters.CompileProblem()
algorithm = algorithm_parameters.compile_algorithm( problem )

engine = OptimizationEngine( problem=problem )

engine.configure( algorithm=algorithm )
engine.launch( termination_criterion=jterm.StoppingByEvaluations( max_evaluations=10000 ) )
engine.wait_termination()

print("Time: {}".format(engine.algorithm.total_computing_time) )

solutions = engine.algorithm.get_result()

front = get_non_dominated_solutions(solutions)

plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y'])
plot_front.plot(front, label='NSGAII-%s' % problem.get_name())

        










