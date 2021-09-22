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


from core.composite_problem import CompositeProblem
from jmetal.core.algorithm import Algorithm
from jmetal.util.termination_criterion as jterm


class OptimizationEngine:
    
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
        
        self.algorithm = None
        
        
        
    def configure(self,
                  algorithm: Algorithm,
                  keep_front: bool = False,
                  max_from_prev_front: float = 0.8):
        
        if self.algorithm is None: #First configuration
            pass
        else:
            pass
        
        self.algorithm = algorithm
    
    
    def __stats_update(self):
        pass
        
    
    def __update_time(self):
        pass
    
    
    def __update_evaluations(self):
        pass
    
    
    def __singlethread_optimizerTask__(self,
                                       termination_criterion: jterm.TerminationCriterion):
        
        
        if self.algorithm is None:
            raise Exception("__singlethread_optimizerTask__(): algorithm uninitialized")
        
        self.algorithm.termination_criterion = termination_criterion
        
        prev_evaluations = self.algorithm.evaluations    
        self.algorithm.evaluations = 0
        
        while not self.algorithm.stopping_condition_is_met():
            self.pause_semaphore.acquire()
            
            algorithm.step()
            algorithm.update_progress()
            self.endOfGen_callback()
            
            self.pause_semaphore.release()
        
        
        self.algorithm.evaluations += prev_evaluations
        
        update_runtime_statistics()
            
        self.termination_callback()
    
    
    def launch( self,
                termination_criterion: jterm.TerminationCriterion):
        
        self.pause_semaphore = threading.Semaphore()
        
        self.stop_var = 0
        self.x = threading.Thread( target=self.__singlethread_optimizerTask__, args=[termination_criterion] )
        self.x.start()
        
        
        
    def pause(self):
        if self.pause_semaphore._value > 0:
            self.pause_semaphore.acquire()
    
    def resume(self):
        if self.pause_semaphore._value == 0:
            self.pause_semaphore.release()
    
    
    def get_front(self):
        solutions = self.algorithm.get_result()
        return [ self.problem.recover_variables(x) for x in solutions ]
    
    
    