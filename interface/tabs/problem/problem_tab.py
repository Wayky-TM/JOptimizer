# -*- coding: utf-8 -*-


import imp
import os
import sys

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
from pathlib import Path
import inspect

# import core.variable as variable_types
# import core.constant as constant_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from core.evaluator import Evaluator
from util.type_check import is_integer, is_float, to_integer
from util.string_utils import remove_whitespaces

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding, EntryInvalidator, EntryValidator, ClearInsertEntry
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame
from interface.style_definitions import AppStyle

""" Frames """
from interface.tabs.problem.frames.problem_frame import ProblemFrame
from interface.tabs.problem.frames.evaluator_frame import EvaluatorFrame
from interface.tabs.problem.frames.python_frame import PythonFrame

from interface.tabs.problem.frames.variables_frame import VariablesFrame
from interface.tabs.problem.frames.constants_frame import ConstantsFrame
from interface.tabs.problem.frames.constraints_frame import ConstraintsFrame

try:
    import matlab.engine
    MATLAB_AVAILABLE=True
except ImportError as e:
    MATLAB_AVAILABLE=False

if MATLAB_AVAILABLE:
    from interface.tabs.problem.frames.matlab_frame import MatlabFrame


class ProblemTab(ttk.Frame):    
    
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            # print(data)
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = data
            self.frames[self.selected_frame_key].display()
        
    def __template_change__(self, new_selection):
        
        self.parameters_listbox.delete(0,'end')
        
        item_list = self.items_list[new_selection]
        
        if self.selected_frame_key not in item_list:
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = item_list[0]
            self.frames[self.selected_frame_key].display()
        
        for option in item_list:
            self.parameters_listbox.insert(tk.END, option)
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ProblemTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        
        # templates_optionlist = [ option.value for option in ProblemParameters.PROBLEM_TEMPLATES ]
        templates_optionlist = [ ProblemParameters.PROBLEM_TEMPLATES.PYTHON.value ]
        
        if MATLAB_AVAILABLE:
            templates_optionlist.append( ProblemParameters.PROBLEM_TEMPLATES.MATLAB.value )
        
        ttk.Label( self, text="Template", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.TemplateOption = tk.StringVar(self)
        self.TemplateOption.set(ProblemParameters.PROBLEM_TEMPLATES.PYTHON.value)
        template_option = tk.OptionMenu(self, self.TemplateOption, *templates_optionlist, command=self.__template_change__)
        template_option.config( font=('URW Gothic L','11') )
        template_option.config( state=tk.NORMAL )
        template_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.frames = {}
        self.frames["Evaluator"] = EvaluatorFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Function"] = PythonFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Script"] = MatlabFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Variables"] = VariablesFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constants"] = ConstantsFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constraints"] = ConstraintsFrame( master=self, problem_parameters=self.problem_parameters )
        
        self.items_list = {}
        self.items_list[ ProblemParameters.PROBLEM_TEMPLATES.GENERIC.value ] = [ "Evaluator", "Variables", "Constants", "Constraints" ]
        self.items_list[ ProblemParameters.PROBLEM_TEMPLATES.PYTHON.value ] = [ "Function", "Variables", "Constants", "Constraints" ]
        self.items_list[ ProblemParameters.PROBLEM_TEMPLATES.MATLAB.value ] = [ "Script", "Variables", "Constants", "Constraints" ]
        self.items_list[ ProblemParameters.PROBLEM_TEMPLATES.CST.value ] = [ "CST", "Variables", "Constants", "Constraints" ]
        
        self.selected_frame_key = "Function"
        self.frames[self.selected_frame_key].display()
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        self.parameters_listbox.insert(0, "Function")
        self.parameters_listbox.insert(tk.END, "Variables")
        self.parameters_listbox.insert(tk.END, "Constants")
        self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        self.parameters_listbox.activate(0)
        
        self.parameters_frame = tk.Frame(master=self)
        self.parameters_frame.place()
        
        """ Error console frame """
        self.error_console_frame = tk.Frame( master=self, bg=AppStyle.frame_background_color )
        self.error_console_frame.config(highlightbackground=AppStyle.frame_border_color, highlightthickness=1)
        self.error_console_frame.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        tk.Label(master=self.error_console_frame, text="Error Console", font=('TkDefaultFont','10','bold'), bg=AppStyle.frame_background_color).place(relx=0.0035, rely=0.03)
        self.console = Console(master=self.error_console_frame, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.0035, rely=0.18, relwidth=0.993, relheight=0.795 )
        
        
    def check_errors(self):
        
        error_list = []
        
        for key in self.items_list[self.TemplateOption.get()]:
            error_list.extend( self.frames[key].check_errors() )
        
        return error_list
    
    def save_parameters(self):
        
        self.problem_parameters.options["template"] = self.TemplateOption.get()
        
        for key in self.items_list[self.TemplateOption.get()]:
            self.frames[key].save_parameters()
            
    def load_parameters(self):
        
        self.problem_parameters.options["template"] = self.TemplateOption.get()
        
        for key in self.items_list[self.TemplateOption.get()]:
            self.frames[key].load_parameters()
    
    def console_print_error(self, string: str):
        self.console.print_error( string+"\n" )
        
    def console_print_warning(self, string: str):
        self.console.print_warning( string+"\n" )
        
    def console_print_message(self, string: str):
        self.console.print_message( string+"\n" )
        
    def console_clear(self):
        self.console.clear_all()
        
        
        