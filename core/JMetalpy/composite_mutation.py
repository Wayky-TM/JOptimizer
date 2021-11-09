# -*- coding: utf-8 -*-

import copy
import random
from typing import List

from jmetal.core.operator import Mutation
from jmetal.operator.mutation import NullMutation
from jmetal.core.solution import Solution, FloatSolution, BinarySolution, PermutationSolution, IntegerSolution, \
    CompositeSolution
from jmetal.util.ckecking import Check


class CompositeMutation(Mutation[Solution]):
    
    def __init__(self,
                 float_mutation: Mutation = NullMutation(),
                 integer_mutation: Mutation = NullMutation(),
                 binary_mutation: Mutation = NullMutation(),
                 permutation_mutation: Mutation = NullMutation()):
        
        super(CompositeMutation,self).__init__(probability=1.0)
        
        self.float_mutation = float_mutation
        self.integer_mutation = integer_mutation
        self.binary_mutation = binary_mutation
        self.permutation_mutation = permutation_mutation
        

    def execute(self, solution: CompositeSolution) -> CompositeSolution:
        Check.is_not_none(solution)

        float_solutions = []
        integer_solutions = []
        binary_solutions = []
        permutation_solutions = []
        
        for solution in solution.float_solutions:
            float_solutions.append( self.float_mutation.execute(solution) )
            
        for solution in solution.integer_solutions:
            integer_solutions.append( self.integer_mutation.execute(solution) )
            
        for solution in solution.binary_solutions:
            binary_solutions.append( self.binary_mutation.execute(solution) )
            
        for solution in solution.permutation_solutions:
            permutation_solutions.append( self.permutation_mutation.execute(solution) )
        
        return CompositeSolution( float_solutions=float_solutions,
                                  integer_solutions=integer_solutions,
                                  binary_solutions=binary_solutions,
                                  permutation_solutions=permutation_solutions,
                                  number_of_objectives=solution.number_of_objectives,
                                  number_of_constraints=solution.number_of_constraints)

    def get_name(self) -> str:
        return "Composite mutation operator"