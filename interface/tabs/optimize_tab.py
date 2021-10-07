# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:56:44 2021

@author: Álvaro
"""
import os
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
from interface.console import Console, TimedConsole
from interface.parameter_binding import ParameterBinding
from interface.parameter_frames import ParameterFrame, ParameterLabelFrame, NullParameterFrame

# from PIL import Image, ImageTk
# import Image
# import ImageTk

class OptimizeTab(ttk.Frame):
    
    class RUNTIME_STATUS(Enum):
        INITIALIZED="Initialized"
        RUNNING="Running"
        PAUSED="Paused"
    
    def __run_pause(self):
        
        if self.runtime_status == OptimizeTab.RUNTIME_STATUS.INITIALIZED:
            self.run_pause_button.config( text="Pause" )
            self.analysis_button.config( state=tk.DISABLED )
            self.save_button.config( state=tk.DISABLED )
            self.runtime_status = OptimizeTab.RUNTIME_STATUS.RUNNING
            
        elif self.runtime_status == OptimizeTab.RUNTIME_STATUS.RUNNING:
            self.run_pause_button.config( text="Run" )
            self.analysis_button.config( state=tk.NORMAL )
            self.save_button.config( state=tk.NORMAL )
            self.runtime_status = OptimizeTab.RUNTIME_STATUS.PAUSED
            
        elif self.runtime_status == OptimizeTab.RUNTIME_STATUS.PAUSED:
            self.run_pause_button.config( text="Pause" )
            self.analysis_button.config( state=tk.DISABLED )
            self.save_button.config( state=tk.DISABLED )
            self.runtime_status = OptimizeTab.RUNTIME_STATUS.RUNNING
            pass
        
    
    def __results_analysis(self):
        pass
    
    def __save_solutions(self):
        pass
    
    def __init__(self, master, *args, **kwargs):
        super(OptimizeTab, self).__init__(master=master, *args, **kwargs)
        
        self.controller = master
        self.runtime_status = OptimizeTab.RUNTIME_STATUS.INITIALIZED
        
        self.runtime_stats_frame = tk.LabelFrame( master=self, text="Runtime stats", font=('URW Gothic L','10','bold') )
        self.runtime_stats_frame.place( relx=0.015, rely=0.024, relwidth=0.4, relheight=0.55 )
        
        self.console_frame = tk.LabelFrame( master=self, text="Runtime console", font=('URW Gothic L','10','bold') )
        self.console_frame.place( relx=0.015, rely=0.598, relwidth=0.4, relheight=0.28 )
        
        self.console = TimedConsole(master=self.console_frame, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.02, rely=0.05, relwidth=0.96, relheight=0.90 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")
        
        self.progress_stats_frame = tk.LabelFrame( master=self, text="Progress statistics", font=('URW Gothic L','10','bold') )
        self.progress_stats_frame.place( relx=0.43, rely=0.024, relwidth=0.555, relheight=0.854 )
        tk.Label( master=self.progress_stats_frame, text="#To be implemented", font=('URW Gothic L','11','bold') ).place(relx=0.45, rely=0.45)
        
        self.progressbar = ttk.Progressbar( master=self )
        self.progressbar.place( relx=0.015, rely=0.902, relwidth=0.7, relheight=0.074 )
        
        self.run_pause_button = tk.Button( master=self, text="Run", command=self.__run_pause, font=('URW Gothic L','12') )
        self.run_pause_button.place( relx=0.73, rely=0.902, relwidth=0.09, relheight=0.074 )
        
        self.analysis_button = tk.Button( master=self, text="Analysis", command=self.__results_analysis, font=('URW Gothic L','12') )
        self.analysis_button.place( relx=0.835, rely=0.902, relwidth=0.09, relheight=0.074 )
        self.analysis_button.config( state=tk.DISABLED )
        
        save_icon_path = os.path.join( os.getcwd(), 'interface', 'resources', 'images', 'save_icon.png' )
        save_icon = tk.PhotoImage( file=save_icon_path )
        # save_icon = save_icon.subsample(2,2)
        
        # self.save_button = tk.Button( master=self, image=save_icon_path, command=self.__run_pause, font=('URW Gothic L','12') )
        self.save_button = tk.Button( master=self, image=save_icon, command=self.__run_pause, compound=tk.CENTER )
        # self.save_button.image = save_icon_tk
        # self.save_button = tk.Button( master=self, command=self.__save_solutions, font=('URW Gothic L','12') )
        self.save_button.place( relx=0.94, rely=0.902, relwidth=0.045, relheight=0.074 )
        self.save_button.config( state=tk.DISABLED )
        
        