# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 20:00:36 2021

@author: Wayky
"""


import sys
sys.path.append(r"../.")

import copy
import random
import math
import time
import threading
import signal

from enum import Enum
from abc import *

from core.engine_parameters import EngineParameters
from core.composite_problem import CompositeProblem
from jmetal.core.algorithm import Algorithm
import jmetal.util.termination_criterion as jterm


class OptimizationEngine:
    
    class TerminationCriterion(Enum):
        EVALUATIONS=1
        TIME=1
    
    def __null_callback():
        pass
    
    def __init__(self,
                 problem: CompositeProblem,
                 endOfGen_callback = __null_callback,
                 termination_callback = __null_callback):
        
        self.problem = problem
        self.endOfGen_callback = endOfGen_callback
        self.termination_callback = termination_callback
        
        self.total_elapsed_time = 0.0
        self.algorithm_time = 0.0
        self.total_evaluations = 0
        self.algorithm = None
        
        self.pause_semaphore = threading.Semaphore()
        
        
        
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
    
    
    def __singlethread_optimizerTask__(self,
                                       termination_criterion: jterm.TerminationCriterion):
        
        if self.algorithm is None:
            raise Exception("__singlethread_optimizerTask__(): algorithm uninitialized")
        
        self.algorithm.observable.deregister( self.algorithm.termination_criterion )
        self.algorithm.termination_criterion = termination_criterion
        self.algorithm.observable.register( self.algorithm.termination_criterion )
        
        self.total_evaluations += self.algorithm.evaluations
        
        self.algorithm.init_progress()
        
        self.algorithm.start_computing_time = time.time()
        
        while not self.algorithm.stopping_condition_is_met():
            self.pause_semaphore.acquire()
            
            self.algorithm.step()
            self.algorithm.update_progress()
            self.endOfGen_callback()
            
            self.pause_semaphore.release()
        
        self.algorithm.total_computing_time = time.time() - self.algorithm.start_computing_time
        
        self.termination_callback()
    
    
    def launch( self ):
    
        
        self.optimizer_thread = threading.Thread( target=self.__singlethread_optimizerTask__, args=[termination_criterion] )
        self.optimizer_thread.start()
        
    def wait_termination(self):
        if self.optimizer_thread != None:
            self.optimizer_thread.join()
        
    def pause(self):
        if self.pause_semaphore._value > 0:
            self.pause_semaphore.acquire( blocking=False )
    
    def resume(self):
        if self.pause_semaphore._value == 0:
            self.pause_semaphore.release( blocking=False )
    
    
    def get_front(self):
        solutions = self.algorithm.get_result()
        return [ self.problem.recover_variables(x) for x in solutions ]
    
    
    