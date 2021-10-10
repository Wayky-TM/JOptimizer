# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 18:35:45 2021

@author: Wayky
"""

import imp
import os
import sys
sys.path.append(r"./../..")

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    # from tkinter import *
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
from pathlib import Path
import inspect

import core.variable as variable_types
import core.constant as constant_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from core.evaluator import Evaluator
from util.type_check import is_integer, is_float, to_integer
from util.string_utils import remove_whitespaces

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator



class StatsTable(ttk.Treeview):
    
    def __init__(self, master, *args, **kwargs):
        self.headers = ["Value"]
        super(StatsTable, self).__init__(master=master, *args, columns=self.headers, selectmode="extended", **kwargs)
    
        self.heading("#0", text="Stat")
        self.column("#0", minwidth=100, width=200, stretch=tk.NO)
        
        self.heading( "Value", text="Value" )
        self.column( "Value", minwidth=100, width=200, stretch=tk.NO )
        
        self.stats_lambdas = {}
        
    def add_stat(self, name: str, update_lambda):
        #TODO: check if item already exists
        self.stats_lambdas[name] = update_lambda
        self.insert('', 'end', text=name, values=("-"))
        
    
    def update_stats(self):
        for iid in self.get_children():
            text = self.item(iid, option='text')
            self.item(iid, text=text, value=( str( self.stats_lambdas[text]() ) ))
            
        


# class MulticellTable():