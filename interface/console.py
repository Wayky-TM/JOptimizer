# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:01:32 2021

@author: Álvaro
"""

import sys
sys.path.append(r"./../..")

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



class Console(tk.scrolledtext.ScrolledText):
    
    def __init__(self, *args, **kwargs):
        kwargs['state']=tk.DISABLED
        kwargs['wrap']=tk.WORD
        super(Console, self).__init__(*args, **kwargs)
        # self.config(state=DISABLED)
        
    def print_error( self, string: str ):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, string, 'error')
        self.tag_config('error', foreground='red')
        self.config(state=tk.DISABLED)
    
    def print_warning( self, string: str ):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, string, 'warning')
        self.tag_config('warning', foreground='#DBC48F')
        self.config(state=tk.DISABLED)
    
    def print_message( self, string: str ):
        self.config(state=tk.NORMAL)
        self.insert(tk.END, string, 'message')
        self.tag_config('message', foreground='black')
        self.config(state=tk.DISABLED)
    
    def clear_all(self):
        self.config(state=tk.NORMAL)
        self.delete('1.0', END)
        self.config(state=tk.DISABLED)
    
    
    
    