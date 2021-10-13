# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 20:33:23 2021

@author: Wayky
"""

import sys
sys.path.append(r"./../..")

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter.ttk import Notebook
    from tkinter import messagebox    
    from tkinter import scrolledtext
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List

from interface.parameter import Parameter

class ParameterBinding:
    
    def __init__( self,
                  parameter: Parameter,
                  widget_read_lambda,
                  variable_store_lambda,
                  variable_read_lambda = lambda *args: None,
                  widget_update_lambda = lambda *args: None,
                  error_set_lambda = lambda *args: None,
                  error_reset_lambda = lambda *args: None):
        
        self.parameter = parameter
        self.widget_read_lambda = widget_read_lambda
        self.variable_store_lambda = variable_store_lambda
        self.variable_read_lambda = variable_read_lambda
        self.widget_update_lambda = widget_update_lambda
        self.error_set_lambda = error_set_lambda
        self.error_reset_lambda = error_reset_lambda
        
        
    def error_check( self ):
        self.parameter.value = self.widget_read_lambda()
        error_list = self.parameter.error_check()

        if len(error_list)>0:
            self.error_set_lambda()
        
        else:
            self.error_reset_lambda()
        
        return error_list
    
    def clear_error(self):
        self.error_reset_lambda()
        
    def store_value( self ):
        self.variable_store_lambda( self.parameter.value )
        
    def load_value(self):
        self.widget_update_lambda( self.variable_read_lambda )
        

class EntryInvalidator:
    
    def __init__(self, entry: tk.Entry):
        self.entry = entry
        
    def __call__(self):
        self.entry.config({"background":"#ffc7c8"})
        
class EntryValidator:
    
    def __init__(self, entry: tk.Entry):
        self.entry = entry
        
    def __call__(self):
        self.entry.config({"background":"White"})
        
        