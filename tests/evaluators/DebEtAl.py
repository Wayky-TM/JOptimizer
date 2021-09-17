# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 21:13:55 2021

@author: Wayky
"""

import sys
sys.path.append(r"../.")

import copy
import random
import math

from enum import Enum
from abc import *

from core.evaluator import Evaluator


class EvaluatorTemplate(Evaluator):
    
    def __init__(self, number_of_variables : int):
        self.number_of_variables = number_of_variables
        self.number_of_objectives = 2
        
    def g( self, *args ):
        return (1 + sum(args[1:])*9.0/29.0)#float(len(solution.variables)-1))
    
    @abstractmethod
    def h( self, x: float, y: float ):
        pass
    
    def f1( self, *args ):
        return args[0]
    
    def f2( self, *args ):
        return self.g(*args) * self.h( self.f1(*args), self.g(*args) )
        
    def evaluate( self, **kwargs ):
        args = [ value for key, value in kwargs.items() ]
        
        return [self.f1(*args), self.f2(*args)]


class Test1Evaluator(EvaluatorTemplate):
    
    def h( self, x: float, y: float ):
        return ( 1 - math.sqrt(x/y) )
    
    
class Test2Evaluator(EvaluatorTemplate):
    
    def h( self, x: float, y: float ):
        return ( 1 - (x/y)**2 )
    
    
class Test3Evaluator(EvaluatorTemplate):
    
    def h( self, x: float, y: float ):
        return ( 1 - math.sqrt(x/y) - (x/y)*math.sin( 10.0*math.pi*x ) )
    
    

    
    







