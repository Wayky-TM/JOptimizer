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
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame


class AlgorithmTab(ttk.Frame):
 
    class AlgorithmFrame(ParameterLabelFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.AlgorithmFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
            
    class PopulationFrame(AlgorithmFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.PopulationFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Population size").place( relx=0.02, rely=0.05 )
            self.population_size_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.population_size_entry.insert(0, self.algorithm_parameters.general_parameters["population_size"])
            self.population_size_entry.place(relx=0.095, rely=0.05+0.005, relwidth=0.08)
            self.population_size_entry.config(state=tk.NORMAL)
            
            self.population_size_parameter = Integer(name="population_size", fancy_name="Population size", lower_bound=3, upper_bound=100000)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.population_size_parameter,
                                                              widget_read_lambda=lambda: self.population_size_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"population_size":var})) )
            
            
    class OffspringFrame(AlgorithmFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.OffspringFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Offspring size").place( relx=0.02, rely=0.05 )
            self.offspring_size_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.offspring_size_entry.insert(0, self.algorithm_parameters.general_parameters["offspring_size"])
            self.offspring_size_entry.place(relx=0.095, rely=0.05+0.005, relwidth=0.08)
            self.offspring_size_entry.config(state=tk.NORMAL)
            
            self.offspring_size_parameter = Integer(name="offspring_size", fancy_name="Offspring size", lower_bound=3, upper_bound=100000)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.offspring_size_parameter,
                                                              widget_read_lambda=lambda: self.offspring_size_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"offspring_size":var})) )        
 
    class SelectionFrame(AlgorithmFrame):
    
        class SelectionParametersPane(ParameterFrame):
            
            def __init__(self, master, algorithm_parameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.SelectionParametersPane,self).__init__(master=master, *args, **kwargs)
                
                self.algorithm_parameters = algorithm_parameters
                
            def display(self):
                self.place( relx=0.18, rely=0.145, relwidth=0.81, relheight=0.615 )
                    
                
        class NaryParametersPane(SelectionParametersPane):
            
            def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.NaryParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)
                
                tk.Label( master=self, text="Number of solutions to select").place( relx=0.02, rely=0.05 )
                
                self.n_solutions_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.n_solutions_entry.insert(0, self.algorithm_parameters.selection_parameters["number_of_solutions_to_be_returned"])
                self.n_solutions_entry.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
                self.n_solutions_entry.config(state=tk.NORMAL)
                
                self.n_solutions_parameter = Integer(name="number_of_solutions_to_be_returned", fancy_name="Number of solutions to select", lower_bound=1, upper_bound=10000)
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.n_solutions_parameter,
                                                                  widget_read_lambda=lambda: self.n_solutions_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.selection_parameters.update({"number_of_solutions_to_be_returned":var})) )        
                
        
        class RankingAndCrowdingParametersPane(SelectionParametersPane):
            
            def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.RankingAndCrowdingParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)
    
                
    
        def update_operator(self, new_value):
            # self.frames[self.selected_frame_key].clear_errors()
            # self.frames[self.selected_frame_key].clear_entries()
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = new_value
            self.frames[self.selected_frame_key].display()
    
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.SelectionFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            paceholder_frame = AlgorithmTab.SelectionFrame.SelectionParametersPane( master=self, algorithm_parameters=self.algorithm_parameters )
            
            self.selection_options = ["Roulette",
                                      "Binary tournament",
                                      "Best solution",
                                      "n-ary random",
                                      "Differential evolution",
                                      "Random selection",
                                      "Roulette",
                                      "Ranking and crowding"]
            
            self.frames = {}
            self.frames["Roulette"] = paceholder_frame
            self.frames["Binary tournament"] = paceholder_frame
            self.frames["Best solution"] = paceholder_frame
            self.frames["n-ary random"] = AlgorithmTab.SelectionFrame.NaryParametersPane(master=self, algorithm_parameters=self.algorithm_parameters)
            self.frames["Differential evolution"] = paceholder_frame
            self.frames["Random selection"] = paceholder_frame
            self.frames["Roulette"] = paceholder_frame
            self.frames["Ranking and crowding"] = AlgorithmTab.SelectionFrame.RankingAndCrowdingParametersPane(master=self, algorithm_parameters=self.algorithm_parameters)
            
            
            tk.Label( master=self, text="Selection operator").place( relx=0.02, rely=0.05 )
            
            self.SelectionOption = tk.StringVar(self)
            self.SelectionOption.set(self.selection_options[0])
            self.selected_frame_key = self.selection_options[0]
            self.frames[self.selected_frame_key].display()
            selection_option = tk.OptionMenu(self, self.SelectionOption, *self.selection_options, command=self.update_operator)
            selection_option.config( font=('URW Gothic L','11') )
            selection_option.config( state=tk.NORMAL )
            selection_option.place( relx=0.08, rely=0.045, relwidth=0.105 )
            
            self.selection_option_parameter = Parameter(name="selection_operator", fancy_name="Selection operator")
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.selection_option_parameter,
                                                              widget_read_lambda=lambda: self.offspring_size_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"offspring_size":var})) )
            
        def check_errors(self):
            
            error_list = super(AlgorithmTab.SelectionFrame, self).check_errors()
            error_list.extend( self.frames[self.selected_frame_key].check_errors() )
                
            return error_list
                
        def save_parameters(self):
            
            super(AlgorithmTab.SelectionFrame, self).save_parameters()
            self.frames[self.selected_frame_key].save_parameters()
    
    def update_algorithm_selection(self, new_selection):
        
        self.parameters_listbox.delete(0,'end')
        
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
 
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AlgorithmTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        # algorithm_optionlist = [ option.value for option in AlgorithmParameters.SUPPORTED_ALGORITHMS ]
        algorithm_optionlist = [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value ]
        
        tk.Label( self, text="Algorithm", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.AlgorithmOption = tk.StringVar(self)
        self.AlgorithmOption.set(algorithm_optionlist[0])
        algorithm_option = tk.OptionMenu(self, self.AlgorithmOption, *algorithm_optionlist)
        algorithm_option.config( font=('URW Gothic L','11') )
        algorithm_option.config( state=tk.NORMAL )
        algorithm_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.frames = {}
        self.frames["Population"] = AlgorithmTab.PopulationFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Offspring"] = AlgorithmTab.OffspringFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Selection"] = AlgorithmTab.SelectionFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Crossover"] = AlgorithmTab.AlgorithmFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Mutation"] = AlgorithmTab.AlgorithmFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        
        self.items_list = {}
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        
        self.selected_frame_key = "Population"
        self.frames[self.selected_frame_key].display()
        self.update_algorithm_selection( "NSGAII" )
        
        self.parameters_listbox.activate(0)
        self.parameters_listbox.selection_set(0)
        
        # self.parameters_listbox.insert(0, "Evaluator")
        # self.parameters_listbox.insert(tk.END, "Variables")
        # self.parameters_listbox.insert(tk.END, "Constants")
        # self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.console = Console(master=self, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")
        
        