# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:51:12 2021

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
    
    
from win32api import GetSystemMetrics
from collections import defaultdict
# import numpy as np

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding




class AlgorithmTab(ttk.Frame):
 
    class AlgorithmFrame(tk.LabelFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.AlgorithmFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            self.parameters_bindings = []
            
        def check_errors(self):
            
            error_list = []
            
            for binding in self.parameters_bindings:
                error_list.extend(binding.error_check())
                
            return error_list
                
        def save_parameters(self):
            
            for binding in self.parameters_bindings:
                binding.store_value()
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
        def hide(self):
            self.place_forget()   
 
    
    def update_algorithm_selection(self, new_selection):
        
        self.parameters_listbox.delete(0,'end')
        
        item_list = self.items_list[new_selection]
        
        if self.selected_frame_key not in item_list:
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = item_list[0]
            self.frames[self.selected_frame_key].display()
            
        
        for option in item_list:
            self.parameters_listbox.insert(tk.END, option)
        
        
 
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AlgorithmTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        # algorithm_optionlist = [ option.value for option in AlgorithmParameters.SUPPORTED_ALGORITHMS ]
        algorithm_optionlist = [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value ]
        
        tk.Label( self, text="Problem", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.AlgorithmOption = tk.StringVar(self)
        self.AlgorithmOption.set(templates_optionlist[0])
        algorithm_option = tk.OptionMenu(self, self.AlgorithmOption, *algorithm_optionlist)
        algorithm_option.config( font=('URW Gothic L','11') )
        algorithm_option.config( state=tk.DISABLED )
        algorithm_option.place( relx=0.055, rely=0.045, relwidth=0.115 )
        
        self.frames = {}
        
        self.items_list = {}
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        
        self.selected_frame_key = "Population"
        self.frames[self.selected_frame_key].display()
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        self.parameters_listbox.activate(0)
        
        # self.parameters_listbox.insert(0, "Evaluator")
        # self.parameters_listbox.insert(tk.END, "Variables")
        # self.parameters_listbox.insert(tk.END, "Constants")
        # self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.console = Console(master=self, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")
        
        