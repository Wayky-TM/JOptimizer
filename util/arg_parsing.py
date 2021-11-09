# -*- coding: utf-8 -*-


import os
import sys
sys.path.append(r"./../..")

import util.string_utils as su

import re



def token_is_arg( string : str ):
    return re.match( "_?[a-zA-Z][a-zA-Z_0-9]*", string )!=None

def token_is_kwarg( string : str ):
    subtokens = string.split( '=' )
    
    if len(subtokens)!=2:
        return None
    
    if token_is_arg(subtokens[0]) and token_is_arg(subtokens[1]):
        return (subtokens[0],subtokens[1])
    
    return None
    
def token_is_unpacked_arg( string : str ):
    
    if re.match( "\*_?[a-zA-Z][a-zA-Z_0-9]*", string )!=None:
        return string.replace('*', '')
    
    return None 

