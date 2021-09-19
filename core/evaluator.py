# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 18:55:58 2021

@author: Wayky
"""

import sys
sys.path.append(r"./..")

import copy
import random
import math

from enum import Enum
from abc import *



class Evaluator(ABC):
    
    def __init__(self):
        self.number_of_variables = 1
        self.number_of_objectives = 1
    
    @abstractmethod
    def evaluate(self, **kwargs):
        pass
    
    def close(self):
        pass