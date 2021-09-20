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
    
    def __init__(self,
                 problem: CompositeProblem,
                 endOfGen_callback = None,
                 termination_callback = None):
        
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
    
    
    def __stats_update(self):
        pass
        
    
    def __singlethread_optimizerTask__(self,
                                       termination_criterion: jterm.TerminationCriterion):
        
        ddd
        
        for i in range(100):
            
            update_runtime_statistics()
            
        termination_callback()
    
    
    def launch( self,
                termination_criterion: jterm.TerminationCriterion):
        
        self.stop_var = 0
        self.x = threading.Thread( target=self.__singlethread_optimizerTask__, args=[termination_criterion] )
        self.x.start()
        
        
        
    def pause(self):
        self.stop_var = 1
    
    
    def get_front(self):
        pass
    
    
    def update_runtime_statistics():
        endOfGen_callback()