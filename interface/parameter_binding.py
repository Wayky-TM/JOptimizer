# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 20:33:23 2021

@author: Wayky
"""

import sys
sys.path.append(r"./../..")

from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List

from interface.parameter import Parameter

class ParameterBinding:
    
    def __init__( self, parameter: Parameter, widget_read_lambda, variable_store_lambda ):
        
        self.parameter = parameter
        self.widget_read_lambda = widget_read_lambda
        self.variable_store_lambda = variable_store_lambda
        
        
    def error_check( self, error_list: List[str] ):
        
        self.parameter.value = self.widget_read_lambda()
        self.parameter.error_check( error_list=error_list )
        
    def store_value( self ):
        self.variable_store_lambda( self.parameter.value )
        
        