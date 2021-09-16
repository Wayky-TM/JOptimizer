# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 18:48:33 2021

@author: Wayky
"""

import os
from abc import ABC, abstractmethod
import copy
from typing import List


from jmetal.core.problem import FloatProblem, Problem
from jmetal.core.solution import FloatSolution, CompositeSolution

from .matlab_function import MatlabFunction

""" TODO list """

# 1. Enable constraints
# 2. Multiple scripts support
# 3. Complete error checking (path, nargs, etc)

class MatlabFloat( FloatProblem, ABC ):
    
    def __init__( self, script_path: str,
                        number_of_variables: int,
                        nargout: int,
                        lower_bounds: List[float] = [],
                        upper_bounds: List[float] = [],
                        args_as_vector: bool = False
                        ):
        
        if not os.path.isfile( script_path ):
            raise ValueError("There isn't a Matlab script with that filename:%s" % script_path)
        
        _, extension = os.path.splitext(script_path)
        
        if extension != ".m":
            raise ValueError("File %s isn't a Matlab script (.m)" % script_path)
        
        
        if number_of_variables < 1:
            raise ValueError("Incorrect number of variables")
        
        
        if nargout < 1:
            raise ValueError("Incorrect number of output args")    
        
        if len(lower_bounds)+len(lower_bounds)==0:
            self.lower_bound = [ 0.0 for _ in range(number_of_variables)]
            self.upper_bound = [ 1.0 for _ in range(number_of_variables)]
            
        elif len(lower_bound)==number_of_variables and len(upper_bound)==number_of_variables:
            self.lower_bound = copy.deepcopy( lower_bounds )
            self.upper_bound = copy.deepcopy( upper_bounds )
        else:
            raise ValueError("Bound vectors of incorrect size")    
        
            
        self.number_of_variables = number_of_variables
        self.script_path = script_path
        self.nargout = nargout
        self.args_as_vector = args_as_vector
        
        self.function = MatlabFunction( script_path=self.script_path, nargin=self.number_of_variables, nargout=self.nargout )
        self.number_of_objectives = self.nargout
        self.number_of_constraints = 0
        
    def evaluate( self, solution: FloatSolution ):
        
        if self.args_as_vector:
            objectives = self.function.call( solution.variables )
        else:
            objectives = self.function.call( *solution.variables )
        
        for i in range(len(objectives)):
            solution.objectives[i] = objectives[i]
        
        return solution
    
    def get_name(self) -> str:
        return ("Matlab Script: %s" % self.script_path)
        
        
    
    
        

    