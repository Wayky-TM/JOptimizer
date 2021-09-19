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
import jmetal.operator.selection as Selection

import core.variable as var_types
from core.composite_problem import CompositeProblem
from core.null import NullCrossoverOperator, NullMutationOperator

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
        # RANKING_AND_FITNESS="ranking_and_fitness"
        # BINARY_TOURNAMENT_2="binary_tournament_2"
    
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
        self.permutation_crossover_choice = AlgorithmParameters.PERMUTATION_CROSSOVER.PMX
        self.permutation_crossover_parameters = defaultdict(lambda: "")
        
        self.permutation_mutation_choice = AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP
        self.permutation_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Selection """
        self.selection_choice = AlgorithmParameters.SELECTION.BINARY_TOURNAMENT
        self.selection_parameters = defaultdict(lambda: "")
        
        
        """ Algorithm-specific """
        self.specific_
        
        
    def compile_algorithm(self, problem: CompositeProblem):
        
        type_set = { type(v) for v in variables }
        
        
        """
            Float
        """
        if problem.include_float:
            
            """ Crossover """
            if self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION:
                float_crossover = Crossover.DifferentialEvolutionCrossover( CR=float(self.float_crossover_parameters["probability"]), F=float(self.float_crossover_parameters["F"]))
                
            elif self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.SBX:
                float_crossover = Crossover.SBXCrossover( probability=float(self.float_crossover_parameters["probability"]), distribution_index=float(self.float_crossover_parameters["distribution_index"]))
                
            
            """ Mutation """
            if self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL:
                float_mutation = Mutation.PolynomialMutation( probability=float(self.float_mutation_parameters["probability"]), distribution_index=float(self.float_mutation_parameters["distribution_index"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM:
                float_mutation = Mutation.SimpleRandomMutation( probability=float(self.float_mutation_parameters["probability"]) )
                
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.UNIFORM:
                float_mutation = Mutation.UniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM:
                float_mutation = Mutation.NonUniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]), max_iterations=int(self.float_mutation_parameters["max_iterations"]) )
            
        else:
            float_crossover = NullCrossoverOperator()
            float_mutation = NullMutationOperator()
            
            
            
        """
            Int/discr
        """
        if problem.include_int or problem.include_discretized:
            
            """ Crossover """
            if self.int_crossover_choice == AlgorithmParameters.INT_CROSSOVER.INT_SBX:
                int_crossover = Crossover.IntegerSBXCrossover( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
            
            """ Mutation """
            if self.int_mutation_choice == AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL:
                int_mutation = Mutation.IntegerPolynomialMutation( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
            
        else:
            int_crossover = NullCrossoverOperator()
            int_mutation = NullMutationOperator()
            
        discr_crossover = int_crossover
        discr_mutation = int_mutation
            
            
            
        """
            Binary
        """
        if problem.include_binary:
            
            """ Crossover """
            if self.binary_crossover_choice == AlgorithmParameters.BINARY_CROSSOVER.SPX:
                binary_crossover = Crossover.SPXCrossover( probability=float(self.binary_crossover_parameters["probability"]) )
            
            """ Mutation """
            if self.binary_mutation_choice == AlgorithmParameters.BINARY_MUTATION.BIT_FLIP:
                binary_mutation = Mutation.BitFlipMutation( probability=float(self.binary_mutation_parameters["probability"]) )
            
        else:
            binary_crossover = NullCrossoverOperator()
            binary_mutation = NullMutationOperator()
            
            
        crossover_operators = [float_crossover, int_crossover, discr_crossover, binary_crossover ]
        mutation_operators = [float_mutation, int_mutation, discr_mutation, binary_mutation ]
        
        
        
        """
            Permutation
        """
        if problem.include_permutation:
            
            """ Crossover """
            if self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.CXC:
                permutation_crossover = Crossover.CXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
            
            elif self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.PMX:
                permutation_crossover = Crossover.PMXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
            
            """ Mutation """
            if self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP:
                permutation_mutation = Mutation.PermutationSwapMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            elif self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.SCRAMBLE_MUTATION:
                permutation_mutation = Mutation.ScrambleMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            crossover_operators.extend( [permutation_crossover]*len(problem.permutation_vars) )
            mutation_operators.extend( [permutation_mutation]*len(problem.permutation_vars) )
            
        
        """
            Selection
        """
        if self.choice != AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD:
            
            if self.selection_choice == AlgorithmParameters.SELECTION.ROULETTE:
                selection_operator = Selection.RouletteWheelSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.BINARY_TOURNAMENT:
                selection_operator = Selection.BinaryTournamentSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.BEST_SOLUTION:
                selection_operator = Selection.BestSolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.NARY_RANDOM:
                selection_operator = Selection.NaryRandomSolutionSelection( number_of_solutions_to_be_returned=int(self.selection_parameters["number_of_solutions_to_be_returned"]) )
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.DIFF_EVOLUTION:
                selection_operator = Selection.DifferentialEvolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.RANDOM:
                selection_operator = Selection.RandomSolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.RANKING_AND_CROWDING:
                selection_operator = Selection.RankingAndCrowdingDistanceSelection( max_population_size=int(self.selection_parameters["max_population_size"]) )
                
            # elif self.selection_choice == AlgorithmParameters.SELECTION.RANKING_AND_FITNESS:
            #     selection_operator = Selection.RankingAndFitnessSelection( max_population_size=int(self.selection_parameters["max_population_size"]), reference_point )
                
            # elif self.selection_choice == AlgorithmParameters.SELECTION.BINARY_TOURNAMENT_2:
            #     selection_operator = Selection.BinaryTournament2Selection(  )
            
            
        
        
        