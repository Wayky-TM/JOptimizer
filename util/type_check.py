# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:25:37 2021

@author: Wayky
"""

import re

""" Validation methods for Tkinter callbacks """

def is_integer(text: str):
    return re.sub(u"\u2212|-", "", text).isdigit()

def to_integer(text: str):
    return int(re.sub(u"\u2212", "-", text))

def is_float(text: str):
    try:
        float(text)
    except:
        return False
    
    return True

def is_alpha(text: str):
    return text.isalpha()

