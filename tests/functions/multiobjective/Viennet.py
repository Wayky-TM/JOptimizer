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
    x >= -3, y <= 3
"""

def Viennet( x, y ):
    
    def f1( x,y ):
        return 0.5*(x*x+y*y) + math.sin(x*x + y*y)
    
    def f2( x,y ):
        return (((3*x-2*y+4)**2)/8) + (((x-y+1)**2)/27) + 15
    
    def f3( x,y ):
        return 1/(x*x + y*y +1) - 1.1*math.exp(-(x*x + y*y))
    
    return [f1(x,y),f2(x,y),f3(x,y)]

