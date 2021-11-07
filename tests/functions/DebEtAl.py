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



    
def __g__( *args ):
    return (1 + sum(args[1:])*9.0/29.0)


def __f1__( *args ):
        return args[0]
    
def __f2__( h, *args ):
    return __g__(*args) * h( __f1__(*args), __g__(*args) )


def Test1( *args ):
    
    def __h1__( x: float, y: float ):
        return ( 1 - math.sqrt(x/y) )
    
    return [__f1__(*args), __f2__(__h1__,*args)]


def Test2( *args ):
    
    def __h2__( x: float, y: float ):
        return ( 1 - (x/y)**2 )
    
    return [__f1__(*args), __f2__(__h2__,*args)]
    
    
def Test3( *args ):
    
    def __h3__( x: float, y: float ):
        return ( 1 - math.sqrt(x/y) - (x/y)*math.sin( 10.0*math.pi*x ) )

    return [__f1__(*args), __f2__(__h3__,*args)]




