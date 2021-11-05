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
import yaml
import os

import imp
from pathlib import Path

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict

import core.variable as Variables
import core.constant as Constants
import core.composite_problem as cproblem

import util.type_check as TC



class ProblemParameters:
    
    class PROBLEM_TEMPLATES(Enum):
        GENERIC="Generic"
        PYTHON="Python"
        CST="CST"
        MATLAB="Matlab"
    
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
        if self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.GENERIC.value:
            # module_evaluator = locate('{package}.{ev_class}'.format(package=self.options["evaluator_path"], ev_class=self.options["evaluator_classname"]))
            evaluator_module = imp.load_source(name=Path(self.options["evaluator_path"]).stem, pathname=self.options["evaluator_path"])
            evaluator_class = getattr(evaluator_module, self.options["evaluator_class"])
            
            evaluator = evaluator_class()
            
        elif self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.PYTHON.value:
            pass
        
        composite_problem = cproblem.CompositeProblem( evaluator=evaluator,
                                                       float_vars=float_vars,
                                                       int_vars=int_vars,
                                                       discretized_vars=disc_vars,
                                                       binary_vars=binary_vars,
                                                       permutation_vars=permutation_vars,
                                                       constants=self.constants)
        
        return composite_problem
        
    
    def save_state(self,
                   dir_path: str,
                   file_name: str = "problem_parameters.yaml"):
        
        if TC.is_dir( dir_path ):
            
            var_dict = { Variables.FloatVariable : "float",
                         Variables.IntegerVariable : "integer",
                         Variables.DiscretizedFloatVariable : "discretized",
                         Variables.BinaryVariable : "binary",
                         Variables.PermutationVariable : "permutation"}
            
            const_dict = { Constants.FloatConstant : "float",
                           Constants.IntegerConstant : "integer",
                           Constants.BinaryConstant : "binary",
                           Constants.PermutationConstant : "permutation",
                           Constants.StringConstant : "string"}
            
            output = {}
            output["options"] = {}
            
            """ Options """
            for key, value in self.options.items():
                output["options"][key] = value
            
            
            """ Variables """
            output["variables"] = {}
            
            for var in self.variables:
                var_data = {}
                
                var_data["name"] = var.name
                var_data["type"] = var_dict[type(var)]
                
                if var_data["type"] == "float":
                    var_data["lower_bound"] = var.lower_bound
                    var_data["upper_bound"] = var.upper_bound
                    
                elif var_data["type"] == "integer":
                    var_data["lower_bound"] = var.lower_bound
                    var_data["upper_bound"] = var.upper_bound
                    
                elif var_data["type"] == "discretized":
                    var_data["lower_bound"] = var.lower_bound
                    var_data["upper_bound"] = var.upper_bound
                    var_data["step"] = var.step
                    
                elif var_data["type"] == "permutation":
                    var_data["elements"] = var.elements
                
                output["variables"][var.keyword] = var_data
            
            """ Constants """    
            output["constants"] = {}
            
            for const in self.constants:
                const_data = {}
                
                const_data["name"] = const.name
                const_data["type"] = const_dict[type(const)]
                const_data["value"] = const.value
                
                output["constants"][const.keyword] = const_data
            
            with open( os.path.join(dir_path, file_name), 'w') as file:
                documents = yaml.dump(output, file)
        
        else:
            raise ValueError("Path '%s' is not a valid directory" % (dir_path))
            
    def load_state(self,
                   dir_path: str,
                   file_name: str = "problem_parameters.yaml"):
    
        
        if TC.is_file( os.path.join(dir_path, file_name) ):
            
            yaml_file = open( os.path.join(dir_path, file_name), 'r')
            yaml_content = yaml.safe_load(yaml_file)
            
            for key, option in yaml_content["options"].items():
                self.options[key] = option
                
            """ Variables """
            self.variables = []
                
            for key, var_data in yaml_content["variables"].items():
                
                if var_data["type"] == "float":
                    self.variables.append( Variables.FloatVariable(keyword=key,
                                                                   name=var_data["name"],
                                                                   lower_bound=var_data["lower_bound"],
                                                                   upper_bound=var_data["upper_bound"]) )
                    
                elif var_data["type"] == "integer":
                    self.variables.append( Variables.IntegerVariable(keyword=key,
                                                                     name=var_data["name"],
                                                                     lower_bound=var_data["lower_bound"],
                                                                     upper_bound=var_data["upper_bound"]) )
                    
                elif var_data["type"] == "discretized":
                    self.variables.append( Variables.DiscretizedFloatVariable(keyword=key,
                                                                                 name=var_data["name"],
                                                                                 lower_bound=var_data["lower_bound"],
                                                                                 upper_bound=var_data["upper_bound"],
                                                                                 step=var_data["step"]) )
                
                elif var_data["type"] == "binary":
                    self.variables.append( Variables.BinaryVariable(keyword=key,
                                                                    name=var_data["name"]) )
                    
                elif var_data["type"] == "permutation":
                    self.variables.append( Variables.BinaryVariable(keyword=key,
                                                                    name=var_data["name"],
                                                                    elements=var_data["elements"]) )
            """ Constants """
            self.constants = []
                    
            for key, const_data in yaml_content["constants"].items():
                
                if const_data["type"] == "float":
                    self.constants.append( Constants.FloatConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "integer":
                    self.constants.append( Constants.IntegeConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "binary":
                    self.constants.append( Constants.BinaryConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "permutation":
                    self.constants.append( Constants.PermutationConstant(keyword=key, value=const_data["value"]) )
                    
                elif const_data["type"] == "string":
                    self.constants.append( Constants.StringConstant(keyword=key, value=const_data["value"]) )
            
        
        else:
            raise ValueError("File '%s' is not a valid file" % (os.path.join(dir_path, file_name)))