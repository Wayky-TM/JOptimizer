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

"""
    Defined in [-5.12,5.12]
"""
def Rastigin( *args ):
    A=10.0
    return (A*len(args) + sum([ (x*x - A*math.cos(2*math.pi*x)) for x in args ]))

