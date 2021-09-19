# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 15:18:14 2021

@author: Wayky
"""

import jmetal.core.solution as jsol
import jmetal.core.operator as jop



class NullSolution(jsol.Solution):
        
        def __init__(self):
            super(NullSolution, self).__init__(number_of_variables=0, number_of_objectives=0, number_of_constraints=0)
            
            
class NullCrossoverOperator( jop.Crossover ):
        
        def __init__(self):
            pass
            
        def get_number_of_parents(self) -> int:
            return 2
    
        def get_number_of_children(self) -> int:
            return 1
        
        def execute(self, parents: List[jsol.Solution]):
            return parents[0]
    
        def get_name(self) -> str:
            return "NullCrossoverOperator"
        
        
class NullMutationOperator( jop.Mutation ):
    
    def __init__(self):
        pass
    
    def execute(self, solution: List[jsol.Solution]):
        return solution

    def get_name(self) -> str:
        return "NullMutationOperator"