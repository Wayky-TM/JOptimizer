# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:18:54 2021

@author: Wayky
"""


import sys
sys.path.append(r"./..")

import copy
import random
import math

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import jmetal.core.operator as jop
import jmetal.operator.crossover as Crossover
import jmetal.operator.mutation as Mutation
import jmetal.operator.selection as Selection
import jmetal.algorithm.multiobjective as Multiobjective
import jmetal.algorithm.singleobjective as Singleobjective
import jmetal.util.aggregative_function as Aggregative
import jmetal.util.archive as Archive
import jmetal.util.neighborhood as Neighborhood

import core.variable as var_types
from core.composite_problem import CompositeProblem
from jmetal.util.termination_criterion import TerminationCriterion
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
        
    
    """
        MOEAD Specific
    """
    class MOEAD_AGGREGATIVE_FUNCTION(Enum):
        # WEIGHTED_SUM = "weighted_sum"
        TSCHEBYCHEFF = "tschebycheff"
            
    """
        MOCELL Specific
    """     
    class MOCELL_ARCHIVE(Enum):
        # NONDOMINATED_SOLUTIONS="non-dominated_solutions"
        CROWDING_DISTANCE="crowding_distance"
        # BOUNDED="bounded"
        
        
    class MOCELL_NEIGHBORHOOD(Enum):
        # WEIGHT_NEIGHBORHOOD="weight_neighborhood"
        # WEIGHT_VECTOR_NEIGHBORHOOD="weight_vector_neighborhood"
        # TWO_DIMENSIONAL_MESH="two-dimensional_mesh"
        C9="C9"
        # L5="L5"
        
        
        
    
    def __init__(self):
        
        self.choice = AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value
        
        """ General """
        self.general_parameters = defaultdict(lambda: "")
        
        """ Float """
        self.float_crossover_choice = AlgorithmParameters.FLOAT_CROSSOVER.SBX.value
        self.float_crossover_parameters = defaultdict(lambda: "")
        
        self.float_mutation_choice = AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value
        self.float_mutation_parameters = defaultdict(lambda: "")
        
        
        
        """ Int """
        self.int_crossover_choice = AlgorithmParameters.INT_CROSSOVER.INT_SBX.value
        self.int_crossover_parameters = defaultdict(lambda: "")
        
        self.int_mutation_choice = AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value
        self.int_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Binary """
        self.binary_crossover_choice = AlgorithmParameters.BINARY_CROSSOVER.SPX.value
        self.binary_crossover_parameters = defaultdict(lambda: "")
        
        self.binary_mutation_choice = AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value
        self.binary_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Permutation """
        self.permutation_crossover_choice = AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value
        self.permutation_crossover_parameters = defaultdict(lambda: "")
        
        self.permutation_mutation_choice = AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP.value
        self.permutation_mutation_parameters = defaultdict(lambda: "")
        
        
        """ Selection """
        self.selection_choice = AlgorithmParameters.SELECTION.BINARY_TOURNAMENT.value
        self.selection_parameters = defaultdict(lambda: "")
        
        
        """ Algorithm-specific """
        self.specific_options = defaultdict(lambda: "")
        self.specific_parameters = defaultdict(lambda: defaultdict(lambda: ""))
        
        
        
    """ Generates an Algorithm object based on algorithm and problem parameters """
    def compile_algorithm(self, problem: CompositeProblem, termination_criterion: TerminationCriterion):
        
        """
            Float
        """
        if problem.include_float:
            
            """ Crossover """
            if self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION.value:
                float_crossover = Crossover.DifferentialEvolutionCrossover( CR=float(self.float_crossover_parameters["probability"]), F=float(self.float_crossover_parameters["F"]))
                
            elif self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
                float_crossover = Crossover.SBXCrossover( probability=float(self.float_crossover_parameters["probability"]), distribution_index=float(self.float_crossover_parameters["distribution_index"]))
                
            
            """ Mutation """
            if self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value:
                float_mutation = Mutation.PolynomialMutation( probability=float(self.float_mutation_parameters["probability"]), distribution_index=float(self.float_mutation_parameters["distribution_index"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM.value:
                float_mutation = Mutation.SimpleRandomMutation( probability=float(self.float_mutation_parameters["probability"]) )
                
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.UNIFORM.value:
                float_mutation = Mutation.UniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM.value:
                float_mutation = Mutation.NonUniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]), max_iterations=int(self.float_mutation_parameters["max_iterations"]) )
            
        else:
            float_crossover = NullCrossoverOperator()
            float_mutation = NullMutationOperator()
            
            
            
        """
            Int/discr
        """
        if problem.include_int or problem.include_discretized:
            
            """ Crossover """
            if self.int_crossover_choice == AlgorithmParameters.INT_CROSSOVER.INT_SBX.value:
                temp_int_crossover = Crossover.IntegerSBXCrossover( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
            
            """ Mutation """
            if self.int_mutation_choice == AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value:
                temp_int_mutation = Mutation.IntegerPolynomialMutation( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
            
            if problem.include_int:
                int_crossover = temp_int_crossover
                int_mutation = temp_int_mutation
            else:
                int_crossover = NullCrossoverOperator()
                int_mutation = NullMutationOperator()    
                
            if problem.include_discretized:
                discr_crossover = temp_int_crossover
                discr_mutation = temp_int_mutation
            else:
                discr_crossover = NullCrossoverOperator()
                discr_mutation = NullMutationOperator()    
        
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
            if self.binary_crossover_choice == AlgorithmParameters.BINARY_CROSSOVER.SPX.value:
                binary_crossover = Crossover.SPXCrossover( probability=float(self.binary_crossover_parameters["probability"]) )
            
            """ Mutation """
            if self.binary_mutation_choice == AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value:
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
            if self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.CXC.value:
                permutation_crossover = Crossover.CXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
            
            elif self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value:
                permutation_crossover = Crossover.PMXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
            
            """ Mutation """
            if self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP.value:
                permutation_mutation = Mutation.PermutationSwapMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            elif self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.SCRAMBLE_MUTATION.value:
                permutation_mutation = Mutation.ScrambleMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            crossover_operators.extend( [permutation_crossover]*len(problem.permutation_vars) )
            mutation_operators.extend( [permutation_mutation]*len(problem.permutation_vars) )
            
        
        composite_crossover = Crossover.CompositeCrossover( crossover_operators )
        composite_mutation = Mutation.CompositeMutation( mutation_operators )
        
        """
            Selection
        """
        if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value]:
            
            if self.selection_choice == AlgorithmParameters.SELECTION.ROULETTE.value:
                selection_operator = Selection.RouletteWheelSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.BINARY_TOURNAMENT.value:
                selection_operator = Selection.BinaryTournamentSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.BEST_SOLUTION.value:
                selection_operator = Selection.BestSolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.NARY_RANDOM.value:
                selection_operator = Selection.NaryRandomSolutionSelection( number_of_solutions_to_be_returned=int(self.selection_parameters["number_of_solutions_to_be_returned"]) )
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.DIFF_EVOLUTION.value:
                selection_operator = Selection.DifferentialEvolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.RANDOM.value:
                selection_operator = Selection.RandomSolutionSelection()
                
            elif self.selection_choice == AlgorithmParameters.SELECTION.RANKING_AND_CROWDING.value:
                selection_operator = Selection.RankingAndCrowdingDistanceSelection( max_population_size=int(self.selection_parameters["max_population_size"]) )
                
            # elif self.selection_choice == AlgorithmParameters.SELECTION.RANKING_AND_FITNESS:
            #     selection_operator = Selection.RankingAndFitnessSelection( max_population_size=int(self.selection_parameters["max_population_size"]), reference_point )
                
            # elif self.selection_choice == AlgorithmParameters.SELECTION.BINARY_TOURNAMENT_2:
            #     selection_operator = Selection.BinaryTournament2Selection(  )
            
            
        population_size = int(self.general_parameters["population_size"])
        
        if self.choice in [AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value]:
            offspring_size = int(self.general_parameters["offspring_size"])
        
            
        """
            Algorithm compilation
        """
        if self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value:
            
            algorithm = Multiobjective.NSGAII(problem=problem,
                                              population_size=population_size,
                                              offspring_population_size=offspring_size,
                                              mutation=composite_mutation,
                                              crossover=composite_crossover,
                                              selection=selection_operator)
            
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value:
            
            algorithm = Singleobjective.GeneticAlgorithm(problem=problem,
                                                         population_size=population_size,
                                                         offspring_population_size=offspring_size,
                                                         mutation=composite_mutation,
                                                         crossover=composite_crossover,
                                                         selection=selection_operator)
            
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value:
            
            if self.specific_options["aggregative"] == AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.TSCHEBYCHEFF.value:
                aggregative_function = Aggregative.Tschebycheff( dimension=int(self.specific_parameters["aggregative"]["dimension"]) )
            
            algorithm = Multiobjective.MOEAD(problem=problem,
                                             population_size=population_size,
                                             mutation=composite_mutation,
                                             crossover=composite_crossover,
                                             aggregative_function=aggregative_function,
                                             neighbourhood_selection_probability=float(self.specific_options["neighborhood_selection_probability"]),
                                             max_number_of_replaced_solutions=int(self.specific_options["max_number_of_replaced_solutions"]),
                                             neighbor_size=int(self.specific_options["neighborhood_size"]),
                                             weight_files_path=self.specific_options["weight_files_path"])
        
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.MOCELL.value:
            
            if self.specific_options["archive"] == AlgorithmParameters.MOCELL_ARCHIVE.CROWDING_DISTANCE.value:
                archive_operator = Archive.CrowdingDistanceArchive( maximum_size=int(self.specific_parameters["archive"]["maximum_size"]) )
                
            
            if self.specific_options["neighborhood"] == AlgorithmParameters.MOCELL_NEIGHBORHOOD.C9.value:
                neighborhood_operator = Neighborhood.C9(rows=int(self.specific_parameters["neighborhood"]["rows"]), columns=int(self.specific_parameters["neighborhood"]["columns"]))
                
            algorithm = Multiobjective.MOCell(problem=problem,
                                              population_size=population_size,
                                              neighborhood=neighborhood_operator,
                                              archive=archive_operator,
                                              mutation=composite_mutation,
                                              crossover=composite_crossover)
            
        
        return algorithm