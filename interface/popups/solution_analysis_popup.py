# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 19:56:28 2021

@author: Wayky
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

from interface.parameter_frames import *



class SolutionsFrame( ParameterFrame ):
    
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        
        self.controller = controller
        
        self.variable_headers = [variable.keyword for variable in self.controller.problem_parameters.variables]
        self.solutions_tree = ttk.Treeview(master=master, columns=self.variable_headers, selectmode="extended")
        self.solutions_tree.heading("#0", text="Index")
        self.solutions_tree.column("#0", stretch=tk.NO)
        
        for variable in self.controller.problem_parameters.variables:
            
            self.solutions_tree.heading( variable.keyword, text=variable.keyword )
            self.solutions_tree.column( variable.keyword, stretch=tk.NO )
        
        self.solutions_tree.grid(row=0, column=0, columnspan=2,
                                 padx=10, pady=10, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.solutions_tree.yview)
        scrollbar.grid(row=0, column=3, sticky="nse", pady="10")
        
        # self.solutions_tree.place(relx=0.02, rely=0.17, relwidth=0.955, relheight=0.8)
    
    def display(self):
        self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
        
    def load_front(self):
        front = self.controller.engine.get_front()
        
        # number_of_variables = len(self.controller.problem_parameters.variables)
                
        for i, solution in enumerate(front):
            values_tuple = tuple( [ str(component[1]) for component in solution] )
            self.solutions_tree.insert('', 'end', text=str(i), values=values_tuple)
            

def solution_analysis_popup( controller ):

    win = tk.Toplevel( master=controller )
    win.wm_title("Solutions analysis tools")
    win.resizable(False,False)
    win.iconbitmap( os.path.join(os.getcwd(), 'interface', 'resources', 'images', 'joptimizer_icon.ico') )

    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    
    window_width = screen_width/2
    window_height = screen_height/2
    
    popup_width=screen_width/2
    popup_height=screen_height/2

    win.geometry("%dx%d+%d+%d" % (window_width, window_height, ((screen_width/2)-((popup_width*0.7)/2)), ((screen_height/2)-((popup_height*0.7)/2))))
    win.grab_set() # Locking root window
    
    notebook = ttk.Notebook(master=win)
    
    solutions_frame = SolutionsFrame(master=notebook, controller=controller)
    solutions_frame.display()
    solutions_frame.load_front()
    
    notebook.add( solutions_frame, text="   Solutions   " )
    notebook.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.95)
    