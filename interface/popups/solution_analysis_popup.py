# -*- coding: utf-8 -*-


import os
import sys
# sys.path.append(r"./../..")

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
from util.type_check import *

import tkinter.tix as tix


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: float(t[0]), reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
                treeview_sort_column(tv, col, not reverse))

def treeview_sort_first_column(tv, col, reverse):
    l = [(tv.item(k)["text"], k) for k in tv.get_children()] #Display column #0 cannot be set
    l.sort(key=lambda t: float(t[0]), reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_first_column(tv, col, not reverse))


class InspectSolutionPopup:
    
    def __init__( self, controller, event ):
        
        self.controller = controller    
        
        self.entry_item = self.controller.solutions_tree.selection()[0]
        self.selection_index = to_integer(self.controller.solutions_tree.item( self.entry_item, "text" ))
        
        self.solution = self.controller.solutions[self.selection_index]
        
        self.variables_popup_win = tk.Toplevel( master=self.controller )
        self.variables_popup_win.wm_title("Solution values")
        self.variables_popup_win.resizable(False,False)
        self.variables_popup_win.iconbitmap( os.path.join(os.getcwd(), 'interface', 'resources', 'images', 'joptimizer_icon.ico') )
        
        screen_width = self.variables_popup_win .winfo_screenwidth()
        screen_height = self.variables_popup_win .winfo_screenheight()
        
        window_width = 500
        window_height = 250
        
        window_x_offset = screen_width//2 - window_width//2
        window_y_offset = screen_height//2 - window_height//2
        
        self.variables_popup_win .wm_geometry("%dx%d+%d+%d" % (window_width, window_height, window_x_offset, window_y_offset))
        self.variables_popup_win .grab_set()
        
        self.variable_headers = [ "Value" ]
        self.solutions_tree = ttk.Treeview(master=self.variables_popup_win, columns=self.variable_headers, selectmode="extended")
        
        self.solutions_tree.heading("#0", text="Variable" )
        self.solutions_tree.column("#0", stretch=tk.NO)
        
        self.solutions_tree.heading("Value", text="Value" )
        self.solutions_tree.column("Value", stretch=tk.NO)
        
        for variable in self.solution[0]:
            self.solutions_tree.insert('', 'end', text=variable[0].keyword, values=(str(variable[1])))
            
        self.solutions_tree.place( relx=0.015, rely=0.03, relwidth=0.97, relheight=0.94 )


class SolutionsFrame( ParameterFrame ):
    
    def __init__(self, master, controller, *args, **kwargs):
        super( SolutionsFrame, self ).__init__(master=master, *args, **kwargs)
        
        self.controller = controller
        
        self.variable_headers = [ objective_name for objective_name in self.controller.problem_parameters.options["objectives_names"] ]
        self.solutions_tree = ttk.Treeview(master=master, columns=self.variable_headers, selectmode="extended")
        self.solutions_tree.heading("#0", text="Index", command=lambda _col="#0": treeview_sort_first_column(self.solutions_tree, _col, False) )
        self.solutions_tree.column("#0", stretch=tk.NO)
        
        # for variable in self.controller.problem_parameters.variables:
            
        #     self.solutions_tree.heading( variable.keyword, text=variable.keyword )
        #     self.solutions_tree.column( variable.keyword, stretch=tk.NO )
        
        for objective_name in self.controller.problem_parameters.options["objectives_names"]:
            
            self.solutions_tree.heading( objective_name, text=objective_name, command=lambda _col=objective_name: treeview_sort_column(self.solutions_tree, _col, False) )
            self.solutions_tree.column( objective_name, stretch=tk.NO )
        
        # self.solutions_tree.grid(row=0, column=0, columnspan=2,
                                 # padx=10, pady=10, sticky="nsew")
        
        # scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.solutions_tree.yview)
        # scrollbar.grid(row=0, column=3, sticky="nse", pady="10")
        
        self.solutions_tree.place(relx=0.02, rely=0.17, relwidth=0.955, relheight=0.8)
        self.solutions_tree.bind("<Double-1>", lambda event: InspectSolutionPopup(controller=self, event=event))
    
    def display(self):
        self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
        
    def load_front(self):
        self.front = self.controller.engine.get_front()
        self.solutions = self.controller.engine.get_variables(self.front)
        
        for i, solution in enumerate(self.solutions):
            values_tuple = tuple( [ str(objective) for objective in solution[-1]] )
            self.solutions_tree.insert('', 'end', text=str(i), values=values_tuple)
            

class Plot2DFrontFrame( ParameterFrame ):
    
    def __init__(self, master, controller, *args, **kwargs):
        super( SolutionsFrame, self ).__init__(master=master, *args, **kwargs)
        
        self.controller = controller

def solution_analysis_popup( master, controller ):

    win = tk.Toplevel( master=master )
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
    