# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:46:16 2021

@author: Álvaro
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


import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle


class AlgorithmFrame(ParameterLabelFrame):
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AlgorithmFrame, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
            
    def display(self):
        self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )