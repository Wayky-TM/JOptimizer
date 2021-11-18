# -*- coding: utf-8 -*-


import imp
import os
import sys
# sys.path.append(r"./../..")

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

# import core.variable as variable_types
# import core.constant as constant_types
# from core.variable import *
# from core.constant import *
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from core.evaluator import Evaluator
from util.type_check import is_integer, is_float, to_integer
from util.string_utils import remove_whitespaces

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle


class ProblemFrame(ParameterLabelFrame):
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ProblemFrame, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
            
    def display(self):
        self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
        
