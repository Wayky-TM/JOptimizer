# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 19:53:45 2021

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

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float



def popup_variables( controller: tk.Tk,
                     problem_parameters: ProblemParameters):
    pass
    #TODO