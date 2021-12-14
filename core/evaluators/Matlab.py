# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 18:31:25 2021

@author: Wayky
"""


import inspect
import imp
import sys
# sys.path.append(r"./..")

from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List
from pathlib import Path

from core.evaluator import Evaluator
from matlab.matlab_function import MatlabFunction



class MatlabFunctionEvaluator(Evaluator):
    
    def __init__( self,
                  number_of_variables: int,
                  number_of_objectives: int,
                  script_path: str,
                  function_name: str ):
        
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.script_path = script_path
        
        self.function = MatlabFunction( script_path=script_path, nargin=number_of_variables, nargout=number_of_objectives )
    
    
    def evaluate( self, *args, **kwargs ):
        
        objectives = self.function.call( *args )
        
        try:
            iterator = iter(objectives)
        except:
            objectives = [objectives]
        
        if len(objectives) != self.number_of_objectives:
            raise ValueError("Function '%s' returned an inappropiate number of values: expected %d, received %d" % (function_name, self.number_of_objectives, len(objectives)))
        
        return objectives


