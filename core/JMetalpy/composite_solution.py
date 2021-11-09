# -*- coding: utf-8 -*-

import copy
import random
from typing import List

from jmetal.core.solution import Solution, FloatSolution, BinarySolution, PermutationSolution, IntegerSolution, \
    CompositeSolution
from jmetal.util.ckecking import Check



class CompositeSolution(Solution):
    """ Class representing solutions composed of a list of solutions. The idea is that each decision  variable can
    be a solution of any type, so we can create mixed solutions (e.g., solutions combining any of the existing
    encodings). The adopted approach has the advantage of easing the reuse of existing variation operators, but all the
    solutions in the list will need to have the same function and constraint violation values.

    It is assumed that problems using instances of this class will properly manage the solutions it contains.
    """

    def __init__(self,
                 float_solutions: FloatSolution = [],
                 integer_solutions: IntegerSolution = [],
                 binary_solutions: BinarySolution = [],
                 permutation_solutions: List[PermutationSolution] = [],
                 number_of_objectives: int,
                 number_of_constraints: int,
                 ):
        
        self.variables = len(float_solutions) + len(integer_solutions) + len(binary_solutions) + len(permutation_solutions)
        
        super(CompositeSolution, self).__init__(self.variables, number_of_objectives, number_of_constraints)
        
        Check.that( len(float_solutions) + len(integer_solutions) + len(binary_solutions) + len(permutation_solutions) > 0,
                    "At least one solution is needed to create a Composite solution")
        
        self.float_solutions = float_solutions
        self.integer_solutions = integer_solutions
        self.binary_solutions = binary_solutions
        self.permutation_solutions = permutation_solutions

    def __copy__(self):
        new_solution = CompositeSolution( float_solutions=self.float_solutions,
                                          integer_solutions=self.integer_solutions,
                                          binary_solutions=self.binary_solutions,
                                          permutation_solutions=self.permutation_solutions)

        new_solution.objectives = self.objectives[:]
        new_solution.constraints = self.constraints[:]
        new_solution.attributes = self.attributes.copy()

        return new_solution
    
    def __eq__(self, solution) -> bool:
        if isinstance(solution, self.__class__):
            try:
                return self.float_solutions == solution.float_solutions and
                       self.integer_solutions == solution.integer_solutions and
                       self.binary_solutions == solution.binary_solutions and
                       self.permutation_solutions == solution.permutation_solutions
            
            except:
                return False
        
        return False

    def __str__(self) -> str:
        return 'Solution(variables={},objectives={},constraints={})'.format( self.float_solutions + self.integer_solutions + self.binary_solutions + self.permutation_solutions,
                                                                            self.objectives,
                                                                            self.constraints)









