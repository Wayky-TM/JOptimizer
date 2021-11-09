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
        value,
        name: str = ""):
        pass

class FloatConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: float,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value= value


class IntegerConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: int,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value = value
    

    
class BinaryConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: bool,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value = value
    

class PermutationConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: List[int],
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value = copy.deepcopy(value)
        
        
class StringConstant(Constant):
    
    def __init__( self,
                  keyword: str,
                  value: str,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value = value
        
        
    