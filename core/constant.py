# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 01:07:50 2021

@author: Wayky
"""

import copy
import random
import math

from enum import Enum
from abc import *

from typing import List


class Constant:
    
    def __init__( self,
                  keyword: str,
                  value):
        
        self.keyword = keyword
        self.value = copy.deepcopy(value)



class FloatConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: float):
        
        super(FloatConstant,self).__init__( keyword=keyword, value=value )



class IntegerConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: int):
        
        super(IntegerConstant,self).__init__( keyword=keyword, value=value )
    

    
class BinaryConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: int):
        
        super(BinaryConstant,self).__init__( keyword=keyword, value=value )
        
        if value < 0 or value > 1:
            raise ValueError("%.__init__(): incorrect binary value: %s" % (type(self).__name__, value))
        

    
class BooleanConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: bool):
        
        super(BooleanConstant,self).__init__( keyword=keyword, value=value )
        


class PermutationConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: List[int]):
        
        super(PermutationConstant,self).__init__( keyword=keyword, value=value )
        
        if len(value) < 2:
            raise ValueError("%.__init__(): element list insufficient length: %s" % (type(self).__name__, len(value)))
        
        
class StringConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: str):
        
        super(StringConstant,self).__init__( keyword=keyword, value=value )
        
        
    