
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

from core.variable import *
                  
from core.problem_parameters import ProblemParameters
from core.constant import FloatConstant, IntegerConstant
from core.evaluator import Evaluator
from core.null import NullSolution


class ARGS_TYPES(Enum):
    VARIABLE=0
    CONSTANT=1
    
class ARGS_MODES(Enum):
    NORMAL=0
    KEYWORD=1
    UNPACKED=2


# class ArgumentsTransformer:
    
#     """
#         arg_index_list is a list of tuples with the form:
#             Constants: (ARGS_TYPES.CONSTANT, ARGS_MODES, keyword, [keyword])
#             Variables: (ARGS_TYPES.VARIABLE, ARGS_MODES, index, [vector_index], [keyword])
#     """
#     def __init__(self, arg_index_list, problem_parameters: ProblemParameters):
#         self.arg_index_list = arg_index_list
#         self.problem_parameters = problem_parameters
#         self.constants_values = {}
        
#         for index in arg_index_list:
            
#             if index[0] == ARGS_TYPES.CONSTANT:
#                 self.constants_values[index[1]] = [ constant for constant in problem_parameters.constants if constant.keyword==index[1] ][0].value
                
    
#     def __call__( solution: jsol.CompositeSolution ):
#         args = []
#         kwargs = {}
        
#         for index in self.arg_index_list:
            
#             if index[0]==ARGS_TYPES.CONSTANT:
#                 value = self.constants_values[index[2]]
            
#             else:
                
#                 if len(index) == 4: # Scalar
#                     value = solution[index[2]].variables[index[3]]
                    
#                 else: # Vector/Permutation/String
#                     value = solution[index[2]]
            
#             if index[1] == ARGS_MODES.NORMAL:
#                 args.append( value )
                
#             elif index[1] == ARGS_MODES.UNPACKED:
#                 args.extend( value )
                
#             elif index[1] == ARGS_MODES.KEYWORD:
#                 kwargs[index[-1]] = value
        
#         return args, kwargs


class CompositeProblem(jprob.Problem[jsol.CompositeSolution], ABC):
        
    def __init__(self,
                 evaluator: Evaluator,
                 problem_parameters: ProblemParameters):
        
        if len(problem_parameters.variables) < 1:
            raise ValueError( "%s.__init__(): at least one variable needed" % (type(self).__name__) )
            
        self.problem_parameters = problem_parameters
            
        # self.float_vars = [ var for self.problem_parameters.variables if type(var)==FloatVariable ]
        # self.integer_vars = [ var for self.problem_parameters.variables if type(var)==IntegerVariable ]
        # self.discretized_vars = [ var for self.problem_parameters.variables if type(var)==DiscretizedFloatVariable ]
        # self.binary_vars = [ var for self.problem_parameters.variables if type(var)==BinaryVariable ]
        # self.permutation_vars = [ var for self.problem_parameters.variables if type(var)==PermutationVariable ]
        # self.floatVector_vars = [ var for self.problem_parameters.variables if type(var)==FloatVectorVariable ]
        # self.integerVector_vars = [ var for self.problem_parameters.variables if type(var)==IntegerVectorVariable ]
        # self.discretizedVector_vars = [ var for self.problem_parameters.variables if type(var)==DiscretizedVectorVariable ]
        
        self.variables = { var.keyword:var for var self.problem_parameters.variables }
        self.constants = { const.keyword:const for const self.problem_parameters.constants }
        
        self.float_solution_counter = 0
        self.float_index = 0
        
        self.integer_solution_counter = 0
        self.integer_index = 0
        
        self.discretized_solution_counter = 0
        self.discretized_index = 0
        
        self.binary_index = 0
        
        self.permutation_solution_counter = 0
        
        var_args = self._compile_call_argument()
        self.argument_list = []
        
        for argument in var_args:
            
            if argument[0] in self.variables:
                """ Format: (Var, index, Mode [, keyword]) """
                
                var = self.variables[argument[0]]
                
                if 
                
            
            elif argument[0] in self.constants:
                """ Format: (Var, Mode [, keyword]) """
                if argument[1] == ARGS_MODES.KEYWORD:
                    self.argument_list.append( (self.variables[argument[0]], argument[1], argument[2]) )
                    
                else:
                    self.argument_list.append( (self.variables[argument[0]], argument[1]) )
                
            
            else:
                raise Exception("CompositeProblem.__init__(): wrong argument '%'" % (argument[0]))
        
        
        """ Variable categorization """
        # for v in self.problem_parameters.variables:
        #     self.symbols[v.keyword] = v
            
        #     if isinstance(v, Variables.FloatVariable):
        #         self.float_vars += 1
                
        #     elif isinstance(v, Variables.IntegerVariable):
        #         self.int_vars += 1
                
        #     elif isinstance(v, Variables.DiscretizedFloatVariable):
        #         self.disc_vars += 1
                
        #     elif isinstance(v, Variables.BinaryVariable):
        #         self.binary_vars += 1
                
        #     elif isinstance(v, Variables.PermutationVariable):
        #         self.permutation_vars += 1
                
        #     elif isinstance(v, Variables.FloatVectorVariable):
        #         self.floatVector_vars += v.length
                
        #     elif isinstance(v, Variables.IntegerVectorVariable):
        #         self.integerVector_vars += v.length
                
        #     elif isinstance(v, Variables.DiscretizedFloatVariable):
        #         self.float_vars += v.length
                
        # for c in self.problem_parameters.constants:
        #     self.symbols[c.keyword] = c
            
        # Shape: (n_float, n_int, n_disc, n_binary, n_permutation)
        self.solution_shape = (self.float_vars, self.int_vars, self.disc_vars, self.binary_vars, self.permutation_vars )
        
        # self.number_of_variables = len(float_vars) + len(int_vars) + len(discretized_vars) + len(binary_vars) + len(permutation_vars) + len(floatVector_vars) + len(integerVector_vars) + len(discretizedVector_vars)
        # self.evaluator = copy.deepcopy( evaluator )
        self.evaluator = evaluator
        self.number_of_objectives = evaluator.number_of_objectives
        
        if (len(self.problem_parameters.variables) + len(self.problem_parameters.constants)) != evaluator.number_of_variables:
            raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
            
        # self.include_float = len(float_vars)>0
        # self.include_int = len(int_vars)>0
        # self.include_discretized = len(discretized_vars)>0
        # self.include_binary = len(binary_vars)>0
        # self.include_permutation = len(permutation_vars)>0
        # self.include_floatVector = len(floatVector_vars)>0
        # self.include_integerVector = len(integerVector_vars)>0
        # self.include_discretizedVector = len(discretizedVector_vars)>0
        
        
        
        # self.constants = copy.deepcopy(constants)
        self.null_solution = NullSolution( number_of_objectives=self.number_of_objectives )
        
        if self.include_float:
            self.float_lower_bounds = [ x.lower_bound for x in float_vars ]
            self.float_upper_bounds = [ x.upper_bound for x in float_vars ]
            
        if self.include_int:
            self.int_lower_bounds = [ x.lower_bound for x in int_vars ]
            self.int_upper_bounds = [ x.upper_bound for x in int_vars ]
            
        if self.include_discretized:
            self.discretized_lower_bounds = [0]*len(discretized_vars)
            self.discretized_upper_bounds = [ x.resolution for x in discretized_vars ]
            
        self.evaluations = 0
    
    # def __init__(self,
    #              evaluator: Evaluator,
    #              float_vars : List[FloatVariable] = [],
    #              int_vars : List[IntegerVariable] = [],
    #              discretized_vars : List[DiscretizedFloatVariable] = [],
    #              binary_vars : List[BinaryVariable] = [],
    #              permutation_vars : List[PermutationVariable] = [],
    #              floatVector_vars : List[FloatVectorVariable] = [],
    #              integerVector_vars : List[IntegerVectorVariable] = [],
    #              discretizedVector_vars : List[DiscretizedVectorVariable] = [],
    #              constants : List = []):
        
    #     if len(float_vars)+len(int_vars)+len(discretized_vars) < 1:
    #         raise ValueError( "%s.__init__(): at least one variable needed" % (type(self).__name__) )
            
    #     self.number_of_variables = len(float_vars) + len(int_vars) + len(discretized_vars) + len(binary_vars) + len(permutation_vars) + len(floatVector_vars) + len(integerVector_vars) + len(discretizedVector_vars)
    #     self.evaluator = copy.deepcopy( evaluator )
    #     self.number_of_objectives = evaluator.number_of_objectives
        
    #     if (self.number_of_variables + len(constants)) != evaluator.number_of_variables:
    #         raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
            
    #     self.include_float = len(float_vars)>0
    #     self.include_int = len(int_vars)>0
    #     self.include_discretized = len(discretized_vars)>0
    #     self.include_binary = len(binary_vars)>0
    #     self.include_permutation = len(permutation_vars)>0
    #     self.include_floatVector = len(floatVector_vars)>0
    #     self.include_integerVector = len(integerVector_vars)>0
    #     self.include_discretizedVector = len(discretizedVector_vars)>0
        
    #     self.float_vars = copy.deepcopy( float_vars )
    #     self.int_vars = copy.deepcopy( int_vars )
    #     self.discretized_vars = copy.deepcopy( discretized_vars )
    #     self.binary_vars = copy.deepcopy( binary_vars )
    #     self.permutation_vars = copy.deepcopy( permutation_vars )
    #     self.floatVector_vars = copy.deepcopy( floatVector_vars )
    #     self.integerVector_vars = copy.deepcopy( integerVector_vars )
    #     self.discretizedVector_vars = copy.deepcopy( discretizedVector_vars )
        
    #     self.constants = copy.deepcopy(constants)
        self.null_solution = NullSolution( number_of_objectives=self.number_of_objectives )
        
    #     if self.include_float:
    #         self.float_lower_bounds = [ x.lower_bound for x in float_vars ]
    #         self.float_upper_bounds = [ x.upper_bound for x in float_vars ]
            
    #     if self.include_int:
    #         self.int_lower_bounds = [ x.lower_bound for x in int_vars ]
    #         self.int_upper_bounds = [ x.upper_bound for x in int_vars ]
            
    #     if self.include_discretized:
    #         self.discretized_lower_bounds = [0]*len(discretized_vars)
    #         self.discretized_upper_bounds = [ x.resolution for x in discretized_vars ]
            
    #     self.evaluations = 0

    def _compile_call_argument(self):
        
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
        solutions = [self.null_solution]*4
        
        if self.include_float:
            temp_solution = jsol.FloatSolution(lower_bound=self.float_lower_bounds, upper_bound=self.float_upper_bounds, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
            temp_solution.variables = [ x.rand() for x in self.float_vars ]
            solutions[0] = temp_solution
            # solutions.append(temp_solution)
            # self.float_index = solution_index
            # solution_index += 1
            
        if self.include_int:
            temp_solution = jsol.IntegerSolution(lower_bound=self.int_lower_bounds, upper_bound=self.int_upper_bounds, number_of_objectives=self.number_of_objectives )
            temp_solution.variables = [ x.rand() for x in self.int_vars ]
            solutions[1] = temp_solution
            # solutions.append(temp_solution)
            # self.int_index = solution_index
            # solution_index += 1
            
        if self.include_discretized:
            temp_solution = jsol.IntegerSolution(lower_bound=self.discretized_lower_bounds, upper_bound=self.discretized_upper_bounds, number_of_objectives=self.number_of_objectives )
            temp_solution.variables = [ x.randint() for x in self.discretized_vars ]
            solutions[2] = temp_solution
            # solutions.append(temp_solution)
            # self.discretized_index = solution_index
            # solution_index += 1
            
        if self.include_binary:
            temp_solution = jsol.BinarySolution(number_of_variables=len(self.binary_vars), number_of_objectives=self.number_of_objectives)
            temp_solution.variables = [ x.rand()==1 for x in self.binary_vars ]
            solutions[3] = temp_solution
            # solutions.append(temp_solution)
            # self.binary_index = solution_index
            # solution_index += 1
            
        if self.include_permutation:
            
            self.permutation_index = solution_index
            solution_index += 1
            
            for x in self.permutation_vars:
                temp_solution = jsol.PermutationSolution(number_of_variables=len(x.elements), number_of_objectives=self.number_of_objectives)
                temp_solution.variables = x.rand()
                solutions.append(temp_solution)
                solution_index += 1
        
        if self.include_floatVector:
            
            self.floatVector_index = solution_index
            solution_index += 1
            
            for x in self.floatVector_vars:
                temp_solution = jsol.FloatSolution(lower_bound=[ x.lower_bound ]*x.length, upper_bound=[ x.upper_bound ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
                temp_solution.variables = x.rand()
                solutions.append(temp_solution)
                solution_index += 1
        
        if self.include_integerVector:
            
            self.integerVector_index = solution_index
            solution_index += 1
            
            for x in self.integerVector_vars:
                temp_solution = jsol.IntegerSolution(lower_bound=[ x.lower_bound ]*x.length, upper_bound=[ x.upper_bound ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
                temp_solution.variables = x.rand()
                solutions.append(temp_solution)
                solution_index += 1
        
        if self.include_discretizedVector:
            
            self.discretizedVector_index = solution_index
            solution_index += 1
            
            for x in self.discretizedVector_vars:
                temp_solution = jsol.IntegerSolution(lower_bound=[0]*x.length, upper_bound=[ x.resolution ]*x.length, number_of_objectives=self.number_of_objectives, number_of_constraints=0 )
                temp_solution.variables = x.randint()
                solutions.append(temp_solution)
                solution_index += 1
        
        return jsol.CompositeSolution( solutions=solutions )
    
    
    
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
        