# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 22:21:46 2021

@author: Wayky
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

from interface.parameter_binding import ParameterBinding
from abc import *


class ParameterFrame(tk.Frame):
    
    def __init__(self, master, *args, **kwargs):
        super(ParameterFrame, self).__init__(master=master, *args, **kwargs)
        
        self.parameters_bindings = []
        
    def check_errors(self):
        
        error_list = []
        
        for binding in self.parameters_bindings:
            error_list.extend(binding.error_check())
            
        return error_list
            
    def save_parameters(self):
        
        for binding in self.parameters_bindings:
            binding.store_value()
        
    @abstractmethod
    def display(self):
        pass
    
    def hide(self):
        self.place_forget()
        
    @abstractmethod
    def disable(self):
        pass
        
    @abstractmethod
    def enable(self):
        pass
                
                
class ParameterLabelFrame(tk.LabelFrame):
    
    def __init__(self, master, *args, **kwargs):
        super(ParameterLabelFrame, self).__init__(master=master, *args, **kwargs)
        
        self.parameters_bindings = []
        
    def check_errors(self):
        
        error_list = []
        
        for binding in self.parameters_bindings:
            error_list.extend(binding.error_check())
            
        return error_list
            
    def save_parameters(self):
        
        for binding in self.parameters_bindings:
            binding.store_value()
            
            
    @abstractmethod
    def display(self):
        pass
    
    def hide(self):
        self.place_forget()
        
    @abstractmethod
    def disable(self):
        pass
        
    @abstractmethod
    def enable(self):
        pass
                
