
# -*- coding: utf-8 -*-



import sys

import copy
import random
import math
import time
import threading
import signal

from enum import Enum
from abc import *
from typing import List

from core.engine_parameters import EngineParameters
from core.problem_parameters import ProblemParameters
from core.algorithm_parameters import AlgorithmParameters
# from core.composite_problem import CompositeProblem
from jmetal.core.algorithm import Algorithm
from jmetal.util.solution import get_non_dominated_solutions
import jmetal.util.termination_criterion as jterm
import core.JMetalpy.composite_solution as CS


class OptimizationEngine:
    
    def __null_callback():
        pass
    
    def __init__(self,
                 engine_parameters: EngineParameters,
                 problem_parameters: ProblemParameters,
                 algorithm_parameters: AlgorithmParameters,
                 endOfGen_callback = __null_callback,
                 termination_callback = __null_callback,
                 paused_callback = __null_callback):
        
        self.engine_parameters = engine_parameters
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        self.endOfGen_callback = endOfGen_callback
        self.termination_callback = termination_callback
        self.paused_callback = paused_callback
        
        self.total_elapsed_time = 0.0
        self.algorithm_time = 0.0
        self.total_evaluations = 0
        self.algorithm = None
        
        # self.pause_semaphore = threading.Semaphore()
        self.pause_event = threading.Event()
        self.pause_event.set()
        
        
    def configure(self,
                  algorithm: Algorithm,
                  engine_parameters: EngineParameters,
                  keep_front: bool = False,
                  max_from_prev_front: float = 0.8):
        
        self.engine_parameters = engine_parameters
        
        if self.algorithm is None: #First configuration
            self.algorithm = algorithm
            self.algorithm.solutions = self.algorithm.create_initial_solutions()
            self.algorithm.solutions = self.algorithm.evaluate(algorithm.solutions)
            
        else: #Reconfigure, keeping previous solution
            new_alg = algorithm
            new_alg.solutions = self.algorithm.solutions
            self.algorithm = new_alg
    
    
    def __singlethread_optimizerTask__(self):
        
        if self.algorithm is None:
            raise Exception("__singlethread_optimizerTask__(): algorithm uninitialized")
        
        # self.total_evaluations += self.algorithm.evaluations
        
        self.algorithm.init_progress()
        self.algorithm.total_computing_time = 0.0
        self.problem.evaluations = 0
        
        self.last_execution_time_resume = time.time()
        self.acum_execution_time = 0.0
        
        """ Evaluation of initial solutions """
        prev_time = time.time()
        self.algorithm.solutions = self.algorithm.create_initial_solutions()
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.solutions)
        self.algorithm.total_computing_time += time.time() - prev_time
        
        """ Optimization loop """
        while not self.algorithm.stopping_condition_is_met():
            
            if not self.pause_event.is_set():
                self.paused_callback()
                self.pause_event.wait()
            
            prev_time = time.time()
            
            self.algorithm.step()
            self.algorithm.update_progress()
            
            self.algorithm.total_computing_time += time.time() - prev_time
            
            self.endOfGen_callback()
        
        self.termination_callback()
    
    
    def launch( self ):
        self.problem = self.problem_parameters.CompileProblem()
        termination_criterion = self.engine_parameters.compile_termination_criterion()
        evaluator = self.engine_parameters.compile_evaluator()
        self.algorithm = self.algorithm_parameters.compile_algorithm( problem=self.problem,
                                                                      termination_criterion=termination_criterion,
                                                                      evaluator=evaluator)
        
        self.optimizer_thread = threading.Thread( target=self.__singlethread_optimizerTask__ )
        self.optimizer_thread.start()
        
    def wait_termination(self):
        if self.optimizer_thread != None:
            self.optimizer_thread.join()
        
    def pause(self):
        self.pause_event.clear()
    
    def resume(self):
        self.pause_event.set()
    
    def get_front(self):
        return get_non_dominated_solutions( self.algorithm.get_result() )
    
    def get_solutions(self):
        return self.algorithm.get_result()
        
    def get_variables(self, solutions: List[CS.CompositeSolution]):
        return [ self.problem.recover_variables(x) for x in solutions ]
    
    
    
    