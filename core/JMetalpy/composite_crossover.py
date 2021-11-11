# -*- coding: utf-8 -*-

import copy
import random
from typing import List

from jmetal.core.operator import Crossover
from jmetal.operator.crossover import NullCrossover
# from jmetal.core.solution import Solution, FloatSolution, BinarySolution, PermutationSolution, IntegerSolution
from jmetal.util.ckecking import Check

from core.JMetalpy.composite_solution import *



class CompositeCrossover(Crossover[CompositeSolution, CompositeSolution]):

    def __init__(self,
                 float_crossover: Crossover = NullCrossover(),
                 integer_crossover: Crossover = NullCrossover(),
                 binary_crossover: Crossover = NullCrossover(),
                 permutation_crossover: Crossover = NullCrossover()):
        
        super(CompositeCrossover, self).__init__(probability=1.0)

        self.float_crossover = float_crossover
        self.integer_crossover = integer_crossover
        self.binary_crossover = binary_crossover
        self.permutation_crossover = permutation_crossover

    def execute(self, solutions: List[CompositeSolution]) -> List[CompositeSolution]:
        Check.is_not_none(solutions)
        Check.that(len(solutions) == 2, "The number of parents is not two: " + str(len(solutions)))

        float_solutions_offspring1 = []
        float_solutions_offspring2 = []
        
        integer_solutions_offspring1 = []
        integer_solutions_offspring2 = []
        
        binary_solutions_offspring1 = []
        binary_solutions_offspring2 = []
        
        permutation_solutions_offspring1 = []
        permutation_solutions_offspring2 = []


        for ParentA, ParentB in zip( solutions[0].float_solutions, solutions[1].float_solutions ):
            children = self.float_crossover.execute( [ParentA, ParentB] )
            float_solutions_offspring1.append( children[0] )
            float_solutions_offspring2.append( children[1] )

        
        for ParentA, ParentB in zip( solutions[0].integer_solutions, solutions[1].integer_solutions ):
            children = self.integer_crossover.execute( [ParentA, ParentB] )
            integer_solutions_offspring1.append( children[0] )
            integer_solutions_offspring2.append( children[1] )
            
            
        for ParentA, ParentB in zip( solutions[0].binary_solutions, solutions[1].binary_solutions ):
            children = self.binary_crossover.execute( [ParentA, ParentB] )
            binary_solutions_offspring1.append( children[0] )
            binary_solutions_offspring2.append( children[1] )
            
            
        for ParentA, ParentB in zip( solutions[0].permutation_solutions, solutions[1].permutation_solutions ):
            children = self.permutation_crossover.execute( [ParentA, ParentB] )
            permutation_solutions_offspring1.append( children[0] )
            permutation_solutions_offspring2.append( children[1] )

        offspring1 = CompositeSolution( float_solutions=float_solutions_offspring1,
                                        integer_solutions=integer_solutions_offspring1,
                                        binary_solutions=binary_solutions_offspring1,
                                        permutation_solutions=permutation_solutions_offspring1,
                                        number_of_objectives=solutions[0].number_of_objectives,
                                        number_of_constraints=solutions[0].number_of_constraints)
        
        offspring2 = CompositeSolution( float_solutions=float_solutions_offspring2,
                                        integer_solutions=integer_solutions_offspring2,
                                        binary_solutions=binary_solutions_offspring2,
                                        permutation_solutions=permutation_solutions_offspring2,
                                        number_of_objectives=solutions[0].number_of_objectives,
                                        number_of_constraints=solutions[0].number_of_constraints)

        return [ offspring1, offspring2 ]

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self) -> str:
        return 'Composite crossover'

