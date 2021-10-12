# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 20:44:34 2021

@author: Wayky
"""


class ThreadSafeCallable:
    
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        
    def __call__(self):
        self.master.after(0, self.callback)