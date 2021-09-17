

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

from core.variable import FloatVariable, IntegerVariable, DiscretizedFloatVariable
from core.constant import FloatConstant, IntegerConstant
from core.evaluator import Evaluator



class CompositeProblem(jprob.Problem[jsol.CompositeSolution], ABC):
        
    def __init__(self,
                 evaluator: Evaluator,
                 float_vars : List[FloatVariable] = [],
                 int_vars : List[IntegerVariable] = [],
                 discretized_vars : List[DiscretizedFloatVariable] = [],
                 constants : List = []):
        
        if len(float_vars)+len(int_vars)+len(discretized_vars) < 1:
            raise ValueError( "%s.__init__(): at least one variable needed" % (type(self).__name__) )
            
        if (len(float_vars) + len(int_vars) + len(discretized_vars) + len(constants)) != evaluator.number_of_variables:
            raise ValueError( "%s.__init__(): provided variables and constants do not match the required by the evaluator" % (type(self).__name__) )
            
        self.include_float = len(float_vars)>0
        self.include_int = len(int_vars)>0
        self.include_discretized = len(discretized_vars)>0
        
        self.float_vars = copy.deepcopy( float_vars )
        self.int_vars = copy.deepcopy( int_vars )
        self.discretized_vars = copy.deepcopy( discretized_vars )
        
        self.constants = copy.deepcopy(constants)
        
        counter = 0
        
        if self.include_float:
            self.float_index = counter
            counter += 1
            
            self.float_lower_bounds = [ x.lower_bound for x in float_vars ]
            self.float_upper_bounds = [ x.upper_bound for x in float_vars ]
            
        if self.include_int:
            self.int_index = counter
            counter += 1
            
            self.int_lower_bounds = [ x.lower_bound for x in int_vars ]
            self.int_upper_bounds = [ x.upper_bound for x in int_vars ]
            
        if self.include_discretized:
            self.discretized_index = counter
            counter += 1
            
            self.discretized_lower_bounds = [0]*len(discretized_vars)
            self.discretized_upper_bounds = [ x.resolution for x in discretized_vars ]
            
        
        self.evaluator = copy.deepcopy( evaluator )
        
        self.number_of_variables = evaluator.number_of_variables
        self.number_of_objectives = evaluator.number_of_objectives
        

    def create_solution(self) -> jsol.CompositeSolution:
        solutions = []
        
        if self.include_float:
            temp_solution = jsol.FloatSolution(self.float_lower_bounds, self.float_upper_bounds, self.number_of_objectives )
            # temp_solution.variables = [random.uniform(self.float_lower_bounds[i], self.float_upper_bounds[i]) for i in range(len(self.float_lower_bounds))]
            temp_solution.variables = [ x.rand() for x in self.float_vars ]
            solutions.append( temp_solution )
            
        if self.include_int:
            temp_solution = jsol.IntegerSolution(self.int_lower_bounds, self.int_upper_bounds, self.number_of_objectives )
            # temp_solution.variables = [random.randint(self.int_lower_bounds[i], self.int_upper_bounds[i]) for i in range(len(self.int_lower_bounds))]
            temp_solution.variables = [ x.rand() for x in self.int_vars ]
            solutions.append( temp_solution )
            
        if self.include_discretized:
            temp_solution = jsol.IntegerSolution(self.discretized_lower_bounds, self.discretized_upper_bounds, self.number_of_objectives )
            # temp_solution.variables = [random.randint(self.discretized_lower_bounds[i], self.discretized_upper_bounds[i]) for i in range(len(self.discretized_lower_bounds))]
            temp_solution.variables = [ x.randint() for x in self.discretized_vars ]
            solutions.append( temp_solution )
        
        return jsol.CompositeSolution( solutions=solutions )
    
    
    
    def evaluate( self, solution: jsol.CompositeSolution):
        
        arguments = {}
        
        if self.include_float:
            float_args = { self.float_vars[i].keyword:solution.variables[self.float_index].variables[i] for i in range(len(self.float_vars)) }
            arguments.update( float_args )
            
        if self.include_int:
            int_args = { self.int_vars[i].keyword:solution.variables[self.int_index].variables[i] for i in range(len(self.int_vars)) }
            arguments.update( int_args )
            
        if self.include_discretized:
            discretized_args = { self.discretized_vars[i].keyword:(float(solution.variables[self.discretized_index].variables[i])*self.discretized_vars[i].step)  for i in range(len(self.discretized_vars)) }
            arguments.update( discretized_args )
        
        if len(self.constants) > 0:
            const_args = { x.keyword:x.value for x in self.constants }
            arguments.update( const_args )
        
        solution.objectives = self.evaluator.evaluate( **arguments )
        
        return solution
    
    def recover_solution( self, solution: jsol.CompositeSolution ):
        
        variables = copy.deepcopy(solution.variables)
        results = []
        
        if self.include_float:
            float_solutions = solution.variables.pop(0)
            results.extend( [ (self.float_vars[i],float_solutions.variables[i]) for i in range(len(float_solutions)) ] )
            
        if self.include_int:
            int_solutions = solution.variables.pop(0)
            results.extend( [ (self.int_vars[i],int_solutions.variables[i]) for i in range(len(int_solutions)) ] )
            
        if self.include_int:
            discretized_solutions = solution.variables.pop(0)
            results.extend( [ (self.discretized_vars[i],discretized_solutions.variables[i]) for i in range(len(discretized_solutions)) ] )
        
        return results
    
    def get_name(self):
        return "CompositeProblem"
        