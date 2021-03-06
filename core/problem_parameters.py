# -*- coding: utf-8 -*-


import sys

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

from core.variable import *
from core.constant import *

import core.JMetalpy.composite_problem as cproblem
import jmetal.core.solution as jsol

from core.evaluators.Python import PythonFunctionEvaluator
from core.evaluators.Matlab import MatlabFunctionEvaluator

import util.type_check as TC
import util.arg_parsing as AP




class ProblemParameters:
    
    class PROBLEM_TEMPLATES(Enum):
        GENERIC="Generic"
        PYTHON="Python"
        CST="CST"
        MATLAB="Matlab"
        
    class OPTIMIZATION_TYPE(Enum):
        MINIMIZE="Minimize"
        MAXIMIZE="Maximize"
    
    def __init__(self):
        self.options = defaultdict(lambda: "")
        self.variables = []
        self.constants = []
        self.defined_symbols = {}
        self.constraints = []
    
        """ Defaults """
        self.options["objectives"] = "1"
        self.options["constraints"] = "0"
    
    def add_variable( self, var: Variable ):
        
        if var.keyword in self.defined_symbols:
            raise ValueError("%s.add_variable(): symbol %s already defined" % (type(self).__name__, var.keyword))
            
        else:
            self.variables.append( var )
            self.defined_symbols[var.keyword] = var
    
    
    def add_constant( self, const: Constant ):
        
        if const.keyword in self.defined_symbols:
            raise ValueError("%s.add_variable(): symbol %s already defined" % (type(self).__name__, const.keyword))
            
        else:
            self.constants.append( const )
            self.defined_symbols[const.keyword] = const
    

    def remove_symbol( self, symbol: str ):
        
        if symbol not in self.defined_symbols:
            raise ValueError("%s.remove_symbol(): symbol %s not defined" % (type(self).__name__, symbol))
            
        else:
            element = self.defined_symbols.pop(symbol)
            
            if isinstance(element, Variable):
                self.variables.remove(element)
            else:
                self.constants.remove(element)

    
    def clear_all_variables(self):
        
        for var in self.variables:
            self.defined_symbols.pop( var.keyword )
            
        self.variables = []
        
        
        
    def clear_all_constants(self):
        
        for const in self.constants:
            self.defined_symbols.pop( const.keyword )
            
        self.constants = []



    def is_symbol_defined( self, symbol: str ):
        return symbol in self.defined_symbols
    
    
    def CompileProblem(self):
        
        """ Problem type selection """
        if self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.GENERIC.value:
            evaluator_module = imp.load_source(name=Path(self.options["evaluator_path"]).stem, pathname=self.options["evaluator_path"])
            evaluator_class = getattr(evaluator_module, self.options["evaluator_class"])
            
            evaluator = evaluator_class()
            
            
        elif self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.PYTHON.value:
            
            evaluator = PythonFunctionEvaluator( #number_of_variables=int(self.options["variables"]),
                                                 number_of_variables=len(self.variables)+len(self.constants),
                                                 number_of_objectives=int(self.options["objectives"]),
                                                 script_path=self.options["python_script_path"],
                                                 function_name=self.options["function_name"] )
            
            
        elif self.options["template"] == ProblemParameters.PROBLEM_TEMPLATES.MATLAB.value:
            
            evaluator = MatlabFunctionEvaluator( #number_of_variables=int(self.options["variables"]),
                                                 number_of_variables=len(self.variables)+len(self.constants),
                                                 number_of_objectives=int(self.options["objectives"]),
                                                 script_path=self.options["matlab_script_path"] )
        
        composite_problem = cproblem.CompositeProblem( evaluator=evaluator,
                                                       problem_parameters=self)
        
        return composite_problem
        
    
    def save_state(self,
                   dir_path: str,
                   file_name: str = "problem_parameters.yaml"):
        
        # Unfinished method
        raise Exception("save_state(): TODO")
        
        if TC.is_dir( dir_path ):
            
            var_dict = { FloatVariable : "float",
                         IntegerVariable : "integer",
                         DiscretizedFloatVariable : "discretized",
                         BinaryVariable : "binary",
                         PermutationVariable : "permutation",
                         }
            
            const_dict = { FloatConstant : "float",
                           IntegerConstant : "integer",
                           BinaryConstant : "binary",
                           PermutationConstant : "permutation",
                           StringConstant : "string"}
            
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
    
        # Unfinished method
        raise Exception("load_state(): TODO")
        
        if TC.is_file( os.path.join(dir_path, file_name) ):
            
            yaml_file = open( os.path.join(dir_path, file_name), 'r')
            yaml_content = yaml.safe_load(yaml_file)
            
            for key, option in yaml_content["options"].items():
                self.options[key] = option
                
            """ Variables """
            self.variables = []
                
            for key, var_data in yaml_content["variables"].items():
                
                if var_data["type"] == "float":
                    self.variables.append( FloatVariable(keyword=key,
                                                                   name=var_data["name"],
                                                                   lower_bound=var_data["lower_bound"],
                                                                   upper_bound=var_data["upper_bound"]) )
                    
                elif var_data["type"] == "integer":
                    self.variables.append( IntegerVariable(keyword=key,
                                                                     name=var_data["name"],
                                                                     lower_bound=var_data["lower_bound"],
                                                                     upper_bound=var_data["upper_bound"]) )
                    
                elif var_data["type"] == "discretized":
                    self.variables.append( DiscretizedFloatVariable(keyword=key,
                                                                                 name=var_data["name"],
                                                                                 lower_bound=var_data["lower_bound"],
                                                                                 upper_bound=var_data["upper_bound"],
                                                                                 step=var_data["step"]) )
                
                elif var_data["type"] == "binary":
                    self.variables.append( BinaryVariable(keyword=key,
                                                                    name=var_data["name"]) )
                    
                elif var_data["type"] == "permutation":
                    self.variables.append( BinaryVariable(keyword=key,
                                                                    name=var_data["name"],
                                                                    elements=var_data["elements"]) )
            """ Constants """
            self.constants = []
                    
            for key, const_data in yaml_content["constants"].items():
                
                if const_data["type"] == "float":
                    self.constants.append( FloatConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "integer":
                    self.constants.append( IntegeConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "binary":
                    self.constants.append( BinaryConstant(keyword=key, value=const_data["value"]) )
                
                elif const_data["type"] == "permutation":
                    self.constants.append( PermutationConstant(keyword=key, value=const_data["value"]) )
                    
                elif const_data["type"] == "string":
                    self.constants.append( StringConstant(keyword=key, value=const_data["value"]) )
            
        
        else:
            raise ValueError("File '%s' is not a valid file" % (os.path.join(dir_path, file_name)))