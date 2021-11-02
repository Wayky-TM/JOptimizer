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
from core.engine_parameters import EngineParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle

""" Frames """
from interface.tabs.runtime_enviroment.frames.termination_criteria_frame import TerminationCriteriaFrame
from interface.tabs.runtime_enviroment.frames.threads_frame import ThreadsFrame
from interface.tabs.runtime_enviroment.frames.statistics_frame import StatisticsFrame
from interface.tabs.runtime_enviroment.frames.state_saving_frame import StateSavingFrame
from interface.tabs.runtime_enviroment.frames.plots_frame import PlotsFrame


class RuntimeTab(ttk.Frame):
    
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
        self.frames["Termination criteria"] = TerminationCriteriaFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Threads"] = ThreadsFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["State saving"] = StateSavingFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Statistics"] = StatisticsFrame(master=self, engine_parameters=self.engine_parameters)
        self.frames["Plots"] = PlotsFrame(master=self, engine_parameters=self.engine_parameters)
        
        
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