# -*- coding: utf-8 -*-


import sys
# sys.path.append(r"./..")

import copy
import random
import math
import yaml
import os

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict

import jmetal.core.problem as jprob
import jmetal.core.solution as jsol
import jmetal.core.operator as jop
import jmetal.operator.crossover as Crossover
import jmetal.operator.mutation as Mutation
import core.JMetalpy.composite_crossover as CC
import core.JMetalpy.composite_mutation as CM
import jmetal.operator.selection as Selection
import jmetal.algorithm.multiobjective as Multiobjective
import jmetal.algorithm.singleobjective as Singleobjective
import jmetal.util.aggregative_function as Aggregative
import jmetal.util.archive as Archive
import jmetal.util.neighborhood as Neighborhood
from jmetal.util.evaluator import Evaluator, SequentialEvaluator

import core.variable as var_types
from core.JMetalpy.composite_problem import CompositeProblem
from jmetal.util.termination_criterion import TerminationCriterion
# from core.null import NullCrossoverOperator, NullMutationOperator

import util.type_check as TC


class AlgorithmParameters:
    
    class SUPPORTED_ALGORITHMS(Enum):
        NSGAII="NSGAII"
        MOCELL="MOCELL"
        MOEAD="MOEAD"
        IBEA="IBEA"
        SPEA2="SPEA2"
        GA_MONO="GA (mono)"
        ANNEALING="Simulated annealing (mono)"
        LOCAL_SEARCH="Local search (mono)"
        
        
    
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
        WEIGHTED_SUM = "weighted_sum"
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
        self.general_parameters["population_size"] = "100"
        self.general_parameters["offspring_size"] = "100"
        
        """ Float """
        self.float_crossover_choice = AlgorithmParameters.FLOAT_CROSSOVER.SBX.value
        self.float_crossover_parameters = defaultdict(lambda: "")
        self.float_crossover_parameters["probability"] = "0.8"
        self.float_crossover_parameters["distribution_index"] = "20"
        
        self.float_mutation_choice = AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value
        self.float_mutation_parameters = defaultdict(lambda: "")
        self.float_mutation_parameters["probability"] = "0.1"
        self.float_mutation_parameters["distribution_index"] = "20"
        
        
        
        """ Int """
        self.int_crossover_choice = AlgorithmParameters.INT_CROSSOVER.INT_SBX.value
        self.int_crossover_parameters = defaultdict(lambda: "")
        self.int_crossover_parameters["probability"] = "0.8"
        self.int_crossover_parameters["distribution_index"] = "20"
        
        self.int_mutation_choice = AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value
        self.int_mutation_parameters = defaultdict(lambda: "")
        self.int_mutation_parameters["probability"] = "0.1"
        self.int_mutation_parameters["distribution_index"] = "20"
        
        
        """ Binary """
        self.binary_crossover_choice = AlgorithmParameters.BINARY_CROSSOVER.SPX.value
        self.binary_crossover_parameters = defaultdict(lambda: "")
        self.binary_crossover_parameters["probability"] = "0.8"
        
        self.binary_mutation_choice = AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value
        self.binary_mutation_parameters = defaultdict(lambda: "")
        self.binary_mutation_parameters["probability"] = "0.1"
        
        
        """ Permutation """
        self.permutation_crossover_choice = AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value
        self.permutation_crossover_parameters = defaultdict(lambda: "")
        self.permutation_crossover_parameters["probability"] = "0.8"
        
        self.permutation_mutation_choice = AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP.value
        self.permutation_mutation_parameters = defaultdict(lambda: "")
        self.permutation_mutation_parameters["probability"] = "0.1"
        
        
        """ Selection """
        self.selection_choice = AlgorithmParameters.SELECTION.BINARY_TOURNAMENT.value
        self.selection_parameters = defaultdict(lambda: "")
        
        
        """ Algorithm-specific """
        self.specific_options = defaultdict(lambda: "")
        self.specific_parameters = defaultdict(lambda: defaultdict(lambda: ""))
        
        
        
    """ Generates an Algorithm object based on algorithm and problem parameters """
    def compile_algorithm(self,
                          problem: CompositeProblem,
                          termination_criterion: TerminationCriterion,
                          evaluator: Evaluator = SequentialEvaluator()):
        
        crossover_operators = {}
        mutation_operators = {}
        
        
        """
            Float
        """
        # if problem.include_float or problem.include_floatVector:
        if problem.include_float:
            
            if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                                   AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:
            
                """ Crossover """
                if self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION.value:
                    float_crossover = Crossover.DifferentialEvolutionCrossover( CR=float(self.float_crossover_parameters["probability"]), F=float(self.float_crossover_parameters["F"]))
                    
                elif self.float_crossover_choice == AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
                    float_crossover = Crossover.SBXCrossover( probability=float(self.float_crossover_parameters["probability"]), distribution_index=float(self.float_crossover_parameters["distribution_index"]))
                    
                crossover_operators["float_crossover"] = float_crossover
            
            """ Mutation """
            if self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value:
                float_mutation = Mutation.PolynomialMutation( probability=float(self.float_mutation_parameters["probability"]), distribution_index=float(self.float_mutation_parameters["distribution_index"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM.value:
                float_mutation = Mutation.SimpleRandomMutation( probability=float(self.float_mutation_parameters["probability"]) )
                
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.UNIFORM.value:
                float_mutation = Mutation.UniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]) )
            
            elif self.float_mutation_choice == AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM.value:
                float_mutation = Mutation.NonUniformMutation(probability=float(self.float_mutation_parameters["probability"]), perturbation=float(self.float_mutation_parameters["perturbation"]), max_iterations=int(self.float_mutation_parameters["max_iterations"]) )
            
            
            mutation_operators["float_mutation"] = float_mutation
            
            
        """
            Int/discr
        """
        # if problem.include_integer or problem.include_discretized or problem.include_integerVector or problem.include_discretizedVector:
        if problem.include_integer:
            
            if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                                   AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:
            
                """ Crossover """
                if self.int_crossover_choice == AlgorithmParameters.INT_CROSSOVER.INT_SBX.value:
                    integer_crossover = Crossover.IntegerSBXCrossover( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
            
                crossover_operators["integer_crossover"] = integer_crossover
            
            """ Mutation """
            if self.int_mutation_choice == AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value:
                integer_mutation = Mutation.IntegerPolynomialMutation( probability=float(self.int_crossover_parameters["probability"]), distribution_index=float(self.int_crossover_parameters["distribution_index"]) )
       
            
            mutation_operators["integer_mutation"] = integer_mutation
        
        """
            Binary
        """
        if problem.include_binary:
            
            if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                                   AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:
            
                """ Crossover """
                if self.binary_crossover_choice == AlgorithmParameters.BINARY_CROSSOVER.SPX.value:
                    binary_crossover = Crossover.SPXCrossover( probability=float(self.binary_crossover_parameters["probability"]) )
                    
                crossover_operators["binary_crossover"] = binary_crossover
            
            """ Mutation """
            if self.binary_mutation_choice == AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value:
                binary_mutation = Mutation.BitFlipMutation( probability=float(self.binary_mutation_parameters["probability"]) )
            
            mutation_operators["binary_mutation"] = binary_mutation
        
        
        
        """
            Permutation
        """
        if problem.include_permutation:
            
            if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                                   AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:
            
                """ Crossover """
                if self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.CXC.value:
                    permutation_crossover = Crossover.CXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
                
                elif self.permutation_crossover_choice == AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value:
                    permutation_crossover = Crossover.PMXCrossover( probability=float(self.permutation_crossover_parameters["probability"]) )
                    
                crossover_operators["permutation_crossover"] = permutation_crossover
            
            """ Mutation """
            if self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.PERMUTATION_SWAP.value:
                permutation_mutation = Mutation.PermutationSwapMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            elif self.permutation_mutation_choice == AlgorithmParameters.PERMUTATION_MUTATION.SCRAMBLE_MUTATION.value:
                permutation_mutation = Mutation.ScrambleMutation( probability=float(self.permutation_mutation_parameters["probability"]) )
            
            
            mutation_operators["permutation_mutation"] = permutation_mutation
            
        composite_crossover = CC.CompositeCrossover( **crossover_operators )
        composite_mutation = CM.CompositeMutation( **mutation_operators )
        
        """
            Selection
        """
        if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value,
                               AlgorithmParameters.SUPPORTED_ALGORITHMS.IBEA.value,
                               AlgorithmParameters.SUPPORTED_ALGORITHMS.SPEA2.value,
                               AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                               AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:
            
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
            

        if self.choice not in [AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value,
                               AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value]:            
            population_size = int(self.general_parameters["population_size"])
        
        if self.choice in [AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value,
                           AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value,
                           AlgorithmParameters.SUPPORTED_ALGORITHMS.IBEA.value,
                           AlgorithmParameters.SUPPORTED_ALGORITHMS.SPEA2.value]:
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
                                              selection=selection_operator,
                                              termination_criterion=termination_criterion,
                                              population_evaluator=evaluator)
            
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value:
            
            algorithm = Singleobjective.GeneticAlgorithm(problem=problem,
                                                         population_size=population_size,
                                                         offspring_population_size=offspring_size,
                                                         mutation=composite_mutation,
                                                         crossover=composite_crossover,
                                                         selection=selection_operator,
                                                         termination_criterion=termination_criterion,
                                                         population_evaluator=evaluator)
            
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.IBEA.value:
            
            kappa = float(self.specific_options["kappa"])
            
            algorithm = Multiobjective.IBEA(problem=problem,
                                            population_size=population_size,
                                            offspring_population_size=offspring_size,
                                            mutation=composite_mutation,
                                            crossover=composite_crossover,
                                            kappa=kappa,
                                            termination_criterion=termination_criterion,
                                            population_evaluator=evaluator)
            
        
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.SPEA2.value:
            
            algorithm = Multiobjective.SPEA2(problem=problem,
                                             population_size=population_size,
                                             offspring_population_size=offspring_size,
                                             mutation=composite_mutation,
                                             crossover=composite_crossover,
                                             termination_criterion=termination_criterion,
                                             population_evaluator=evaluator)
            
        
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.ANNEALING.value:
            
            algorithm = Singleobjective.SimulatedAnnealing(problem=problem,
                                                         mutation=composite_mutation,
                                                         termination_criterion=termination_criterion )
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.LOCAL_SEARCH.value:
            
            algorithm = Singleobjective.LocalSearch(problem=problem,
                                                    mutation=composite_mutation,
                                                    termination_criterion=termination_criterion )
            
            
        elif self.choice == AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value:
            
            if self.specific_options["aggregative"] == AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.TSCHEBYCHEFF.value:
                aggregative_function = Aggregative.Tschebycheff( dimension=int(self.specific_parameters["aggregative"]["dimension"]) )
                
            elif self.specific_options["aggregative"] == AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.WEIGHTED_SUM.value:
                aggregative_function = Aggregative.WeightedSum()
            
            algorithm = Multiobjective.MOEAD(problem=problem,
                                             population_size=population_size,
                                             mutation=composite_mutation,
                                             crossover=composite_crossover,
                                             aggregative_function=aggregative_function,
                                             neighbourhood_selection_probability=float(self.specific_options["neighborhood_selection_probability"]),
                                             max_number_of_replaced_solutions=int(self.specific_options["max_number_of_replaced_solutions"]),
                                             neighbor_size=int(self.specific_options["neighborhood_size"]),
                                             weight_files_path=self.specific_options["weight_files_path"],
                                             termination_criterion=termination_criterion,
                                             population_evaluator=evaluator)
        
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
                                              crossover=composite_crossover,
                                              termination_criterion=termination_criterion,
                                              population_evaluator=evaluator)
            
        
        return algorithm
    
    def save_state(self,
                   dir_path: str,
                   file_name: str = "algorithm_parameters.yaml"):
        
        if TC.is_dir( dir_path ):
            
            output = {}
            
            output["choice"] = self.choice
            
            output["general_parameters"] = {}
            
            for key, value in self.general_parameters.items():
                output["general_parameters"][key] = value
                
            """ Float """
            output["float"] = {}
            output["float"]["crossover"] = {}
            output["float"]["crossover"]["choice"] = self.float_crossover_choice
            output["float"]["crossover"]["parameters"] = {}
            
            output["float"]["mutation"] = {}
            output["float"]["mutation"]["choice"] = self.float_mutation_choice
            output["float"]["mutation"]["parameters"] = {}
            
            for key, value in self.float_crossover_parameters.items():
                output["float"]["crossover"]["parameters"][key] = value
                
            for key, value in self.float_mutation_parameters.items():
                output["float"]["mutation"]["parameters"][key] = value
                
            """ Integer """
            output["integer"] = {}
            output["integer"]["crossover"] = {}
            output["integer"]["crossover"]["choice"] = self.int_crossover_choice
            output["integer"]["crossover"]["parameters"] = {}
            
            output["integer"]["mutation"] = {}
            output["integer"]["mutation"]["choice"] = self.int_mutation_choice
            output["integer"]["mutation"]["parameters"] = {}
            
            for key, value in self.int_crossover_parameters.items():
                output["integer"]["crossover"]["parameters"][key] = value
                
            for key, value in self.int_mutation_parameters.items():
                output["integer"]["mutation"]["parameters"][key] = value
                
            """ Binary """
            output["binary"] = {}
            output["binary"]["crossover"] = {}
            output["binary"]["crossover"]["choice"] = self.binary_crossover_choice
            output["binary"]["crossover"]["parameters"] = {}
            
            output["binary"]["mutation"] = {}
            output["binary"]["mutation"]["choice"] = self.binary_mutation_choice
            output["binary"]["mutation"]["parameters"] = {}
            
            for key, value in self.binary_crossover_parameters.items():
                output["binary"]["crossover"]["parameters"][key] = value
                
            for key, value in self.binary_mutation_parameters.items():
                output["binary"]["mutation"]["parameters"][key] = value
                
            """ Permutation """
            output["permutation"] = {}
            output["permutation"]["crossover"] = {}
            output["permutation"]["crossover"]["choice"] = self.permutation_crossover_choice
            output["permutation"]["crossover"]["parameters"] = {}
            
            output["permutation"]["mutation"] = {}
            output["permutation"]["mutation"]["choice"] = self.permutation_mutation_choice
            output["permutation"]["mutation"]["parameters"] = {}
            
            for key, value in self.permutation_crossover_parameters.items():
                output["permutation"]["crossover"]["parameters"][key] = value
                
            for key, value in self.permutation_mutation_parameters.items():
                output["permutation"]["mutation"]["parameters"][key] = value
                
            """ Selection """
            output["selection"] = {}
            output["selection"]["choice"] = self.selection_choice
            output["selection"]["parameters"] = {}
            
            for key, value in self.selection_parameters.items():
                output["selection"]["parameters"][key] = value
             
                
            """ Algorithm specific """
            output["specific"] = {}
            output["specific"]["options"] = {}
            output["specific"]["parameters"] = {}
            
            for key, value in self.specific_options.items():
                output["specific"]["options"][key] = value
                
            for key, value in self.specific_parameters.items():
                parameter_dict = {}
                
                for key1, value1 in value.items():
                    parameter_dict[key1] = value1
                    
                output["specific"]["parameters"][key] = parameter_dict
                
                
            with open( os.path.join(dir_path, file_name), 'w') as file:
                documents = yaml.dump(output, file)
        
        else:
            raise ValueError("Path '%s' is not a valid directory" % (dir_path))    
    
    def load_state(self,
                   dir_path: str,
                   file_name: str = "algorithm_parameters.yaml"):
        
        if TC.is_file( os.path.join(dir_path, file_name) ):
            
            yaml_file = open( os.path.join(dir_path, file_name), 'r')
            yaml_content = yaml.safe_load(yaml_file)
            
            """ Algorithm choice """
            self.choice = yaml_content["choice"]
            
            """ General parameters """
            for key, value in yaml_content["general_parameters"].items():
                self.general_parameters[key] = value
            
            """ Float """
            self.float_crossover_choice = yaml_content["float"]["crossover"]["choice"]
            
            for key, value in yaml_content["float"]["crossover"]["parameters"].items():
                self.float_crossover_parameters[key] = value
                
            self.float_mutation_choice = yaml_content["float"]["mutation"]["choice"]
            
            for key, value in yaml_content["float"]["mutation"]["parameters"].items():
                self.float_mutation_parameters[key] = value
                
            """ Integer """
            self.int_crossover_choice = yaml_content["integer"]["crossover"]["choice"]
            
            for key, value in yaml_content["integer"]["crossover"]["parameters"].items():
                self.int_crossover_parameters[key] = value
                
            self.int_mutation_choice = yaml_content["integer"]["mutation"]["choice"]
            
            for key, value in yaml_content["integer"]["mutation"]["parameters"].items():
                self.int_mutation_parameters[key] = value
                
            """ Binary """
            self.binary_crossover_choice = yaml_content["binary"]["crossover"]["choice"]
            
            for key, value in yaml_content["binary"]["crossover"]["parameters"].items():
                self.binary_crossover_parameters[key] = value
                
            self.binary_mutation_choice = yaml_content["binary"]["mutation"]["choice"]
            
            for key, value in yaml_content["binary"]["mutation"]["parameters"].items():
                self.binary_mutation_parameters[key] = value
                
            """ Permutation """
            self.permutation_crossover_choice = yaml_content["permutation"]["crossover"]["choice"]
            
            for key, value in yaml_content["permutation"]["crossover"]["parameters"].items():
                self.permutation_crossover_parameters[key] = value
                
            self.permutation_mutation_choice = yaml_content["permutation"]["mutation"]["choice"]
            
            for key, value in yaml_content["permutation"]["mutation"]["parameters"].items():
                self.permutation_mutation_parameters[key] = value
                
            """ Selection """
            self.selection_choice = yaml_content["selection"]["choice"]
            
            for key, value in yaml_content["selection"]["parameters"].items():
                self.selection_parameters[key] = value
            
            """ Algorithm-specific """
            # output["specific"]["options"] = {}
            # output["specific"]["parameters"] = {}
            
            for key, value in yaml_content["specific"]["options"].items():
                self.specific_options[key] = value
                
            for key, value in yaml_content["specific"]["parameters"].items():
                parameter_dict = defaultdict( lambda: "" )
                
                for key1, value1 in value.items():
                    parameter_dict[key1] = value1
                    
                self.specific_parameters[key] = parameter_dict
                
            
        else:
            raise ValueError("File '%s' is not a valid file" % (os.path.join(dir_path, file_name)))