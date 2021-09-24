# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:25:11 2021

@author: Álvaro
"""

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
# import numpy as np

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float

from interface.console import Console




class ProblemTab(ttk.Frame):
    
    class ProblemFrame(tk.Frame):
        def __init__(self, master, *args, **kwargs):
            super(ProblemTab, self).__init__(master=master, *args, **kwargs)
        
    
    def __listbox_selection_handler__(self, event):
        print("pacopepe")
    
    def __init__(self, master, *args, **kwargs):
        super(ProblemTab, self).__init__(master=master, *args, **kwargs)
        
        templates_optionlist = [ option.value for option in ProblemParameters.PROBLEM_TEMPLATES ]
        
        tk.Label( self, text="Template", font=('URW Gothic L','11','bold') ).place( relx=0.015, rely=0.048 )
        self.TemplateOption = tk.StringVar(self)
        self.TemplateOption.set(templates_optionlist[0])
        template_option = tk.OptionMenu(self, self.TemplateOption, *templates_optionlist)
        template_option.config( font=('URW Gothic L','11') )
        template_option.config( state=tk.DISABLED )
        template_option.place( relx=0.07, rely=0.045, relwidth=0.1 )
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        self.parameters_listbox.insert(0, "Evaluator")
        self.parameters_listbox.insert(tk.END, "Variables")
        self.parameters_listbox.insert(tk.END, "Constants")
        self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.parameters_listbox.place( relx=0.01, rely=0.125, relwidth=0.16, relheight=0.85 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        self.parameters_listbox.activate(0)
        
        self.console = Console(master=self, wrap=tk.WORD, font=("Times New Roman", 9))
        self.console.place( relx=0.2, rely=0.7, relwidth=0.6, relheight=0.5 )
        self.console.print_message("Hola\n")
        self.console.print_warning("Que haces???\n")
        self.console.print_error("Cabrón!!!\n")
        
    def check_errors(self):
        pass
        
        