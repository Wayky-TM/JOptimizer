
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
        
        # self.float_vars = [ var for self.problem_parameters.variables if type(var)==FloatVariable ]
        # self.integer_vars = [ var for self.problem_parameters.variables if type(var)==IntegerVariable ]
        # self.discretized_vars = [ var for self.problem_parameters.variables if type(var)==DiscretizedFloatVariable ]
        # self.binary_vars = [ var for self.problem_parameters.variables if type(var)==BinaryVariable ]
        # self.permutation_vars = [ var for self.problem_parameters.variables if type(var)==PermutationVariable ]
        # self.floatVector_vars = [ var for self.problem_parameters.variables if type(var)==FloatVectorVariable ]
        # self.integerVector_vars = [ var for self.problem_parameters.variables if type(var)==IntegerVectorVariable ]
        # self.discretizedVector_vars = [ var for self.problem_parameters.variables if type(var)==DiscretizedVectorVariable ]
        
        # self.include_float = len(float_vars)>0
        # self.include_int = len(int_vars)>0
        # self.include_discretized = len(discretized_vars)>0
        # self.include_binary = len(binary_vars)>0
        # self.include_permutation = len(permutation_vars)>0
        # self.include_floatVector = len(floatVector_vars)>0
        # self.include_integerVector = len(integerVector_vars)>0
        # self.include_discretizedVector = len(discretizedVector_vars)>0
        
        self.variables = { var.keyword:var for var self.problem_parameters.variables }
        self.constants = { const.keyword:const for const self.problem_parameters.constants }
        
        self.float_index = 0
        self.integer_index = 0
        self.binary_index = 0
        self.permutation_solution_counter = 0
        
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
                        index = (self.float_index,self.float_index+var.length)
                        self.float_index += var.length
                        self.float_lower_bounds.extend(var.lower_bound)
                        self.float_upper_bounds.extend(var.upper_bound)
                        
                    elif type(var) == FloatVariable:
                        index = (self.float_index,self.float_index+1)
                        self.float_index += 1
                        self.float_lower_bounds.append(var.lower_bound)
                        self.float_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == IntegerVectorVariable:
                        index = (self.integer_index, self.integer_index+var.length)
                        self.integer_index += var.length
                        self.integer_lower_bounds.extend(var.lower_bound)
                        self.integer_upper_bounds.extend(var.upper_bound)
                        
                    elif type(var) == DiscretizedVectorVariable:
                        index = (self.integer_index, self.integer_index+var.length)
                        self.integer_index += var.length
                        self.integer_lower_bounds.extend( [0]*var.length )
                        self.integer_upper_bounds.extend( var.resolution )
                        
                    elif type(var) == IntegerVariable:
                        index = (self.integer_index,self.integer_index+1)
                        self.integer_index += 1
                        self.integer_lower_bounds.append(var.lower_bound)
                        self.integer_upper_bounds.append(var.upper_bound)
                        
                    elif type(var) == DiscretizedVariable:
                        index = (self.integer_index,self.integer_index+1)
                        self.integer_index += 1
                        self.integer_lower_bounds.append(0)
                        self.integer_upper_bounds.append(var.resolution)
                        
                    elif type(var) == BinaryVariable:
                        index = (self.binary_index,self.binary_index+1)
                        self.binary_index += 1
                        
                    elif type(var) == PermutationVariable:
                        index = self.permutation_solution_counter
                        self.permutation_solution_counter += 1
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
        
        
        self.solution_shape = ( self.float_index, self.integer_index, self.binary_index, self.permutation_index )
        
        
        if (len(self.problem_parameters.variables) + len(self.problem_parameters.constants)) != evaluator.number_of_variables:
            raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
        
            
        self.evaluations = 0
        
        # self.null_solution = NullSolution( number_of_objectives=self.number_of_objectives )

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
                    
            elif isinstance(arg[0], Variables):
                
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
        
        arg_string = su.remove_whitespaces( self.options["call_args"] )
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
            
        if self.solution_shape[3] > 0: # Binary
        
            permutation_solutions = []
        
            for permutation in self.permutations:
                temp_solution = jsol.PermutationSolution(number_of_objectives=self.number_of_objectives, number_of_constraints=0 )    
                temp_solution.variables = random.shuffle( permutation )
                permutation_solutions.append( temp_solution )
                
            
            kwargs["permutation_solutions"] = permutation_solutions
        
        
        # if self.include_float:
        #     temp_solution = jsol.FloatSolution(lower_bound=self.float_lower_bounds, upper_bound=self.float_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
        #     temp_solution.variables = [ x.rand() for x in self.float_vars ]
        #     solutions[0] = temp_solution
        #     # solutions.append(temp_solution)
        #     # self.float_index = solution_index
        #     # solution_index += 1
            
        # if self.include_int:
        #     temp_solution = jsol.IntegerSolution(lower_bound=self.int_lower_bounds, upper_bound=self.int_upper_bounds, number_of_objectives=self.number_of_objectives )
        #     temp_solution.variables = [ x.rand() for x in self.int_vars ]
        #     solutions[1] = temp_solution
        #     # solutions.append(temp_solution)
        #     # self.int_index = solution_index
        #     # solution_index += 1
            
        # if self.include_discretized:
        #     temp_solution = jsol.IntegerSolution(lower_bound=self.discretized_lower_bounds, upper_bound=self.discretized_upper_bounds, number_of_objectives=self.number_of_objectives )
        #     temp_solution.variables = [ x.randint() for x in self.discretized_vars ]
        #     solutions[2] = temp_solution
        #     # solutions.append(temp_solution)
        #     # self.discretized_index = solution_index
        #     # solution_index += 1
            
        # if self.include_binary:
        #     temp_solution = jsol.BinarySolution(number_of_variables=len(self.binary_vars), number_of_objectives=self.number_of_objectives)
        #     temp_solution.variables = [ x.rand()==1 for x in self.binary_vars ]
        #     solutions[3] = temp_solution
        #     # solutions.append(temp_solution)
        #     # self.binary_index = solution_index
        #     # solution_index += 1
            
        # if self.include_permutation:
            
        #     self.permutation_index = solution_index
        #     solution_index += 1
            
        #     for x in self.permutation_vars:
        #         temp_solution = jsol.PermutationSolution(number_of_variables=len(x.elements), number_of_objectives=self.number_of_objectives)
        #         temp_solution.variables = x.rand()
        #         solutions.append(temp_solution)
        #         solution_index += 1
        
        # if self.include_floatVector:
            
        #     self.floatVector_index = solution_index
        #     solution_index += 1
            
        #     for x in self.floatVector_vars:
        #         temp_solution = jsol.FloatSolution(lower_bound=[ x.lower_bound ]*x.length, upper_bound=[ x.upper_bound ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
        #         temp_solution.variables = x.rand()
        #         solutions.append(temp_solution)
        #         solution_index += 1
        
        # if self.include_integerVector:
            
        #     self.integerVector_index = solution_index
        #     solution_index += 1
            
        #     for x in self.integerVector_vars:
        #         temp_solution = jsol.IntegerSolution(lower_bound=[ x.lower_bound ]*x.length, upper_bound=[ x.upper_bound ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
        #         temp_solution.variables = x.rand()
        #         solutions.append(temp_solution)
        #         solution_index += 1
        
        # if self.include_discretizedVector:
            
        #     self.discretizedVector_index = solution_index
        #     solution_index += 1
            
        #     for x in self.discretizedVector_vars:
        #         temp_solution = jsol.IntegerSolution(lower_bound=[0]*x.length, upper_bound=[ x.resolution ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
        #         temp_solution.variables = x.randint()
        #         solutions.append(temp_solution)
        #         solution_index += 1
        
        return CS.CompositeSolution( **kwargs )
    
    
    
    def evaluate( self, solution: jsol.CompositeSolution):
        
        arguments = {}
        kwargs = {}
        args = []
        
        if self.include_float:
            float_args = { self.float_vars[i].keyword:solution.variables[0].variables[i] for i in range(len(self.float_vars)) }
            arguments.update( float_args )
            
        if self.include_int:
            int_args = { self.int_vars[i].keyword:solution.variables[1].variables[i] for i in range(len(self.int_vars)) }
            arguments.update( int_args )
            
        if self.include_discretized:
            discretized_args = { self.discretized_vars[i].keyword:(float(solution.variables[2].variables[i])*self.discretized_vars[i].step)  for i in range(len(self.discretized_vars)) }
            arguments.update( discretized_args )
        
        if self.include_binary:
            binary_args = { self.binary_vars[i].keyword:solution.variables[3].variables[i] for i in range(len(self.binary_vars)) }
            arguments.update( binary_args )
        
        if self.include_permutation:
            permutation_args = {}
            
            for i in range(len(self.permutation_vars)):
                permutation_args[self.permutation_vars[i].keyword] = solution.variables[4+i].variables
            
            arguments.update( permutation_args )
            
        
        if len(self.constants) > 0:
            const_args = { x.keyword:x.value for x in self.constants }
            arguments.update( const_args )
        
        solution.objectives = self.evaluator.evaluate( *args, **kwargs )
        
        self.evaluations += 1
        
        return solution
    
    def recover_variables( self, solution: jsol.CompositeSolution ):
        
        # variables = copy.deepcopy(solution.variables)
        results = []
        
        if self.include_float:
            float_solutions = copy.deepcopy(solution.variables[0])
            results.extend( [ (self.float_vars[i],float_solutions.variables[i]) for i in range(len(float_solutions.variables)) ] )
            
        if self.include_int:
            int_solutions = copy.deepcopy(solution.variables[1])
            results.extend( [ (self.int_vars[i],int_solutions.variables[i]) for i in range(len(int_solutions.variables)) ] )
            
        if self.include_discretized:
            discretized_solutions = copy.deepcopy(solution.variables[2])
            results.extend( [ (self.discretized_vars[i],discretized_solutions.variables[i]) for i in range(len(discretized_solutions.variables)) ] )
            
        if self.include_binary:
            binary_solutions = copy.deepcopy(solution.variables[3])
            results.extend( [ (self.binary_vars[i],binary_solutions.variables[i]) for i in range(len(binary_solutions.variables)) ] )
            
        if self.include_permutation:
            
            for i in range(len(self.permutation_vars)):
                permutation_solution = copy.deepcopy(solution.variables[4+i])
                results.append( (self.permutation_vars[i],permutation_solution.variables) )
        
        return results
    
    def get_name(self):
        return "CompositeProblem"
        