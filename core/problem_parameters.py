# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 17:53:21 2021

@author: Wayky
"""

import sys
sys.path.append(r"./..")

import copy
import random
import math
# import importlib
# from pydoc import locate
import imp
from pathlib import Path

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict

import core.variable as Variables
import core.composite_problem as cproblem

class ProblemParameters:
    
    class PROBLEM_TEMPLATES(Enum):
        UNIVERSAL="universal"
        # CST="CST"
        # MATLAB="matlab"
    
    def __init__(self):
        self.options = defaultdict(lambda: "")
        self.variables = []
        self.constants = []
        self.constraints = []
    
    def CompileProblem(self):
        
        float_vars = []
        int_vars = []
        disc_vars = []
        binary_vars = []
        permutation_vars = []
        
        
        """ Variable categorization """
        for v in self.variables:
            
            if isinstance(v, Variables.FloatVariable):
                float_vars.append( v )
                
            elif isinstance(v, Variables.IntegerVariable):
                int_vars.append( v )
                
            elif isinstance(v, Variables.DiscretizedFloatVariable):
                disc_vars.append( v )
                
            elif isinstance(v, Variables.BinaryVariable):
                binary_vars.append( v )
                
            elif isinstance(v, Variables.PermutationVariable):
                permutation_vars.append( v )
        
        """ Problem type selection """
        if self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.UNIVERSAL:
            # module_evaluator = locate('{package}.{ev_class}'.format(package=self.options["evaluator_path"], ev_class=self.options["evaluator_classname"]))
            evaluator_module = imp.load_source(name=Path(self.options["evaluator_path"]).stem, pathname=self.options["evaluator_path"])
            evaluator_class = getattr(evaluator_module, self.options["evaluator_classname"])
            
            evaluator = evaluator_class()
        
        composite_problem = cproblem.CompositeProblem( evaluator=evaluator,
                                                       float_vars=float_vars,
                                                       int_vars=int_vars,
                                                       discretized_vars=disc_vars,
                                                       binary_vars=binary_vars,
                                                       permutation_vars=permutation_vars,
                                                       constants=self.constants)
        
        return composite_problem
        