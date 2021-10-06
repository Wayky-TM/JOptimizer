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
# import numpy as np

import core.variable as variable_types
# from core.algorithm_parameters import AlgorithmParameters
# from core.problem_parameters import ProblemParameters
from core.engine_parameters import EngineParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame




class RuntimeTab(ttk.Frame):
    
    class RuntimeFrame(ParameterLabelFrame):
        def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
            super(RuntimeTab.RuntimeFrame, self).__init__(master=master, *args, **kwargs)
            
            self.engine_parameters = engine_parameters
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
            
    class TerminationCriteriaFrame(RuntimeFrame):
        
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
            self.timescale_option.place(relx=0.17,rely=0.11-0.5, relwidth=0.07)
            self.timescale_option.config(state=tk.DISABLED)
            
            self.time_checkbox_var = tk.BooleanVar(master=self)
            self.time_checkbox = ttk.Checkbutton(master=self, text="Time", variable=self.time_checkbox_var, command=self._time_checkbox_command_)
            self.time_checkbox.config( state=tk.NORMAL )
            self.time_checkbox.place( relx=0.05,rely=0.11 )
            
        def _time_checkbox_command_(self):
            
            if self.time_checkbox_var.get():
                self.timescale_option.configure( state=tk.NORMAL )
                self.time_entry.configure( state=tk.NORMAL )
            else:
                self.timescale_option.configure( state=tk.DISABLED )
                self.time_entry.configure( state=tk.DISABLED )
                
            
            
            
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
        self.items_list[EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value] = ["Termination criteria", "Runtime state saving", "Runtime statistics", "Runtime plots"]
        
        self.frames = {}
        self.frames["Termination criteria"] = RuntimeTab.TerminationCriteriaFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Runtime state saving"] = RuntimeTab.StateSavingFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Runtime statistics"] = RuntimeTab.StatisticsFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Runtime plots"] = RuntimeTab.PlotsFrame(master=self, engine_parameters=self.engine_parameters)
        
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        
        self.selected_frame_key = "Termination criteria"
        self.frames[self.selected_frame_key].display()
        self.update_mode_selection( EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value )
        
        self.parameters_listbox.activate(0)
        self.parameters_listbox.selection_set(0)
        
        self.console = Console(master=self, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")