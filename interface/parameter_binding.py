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

    def __default_
    
    def __init__( self,
                  parameter: Parameter,
                  widget_read_lambda,
                  variable_store_lambda,
                  error_set_lambda = lambda *args: None,
                  error_reset_lambda = lambda *args: None):
        
        self.parameter = parameter
        self.widget_read_lambda = widget_read_lambda
        self.variable_store_lambda = variable_store_lambda
        
        
    # def error_check( self, error_list: List[str] ):
        
    #     self.parameter.value = self.widget_read_lambda()
    #     self.parameter.error_check( error_list=error_list )
        
    def error_check( self ):
        self.parameter.value = self.widget_read_lambda()
        error_list = self.parameter.error_check()

        if len(error_list)>0:
            
        
        return error_list
    
    def clear_error(self):
        self.error_reset_lambda()
        
    def store_value( self ):
        self.variable_store_lambda( self.parameter.value )
        
        