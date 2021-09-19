# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:18:54 2021

@author: Wayky
"""


import copy
import random
import math

from enum import Enum
from abc import *
from typing import List

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import jmetal.core.operator as jop
import jmetal.operator.crossover as Crossover
import jmetal.operator.mutation as Mutation

import core.variable as var_types
from core.composite_problem import CompositeProblem

class AlgorithmParameters:
    
    class SUPPORTED_ALGORITHMS(Enum):
        NSGAII="NSGAII"
        MOCELL="MOCELL"
        MOEAD="MOEAD"
        GA_MONO="GA_mono-objective"
        
        
    
    class FLOAT_CROSSOVER(Enum):
        SBX="SBX"
        DIFF_EVOLUTION="differential_evolution"
        
    class FLOAT_MUTATION(Enum):
        POLYNOMIAL="polynomial"
        SIMPLE_RANDOM="simple_random"
        UNIFORM="uniform"
        NON_UNIFORM="non_uniform"
        
        
        
    class INT_CROSSOVER(Enum):
        INT_SBX="int_SBX"
        
    class INT_MUTATION(Enum):
        INT_POLYNOMIAL="int_polynomial"
        
        
        
    class BINARY_CROSSOVER(Enum):
        SPX="SPX"
        
    class BINARY_MUTATION(Enum):
        BIT_FLIP="bit_flip"
        
        
        
    class PERMUTATION_CROSSOVER(Enum):
        PMX="PMX"
        CXC="CXC"
        
    class PERMUTATION_MUTATION(Enum):
        PERMUTATION_SWAP="permutation_swap"
        SCRAMBLE_MUTATION="scramble_mutation"
        
        
        
    class SELECTION(Enum):
        ROULETTE="roulette"
        BINARY_TOURNAMENT="binary_tournament"
        BEST_SOLUTION="best_solution"
        NARY_RANDOM="n-ary_random"
        DIFF_EVOLUTION="differential_volution"
        RANDOM="random"
        RANKING_AND_CROWDING="ranking_and_crowding"
        RANKING_AND_FITNESS="ranking_and_fitness"
        BINARY_TOURNAMENT_2="binary_tournament_2"
    
    def __init__(self):
        
        self.choice = AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII
        
        """ Float """
        self.float_crossover_choice = AlgorithmParameters.FLOAT_CROSSOVER.SBX
        self.float_crossover_parameters = defaultdict(lambda: "")
        
        self.float_mutation_choice = AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL
        self.float_mutation_parameters = defaultdict(lambda: "")
        
        
        
        """ Int """
        self.int_crossover_choice = AlgorithmParameters.INT_CROSSOVER.INT_SBX
        self.int_crossover_parameters = defaultdict(lambda: "")
        
        self.int_mutation_choice = AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL
        self.int_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Binary """
        self.binary_crossover_choice = AlgorithmParameters.BINARY_CROSSOVER.SPX
        self.binary_crossover_parameters = defaultdict(lambda: "")
        
        self.binary_mutation_choice = AlgorithmParameters.BINARY_MUTATION.BIT_FLIP
        self.binary_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Permutation """
        self.binary_crossover_choice = AlgorithmParameters.PERMUTATION_CROSSOVER.PMX
        self.binary_crossover_parameters = defaultdict(lambda: "")
        
        self.binary_mutation_choice = AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP
        self.binary_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Selection """
        self.selection_choice = AlgorithmParameters.SELECTION.BINARY_TOURNAMENT
        self.selection_parameters = defaultdict(lambda: "")
        
        
        
    class NullCrossoverOperator( jop.Crossover ):
        
        def __init__(self):
            pass
            
        def get_number_of_parents(self) -> int:
            return 2
    
        def get_number_of_children(self) -> int:
            return 1
        
        def execute(self, parents: List[Solution]):
            return parents[0]
    
        def get_name(self) -> str:
            return "NullCrossoverOperator"
        
        
    class NullMutationOperator( jop.Mutation ):
        
        def __init__(self):
            pass
        
        def execute(self, solution):
            return solution
    
        def get_name(self) -> str:
            return "NullMutationOperator"
        
        
        
    def compile_algorithm(self, problem: CompositeProblem, variables: List[var_types]):
        
        type_set = { type(v) for v in variables }
        
        
        """
            Float
        """
        if problem.include_float:
            
            """ Crossover """
            if self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION:
                pass
            elif self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.SBX:
                pass
                
            
            """ Mutation """
            
        else:
            float_crossover = NullCrossoverOperator()
            float_mutation = NullMutationOperator()
            
            
        """
            Int/discr
        """
        if problem.include_int or problem.include_discretized:
            
            """ Crossover """
            if self.int_crossover_choice == AlgorithmParameters
            
            """ Mutation """
            
        else:
            int_crossover = NullCrossoverOperator()
            int_mutation = NullMutationOperator()
            
            discr_crossover = int_crossover
            discr_mutation = int_mutation
            
            
        """
            Binary
        """
        if var_types.BinaryVariable in type_set:
            
        else:
            binary_crossover = NullCrossoverOperator()
            binary_mutation = NullMutationOperator()
            
            
        crossover_operators = [float_crossover, int_crossover, discr_crossover, binary_crossover ]
        mutation_operators = [float_mutation, int_mutation, discr_mutation, binary_mutation ]
        
        
        """
            Permutation
        """