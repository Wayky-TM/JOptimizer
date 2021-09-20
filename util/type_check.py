# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:25:37 2021

@author: Wayky
"""

""" Validation methods for Tkinter callbacks """

def is_integer(text):
    return text.isdigit()

def is_float(text):
    try:
        float(text)
    except:
        return False
    
    return True

def is_alpha(text):
    return text.isalpha()



