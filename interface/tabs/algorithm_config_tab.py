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
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame


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
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"population_size":var}),
                                                              error_set_lambda=EntryInvalidator(self.population_size_entry),
                                                              error_reset_lambda=EntryValidator(self.population_size_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.general_parameters["population_size"],
                                                              widget_update_lambda=lambda var: self.population_size_entry.set(var)) )
            
            
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
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"offspring_size":var}),
                                                              error_set_lambda=EntryInvalidator(self.offspring_size_entry),
                                                              error_reset_lambda=EntryValidator(self.offspring_size_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.general_parameters["offspring_size"],
                                                              widget_update_lambda=lambda var: self.offspring_size_entry.set(var)) )        
 
    class SelectionFrame(AlgorithmFrame):
    
        class SelectionParametersPane(ParameterLabelFrame):
            
            def __init__(self, master, algorithm_parameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.SelectionParametersPane,self).__init__(master=master, *args, **kwargs)
                
                self.algorithm_parameters = algorithm_parameters
                
            def display(self):
                self.place( relx=0.05, rely=0.16, relwidth=0.9, relheight=0.79 )
                    
                
        class NaryParametersPane(SelectionParametersPane):
            
            def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.NaryParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)
                
                tk.Label( master=self, text="Number of solutions to select").place( relx=0.02, rely=0.05 )
                
                self.n_solutions_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.n_solutions_entry.insert(0, self.algorithm_parameters.selection_parameters["number_of_solutions_to_be_returned"])
                self.n_solutions_entry.place(relx=0.185, rely=0.05+0.005, relwidth=0.06)
                self.n_solutions_entry.config(state=tk.NORMAL)
                
                self.n_solutions_parameter = Integer(name="number_of_solutions_to_be_returned", fancy_name="Number of solutions to select", lower_bound=1, upper_bound=10000)
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.n_solutions_parameter,
                                                                  widget_read_lambda=lambda: self.n_solutions_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.selection_parameters.update({"number_of_solutions_to_be_returned":var}),
                                                                  error_set_lambda=EntryInvalidator(self.n_solutions_entry),
                                                                  error_reset_lambda=EntryValidator(self.n_solutions_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.selection_parameters["number_of_solutions_to_be_returned"],
                                                                  widget_update_lambda=lambda var: self.n_solutions_entry.set(var)) )        
                
        
        class RankingAndCrowdingParametersPane(SelectionParametersPane):
            
            def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.SelectionFrame.RankingAndCrowdingParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)
    
                tk.Label( master=self, text="Max. population size").place( relx=0.02, rely=0.05 )
                
                self.max_population_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.max_population_entry.insert(0, self.algorithm_parameters.selection_parameters["max_population_size"])
                self.max_population_entry.place(relx=0.15, rely=0.05+0.005, relwidth=0.06)
                self.max_population_entry.config(state=tk.NORMAL)
                
                self.max_population_parameter = Integer(name="max_population_size", fancy_name="Max. population size", lower_bound=1, upper_bound=1000)
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.max_population_parameter,
                                                                  widget_read_lambda=lambda: self.max_population_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.selection_parameters.update({"max_population_size":var}),
                                                                  error_set_lambda=EntryInvalidator(self.max_population_entry),
                                                                  error_reset_lambda=EntryValidator(self.max_population_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.selection_parameters["max_population_size"],
                                                                  widget_update_lambda=lambda var: self.max_population_entry.set(var)) )        
    
        def update_operator(self, new_value):
            # self.frames[self.selected_frame_key].clear_errors()
            # self.frames[self.selected_frame_key].clear_entries()
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = new_value
            self.frames[self.selected_frame_key].display()
    
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.SelectionFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            paceholder_frame = AlgorithmTab.SelectionFrame.SelectionParametersPane( master=self, algorithm_parameters=self.algorithm_parameters, borderwidth=0, highlightthickness=0 )
            
            self.selection_options = [ option.value for option in AlgorithmParameters.SELECTION ]
            
            self.frames = {}
            self.frames[ AlgorithmParameters.SELECTION.ROULETTE.value ] = paceholder_frame
            self.frames[ AlgorithmParameters.SELECTION.BINARY_TOURNAMENT.value ] = paceholder_frame
            self.frames[ AlgorithmParameters.SELECTION.BEST_SOLUTION.value ] = paceholder_frame
            self.frames[ AlgorithmParameters.SELECTION.NARY_RANDOM.value ] = AlgorithmTab.SelectionFrame.NaryParametersPane(master=self, algorithm_parameters=self.algorithm_parameters, text="Parameters")
            self.frames[ AlgorithmParameters.SELECTION.DIFF_EVOLUTION.value ] = paceholder_frame
            self.frames[ AlgorithmParameters.SELECTION.RANDOM.value ] = paceholder_frame
            self.frames[ AlgorithmParameters.SELECTION.RANKING_AND_CROWDING.value ] = AlgorithmTab.SelectionFrame.RankingAndCrowdingParametersPane(master=self, algorithm_parameters=self.algorithm_parameters, text="Parameters")
            
            
            tk.Label( master=self, text="Selection operator").place( relx=0.02, rely=0.05 )
            
            self.SelectionOption = tk.StringVar(self)
            self.SelectionOption.set(self.selection_options[0])
            self.selected_frame_key = self.selection_options[0]
            self.frames[self.selected_frame_key].display()
            selection_option = tk.OptionMenu(self, self.SelectionOption, *self.selection_options, command=self.update_operator)
            # selection_option.config( font=('URW Gothic L','11') )
            selection_option.config( state=tk.NORMAL )
            selection_option.place( relx=0.11, rely=0.045, relwidth=0.15 )
            
            self.selection_option_parameter = Parameter(name="selection_operator", fancy_name="Selection operator")
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.selection_option_parameter,
                                                              widget_read_lambda=lambda: self.SelectionOption.get(),
                                                              variable_store_lambda=self.__store_selection_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.selection_choice,
                                                              widget_update_lambda=lambda var: self.SelectionOption.set(var)) )
            
        def __store_selection_option(self, value):
            self.algorithm_parameters.selection_choice = value
            
        def check_errors(self):
            
            error_list = super(AlgorithmTab.SelectionFrame, self).check_errors()
            error_list.extend( self.frames[self.selected_frame_key].check_errors() )
                
            return error_list
                
        def save_parameters(self):
            
            super(AlgorithmTab.SelectionFrame, self).save_parameters()
            self.frames[self.selected_frame_key].save_parameters()
            
        def load_parameters(self):
            
            super(AlgorithmTab.SelectionFrame, self).load_parameters()
            self.frames[self.selected_frame_key].load_parameters()
            
            
    class ByTypeFrame(ParameterLabelFrame):
            
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.CrossoverFrame.ByTypeFrame,self).__init__(master=master, *args, **kwargs)
            
            self.algorithm_parameters = algorithm_parameters
            self.problem_parameters = problem_parameters
            
        @abstractmethod
        def disable(self):
            pass
            
        @abstractmethod
        def enable(self):
            pass
        
    class CrossoverFrame(AlgorithmFrame):
        
        class FloatCrossoverFrame(ParameterLabelFrame):
            
            class SBXFrame(ParameterLabelFrame):
                
                def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                    super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame.SBXFrame,self).__init__(master=master, *args, **kwargs)
                    
                    self.problem_parameters = problem_parameters
                    self.algorithm_parameters = algorithm_parameters
                    
                    self.probability_label = tk.Label( self, text="Probability" ).place( relx=0.01, rely=0.048 )
                    self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.probability_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["probability"])
                    self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
                    self.probability_entry.config(state=tk.NORMAL)
                    
                    self.distribution_index_label = tk.Label( self, text="Distribution index" ).place( relx=0.01, rely=0.448 )
                    self.distribution_index_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.distribution_index_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["distribution_index"])
                    self.distribution_index_entry.place(relx=0.23, rely=0.45+0.005, relwidth=0.08)
                    self.distribution_index_entry.config(state=tk.NORMAL)
                    
                    self.probability_parameter = Float(name="probability", fancy_name="Probability (float crossover)", lower_bound=0.0, upper_bound=1.0)
                    self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (float crossover)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
                    self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                      widget_read_lambda=lambda: self.probability_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"probability":var}),
                                                                      error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                      error_reset_lambda=EntryValidator(self.probability_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["probability"],
                                                                      widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                                      widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"distribution_index":var}),
                                                                      error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                                      error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["distribution_index"],
                                                                      widget_update_lambda=lambda var: self.distribution_index_entry.set(var)) )
                
                def display(self):
                    self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                    
                def disable(self):
                    self.probability_entry.config(state=tk.DISABLED)
                    self.distribution_index_entry.config(state=tk.DISABLED)
                
                def enable(self):
                    self.probability_entry.config(state=tk.NORMAL)
                    self.distribution_index_entry.config(state=tk.NORMAL)
            
            class DiffEvolFrame(ParameterLabelFrame):
                
                def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                    super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame.DiffEvolFrame,self).__init__(master=master, *args, **kwargs)
                    
                    self.problem_parameters = problem_parameters
                    self.algorithm_parameters = algorithm_parameters
                    
                    self.probability_label = tk.Label( self, text="Probability" ).place( relx=0.01, rely=0.048 )
                    self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.probability_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["probability"])
                    self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
                    self.probability_entry.config(state=tk.NORMAL)
                    
                    self.F_label = tk.Label( self, text="F" ).place( relx=0.01, rely=0.348 )
                    self.F_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.F_entry.place(relx=0.13, rely=0.35+0.005, relwidth=0.08)
                    self.F_entry.config(state=tk.NORMAL)
                    
                    self.K_label = tk.Label( self, text="K" ).place( relx=0.01, rely=0.648 )
                    self.K_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.K_entry.place(relx=0.13, rely=0.65+0.005, relwidth=0.08)
                    self.K_entry.config(state=tk.NORMAL)
                    
                    self.probability_parameter = Float(name="probability", fancy_name="Probability (float crossover)", lower_bound=0.0, upper_bound=1.0)
                    self.F_parameter = Float(name="F", fancy_name="F", lower_bound=float("-Inf"), upper_bound=float("Inf"))
                    self.K_parameter = Float(name="K", fancy_name="K", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
                    self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                      widget_read_lambda=lambda: self.probability_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"probability":var}),
                                                                      error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                      error_reset_lambda=EntryValidator(self.probability_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["probability"],
                                                                      widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.F_parameter,
                                                                      widget_read_lambda=lambda: self.F_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"F":var}),
                                                                      error_set_lambda=EntryInvalidator(self.F_entry),
                                                                      error_reset_lambda=EntryValidator(self.F_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["F"],
                                                                      widget_update_lambda=lambda var: self.F_entry.set(var)) )
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.K_parameter,
                                                                      widget_read_lambda=lambda: self.K_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"K":var}),
                                                                      error_set_lambda=EntryInvalidator(self.K_entry),
                                                                      error_reset_lambda=EntryValidator(self.K_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["K"],
                                                                      widget_update_lambda=lambda var: self.K_entry.set(var)) )
                    
                def display(self):
                    self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                
                def disable(self):
                    self.probability_entry.config(state=tk.DISABLED)
                    self.F_entry.config(state=tk.DISABLED)
                    self.K_entry.config(state=tk.DISABLED)
                
                def enable(self):
                    self.probability_entry.config(state=tk.NORMAL)
                    self.F_entry.config(state=tk.NORMAL)
                    self.K_entry.config(state=tk.NORMAL)
                    
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame,self).__init__(master=master, text="Float crossover", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.crossover_options = [ option.value for option in AlgorithmParameters.FLOAT_CROSSOVER ]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
                self.CrossoverOption = tk.StringVar(self)
                self.CrossoverOption.set( AlgorithmParameters.FLOAT_CROSSOVER.SBX.value )
                self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options, command=self.option_change)
                self.crossover_option.config( state=tk.NORMAL )
                self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                self.frames = {}
                self.frames[AlgorithmParameters.FLOAT_CROSSOVER.SBX.value] = AlgorithmTab.CrossoverFrame.FloatCrossoverFrame.SBXFrame(master=self,
                                                                                                                                      problem_parameters=self.problem_parameters,
                                                                                                                                      algorithm_parameters=self.algorithm_parameters)
                
                self.frames[AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION.value] = AlgorithmTab.CrossoverFrame.FloatCrossoverFrame.DiffEvolFrame(master=self,
                                                                                                                                           problem_parameters=self.problem_parameters,
                                                                                                                                           algorithm_parameters=self.algorithm_parameters)
                
                self.selected_frame_key = AlgorithmParameters.FLOAT_CROSSOVER.SBX.value
                self.frames[self.selected_frame_key].display()
                
                self.crossover_option_parameter = Parameter( name="float_crossover_option", fancy_name="Float crossover option" )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                                  widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                                  variable_store_lambda=self.__store_float_crossover_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_choice,
                                                                  widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
                
            def __store_float_crossover_option(self, value):
                self.algorithm_parameters.float_crossover_choice = value
                
            def option_change(self, new_value):
                
                if new_value != self.selected_frame_key:
                    self.frames[self.selected_frame_key].hide()
                    self.selected_frame_key = new_value
                    self.frames[self.selected_frame_key].display()
                
            def check_errors(self):
                error_list = super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame,self).check_errors()
                error_list.extend( self.frames[self.selected_frame_key].check_errors() )
                
                return error_list
            
            def save_parameters(self):
                super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame, self).save_parameters()
                self.frames[self.selected_frame_key].save_parameters()
                
            def load_parameters(self):
                super(AlgorithmTab.CrossoverFrame.FloatCrossoverFrame, self).load_parameters()
                self.frames[self.selected_frame_key].load_parameters()
                
            def disable(self):
                self.configure(text="Float crossover (Disabled)")
                self.crossover_option.config(state=tk.DISABLED)
                self.frames[self.selected_frame_key].disable()
                
            def enable(self):
                self.configure(text="Float crossover")
                self.crossover_option.config(state=tk.NORMAL)
                self.frames[self.selected_frame_key].enable()
            
            
        class IntCrossoverFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.CrossoverFrame.IntCrossoverFrame,self).__init__(master=master, text="Integer crossover", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.crossover_options = [AlgorithmParameters.INT_CROSSOVER.INT_SBX.value]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
                self.CrossoverOption = tk.StringVar(self)
                self.CrossoverOption.set( AlgorithmParameters.INT_CROSSOVER.INT_SBX.value )
                self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
                self.crossover_option.config( state=tk.DISABLED )
                self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                self.labelframe_params = tk.LabelFrame(master=self)
                
                tk.Label( master=self.labelframe_params, text="Probability" ).place( relx=0.01, rely=0.05 )
                self.probability_entry = tk.Entry(master=self.labelframe_params, state=tk.NORMAL)
                self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                self.distribution_index_label = tk.Label( self.labelframe_params, text="Distribution index" ).place( relx=0.01, rely=0.448 )
                self.distribution_index_entry = tk.Entry(master=self.labelframe_params, state=tk.NORMAL)
                self.distribution_index_entry.place(relx=0.23, rely=0.45+0.005, relwidth=0.08)
                self.distribution_index_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["distribution_index"])
                self.distribution_index_entry.config(state=tk.NORMAL)
                
                self.labelframe_params.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                
                self.crossover_option_parameter = Parameter( name="int_crossover_option", fancy_name="Integer crossover option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (int crossover)", lower_bound=0.0, upper_bound=1.0)
                self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (int crossover)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.int_crossover_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                                  widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.int_crossover_parameters.update({"distribution_index":var}),
                                                                  error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                                  error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_parameters["distribution_index"],
                                                                  widget_update_lambda=lambda var: self.distribution_index_entry.set(var)) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                                  widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                                  variable_store_lambda=self.__store_int_crossover_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_choice,
                                                                  widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
                
            def __store_int_crossover_option(self, value):
                self.algorithm_parameters.int_crossover_choice = value
                
            def disable(self):
                self.configure(text="Integer crossover (Disabled)")
                self.crossover_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                self.distribution_index_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Integer crossover")
                self.crossover_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
                self.distribution_index_entry.config(state=tk.NORMAL)
                
        class BinaryCrossoverFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.CrossoverFrame.BinaryCrossoverFrame,self).__init__(master=master, text="Binary crossover", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.crossover_options = [AlgorithmParameters.BINARY_CROSSOVER.SPX.value]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.3 )
                self.CrossoverOption = tk.StringVar(self)
                self.CrossoverOption.set( self.crossover_options[0] )
                self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
                self.crossover_option.config( state=tk.DISABLED )
                self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.binary_crossover_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                
                self.crossover_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (binary crossover)", lower_bound=0.0, upper_bound=1.0)
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.binary_crossover_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.binary_crossover_parameters["distribution_index"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
                    
                self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                                  widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                                  variable_store_lambda=self.__store_binary_crossover_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.binary_crossover_choice,
                                                                  widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
                
            def __store_binary_crossover_option(self, value):
                self.algorithm_parameters.binary_crossover_choice = value
                
            def disable(self):
                self.configure(text="Binary crossover (Disabled)")
                self.crossover_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Binary crossover")
                self.crossover_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
        
                
        class PermutationCrossoverFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.CrossoverFrame.PermutationCrossoverFrame,self).__init__(master=master, text="Permutation crossover", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.crossover_options = [AlgorithmParameters.PERMUTATION_CROSSOVER.CXC.value, AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.35 )
                self.CrossoverOption = tk.StringVar(self)
                self.CrossoverOption.set( AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value )
                self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
                self.crossover_option.config( state=tk.NORMAL )
                self.crossover_option.place( relx=0.15, rely=0.17, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.permutation_crossover_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                self.crossover_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (permutation crossover)", lower_bound=0.0, upper_bound=1.0)
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.permutation_crossover_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.permutation_crossover_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
                    
                self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                                  widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                                  variable_store_lambda=self.__store_permutation_crossover_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.permutation_crossover_choice,
                                                                  widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
                
            def __store_permutation_crossover_option(self, value):
                self.algorithm_parameters.permutation_crossover_choice = value
                
            def disable(self):
                self.configure(text="Permutation crossover (Disabled)")
                self.crossover_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Permutation crossover")
                self.crossover_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
            
        def check_errors(self):
            error_list = super(AlgorithmTab.CrossoverFrame,self).check_errors()
            
            used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            if variable_types.FloatVariable in used_variable_types:
                error_list.extend( self.float_frame.check_errors() )
            
            if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
                error_list.extend( self.int_frame.check_errors() )
            
            if variable_types.BinaryVariable in used_variable_types:
                error_list.extend( self.binary_frame.check_errors() )
            
            if variable_types.PermutationVariable in used_variable_types:
                error_list.extend( self.permutation_frame.check_errors() )
            
            return error_list
        
        
        def save_parameters(self):
            
            used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            if variable_types.FloatVariable in used_variable_types:
                self.float_frame.save_parameters()
            
            if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
                self.int_frame.save_parameters()
            
            if variable_types.BinaryVariable in used_variable_types:
                self.binary_frame.save_parameters()
            
            if variable_types.PermutationVariable in used_variable_types:
                self.permutation_frame.save_parameters()
                
        def load_parameters(self):
            
            used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            self.float_frame.load_parameters()
            self.int_frame.load_parameters()
            self.binary_frame.load_parameters()
            self.permutation_frame.load_parameters()
            
            # if variable_types.FloatVariable in used_variable_types:
            #     self.float_frame.load_parameters()
            
            # if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
            #     self.int_frame.load_parameters()
            
            # if variable_types.BinaryVariable in used_variable_types:
            #     self.binary_frame.load_parameters()
            
            # if variable_types.PermutationVariable in used_variable_types:
            #     self.permutation_frame.load_parameters()
                
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.CrossoverFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            self.float_frame = AlgorithmTab.CrossoverFrame.FloatCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.int_frame = AlgorithmTab.CrossoverFrame.IntCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.binary_frame = AlgorithmTab.CrossoverFrame.BinaryCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.permutation_frame = AlgorithmTab.CrossoverFrame.PermutationCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            
            self.float_frame.place( relx=0.025, rely=0.05, relwidth=0.4, relheight=0.3 )
            self.int_frame.place( relx=0.025, rely=0.38, relwidth=0.4, relheight=0.3 )
            self.binary_frame.place( relx=0.025, rely=0.71, relwidth=0.4, relheight=0.11 )
            self.permutation_frame.place( relx=0.025, rely=0.85, relwidth=0.4, relheight=0.11 )
            
            self.float_frame.disable()
            self.int_frame.disable()
            self.binary_frame.disable()
            self.permutation_frame.disable()
                
                
    class MutationFrame(AlgorithmFrame):
        
        class FloatMutationFrame(ParameterLabelFrame):
            
            class PolynomialMutation(ParameterLabelFrame):
            
                def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                    super(AlgorithmTab.MutationFrame.FloatMutationFrame.PolynomialMutation,self).__init__(master=master, *args, **kwargs)
                    
                    self.problem_parameters = problem_parameters
                    self.algorithm_parameters = algorithm_parameters
                    
                    self.distribution_index_label = tk.Label( master=self, text="Distribution index" ).place( relx=0.01, rely=0.048 )
                    self.distribution_index_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.distribution_index_entry.place(relx=0.23, rely=0.048+0.005, relwidth=0.08)
                    self.distribution_index_entry.insert(0, self.algorithm_parameters.float_mutation_parameters["distribution_index"])
                    self.distribution_index_entry.config(state=tk.NORMAL)
                    
                    self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (float mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                                      widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"distribution_index":var}),
                                                                      error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                                      error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["distribution_index"],
                                                                      widget_update_lambda=lambda var: self.distribution_index_entry.set(var)) )
                    
                def display(self):
                    self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                    
                def disable(self):
                    self.distribution_index_entry.config(state=tk.DISABLED)
                
                def enable(self):
                    self.distribution_index_entry.config(state=tk.NORMAL)
            
            class UniformMutation(ParameterLabelFrame):
            
                def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                    super(AlgorithmTab.MutationFrame.FloatMutationFrame.UniformMutation,self).__init__(master=master, *args, **kwargs)
                    
                    self.problem_parameters = problem_parameters
                    self.algorithm_parameters = algorithm_parameters
                    
                    self.perturbation_label = tk.Label( self, text="Perturbation" ).place( relx=0.01, rely=0.048 )
                    self.perturbation_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.perturbation_entry.place(relx=0.145, rely=0.05+0.005, relwidth=0.08)
                    self.perturbation_entry.config(state=tk.NORMAL)
                    
                    self.perturbation_parameter = Float(name="perturbation", fancy_name="Perturbation (float mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.perturbation_parameter,
                                                                      widget_read_lambda=lambda: self.perturbation_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"perturbation":var}),
                                                                      error_set_lambda=EntryInvalidator(self.perturbation_entry),
                                                                      error_reset_lambda=EntryValidator(self.perturbation_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["perturbation"],
                                                                      widget_update_lambda=lambda var: self.perturbation_entry.set(var)) )
                    
                def display(self):
                    self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                    
                def disable(self):
                    self.perturbation_entry.config(state=tk.DISABLED)
                
                def enable(self):
                    self.perturbation_entry.config(state=tk.NORMAL)
                    
            class NonUniformMutation(UniformMutation):
            
                def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                    super(AlgorithmTab.MutationFrame.FloatMutationFrame.NonUniformMutation,self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
                    
                    self.max_iter_label = tk.Label( self, text="Max. iterations" ).place( relx=0.01, rely=0.248 )
                    self.max_iter_entry = tk.Entry(master=self, state=tk.NORMAL)
                    self.max_iter_entry.place(relx=0.145, rely=0.25+0.005, relwidth=0.08)
                    self.max_iter_entry.config(state=tk.NORMAL)
                    
                    self.max_iter_parameter = Integer(name="max_iterations", fancy_name="Max. iterations (float mutation)", lower_bound=1, upper_bound=100)
                    
                    self.parameters_bindings.append( ParameterBinding(parameter=self.max_iter_parameter,
                                                                      widget_read_lambda=lambda: self.max_iter_entry.get(),
                                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"max_iterations":var}),
                                                                      error_set_lambda=EntryInvalidator(self.max_iter_entry),
                                                                      error_reset_lambda=EntryValidator(self.max_iter_entry),
                                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["max_iterations"],
                                                                      widget_update_lambda=lambda var: self.max_iter_entry.set(var)) )
                
                    
                def disable(self):
                    super(AlgorithmTab.MutationFrame.FloatMutationFrame.NonUniformMutation,self).disable()
                    self.max_iter_entry.config(state=tk.DISABLED)
                
                def enable(self):
                    super(AlgorithmTab.MutationFrame.FloatMutationFrame.NonUniformMutation,self).enable()
                    self.max_iter_entry.config(state=tk.NORMAL)
                    
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.MutationFrame.FloatMutationFrame,self).__init__(master=master, text="Float mutation", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.mutation_options = [ option.value for option in AlgorithmParameters.FLOAT_MUTATION ]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
                self.MutationOption = tk.StringVar(self)
                self.MutationOption.set( self.mutation_options[0] )
                self.mutation_option = tk.OptionMenu(self, self.MutationOption, *self.mutation_options, command=self.option_change)
                self.mutation_option.config( state=tk.NORMAL )
                self.mutation_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.05 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.64, rely=0.055, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.float_mutation_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                self.frames = {}
                self.frames[AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM.value] = NullParameterFrame(master=self)
                self.frames[AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value] = AlgorithmTab.MutationFrame.FloatMutationFrame.PolynomialMutation(master=self,
                                                                                                                                                    problem_parameters=self.problem_parameters,
                                                                                                                                                    algorithm_parameters=self.algorithm_parameters)
                
                self.frames[AlgorithmParameters.FLOAT_MUTATION.UNIFORM.value] = AlgorithmTab.MutationFrame.FloatMutationFrame.UniformMutation(master=self,
                                                                                                                                            problem_parameters=self.problem_parameters,
                                                                                                                                            algorithm_parameters=self.algorithm_parameters)
                
                self.frames[AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM.value] = AlgorithmTab.MutationFrame.FloatMutationFrame.NonUniformMutation(master=self,
                                                                                                                                                    problem_parameters=self.problem_parameters,
                                                                                                                                                    algorithm_parameters=self.algorithm_parameters)
                
                self.selected_frame_key = self.mutation_options[0]
                self.frames[self.selected_frame_key].display()
                
                self.mutation_option_parameter = Parameter( name="float_mutation_option", fancy_name="Float mutation option" )
                self.probability_parameter = Float(name="probability", fancy_name="probability", lower_bound=0.0, upper_bound=1.0)
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                                  widget_read_lambda=lambda: self.MutationOption.get(),
                                                                  variable_store_lambda=self.__store_float_mutation_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_choice,
                                                                  widget_update_lambda=lambda var: self.MutationOption.set(var)) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
            def __store_float_mutation_option(self, value):
                self.algorithm_parameters.float_mutation_choice = value
                
                
            def option_change(self, new_value):
                
                if new_value != self.selected_frame_key:
                    self.frames[self.selected_frame_key].hide()
                    self.selected_frame_key = new_value
                    self.frames[self.selected_frame_key].display()
                
            def check_errors(self):
                error_list = super(AlgorithmTab.MutationFrame.FloatMutationFrame,self).check_errors()
                error_list.extend( self.frames[self.selected_frame_key].check_errors() )
                
                return error_list
            
            def save_parameters(self):
                
                super(AlgorithmTab.MutationFrame.FloatMutationFrame,self).save_parameters()
                self.frames[self.selected_frame_key].save_parameters()
                
            def load_parameters(self):
                
                super(AlgorithmTab.MutationFrame.FloatMutationFrame,self).load_parameters()
                self.frames[self.selected_frame_key].load_parameters()
                
            def disable(self):
                self.configure(text="Float mutation (Disabled)")
                self.mutation_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                self.frames[self.selected_frame_key].disable()
                
            def enable(self):
                self.configure(text="Float mutation")
                self.mutation_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
                self.frames[self.selected_frame_key].enable()
            
            
        class IntMutationFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.MutationFrame.IntMutationFrame,self).__init__(master=master, text="Integer mutation", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.mutation_options = [AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
                self.MutationOption = tk.StringVar(self)
                self.MutationOption.set( self.mutation_options[0] )
                self.mutation_option = tk.OptionMenu(self, self.MutationOption, *self.mutation_options)
                self.mutation_option.config( state=tk.DISABLED )
                self.mutation_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.05 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.64, rely=0.055, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.int_mutation_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                self.labelframe_params = tk.LabelFrame(master=self)
                
                self.distribution_index_label = tk.Label( self.labelframe_params, text="Distribution index" ).place( relx=0.01, rely=0.048 )
                self.distribution_index_entry = tk.Entry(master=self.labelframe_params, state=tk.NORMAL)
                self.distribution_index_entry.place(relx=0.23, rely=0.048+0.005, relwidth=0.08)
                self.distribution_index_entry.insert(0, self.algorithm_parameters.int_mutation_parameters["distribution_index"])
                self.distribution_index_entry.config(state=tk.NORMAL)
                
                self.labelframe_params.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                
                self.mutation_option_parameter = Parameter( name="int_mutation_option", fancy_name="Integer mutation option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (int mutation)", lower_bound=0.0, upper_bound=1.0)
                self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (int mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.int_mutation_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                                  widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.int_mutation_parameters.update({"distribution_index":var}),
                                                                  error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                                  error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_parameters["distribution_index"],
                                                                  widget_update_lambda=lambda var: self.distribution_index_entry.set(var)) )
                
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                                  widget_read_lambda=lambda: self.MutationOption.get(),
                                                                  variable_store_lambda=self.__store_int_mutation_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_choice,
                                                                  widget_update_lambda=lambda var: self.MutationOption.set(var)) )

            def __store_int_mutation_option(self, value):
                self.algorithm_parameters.int_mutation_choice = value
                
            def disable(self):
                self.configure(text="Integer mutation (Disabled)")
                self.mutation_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                self.distribution_index_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Integer mutation")
                self.mutation_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
                self.distribution_index_entry.config(state=tk.NORMAL)
                
        class BinaryMutationFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.MutationFrame.BinaryMutationFrame,self).__init__(master=master, text="Binary mutation", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.mutation_options = [AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.3 )
                self.MutationOption = tk.StringVar(self)
                self.MutationOption.set( self.mutation_options[0] )
                self.mutation_option = tk.OptionMenu(self, self.MutationOption, *self.mutation_options)
                self.mutation_option.config( state=tk.DISABLED )
                self.mutation_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.binary_mutation_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                
                self.mutation_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (Binary mutation)", lower_bound=0.0, upper_bound=1.0)
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.binary_mutation_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.binary_mutation_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
            
                    
                self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                                  widget_read_lambda=lambda: self.MutationOption.get(),
                                                                  variable_store_lambda=self.__store_binary_mutation_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.binary_mutation_choice,
                                                                  widget_update_lambda=lambda var: self.MutationOption.set(var)) )
                
            
            def __store_binary_mutation_option(self, value):
                self.algorithm_parameters.binary_mutation_choice = value
                
            def disable(self):
                self.configure(text="Binary mutation (Disabled)")
                self.mutation_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Binary mutation")
                self.mutation_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
        
                
        class PermutationMutationFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(AlgorithmTab.MutationFrame.PermutationMutationFrame,self).__init__(master=master, text="Permutation mutation", *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.mutation_options = [option.value for option in AlgorithmParameters.PERMUTATION_MUTATION]
                
                tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.35 )
                self.MutationOption = tk.StringVar(self)
                self.MutationOption.set( self.mutation_options[0] )
                self.mutation_option = tk.OptionMenu(self, self.MutationOption, *self.mutation_options)
                self.mutation_option.config( state=tk.NORMAL )
                self.mutation_option.place( relx=0.15, rely=0.17, relwidth=0.3 )
                
                tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
                self.probability_entry.insert(0, self.algorithm_parameters.permutation_mutation_parameters["probability"])
                self.probability_entry.config(state=tk.NORMAL)
                
                self.mutation_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
                self.probability_parameter = Float(name="probability", fancy_name="Probability (Permutation mutation)", lower_bound=0.0, upper_bound=1.0)
            
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.permutation_mutation_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.permutation_mutation_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.probability_entry.set(var)) )
                
                    
                self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                                  widget_read_lambda=lambda: self.MutationOption.get(),
                                                                  variable_store_lambda=self.__store_permutation_mutation_option,
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.permutation_mutation_choice,
                                                                  widget_update_lambda=lambda var: self.MutationOption.set(var)) )
                
            def __store_permutation_mutation_option(self, value):
                self.algorithm_parameters.permutation_mutation_choice = value
                
            def disable(self):
                self.configure(text="Permutation mutation (Disabled)")
                self.mutation_option.config(state=tk.DISABLED)
                self.probability_entry.config(state=tk.DISABLED)
                
            def enable(self):
                self.configure(text="Permutation mutation")
                self.mutation_option.config(state=tk.NORMAL)
                self.probability_entry.config(state=tk.NORMAL)
                
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AlgorithmTab.MutationFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            self.float_frame = AlgorithmTab.MutationFrame.FloatMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.int_frame = AlgorithmTab.MutationFrame.IntMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.binary_frame = AlgorithmTab.MutationFrame.BinaryMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            self.permutation_frame = AlgorithmTab.MutationFrame.PermutationMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
            
            self.float_frame.place( relx=0.025, rely=0.05, relwidth=0.4, relheight=0.3 )
            self.int_frame.place( relx=0.025, rely=0.38, relwidth=0.4, relheight=0.3 )
            self.binary_frame.place( relx=0.025, rely=0.71, relwidth=0.4, relheight=0.11 )
            self.permutation_frame.place( relx=0.025, rely=0.85, relwidth=0.4, relheight=0.11 )
            
            self.float_frame.disable()
            self.int_frame.disable()
            self.binary_frame.disable()
            self.permutation_frame.disable()
            
        def check_errors(self):
            error_list = super(AlgorithmTab.MutationFrame,self).check_errors()
            
            used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            if variable_types.FloatVariable in used_variable_types:
                error_list.extend( self.float_frame.check_errors() )
            
            if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
                error_list.extend( self.int_frame.check_errors() )
            
            if variable_types.BinaryVariable in used_variable_types:
                error_list.extend( self.binary_frame.check_errors() )
            
            if variable_types.PermutationVariable in used_variable_types:
                error_list.extend( self.permutation_frame.check_errors() )
            
            return error_list
        
        
        def save_parameters(self):
            
            used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            if variable_types.FloatVariable in used_variable_types:
                self.float_frame.save_parameters()
            
            if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
                self.int_frame.save_parameters()
            
            if variable_types.BinaryVariable in used_variable_types:
                self.binary_frame.save_parameters()
            
            if variable_types.PermutationVariable in used_variable_types:
                self.permutation_frame.save_parameters()
                
        def load_parameters(self):
            
            # used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
            
            self.float_frame.load_parameters()
            self.int_frame.load_parameters()
            self.binary_frame.load_parameters()
            self.permutation_frame.load_parameters()
            
    
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
 
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AlgorithmTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        # algorithm_optionlist = [ option.value for option in AlgorithmParameters.SUPPORTED_ALGORITHMS ]
        algorithm_optionlist = [ AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value, AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value ]
        
        tk.Label( self, text="Algorithm", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.AlgorithmOption = tk.StringVar(self)
        self.AlgorithmOption.set(algorithm_optionlist[0])
        algorithm_option = tk.OptionMenu(self, self.AlgorithmOption, *algorithm_optionlist, command=self.update_algorithm_selection)
        algorithm_option.config( font=('URW Gothic L','11') )
        algorithm_option.config( state=tk.NORMAL )
        algorithm_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.frames = {}
        self.frames["Population"] = AlgorithmTab.PopulationFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Offspring"] = AlgorithmTab.OffspringFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Selection"] = AlgorithmTab.SelectionFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Crossover"] = AlgorithmTab.CrossoverFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        self.frames["Mutation"] = AlgorithmTab.MutationFrame( master=self, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters )
        
        self.items_list = {}
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        self.items_list[AlgorithmParameters.SUPPORTED_ALGORITHMS.GA_MONO.value] = ["Population", "Offspring", "Selection", "Crossover", "Mutation"]
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        
        self.selected_frame_key = "Population"
        self.frames[self.selected_frame_key].display()
        self.update_algorithm_selection( AlgorithmParameters.SUPPORTED_ALGORITHMS.NSGAII.value )
        
        self.parameters_listbox.activate(0)
        self.parameters_listbox.selection_set(0)
        
        self.console = Console(master=self, font=("Liberation Mono", 11))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        # self.console.print_message("Mensaje\n")
        # self.console.print_warning("Advertencia\n")
        # self.console.print_error("Error\n")
        
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
        
        self.algorithm_parameters.choice = self.AlgorithmOption.get()
        
        for key in self.items_list[self.AlgorithmOption.get()]:
            self.frames[key].save_parameters()
            
    def load_parameters(self):
        
        self.algorithm_parameters.choice = self.AlgorithmOption.get()
        
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