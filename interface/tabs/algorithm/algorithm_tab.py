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
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle

""" General frames """
from interface.tabs.algorithm.frames.algorithm_frame import AlgorithmFrame
from interface.tabs.algorithm.frames.population_frame import PopulationFrame
from interface.tabs.algorithm.frames.offspring_frame import OffspringFrame
from interface.tabs.algorithm.frames.selection_frame import SelectionFrame
from interface.tabs.algorithm.frames.crossover_frame import CrossoverFrame
from interface.tabs.algorithm.frames.mutation_frame import MutationFrame

""" MOEAD frames """
from interface.tabs.algorithm.frames.aggregative_frame import AggregativeFrame
from interface.tabs.algorithm.frames.MOEAD_parameters_frame import MOEADParametersFrame

class AlgorithmTab(ParameterFrame):
    
    def update_algorithm_selection(self, new_selection):
        
        self.parameters_listbox.delete(0,'end')
        self.selected_algorithm = new_selection
        
        item_list = self.items_list[new_selection]
        
        if self.selected_frame_key not in item_list:
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = item_list[0]
            self.frames[self.selected_frame_key].display()
            
        
        for option in item_list:
            self.parameters_listbox.insert(tk.END, option)
        
        
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            # print(data)
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = data
            self.frames[self.selected_frame_key].display()
 
    def __algorithm_option_update__(self, var):
        self.update_algorithm_selection(var)
        self.AlgorithmOption.set(var)
 
    def __algorithm_option_save__(self, var):
        self.algorithm_parameters.choice = var
 
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AlgorithmTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        algorithm_optionlist = [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value,
                                 AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value,
                                 AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value ]
        
        tk.Label( self, text="Algorithm", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.AlgorithmOption = tk.StringVar(self)
        self.AlgorithmOption.set(algorithm_optionlist[0])
        algorithm_option = tk.OptionMenu(self, self.AlgorithmOption, *algorithm_optionlist, command=self.update_algorithm_selection)
        algorithm_option.config( font=('URW Gothic L','11') )
        algorithm_option.config( state=tk.NORMAL )
        algorithm_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.frames = {}
        self.frames["Population"] = PopulationFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Offspring"] = OffspringFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Selection"] = SelectionFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Crossover"] = CrossoverFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Mutation"] = MutationFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Aggregative"] = AggregativeFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["MOEAD"] = MOEADParametersFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        
        self.items_list = {}
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.MOEAD.value] = ["Population", "Crossover", "Mutation", "MOEAD", "Aggregative"]
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        
        self.selected_frame_key = "Population"
        self.frames[self.selected_frame_key].display()
        self.update_algorithm_selection( AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value )
        
        self.parameters_listbox.activate(0)
        self.parameters_listbox.selection_set(0)
        
        # self.algorithm_option_parameter = Parameter(name="Algorithm", fancy_name="algorithm")
            
        # self.parameters_bindings.append( ParameterBinding(parameter=self.algorithm_option_parameter,
        #                                                     widget_read_lambda=lambda: self.AlgorithmOption.get(),
        #                                                     variable_store_lambda=lambda var: self.__algorithm_option_save__(var),
        #                                                     variable_read_lambda=lambda: self.algorithm_parameters.choice,
        #                                                     widget_update_lambda=lambda var: self.__algorithm_option_update__(var) ) )
        
        
        """ Error console frame """
        self.error_console_frame = tk.Frame( master=self, bg=AppStyle.frame_background_color )
        self.error_console_frame.config(highlightbackground=AppStyle.frame_border_color, highlightthickness=1)
        self.error_console_frame.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        tk.Label(master=self.error_console_frame, text="Error Console", font=('TkDefaultFont','10','bold'), bg=AppStyle.frame_background_color).place(relx=0.0035, rely=0.03)
        self.console = Console(master=self.error_console_frame, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.0035, rely=0.18, relwidth=0.993, relheight=0.795 )
        
    def update_types(self):
        
        used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
        
        crossover_frame = self.frames["Crossover"]
        mutation_frame = self.frames["Mutation"]
        
        if variable_types.FloatVariable in used_variable_types:
            crossover_frame.float_frame.enable()
            mutation_frame.float_frame.enable()
        else:
            crossover_frame.float_frame.disable()
            mutation_frame.float_frame.disable()
        
        
        if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
            crossover_frame.int_frame.enable()
            mutation_frame.int_frame.enable()
        else:
            crossover_frame.int_frame.disable()
            mutation_frame.int_frame.disable()
        
        if variable_types.BinaryVariable in used_variable_types:
            crossover_frame.binary_frame.enable()
            mutation_frame.binary_frame.enable()
        else:
            crossover_frame.binary_frame.disable()
            mutation_frame.binary_frame.disable()
        
        if variable_types.PermutationVariable in used_variable_types:
            crossover_frame.permutation_frame.enable()
            mutation_frame.permutation_frame.enable()
        else:
            crossover_frame.permutation_frame.disable()
            mutation_frame.permutation_frame.disable()
        
        
    def check_errors(self):
        
        error_list = []
        
        for key in self.items_list[self.selected_algorithm]:
            #TODO: check if specified evaluator class name is correct
            error_list.extend( self.frames[key].check_errors() )
        
        return error_list
    
    def save_parameters(self):
        # super(AlgorithmTab, self).save_parameters()
        
        self.algorithm_parameters.choice = self.AlgorithmOption.get()
        
        for key in self.items_list[self.AlgorithmOption.get()]:
            self.frames[key].save_parameters()
            
    def load_parameters(self):
        # super(AlgorithmTab, self).load_parameters()
        
        self.AlgorithmOption.set( self.algorithm_parameters.choice )
        self.update_algorithm_selection( self.algorithm_parameters.choice )
        self.update_types()
        
        for key in self.items_list[self.AlgorithmOption.get()]:
            self.frames[key].load_parameters()
        
    def console_print_error(self, string: str):
        self.console.print_error( string+"\n" )
        
    def console_print_warning(self, string: str):
        self.console.print_warning( string+"\n" )
        
    def console_print_message(self, string: str):
        self.console.print_message( string+"\n" )
        
    def console_clear(self):
        self.console.clear_all()