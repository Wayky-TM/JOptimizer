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
from typing import List

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding



class ProblemTab(ttk.Frame):
    
    class ProblemFrame(tk.LabelFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ProblemFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.parameters_bindings = []
            
        def error_check(self, error_list: List[str]):
            
            for binding in self.parameters_bindings:
                binding.error_check(error_list)
                
        def save_parameters(self):
            
            for binding in self.parameters_bindings:
                binding.store_value()
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
        def hide(self):
            self.place_forget()
            
            
            
    class EvaluatorFrame(ProblemFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ProblemFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Evaluator script path").place( relx=0.05, rely=0.2 )
            self.evaluator_path_entry = tk.Entry( master=self , state=NORMAL)
            evaluator_path_parameter = FilePath( fancy_name="Evaluator script path" )
            
            evaluator_path_ = 
            
        
    
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
        
        
        
        self.generic_problem_items = [ "Evaluator", "Variables", "Constants", "Contraints" ]
        self.matlab_problem_items = [ "Script", "Variables", "Constants", "Contraints" ]
        self.CST_problem_items = [ "CST", "Variables", "Constants", "Contraints" ]
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        self.parameters_listbox.insert(0, "Evaluator")
        self.parameters_listbox.insert(tk.END, "Variables")
        self.parameters_listbox.insert(tk.END, "Constants")
        self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.parameters_listbox.place( relx=0.01, rely=0.125, relwidth=0.16, relheight=0.85 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        self.parameters_listbox.activate(0)
        
        self.parameters_frame = tk.Frame(master=self)
        self.parameters_frame.place()
        
        self.console = Console(master=self, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")
        
        test_problem_parameters = ProblemParameters()
        self.prueba = ProblemTab.ProblemFrame(master=self, problem_parameters=test_problem_parameters)
        self.prueba.display()
        
    def check_errors(self):
        pass
        
        