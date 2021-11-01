# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:55:55 2021

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
import multiprocessing
# import numpy as np

import core.variable as variable_types
# from core.algorithm_parameters import AlgorithmParameters
# from core.problem_parameters import ProblemParameters
from core.engine_parameters import EngineParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle



class RuntimeTab(ttk.Frame):
    
    class RuntimeFrame(ParameterLabelFrame):
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.RuntimeFrame, self).__init__(master=master, *args, **kwargs)
            
            self.engine_parameters = engine_parameters
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
    class TerminationCriteriaFrame(RuntimeFrame):
        
        def __update_time__(self, var):
            self.time_entry.configure( state=tk.NORMAL )
            
            ClearInsertEntry(self.time_entry, str(var))
            
            if EngineParameters.TERMINATION_CRITERIA.TIME.value not in self.engine_parameters.temination_criteria:
                self.time_entry.configure( state=tk.DISABLED )
            
        def __update_timescale__(self, var):
            self.TimescaleOption.set(var)
            
            if EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
                self.timescale_option.configure( state=tk.NORMAL )
                
            else:
                self.timescale_option.configure( state=tk.DISABLED )
            
        def __update_evaluations__(self, var):
            self.eval_entry.configure( state=tk.NORMAL )
            ClearInsertEntry(self.eval_entry, str(var))
            
            if EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value not in self.engine_parameters.temination_criteria:
                self.eval_entry.configure( state=tk.DISABLED )
            
        
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.TerminationCriteriaFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Stop by:").place( relx=0.02, rely=0.05 )
            
            self.time_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.time_entry.insert(0, self.engine_parameters.termination_parameters["time"])
            self.time_entry.place(relx=0.10, rely=0.11+0.005, relwidth=0.06)
            self.time_entry.config(state=tk.DISABLED)
            
            self.timescale_optionlist = [ option.value for option in EngineParameters.TIME_SCALE ]
            self.TimescaleOption = tk.StringVar(master=self)
            self.TimescaleOption.set( self.timescale_optionlist[0] )
            self.timescale_option = tk.OptionMenu(self, self.TimescaleOption, *self.timescale_optionlist)
            self.timescale_option.place(relx=0.17,rely=0.11-0.005, relwidth=0.07)
            self.timescale_option.config(state=tk.DISABLED)
            
            self.time_checkbox_var = tk.BooleanVar(master=self)
            self.time_checkbox = ttk.Checkbutton(master=self, text="Time", variable=self.time_checkbox_var, command=self._time_checkbox_command_)
            self.time_checkbox.config( state=tk.NORMAL )
            self.time_checkbox.place( relx=0.05,rely=0.11 )
            
            self.eval_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.eval_entry.insert(0, self.engine_parameters.termination_parameters["evaluations"])
            self.eval_entry.place(relx=0.12, rely=0.17+0.005, relwidth=0.04)
            self.eval_entry.config(state=tk.DISABLED)
            
            self.eval_checkbox_var = tk.BooleanVar(master=self)
            self.eval_checkbox = ttk.Checkbutton(master=self, text="Evaluations", variable=self.eval_checkbox_var, command=self._eval_checkbox_command_)
            self.eval_checkbox.config( state=tk.NORMAL )
            self.eval_checkbox.place( relx=0.05,rely=0.17 )
            
            self.by_time_parameter = Parameter( name="by_time" )
            self.by_eval_parameter = Parameter( name="by_eval" )
            self.time_parameter = Integer( name="time", fancy_name="Time", lower_bound=1, upper_bound=99999999 )
            self.eval_parameter = Integer( name="evaluations", fancy_name="Evaluations", lower_bound=1, upper_bound=99999999 )
            self.time_scale_parameter = Parameter( name="time_scale" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.by_time_parameter,
                                                              widget_read_lambda=lambda: self.time_checkbox_var.get(),
                                                              variable_store_lambda=self._save_time_boolean,
                                                              variable_read_lambda=lambda: EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria,
                                                              widget_update_lambda=lambda var: self.time_checkbox_var.set(var)) )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.by_eval_parameter,
                                                              widget_read_lambda=lambda: self.eval_checkbox_var.get(),
                                                              variable_store_lambda=self._save_eval_boolean,
                                                              variable_read_lambda=lambda: EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria,
                                                              widget_update_lambda=lambda var: self.eval_checkbox_var.set(var)) )
            
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.eval_parameter,
                                                              widget_read_lambda=lambda: self.eval_entry.get(),
                                                              variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"evaluations":var}),
                                                              error_set_lambda=EntryInvalidator(self.eval_entry),
                                                              error_reset_lambda=EntryValidator(self.eval_entry),
                                                              variable_read_lambda=lambda: self.engine_parameters.termination_parameters["evaluations"],
                                                              widget_update_lambda=lambda var: self.__update_evaluations__(var)) )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.time_parameter,
                                                              widget_read_lambda=lambda: self.time_entry.get(),
                                                              variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"time":var}),
                                                              error_set_lambda=EntryInvalidator(self.time_entry),
                                                              error_reset_lambda=EntryValidator(self.time_entry),
                                                              variable_read_lambda=lambda: self.engine_parameters.termination_parameters["time"],
                                                              widget_update_lambda=lambda var: self.__update_time__(var)) )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.time_scale_parameter,
                                                              widget_read_lambda=lambda: self.TimescaleOption.get(),
                                                              variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"time_scale":var}),
                                                              variable_read_lambda=lambda: self.engine_parameters.termination_parameters["time_scale"],
                                                              widget_update_lambda=lambda var: self.__update_timescale__(var)) )
        
        
        def _save_time_boolean(self, var):
            
            if var:
                self.engine_parameters.temination_criteria.add( EngineParameters.TERMINATION_CRITERIA.TIME.value )
            else:
                if EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
                    self.engine_parameters.temination_criteria.remove( EngineParameters.TERMINATION_CRITERIA.TIME.value )
                
        def _save_eval_boolean(self, var):
            
            if var:
                self.engine_parameters.temination_criteria.add( EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value )
            else:
                if EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria:
                    self.engine_parameters.temination_criteria.remove( EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value )
            
        def _time_checkbox_command_(self):
            
            if self.time_checkbox_var.get():
                self.timescale_option.configure( state=tk.NORMAL )
                self.time_entry.configure( state=tk.NORMAL )
            else:
                self.timescale_option.configure( state=tk.DISABLED )
                self.time_entry.configure( state=tk.DISABLED )
                
        def _eval_checkbox_command_(self):
            
            if self.eval_checkbox_var.get():
                self.eval_entry.configure( state=tk.NORMAL )
            else:
                self.eval_entry.configure( state=tk.DISABLED )
            
                
    class ThreadsFrame(RuntimeFrame):
        
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.ThreadsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
            
            self.threads_label = tk.Label(master=self, text="Threads")
            self.threads_label.place( relx=0.02, rely=0.05 )
            
            self.threads_optionlist = [i for i in range(1,multiprocessing.cpu_count()+1)]
            self.ThreadsOption = tk.IntVar(master=self)
            self.ThreadsOption.set( self.threads_optionlist[0] )
            self.threads_option = tk.OptionMenu(self, self.ThreadsOption, *self.threads_optionlist)
            self.threads_option.place(relx=0.08,rely=0.05-0.005, relwidth=0.06)
            self.threads_option.config(state=tk.NORMAL)
            
            self.threads_parameter = Parameter( name="threads", fancy_name="Threads" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.threads_parameter,
                                                              widget_read_lambda=lambda: self.ThreadsOption.get(),
                                                              variable_store_lambda=lambda var: self.engine_parameters.mode_parameters.update( {"threads":var} ),
                                                              variable_read_lambda=lambda: self.engine_parameters.termination_parameters["threads"],
                                                              widget_update_lambda=lambda var: self.ThreadsOption.set(var)) )
            
            
    class StateSavingFrame(RuntimeFrame):
        
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.StateSavingFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Runtime state saving").place( relx=0.5, rely=0.5 )
            
            
    class StatisticsFrame(RuntimeFrame):
        
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.StatisticsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Runtime Statistics").place( relx=0.5, rely=0.5 )
            
            
    class PlotsFrame(RuntimeFrame):
        
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.PlotsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Runtime plots").place( relx=0.5, rely=0.5 )
    
    
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = data
            self.frames[self.selected_frame_key].display()
            
    def update_mode_selection(self, new_selection):
        
        self.parameters_listbox.delete(0,'end')
        self.selected_mode = new_selection
        
        item_list = self.items_list[new_selection]
        
        if self.selected_frame_key not in item_list:
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = item_list[0]
            self.frames[self.selected_frame_key].display()
            
        
        for option in item_list:
            self.parameters_listbox.insert(tk.END, option)
    
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(RuntimeTab, self).__init__(master=master, *args, **kwargs)
        
        self.engine_parameters = engine_parameters
        
        mode_optionlist = [ option.value for option in EngineParameters.SUPPORTED_MODES ]
        
        tk.Label( self, text="Mode", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.ModeOption = tk.StringVar(self)
        self.ModeOption.set(mode_optionlist[0])
        algorithm_option = tk.OptionMenu(self, self.ModeOption, *mode_optionlist, command=self.update_mode_selection)
        algorithm_option.config( font=('URW Gothic L','11') )
        algorithm_option.config( state=tk.NORMAL )
        algorithm_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.items_list = {}
        self.items_list[EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value] = ["Termination criteria", "State saving", "Statistics", "Plots"]
        self.items_list[EngineParameters.SUPPORTED_MODES.MULTITHREADED.value] = ["Termination criteria", "Threads", "State saving", "Statistics", "Plots"]
        self.selected_mode = EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value
        
        self.frames = {}
        self.frames["Termination criteria"] = RuntimeTab.TerminationCriteriaFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Threads"] = RuntimeTab.ThreadsFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["State saving"] = RuntimeTab.StateSavingFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Statistics"] = RuntimeTab.StatisticsFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Plots"] = RuntimeTab.PlotsFrame(master=self, engine_parameters=self.engine_parameters)
        
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        
        self.selected_frame_key = "Termination criteria"
        self.frames[self.selected_frame_key].display()
        self.update_mode_selection( EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value )
        
        self.parameters_listbox.activate(0)
        self.parameters_listbox.selection_set(0)
        
        """ Error console frame """
        self.error_console_frame = tk.Frame( master=self, bg=AppStyle.frame_background_color )
        self.error_console_frame.config(highlightbackground=AppStyle.frame_border_color, highlightthickness=1)
        self.error_console_frame.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        tk.Label(master=self.error_console_frame, text="Error Console", font=('TkDefaultFont','10','bold'), bg=AppStyle.frame_background_color).place(relx=0.0035, rely=0.03)
        self.console = Console(master=self.error_console_frame, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.0035, rely=0.18, relwidth=0.993, relheight=0.795 )
        
    def check_errors(self):
        
        error_list = []
        
        for key in self.items_list[self.selected_mode]:
            error_list.extend( self.frames[key].check_errors() )
        
        return error_list
    
    def save_parameters(self):
        
        self.engine_parameters.mode = self.ModeOption.get()
        
        for key in self.items_list[self.ModeOption.get()]:
            self.frames[key].save_parameters()
            
    def load_parameters(self):
        
        self.ModeOption.set( self.engine_parameters.mode )
        
        for key in self.items_list[ self.engine_parameters.mode ]:
            self.frames[key].load_parameters()
        
    def console_print_error(self, string: str):
        self.console.print_error( string+"\n" )
        
    def console_print_warning(self, string: str):
        self.console.print_warning( string+"\n" )
        
    def console_print_message(self, string: str):
        self.console.print_message( string+"\n" )
        
    def console_clear(self):
        self.console.clear_all()