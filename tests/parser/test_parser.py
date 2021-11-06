# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 12:16:36 2021

@author: Álvaro
"""


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


def main():

    normal_vars = { 'x' : 1,
                      'y' : 2,
                      'z' : 3,
                      't' : 4 }
    
    vector_vars = { 'w' : [0, 1, 2, 3],
                    'u' : [ 0, 1, 2, 3, 4, 5 ]}
    
    matrix_vars = { 'M' : [[1, 0], [0, 1]] }
    
    
    simple_symbols = set()
    keyword_symbols = {}
    unpack_symbols = set()
    
    
    while(True):    
        arg_string = input()
        
        arg_string = su.remove_whitespaces( arg_string )
        arg_tokens = arg_string.split(',')
        
        keywargs_ended = False
        
        for token in arg_tokens:
            
            ret = token_is_kwarg(token)
            
            
            if ret != None:
                
                if keywargs_ended:
                    print( "keyword args (%=%) must be declared before any other type" % (ret[0], ret[1]) )
                    break
                
                elif (ret[1] not in normal_vars) and (ret[1] not in vector_vars) and (ret[1] not in matrix_vars):
                    print( "Variable '%s' not defined" % ret[1] )
                    break
                    
                else:
                    keyword_symbols[ret[0]] = ret[1]
                    
                    
            else:
                
                keywargs_ended = True
                ret = token_is_unpacked_arg(token)
                
                if ret!=None:
                    
                    if ret not in vector_vars:
                        print( "Variable '%s' is not defined or of an unpackable type" % ret )
                        break
                        
                    else:
                        unpack_symbols.add( ret )
                        
                else:
                    
                    if token_is_arg(token) and (token in normal_vars or token in vector_vars or token in matrix_vars):
                        simple_symbols.add(token)
                        
                    else:
                        print( "Variable '%s' is not defined or is syntactically incorrect" % token )
                        break
                        
                    
                    
                
        
        print(arg_tokens)
        

if __name__ == "__main__":
   main()
    