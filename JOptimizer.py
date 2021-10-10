# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:05:45 2021

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
from typing import List
# import numpy as np

import core.variable as variable_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from core.engine_parameters import EngineParameters
from core.engine import OptimizationEngine
from util.type_check import is_integer, is_float

from interface.tabs.problem_definition_tab import ProblemTab
from interface.tabs.algorithm_config_tab import AlgorithmTab
from interface.tabs.runtime_config_tab import RuntimeTab
from interface.tabs.optimize_tab import OptimizeTab


class JOptimizer_App(tk.Tk):
    
    def __endOfGen_callback__(self):
        pass
    
    def __termination_callback__(self):
        self.__refresh_stats__()
        self.optimize_tab.__finnished()
    
    def __evaluations_callback__(self):
        return self.engine.algorithm.evaluations
    
    def __avgTimeEvaluation_callback__(self):
        if self.engine.algorithm.evaluations > 0:
            return time.strftime('%H:%M:%S', time.gmtime(self.engine.total_computing_time()/float(self.engine.algorithm.evaluations)))
                                 
        return "--:--:--"
    
    def __elapsedTime_callback__(self):
        time = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
        return time.strftime('%H:%M:%S', time.gmtime( time ))
    
    def __elapsedComputingTime_callback__(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.engine.total_computing_time()))
    
    def __ETA_callback__(self):
        estimations = []
        
        if self.engine_parameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria:
            time = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
            estimations.append( (time/float(self.engine.algorithm.evaluations))*(int(self.engine_parameters.termination_parameters["evaluations"]) - self.engine.algorithm.evaluations) )
            
        if self.engine_parameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
            time = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
            estimations.append( float(self.engine_parameters.termination_parameters["time"]) - time )
            
        if self.engine_parameters.TERMINATION_CRITERIA.DATE.value in self.engine_parameters.temination_criteria:
            estimations.append( self.engine_parameters.termination_parameters["datetime"] - datetime.datetime.now() )
            
        return time.strftime('%H:%M:%S', time.gmtime( min(estimations) ))
    
    
    def __refresh_stats__(self):
        self.optimize_tab.__refresh_stats__()
        
    
    def __init__(self, *args, **kwargs):
        super( JOptimizer_App, self ).__init__(*args, **kwargs)
        
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)
        
        self.window_width = int(self.screen_width*0.8)
        self.window_height = int(self.screen_height*0.8)
        
        self.wm_title("JOptimizer")
        self.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, ((self.screen_width/2)-(self.window_width/2)), ((self.screen_height/2)-(self.window_height/2))))
        self.title_font = tkfont.Font(family='Helvetica', size=int(0.01*self.screen_width), weight="bold", slant="italic")


        """
            Config. variables
        """
        self.engine_parameters = EngineParameters()
        self.problem_parameters = ProblemParameters()
        self.algorithm_parameters = AlgorithmParameters()
        self.engine = OptimizationEngine( engine_parameters=self.engine_parameters,
                                          problem_parameters=self.problem_parameters,
                                          algorithm_parameters=self.algorithm_parameters,
                                          endOfGen_callback=self.__endOfGen_callback__,
                                          termination_callback=self.__termination_callback__)

        """
            Menu
        """
        self. menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        

        """
            Tabs
        """
        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('URW Gothic L','11','bold') )
        
        self.tabs = ttk.Notebook( self )
        
        self.problem_tab = ProblemTab(master=self.tabs, problem_parameters=self.problem_parameters)
        self.algorithm_tab = AlgorithmTab(master=self.tabs, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters)
        self.runtime_enviroment_tab = RuntimeTab(master=self.tabs, engine_parameters=self.engine_parameters)
        self.optimize_tab = OptimizeTab(master=self.tabs, controller=self)
        
        self.tabs.add( self.problem_tab, text="   Problem   " )
        self.tabs.add( self.algorithm_tab, text="   Algorithm   " )
        self.tabs.add( self.runtime_enviroment_tab, text="   Runtime enviroment   " )
        self.tabs.add( self.optimize_tab, text="   Optimize   " )
        
        self.tabs.bind('<<NotebookTabChanged>>', self.changed_tag_handler)
        
        self.tabs.place( relx=0.01, rely=0.03, relwidth=0.98, relheight=0.95 )
        
        
    def check_parameter_correctness(self):
        
        self.problem_tab.console_clear()
        self.algorithm_tab.console_clear()
        self.runtime_enviroment_tab.console_clear()
        
        error_list = []
        
        problem_errors = self.problem_tab.check_errors()
        algorithm_errors = self.algorithm_tab.check_errors()
        runtime_enviroment_errors = self.runtime_enviroment_tab.check_errors()
        
        if len(problem_errors) > 0:
            
            for error in problem_errors:
                self.problem_tab.console_print_error( error )
            
            error_list.append("Problem parameters")
            
        if len(algorithm_errors) > 0:
            
            for error in algorithm_errors:
                self.algorithm_tab.console_print_error( error )
            
            error_list.append("Algorithm parameters")
            
        if len(runtime_enviroment_errors) > 0:
            
            for error in runtime_enviroment_errors:
                self.runtime_enviroment_tab.console_print_error( error )
            
            error_list.append("Runtime enviroment parameters")
        
        if len(error_list)>0:
            tk.messagebox.showerror(title="Invalid parameter(s)", message="Errors where found on the following tabs:\n\n" + "\n".join(["\t-" + s for s in error_list]) + "\n\nCheck error consoles for more information")
            return False
        
        return True
    
    def save_parameters(self):
        
        self.problem_tab.save_parameters()
        self.algorithm_tab.save_parameters()
        self.runtime_enviroment_tab.save_parameters()
        
    def launch_optimization(self):
        
        if self.check_parameter_correctness():    
            self.save_parameters()
            self.engine.launch()
            return True
            
        return False
        
        
    def changed_tag_handler(self, event):
        index = event.widget.index("current")
        
        if index == 1:
            self.algorithm_tab.update_types()
        

app = JOptimizer_App()
app.mainloop()