# -*- coding: utf-8 -*-


import sys
# sys.path.append(r"./..")

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
"""



"""
    Scalar variables
"""

class Variable:
    
    def __init__( self, keyword: str):    
        self.keyword = keyword
    
    @abstractmethod
    def rand(self):
        pass
    
    @abstractmethod
    def within_bounds( self, value ):
        pass
    
    
    

class FloatVariable(Variable):
    
    def __init__( self,
                  keyword: str,
                  lower_bound: float,
                  upper_bound: float):
        
        super(FloatVariable,self).__init__(keyword=keyword)
        
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def rand(self) -> float:
        return random.uniform(self.lower_bound, self.upper_bound)
    
    def within_bounds( self, value: float ):
        return (value >= self.lower_bound) and (value <= self.upper_bound)




class IntegerVariable(Variable):
    
    def __init__( self,
                  keyword: str,
                  lower_bound: int,
                  upper_bound: int):
               
        super(IntegerVariable,self).__init__(keyword=keyword)
        
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def rand(self):
        return random.randint(self.lower_bound, self.upper_bound)
    
    def within_bounds( self, value: int ):
        return (value >= self.lower_bound) and (value <= self.upper_bound)        
    
    


class DiscretizedFloatVariable(FloatVariable):
    
    def __init__( self,
                  keyword: str,
                  lower_bound: float,
                  upper_bound: float,
                  step: float):
        
        super(DiscretizedFloatVariable,self).__init__(keyword=keyword, lower_bound=lower_bound, upper_bound=upper_bound)
        
        if 2.0*step > upper_bound-lower_bound:
            raise ValueError( "%s.__init__(): parameter 'step' must be smaller than half of the variable interval" % (type(self).__name__) )
        
        self.step = step
        self.resolution = int( math.floor((upper_bound - lower_bound)/step) ) # Max value of the internal integer codification
        
    def rand(self):
        return float( random.randint(0, self.resolution-1) )*self.step + self.lower_bound
   
    def randint(self):
        return random.randint(0, self.resolution-1)
    
    def within_bounds_int( self, value: int ):
        return (value >= 0) and (value < self.resolution)
    
    def to_float( self, value: int ):
        return self.lower_bound + float(value)*self.step
    
    
    
    
class BinaryVariable(IntegerVariable):
    
    def __init__( self,
                  keyword: str):
        
        super( BinaryVariable, self ).__init__( keyword=keyword, lower_bound=0, upper_bound=1)
    
    
    
    
class BooleanVariable(Variable):
    
    def __init__( self,
                  keyword: str):
        
        self.keyword = keyword
        
    def rand(self):
        return bool(random.getrandbits(1))
    
    
    
    
class PermutationVariable(Variable):
    
    def __init__( self,
                  keyword: str,
                  elements: List[int]):
        
        super(PermutationVariable,self).__init__(keyword=keyword)
        
        if len(elements)<2:
            raise ValueError( "%s.__init__(): permutation variable of less than 2 elements" % (type(self).__name__) )
        
        self.elements = copy.deepcopy( elements )
        
    def rand(self):
        return random.shuffle( copy.deepcopy( self.elements ) )
    
    
    


"""
    Vector variables
"""
    

class VECTOR_TYPE(Enum):
    PYTHON="Python"
    NUMPY="Numpy"



    
class VectorVariable(Variable):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        super(VectorVariable, self).__init__(keyword=keyword)
        
        if length < 1:
            raise ValueError( "%s.__init__(): vector length must be greater than 0: %d" % (type(self).__name__, length) )
        
        if vector_type not in [ option for option in VECTOR_TYPE ]:
            raise ValueError( "%s.__init__(): unsopported vector type: %d" % (type(self).__name__, vector_type) )
        
        self.length=length
        self.vector_type = vector_type




class FloatVectorVariable( VectorVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: float,
                  upper_bound: float,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        super(FloatVectorVariable, self).__init__( keyword=keyword, length=length, vector_type=vector_type )
        
        # if len(lower_bound) != length or len(upper_bound) != length:
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): Invalid bounds" % (type(self).__name__) )
        
        self.lower_bound=lower_bound
        self.upper_bound=upper_bound
        
    def rand(self):
        v = [random.uniform(self.lower_bound, self.upper_bound) for i in range(self.length)]
        
        if self.vector_type == VECTOR_TYPE.NUMPY:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )

    

    
class IntegerVectorVariable( VectorVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: int,
                  upper_bound: int,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        super(IntegerVectorVariable, self).__init__( keyword=keyword, length=length, vector_type=vector_type )
        
        # if len(lower_bound) != length or len(upper_bound) != length:
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): Invalid bounds" % (type(self).__name__) )
        
        self.lower_bound=lower_bound
        self.upper_bound=upper_bound
        
    def rand(self):
        v = [random.randint(self.lower_bound, self.upper_bound) for i in range(self.length)]
        
        if self.vector_type == VECTOR_TYPE.NUMPY:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )
    
    
    
class DiscretizedVectorVariable( VectorVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  lower_bound: float,
                  upper_bound: float,
                  step: float,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        super(DiscretizedVectorVariable, self).__init__( keyword=keyword, length=length, vector_type=vector_type )
        
        # if len(lower_bound) != length or len(upper_bound) != length:
        if lower_bound >= upper_bound:
            raise ValueError( "%s.__init__(): Invalid bounds" % (type(self).__name__) )
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.step = step
        # self.resolution = [ int( math.floor((UB - LB)/step) ) for LB, UB in zip(self.lower_bound, self.upper_bound) ]
        self.resolution = int( math.floor((upper_bound - lower_bound)/step) )
        
    def rand(self):
        v = [ (float( random.randint(0, self.resolution[i]) )*self.step + self.lower_bound) for i in range(self.length)]
        
        if self.vector_type == VECTOR_TYPE.NUMPY:
            return np.array( v )
        
        return v
    
    def randint(self):
        v = [ random.randint(0, self.resolution-1) for i in range(self.length) ]
        
        if self.vector_type == VECTOR_TYPE.NUMPY:
            return np.array( v )
        
        return v
    
    def within_bounds( self, vector ):
        return all( [(value >= self.lower_bound) and (value <= self.upper_bound) for value in vector] )    

    def to_float( self, values: List[int] ):
        return [self.lower_bound + float(x)*self.step for x in values]


class BinaryVectorVariable( VectorVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        # super(BinaryVectorVariable, self).__init__(keyword=keyword, length=length, lower_bound=0, upper_bound=1, vector_type=vector_type)
        super(BinaryVectorVariable, self).__init__( keyword=keyword, length=length, vector_type=vector_type )
    
    
 
    
class BooleanVectorVariable( VectorVariable ):
    
    def __init__( self,
                  keyword: str,
                  length: int,
                  vector_type: VECTOR_TYPE = VECTOR_TYPE.PYTHON):
        
        super(BooleanVectorVariable, self).__init__( keyword=keyword, length=length, vector_type=vector_type )
        
        
    def rand(self):
        v = [ bool(random.getrandbits(1)) for i in range(self.length) ]
        
        if self.vector_type == VECTOR_TYPE.NUMPY:
            return np.array(v)
        
        return v
        
        
    