# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:05:45 2021

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


# from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List
import time
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
from interface.threadSafe_callable import ThreadSafeCallable
from interface.style_definitions import AppStyle

class JOptimizer_App(tk.Tk):
    
    def __paused_callback__(self):
        self.optimize_tab.paused()
    
    def __endOfGen_callback__(self):
        pass
    
    def __termination_callback__(self):
        
        if self._update_job != None:
            self.after_cancel(self._update_job)
            self._update_job = None
        
        self.optimize_tab.__refresh_stats__()
        self.optimize_tab.finished()
    
    
    
    def __evaluations_callback__(self):
        return self.engine.problem.evaluations
    
    def __avgTimeEvaluation_callback__(self):
        if self.engine.problem.evaluations > 0:
            return time.strftime('%H:%M:%S', time.gmtime(self.engine.algorithm.total_computing_time/float(self.engine.problem.evaluations)))
                                 
        return "--:--:--"
    
    def __elapsedTime_callback__(self):
        time_elapsed = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
        return time.strftime('%H:%M:%S', time.gmtime( time_elapsed ))
    
    def __elapsedComputingTime_callback__(self):
        return time.strftime('%H:%M:%S', time.gmtime(self.engine.algorithm.total_computing_time))
    
    def _compute_ETA_(self):
        estimations = []
        
        if self.engine_parameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria:
            time_elapsed = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
            estimations.append( (time_elapsed/float(self.engine.problem.evaluations))*(int(self.engine_parameters.termination_parameters["evaluations"]) - self.engine.problem.evaluations) )
            
        if self.engine_parameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
            time_elapsed = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
            estimations.append( float(self.engine_parameters.termination_parameters["time"]) - time_elapsed )
            
        if self.engine_parameters.TERMINATION_CRITERIA.DATE.value in self.engine_parameters.temination_criteria:
            estimations.append( self.engine_parameters.termination_parameters["datetime"] - datetime.datetime.now() )
            
        self.ETA = min(estimations)
    
    def __ETA_callback__(self):
        
        self._compute_ETA_()
        
        return time.strftime('%H:%M:%S', time.gmtime( self.ETA ))
    
    
    def __refresh_stats__(self):
        # self._compute_ETA_()
        self.optimize_tab.__refresh_stats__()
        time_elapsed = self.engine.acum_execution_time + (time.time() - self.engine.last_execution_time_resume)
        # self.optimize_tab.progressbar.step( 100.0*(time_elapsed)/(time_elapsed+self.ETA) )
        self.optimize_tab.progressbar['value'] = 100.0*(time_elapsed)/(time_elapsed+self.ETA)
        self._update_job =  self.after(ms=1000, func=self.__refresh_stats__)
        
    
    def _disable_tabs(self):
        tabs = self.tabs.tabs()
        
        self.tabs.tab(0, state='disabled')
        self.tabs.tab(1, state='disabled')
        self.tabs.tab(2, state='disabled')

        
    
    def _enable_tabs(self):
        tabs = self.tabs.tabs()
        
        # for i, item in enumerate(tabs): 
        #     self.tabs.tab(item, state='normal')
        
        self.tabs.tab(0, state='normal')
        self.tabs.tab(1, state='normal')
        self.tabs.tab(2, state='normal')
    
    def __init__(self, *args, **kwargs):
        super( JOptimizer_App, self ).__init__(*args, **kwargs)
        
        self.configure(bg=AppStyle.global_background_color, highlightbackground=AppStyle.global_border_color, highlightthickness=1)
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.window_width = int(self.screen_width*0.8)
        self.window_height = int(self.screen_height*0.8)
        
        self.wm_title("JOptimizer")
        self.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, ((self.screen_width/2)-(self.window_width/2)), ((self.screen_height/2)-(self.window_height/2))))
        self.title_font = tkfont.Font(family='Helvetica', size=int(0.01*self.screen_width), weight="bold", slant="italic")

        self.iconbitmap( os.path.join(os.getcwd(), 'interface', 'resources', 'images', 'joptimizer_icon.ico') )

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
                                          termination_callback=ThreadSafeCallable(master=self, callback=self.__termination_callback__),
                                          paused_callback=ThreadSafeCallable(master=self, callback=self.__paused_callback__))

        """
            Menu
        """
        self. menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        self.file_menu.add_command( label="Save configuration", command=self.SaveConfigCommand )
        self.file_menu.add_command( label="Load configuration", command=self.LoadConfigCommand )
        
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        

        """
            Tabs
        """
        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('TkDefaultFont','11','bold') )
        s.theme_use('vista')
        s.configure("Treeview.Heading", font=('TkDefaultFont','10','bold'), background="#e6f2ff")
        s.configure("Treeview", font=('TkDefaultFont','10'), rowheight=30)
        s.configure( "TNotebook", background=AppStyle.global_background_color, highlightbackground=AppStyle.global_border_color, highlightthickness=1 )
        s.configure( "TNotebook.Tab", background=AppStyle.global_background_color, highlightbackground=AppStyle.global_border_color, highlightthickness=1 )
        
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
    
        
    def SaveConfigCommand(self):
        
        if self.check_parameter_correctness():  
            self.save_parameters()
        
            path = filedialog.askdirectory(title = "Select a directory with configuration files", initialdir=os.getcwd() )
            
            self.engine_parameters.save_state( dir_path=path )
            self.problem_parameters.save_state( dir_path=path )
            self.algorithm_parameters.save_state( dir_path=path )
    
    def LoadConfigCommand(self):
        
        path = filedialog.askdirectory(title = "Select a directory with configuration files", initialdir=os.getcwd() )
    
        if path != "":
            try:
                self.engine_parameters.load_state( dir_path=path )
                self.problem_parameters.load_state( dir_path=path )
                self.algorithm_parameters.load_state( dir_path=path )
                
                self.load_parameters()
                
            except ValueError as error:
                
                tk.messagebox.showerror(title="Invalid folder path", message="Selected file does not exit or is of incorrect type")
                print(error)
            
        
        
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
        
    def load_parameters(self):
        
        self.problem_tab.load_parameters()
        self.algorithm_tab.load_parameters()
        self.runtime_enviroment_tab.load_parameters()
        
    def launch_optimization(self):
        
        if self.check_parameter_correctness():    
            self.save_parameters()
            self.engine.launch()
            self._update_job =  self.after(ms=1000, func=self.__refresh_stats__)
            return True
            
        return False
    
    def pause_optimization(self):
        
        if self._update_job != None:
            self.after_cancel(self._update_job)
            self._update_job = None
            
        self.engine.pause()
        
    def resume_optimization(self):
        self.engine.resume()
        self._update_job =  self.after(ms=1000, func=self.__refresh_stats__)
        
    def changed_tag_handler(self, event):
        index = event.widget.index("current")
        
        if index == 1:
            self.algorithm_tab.update_types()
        

app = JOptimizer_App()
app.mainloop()