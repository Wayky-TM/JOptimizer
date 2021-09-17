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



class FloatConstant:
    
    def __init__( self,
                  keyword: str,
                  value: float,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value= value



class IntegerConstant:
    
    def __init__( self,
                  keyword: str,
                  value: int,
                  name: str = ""):
        
        self.name = name
        self.keyword = keyword
        self.value = value
    

    
    
    
    