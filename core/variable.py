# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 01:07:50 2021

@author: Wayky
"""

import sys
sys.path.append(r"./..")

import copy
import random
import math
import numpy as np

from enum import Enum
from abc import *
from typing import List

"""
    TODO:
        -Multiple lower & upper bounds
        -Inheritance
"""

class FloatVariable:
    
    def __init__( self,
                  keyword: str,
                  lower_bound: float,
                  upper_bound: float,
                  name: str = ""):
                
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
        
        self.name = name
        self.keyword = keyword
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def rand(self):
        return random.uniform(self.lower_bound, self.upper_bound)
    
    def within_bounds( self, value: float ):
        return (value >= self.lower_bound) and (value <= self.upper_bound)


class IntegerVariable:
    
    def __init__( self,
                  keyword: str,
                  lower_bound: int,
                  upper_bound: int,
                  name: str = ""):
                
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
        
        self.name = name
        self.keyword = keyword
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def rand(self):
        return random.randint(self.lower_bound, self.upper_bound)
    
    def within_bounds( self, value: int ):
        return (value >= self.lower_bound) and (value <= self.upper_bound)        
    
    

class DiscretizedFloatVariable:
    
    def __init__( self,
                  keyword: str,
                  lower_bound: float,
                  upper_bound: float,
                  step: float,
                  name: str = ""):
                
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
        
        self.name = name
        self.keyword = keyword
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.step = step
        
        self.resolution = int( math.floor((upper_bound - lower_bound)/step) )
        
    def rand(self):
        return float( random.randint(0, self.resolution-1) )*self.step + self.lower_bound
    
    def randint(self):
        return random.randint(0, self.resolution-1)
    
    def within_bounds( self, value: float ):
        return (value >= self.lower_bound) and (value <= self.upper_bound)
    
    
    
class BinaryVariable(IntegerVariable):
    
    def __init__( self,
                  keyword: str,
                  name: str = ""):
        
        super( BinaryVariable, self ).__init__( keyword=keyword, lower_bound=0, upper_bound=1, name=name )
    
    
class PermutationVariable:
    
    def __init__( self,
                  keyword: str,
                  elements: List[int],
                  name: str = ""):
        
        if len(elements)<2:
            raise ValueError( "%s.__init__(): permutation variable of less than 2 elements" % (type(self).__name__) )
        
        self.name = name
        self.keyword = keyword
        self.elements = copy.deepcopy( elements )
        
    def rand(self):
        return random.shuffle( copy.deepcopy( self.elements ) )
    
    
    
class VECTOR_TYPE(Enum):
    PYTHON="Python"
    NUMPY="Numpy"
    
class MATRIX_TYPE(Enum):
    PYTHON="Python"
    NUMPY="Numpy"

    
class FloatVectorVariable( FloatVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: float,
                  upper_bound: float,
                  name: str = "",
                  vector_type: str = VECTOR_TYPE.PYTHON.value):
        
        super(FloatVectorVariable, self).__init__( keyword=keyword, lower_bound=lower_bound, upper_bound=upper_bound, name=name )
        
        if length < 2:
             raise ValueError( "Vector of invalid length: %d" % (length) )
        
        self.vector_type = vector_type
        self.length = length
        
    def rand(self):
        v = [random.uniform(self.lower_bound, self.upper_bound) for i in range(self.length)]
        
        if self.vector_type = VECTOR_TYPE.NUMPY.value:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )
    
    
    
class IntegerVectorVariable( IntegerVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: int,
                  upper_bound: int,
                  name: str = "",
                  vector_type: str = VECTOR_TYPE.PYTHON.value):
        
        super(IntegerVectorVariable, self).__init__( keyword=keyword, lower_bound=lower_bound, upper_bound=upper_bound, name=name )
        
        if length < 2:
             raise ValueError( "Vector of invalid length: %d" % (length) )
        
        self.vector_type = vector_type
        self.length = length
        
    def rand(self):
        v = [random.randint(self.lower_bound, self.upper_bound) for i in range(self.length)]
        
        if self.vector_type = VECTOR_TYPE.NUMPY.value:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )
    
    
class DiscretizedVectorVariable( DiscretizedFloatVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: float,
                  upper_bound: float,
                  step: float,
                  name: str = "",
                  vector_type: str = VECTOR_TYPE.PYTHON.value):
        
        super(DiscretizedVectorVariable, self).__init__( keyword=keyword, lower_bound=lower_bound, upper_bound=upper_bound, step=step, name=name )
        
        if length < 2:
             raise ValueError( "Vector of invalid length: %d" % (length) )
        
        self.vector_type = vector_type
        self.length = length
        
    def rand(self):
        v = [ (float( random.randint(0, self.resolution-1) )*self.step + self.lower_bound) for i in range(self.length)]
        
        if self.vector_type = VECTOR_TYPE.NUMPY.value:
            return np.array( v )
        
        return v
    
    def randint(self):
        v = [ random.randint(0, self.resolution-1) for i in range(self.length) ]
        
        if self.vector_type = VECTOR_TYPE.NUMPY.value:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )    

    
    