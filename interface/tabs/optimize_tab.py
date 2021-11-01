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
from interface.stats_table import StatsTable
from interface.popups.solution_analysis_popup import solution_analysis_popup
from interface.style_definitions import AppStyle

class OptimizeTab(ttk.Frame):
    
    class RUNTIME_STATUS(Enum):
        INITIALIZED="Initialized"
        RUNNING="Running"
        PAUSED="Paused"
        FINISHED="Paused"
    
        
    def finished(self):
        self.run_pause_button.config( text="Run", state=tk.DISABLED )
        self.analysis_button.config( state=tk.NORMAL )
        self.save_button.config( state=tk.NORMAL )
        self.runtime_status = OptimizeTab.RUNTIME_STATUS.FINISHED
        self.console.print_message("Algorithm execution finished")
        self.controller.bell()
        self.controller._enable_tabs()
        self.progressbar['value'] = 100
    
    def paused(self):
        self.run_pause_button.config( text="Run" )
        self.run_pause_button.config( state=tk.NORMAL )
        self.analysis_button.config( state=tk.NORMAL )
        self.save_button.config( state=tk.NORMAL )
        self.runtime_status = OptimizeTab.RUNTIME_STATUS.PAUSED
        self.console.print_message("Algorithm execution paused")
    
    def __run_pause(self):
        
        if self.runtime_status == OptimizeTab.RUNTIME_STATUS.INITIALIZED:
            self.run_pause_button.config( state=tk.DISABLED )
            self.analysis_button.config( state=tk.DISABLED )
            self.save_button.config( state=tk.DISABLED )
            # self.console.print_message("Initializing engine...")
            
            if self.controller.launch_optimization():
                self.run_pause_button.config( text="Pause" )
                self.runtime_status = OptimizeTab.RUNTIME_STATUS.RUNNING
                self.console.print_message("Successful engine initialization")
                self.controller._disable_tabs()
                self.console.print_message("Launching algorithm")
                
            else:
                self.console.print_error("Optimization engine could not be launched")
                
            self.run_pause_button.config( state=tk.NORMAL )
            
        elif self.runtime_status == OptimizeTab.RUNTIME_STATUS.RUNNING:
            self.console.print_warning("Pause requested, waiting evaluation(s) to complete")
            self.run_pause_button.config( state=tk.DISABLED )
            self.controller.pause_optimization()
            
        elif self.runtime_status == OptimizeTab.RUNTIME_STATUS.PAUSED:
            self.console.print_message("Resuming execution")
            self.controller.resume_optimization()
            self.run_pause_button.config( text="Pause" )
            self.analysis_button.config( state=tk.DISABLED )
            self.save_button.config( state=tk.DISABLED )
            self.runtime_status = OptimizeTab.RUNTIME_STATUS.RUNNING
        
    
    def __results_analysis(self):
        solution_analysis_popup( controller=self.controller )
    
    def __save_solutions(self):
        pass
    
    def __refresh_stats__(self):
        self.stats_tree.update_stats()
    
    def __init__(self, master, controller, *args, **kwargs):
        super(OptimizeTab, self).__init__(master=master, *args, **kwargs)
        
        self.background_color = "#99ccff"
        self.border_color = "#004d99"
        
        self.controller = controller
        self.runtime_status = OptimizeTab.RUNTIME_STATUS.INITIALIZED
        
        # self.runtime_stats_frame = tk.LabelFrame( master=self, text="Runtime stats", font=('TkDefaultFont','10','bold'), bg="#66b3ff" )
        self.runtime_stats_frame = tk.Frame( master=self, bg=AppStyle.frame_background_color )
        self.runtime_stats_frame.config(highlightbackground=AppStyle.frame_border_color, highlightthickness=1)
        self.runtime_stats_frame.place( relx=0.015, rely=0.024, relwidth=0.4, relheight=0.55 )
        
        Label( master=self.runtime_stats_frame, text="Runtime Stats", font=('TkDefaultFont','10','bold'), bg=self.background_color ).place( relx=0.005, rely=0.005 )
        
        self.stats_tree = StatsTable(master=self.runtime_stats_frame)
        
        # self.stats_tree.place( relx=0, rely=0.05, relwidth=1.0, relheight=0.95 )
        self.stats_tree.place( relx=0.005, rely=0.065, relwidth=0.99, relheight=0.93 )
        
        self.stats_tree.add_stat(name="Evaluations", update_lambda=self.controller.__evaluations_callback__)
        self.stats_tree.add_stat(name="Avg. Time/evaluation", update_lambda=self.controller.__avgTimeEvaluation_callback__)
        self.stats_tree.add_stat(name="Elapsed time", update_lambda=self.controller.__elapsedTime_callback__)
        self.stats_tree.add_stat(name="Elapsed computation time", update_lambda=self.controller.__elapsedComputingTime_callback__)
        self.stats_tree.add_stat(name="ETA", update_lambda=self.controller.__ETA_callback__)
        
        # self.console_frame = tk.LabelFrame( master=self, text="Runtime console", font=('URW Gothic L','10','bold') )
        self.console_frame = tk.Frame( master=self, bg=self.background_color )
        self.console_frame.config(highlightbackground=self.border_color, highlightthickness=1)
        self.console_frame.place( relx=0.015, rely=0.598, relwidth=0.4, relheight=0.28 )
        self.console_frame.config(highlightbackground=self.border_color, highlightthickness=1)
        
        
        Label( master=self.console_frame, text="Runtime Console", font=('TkDefaultFont','10','bold'), bg=self.background_color ).place( relx=0.005, rely=0.0125 )
        
        self.console = TimedConsole(master=self.console_frame, font=("Liberation Mono", 11))
        self.console.place( relx=0.005, rely=0.132, relwidth=0.9875, relheight=0.85 )
        
        # self.progress_stats_frame = tk.LabelFrame( master=self, text="Progress statistics", font=('URW Gothic L','10','bold') )
        self.progress_stats_frame = tk.Frame( master=self, bg=self.background_color )
        self.progress_stats_frame.config(highlightbackground=self.border_color, highlightthickness=1)
        self.progress_stats_frame.place( relx=0.43, rely=0.024, relwidth=0.555, relheight=0.854 )
        tk.Label( master=self.progress_stats_frame, text="Progress Statistics", bg=self.background_color, font=('TkDefaultFont L','11','bold') ).place(relx=0.005, rely=0.005)
        self.stats_frame = tk.Frame( master=self.progress_stats_frame, bg="white" )
        self.stats_frame.place( relx=0.005, rely=0.045, relwidth=0.99, relheight=0.95 )
        tk.Label( master=self.stats_frame, text="#To be implemented", font=('URW Gothic L','11','bold') ).place(relx=0.45, rely=0.45)
        
        self.progressbar = ttk.Progressbar( master=self, mode='determinate' )
        self.progressbar.place( relx=0.015, rely=0.902, relwidth=0.7, relheight=0.074 )
        
        self.run_pause_button = tk.Button( master=self, text="Run", command=self.__run_pause, font=('URW Gothic L','12') )
        self.run_pause_button.place( relx=0.73, rely=0.902, relwidth=0.09, relheight=0.074 )
        
        self.analysis_button = tk.Button( master=self, text="Analysis", command=self.__results_analysis, font=('URW Gothic L','12') )
        self.analysis_button.place( relx=0.835, rely=0.902, relwidth=0.09, relheight=0.074 )
        self.analysis_button.config( state=tk.DISABLED )
        
        # save_icon_path = os.path.join( os.getcwd(), 'interface', 'resources', 'images', 'save_icon.png' )
        # save_icon = tk.PhotoImage( file=save_icon_path )
        # save_icon = save_icon.subsample(2,2)
        
        self.save_button = tk.Button( master=self, text="Save", command=self.__save_solutions, font=('URW Gothic L','12') )
        # self.save_button = tk.Button( master=self, image=save_icon, command=self.__save_solutions, compound=tk.CENTER )
        # self.save_button.image = save_icon_tk
        # self.save_button = tk.Button( master=self, command=self.__save_solutions, font=('URW Gothic L','12') )
        self.save_button.place( relx=0.94, rely=0.902, relwidth=0.045, relheight=0.074 )
        self.save_button.config( state=tk.DISABLED )
        
        