# -*- coding: utf-8 -*-


import inspect
import imp
import sys
import matlab.engine

from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List
from pathlib import Path

from core.evaluator import Evaluator
from core.matlab.matlab_function import MatlabFunction



class MatlabFunctionEvaluator(Evaluator):
    
    def __init__( self,
                  number_of_variables: int,
                  number_of_objectives: int,
                  script_path: str ):
        
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.script_path = script_path
        
        self.engine = matlab.engine.start_matlab()
        self.function = MatlabFunction( script_path=script_path, nargin=number_of_variables, nargout=number_of_objectives, mat_engine=self.engine )
    
    
    def evaluate( self, *args, **kwargs ):
        
        objectives = self.function.call( *args )
        
        try:
            iterator = iter(objectives)
        except:
            objectives = [objectives]
        
        if len(objectives) != self.number_of_objectives:
            raise ValueError("Function '%s' returned an inappropiate number of values: expected %d, received %d" % (function_name, self.number_of_objectives, len(objectives)))
        
        if isinstance( objectives, tuple ):
            objectives = list( objectives )
        
        return objectives


