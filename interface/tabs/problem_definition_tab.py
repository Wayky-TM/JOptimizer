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
        
        def _browse(self): 
            
            path = filedialog.askopenfilename(title = "Select a file which contains the evaluator")
            
            self.OperatorFilePath.config(state=tk.NORMAL)
            self.OperatorFilePath.insert( 0, path )
            self.OperatorFilePath.config(state="readonly")
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.EvaluatorFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Evaluator script path").place( relx=0.05, rely=0.2 )
            self.OperatorFilePath = tk.Entry(master=self, state=tk.NORMAL)
            self.OperatorFilePath.insert(0, problem_parameters.options["evaluator_classname"])
            self.OperatorFilePath.place(relx=0.15, rely=0.2, relwidth=0.52)
            self.OperatorFilePath.config(state=tk.DISABLED)
            self.button_browse_operator = tk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.73, rely=0.2 - 0.0125, relwidth=0.1)
            
            evaluator_path_parameter = FilePath( fancy_name="Evaluator script path" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=evaluator_path_parameter,
                                                              widget_read_lambda=lambda: self.evaluator_class_entry.get(),
                                                              variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var})) )
            
            
            
            tk.Label( master=self, text="Evaluator class").place( relx=0.05, rely=0.3 )
            self.evaluator_class_entry = tk.Entry( master=self , state=tk.NORMAL)
            
            evaluator_class_parameter = Parameter( fancy_name="Evaluator class" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=evaluator_class_parameter,
                                                              widget_read_lambda=lambda: self.evaluator_class_entry.get(),
                                                              variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var})) )
            
        
    class VariablesFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.VariablesFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Variables").place( relx=0.5, rely=0.5 )
            
            
    class ConstantsFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstantsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Constants").place( relx=0.5, rely=0.5 )
            
            
    class ConstraintsFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstraintsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Constraints").place( relx=0.5, rely=0.5 )
            
        
    
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            print(data)
            self.selected_frame.hide()
            self.selected_frame = self.frames[data]
            self.selected_frame.display()
        
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ProblemTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        
        templates_optionlist = [ option.value for option in ProblemParameters.PROBLEM_TEMPLATES ]
        
        tk.Label( self, text="Template", font=('URW Gothic L','11','bold') ).place( relx=0.015, rely=0.048 )
        self.TemplateOption = tk.StringVar(self)
        self.TemplateOption.set(templates_optionlist[0])
        template_option = tk.OptionMenu(self, self.TemplateOption, *templates_optionlist)
        template_option.config( font=('URW Gothic L','11') )
        template_option.config( state=tk.DISABLED )
        template_option.place( relx=0.07, rely=0.045, relwidth=0.1 )
        
        self.frames = {}
        self.frames["Evaluator"] = ProblemTab.EvaluatorFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Variables"] = ProblemTab.VariablesFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constants"] = ProblemTab.ConstantsFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constraints"] = ProblemTab.ConstraintsFrame( master=self, problem_parameters=self.problem_parameters )
        
        self.selected_frame = self.frames["Evaluator"]
        self.selected_frame.display()
        
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
        
        # self.prueba = ProblemTab.ProblemFrame(master=self, problem_parameters=self.problem_parameters)
        # self.prueba.display()
        
    def check_errors(self):
        pass
        
        