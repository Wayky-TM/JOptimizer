# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:25:37 2021

@author: Wayky
"""

import re

""" Validation methods for Tkinter callbacks """

def is_integer(value):
    
    if type(value) == int:
        return True
    
    if type(value) == str:
        return re.sub(u"\u2212|-", "", value).isdigit()
    
    return False
    

def to_integer(value):
    
    if type(value) == int:
        return value
    
    return int(re.sub(u"\u2212", "-", value))

def is_float(value):
    
    if type(value) == float:
        return True

    try:
        float(value)
    except:
        return False
    
    return True

def is_alpha(text: str):
    return text.isalpha()

