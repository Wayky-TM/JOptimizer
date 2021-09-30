# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:32:22 2021

@author: Wayky
"""

import re

def remove_whitespaces( string: str ):
    return re.sub(r'(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', string)