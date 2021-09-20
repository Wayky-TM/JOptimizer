# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 18:59:15 2021

@author: Wayky
"""

import sys
sys.path.append(r"./..")

import copy
import random
import math
import time

from core.evaluator import Evaluator


class EvaluatorPrueba(Evaluator):
    
    def __init__(self):
        super( EvaluatorPrueba, self ).__init__()
        self.number_of_variables = 4
        self.number_of_objectives = 2
    
    def evaluate(self, x, y, z, t):
        f1 = x
        g = 1.0 + 9.0*(y+z+t)/3.0
        h = 1 - math.sqrt(f1/g)
        return [x, g*h]