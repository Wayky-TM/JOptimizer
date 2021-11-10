
import sys
sys.path.append(r"./..")

import copy
import random
import math

from enum import Enum
from abc import *
from typing import List

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import jmetal.operator.crossover as Crossover
import jmetal.operator.mutation as Mutation
import core.JMetalpy.composite_solution as CS

from core.variable import *
from core.constant import *
                  
from core.problem_parameters import ProblemParameters
from core.constant import FloatConstant, IntegerConstant
from core.evaluator import Evaluator
from core.null import NullSolution

# class ARGS_TYPES(Enum):
#     VARIABLE=0
#     CONSTANT=1
    
class ARGS_MODES(Enum):
    NORMAL=0
    KEYWORD=1
    UNPACKED=2



class CompositeProblem(jprob.Problem[jsol.CompositeSolution], ABC):
        
    def __init__(self,
                 evaluator: Evaluator,
                 problem_parameters: ProblemParameters):
        
        if len(problem_parameters.variables) < 1:
            raise ValueError( "%s.__init__(): at least one variable needed" % (type(self).__name__) )
            
        self.problem_parameters = problem_parameters
        self.evaluator = evaluator
        self.number_of_objectives = evaluator.number_of_objectives
        
        self.variables = { var.keyword:var for var in self.problem_parameters.variables }
        self.constants = { const.keyword:const for const in self.problem_parameters.constants }
        
        self.float_count = 0
        self.integer_count = 0
        self.binary_count = 0
        self.permutation_solution_count = 0
        
        self.float_lower_bounds = []
        self.float_upper_bounds = []
        
        self.integer_lower_bounds = []
        self.integer_upper_bounds = []
        
        self.permutations = []
        
        var_args = self._compile_call_arguments()
        
        self.included_variables_dict = {}
        self.argument_list = []
        
        for argument in var_args:
            
            if argument[0] in self.variables:
                """ Format: (Var, index, Mode [, keyword]) """
                
                var = self.variables[argument[0]]
                
                if not var in self.included_variables_dict:
                
                    if type(var) == FloatVectorVariable:
                        index = (self.float_count,self.float_count+var.length)
                        self.float_count += var.length
                        self.float_lower_bounds.extend(var.lower_bound)
                        self.float_upper_bounds.extend(var.upper_bound)
                        
                    elif type(var) == FloatVariable:
                        index = (self.float_count,self.float_count+1)
                        self.float_count += 1
                        self.float_lower_bounds.append(var.lower_bound)
                        self.float_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == IntegerVectorVariable:
                        index = (self.integer_count, self.integer_count+var.length)
                        self.integer_count += var.length
                        self.integer_lower_bounds.extend(var.lower_bound)
                        self.integer_upper_bounds.extend(var.upper_bound)
                        
                    elif type(var) == DiscretizedVectorVariable:
                        index = (self.integer_count, self.integer_count+var.length)
                        self.integer_count += var.length
                        self.integer_lower_bounds.extend( [0]*var.length )
                        self.integer_upper_bounds.extend( var.resolution )
                        
                    elif type(var) == IntegerVariable:
                        index = (self.integer_count,self.integer_count+1)
                        self.integer_count += 1
                        self.integer_lower_bounds.append(var.lower_bound)
                        self.integer_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == DiscretizedVariable:
                        index = (self.integer_count,self.integer_count+1)
                        self.integer_count += 1
                        self.integer_lower_bounds.append(0)
                        self.integer_upper_bounds.append(var.resolution)
                        
                    elif type(var) == BinaryVariable:
                        index = (self.binary_count,self.binary_count+1)
                        self.binary_count += 1
                        
                    elif type(var) == PermutationVariable:
                        index = self.permutation_solution_count
                        self.permutation_solution_count += 1
                        self.permutations.append( var.elements )
                    
                    self.included_variables_dict[var] = index
                    
                else:
                    index = self.included_variables_dict[var]
                    
                if argument[1] == ARGS_MODES.KEYWORD:
                    self.argument_list.append( (var, index, argument[1], argument[2]) )
                
                else:
                    self.argument_list.append( (var, index, argument[1]) )
                    
            
            elif argument[0] in self.constants:
                """ Format: (Var, Mode [, keyword]) """
                if argument[1] == ARGS_MODES.KEYWORD:
                    self.argument_list.append( (self.variables[argument[0]], argument[1], argument[2]) )
                    
                else:
                    self.argument_list.append( (self.variables[argument[0]], argument[1]) )
                
            
            else:
                raise Exception("CompositeProblem.__init__(): wrong argument '%'" % (argument[0]))
        
        
        self.solution_shape = ( self.float_count, self.integer_count, self.binary_count, self.permutation_index )
        
        
        if (len(self.problem_parameters.variables) + len(self.problem_parameters.constants)) != evaluator.number_of_variables:
            raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
        
        self.evaluations = 0
        
        

    def _generate_args( self, solution: CS.CompositeSolution ):
        
        args = []
        kwargs = {}
        
        for arg in self.argument_list:
            
            if isinstance(arg[0], Constant):
                
                if arg[1] == ARGS_MODES.NORMAL:
                    args.append( arg[0].value )
                
                elif arg[1] == ARGS_MODES.KEYWORD:
                    kwargs[arg[-1]] = arg[0].value
                    
                elif arg[1] == ARGS_MODES.UNPACKED:
                    args.extend( arg[0].value )
                    
                else:
                    raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                    
            elif isinstance(arg[0], Variable):
                
                if type(arg[0]) == FloatVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == IntegerVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == FloatVectorVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == IntegerVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == BinaryVariable:
                    value = solution.binary_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == PermutationVariable:
                    value = solution.permutation_solutions[arg[1][0]].variables
                    
                    
                if arg[1] == ARGS_MODES.NORMAL:
                    args.append( value )
                
                elif arg[1] == ARGS_MODES.KEYWORD:
                    kwargs[arg[-1]] = value
                    
                elif arg[1] == ARGS_MODES.UNPACKED:
                    args.extend( value )
                    
                else:
                    raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                
            else:
                raise ValueError("_generate_args(): invalid symbol type: %s" % (type(arg[0])))
                
                
                
        return args, kwargs

    def _compile_call_arguments(self):
        
        arg_string = su.remove_whitespaces( self.problem_parameters.options["call_args"] )
        arg_tokens = arg_string.split(',')
        
        arg_list = []
        
        for token in arg_tokens:
            
            ret = AP.token_is_kwarg(token)    
            
            if ret != None:
                arg_list.append( (ret[1],ARGS_MODES.KEYWORD,ret[0]) )
                
            else:
                ret = token_is_unpacked_arg(token)
                
                if ret!=None:
                    arg_list.add( (ret,ARGS_MODES.UNPACKED) )
                        
                else:
                    if token_is_arg(token):
                        arg_list.add( (token,ARGS_MODES.NORMAL) )

        return arg_list
    

    def create_solution(self) -> jsol.CompositeSolution:
        
        kwargs = {}
        
        if self.solution_shape[0] > 0: # Floats
            temp_solution = jsol.FloatSolution(lower_bound=self.float_lower_bounds, upper_bound=self.float_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ random.uniform(a, b) for lower, upper in zip(self.float_lower_bounds, self.float_upper_bounds) ]
            kwargs["float_solutions"] = [temp_solution]
        
        if self.solution_shape[1] > 0: # Integers
            temp_solution = jsol.IntegerSolution(lower_bound=self.integer_lower_bounds, upper_bound=self.integer_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ random.uniform(a, b) for lower, upper in zip(self.integer_lower_bounds, self.integer_upper_bounds) ]
            kwargs["integer_solutions"] = [temp_solution]
            
        if self.solution_shape[2] > 0: # Binary
            temp_solution = jsol.BinarySolution(number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ bool(random.getrandbits(1)) for i in range(self.solution_shape[2]) ]
            kwargs["binary_solutions"] = [temp_solution]
            
        if self.solution_shape[3] > 0: # Permutation
        
            permutation_solutions = []
        
            for permutation in self.permutations:
                temp_solution = jsol.PermutationSolution(number_of_objectives=self.number_of_objectives, number_of_constraints=0 )    
                temp_solution.variables = random.shuffle( permutation )
                permutation_solutions.append( temp_solution )
                
            
            kwargs["permutation_solutions"] = permutation_solutions
        
        return CS.CompositeSolution( **kwargs )
    
    
    
    def evaluate( self, solution: jsol.CompositeSolution):
        
        args, kwargs = _generate_args(solution)
        solution.objectives = self.evaluator.evaluate( *args, **kwargs )
        self.evaluations += 1
        
        return solution
    
    def recover_variables( self, solution: jsol.CompositeSolution ):
        
        variables_list = []
        variables_dictionary = {}
        
        for arg in self.argument_list:
                    
            if isinstance(arg[0], Variable):
                
                if type(arg[0]) == FloatVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == IntegerVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == FloatVectorVariable:
                    value = solution.float_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == IntegerVectorVariable:
                    value = solution.integer_solutions[0].variables[arg[1][0]:arg[1][1]]
                
                elif type(arg[0]) == BinaryVariable:
                    value = solution.binary_solutions[0].variables[arg[1][0]]
                
                elif type(arg[0]) == PermutationVariable:
                    value = solution.permutation_solutions[arg[1][0]]
                    
                else:
                    raise ValueError("_generate_args(): invalid arg type: %s" % (arg[1]))
                    
                var = ( arg[0], value )
                variables_list.append( var )
                variables_dictionary[arg[0].keyword] = var
                
            else:
                raise ValueError("_generate_args(): invalid symbol type: %s" % (type(arg[0])))
                
        
        return variables_dictionary, variables_list
    
    def get_name(self):
        return "CompositeProblem"
        