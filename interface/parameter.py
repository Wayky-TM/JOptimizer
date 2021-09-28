# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 19:27:06 2021

@author: Wayky
"""

""" TODO list """
# 1. Add support for list of integers and floats

from enum import Enum
from abc import *

import os.path

from typing import List

import util.type_check as TC

class Parameter:

    class Error:
        
        def __init__( self, parameter: 'Parameter', err_str: str = "" )        :
            self.parameter = parameter
            self.err_str = err_str
    
    def __init__( self,
                  name: str = "",
                  fancy_name: str = "" ): # Name to display in the GUI
        
        if type(name) != str:
            raise ValueError( "%s.__init__(): parameter 'name' must be a string" )
            
        if type(fancy_name) != str:
            raise ValueError( "%s.__init__(): parameter 'fancy_name' must be a string" )
        
        self.name = name
        
        if fancy_name == "":
            self.fancy_name = name
        else:
            self.fancy_name = fancy_name
            
        self.string_value = ""
        self.value = None

    def get_string( self ):
        return self.value
    
    @abstractmethod
    def get_value( self ):
        pass

    @abstractmethod
    def error_check( self, error_list: List[Error] ):
        pass

class Float(Parameter):
    
    def __init__( self, name: str = "", fancy_name: str = "", lower_bound: float = 0.0, upper_bound: float = 1.0 ):
        
        if lower_bound <= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
            
        elif type(lower_bound) != float:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be a float" % (type(self).__name__) )
            
        elif type(upper_bound) != float:
            raise ValueError( "%s.__init__(): parameter 'upper_bound' must be a float" % (type(self).__name__) )
        
        super( Float, self ).__init__( name, fancy_name )
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def error_check( self, error_list: List[Parameter.Error] ):
        
        if type(self.value)!=str or not TC.is_float(self.value) or self.value < self.lower_bound or self.value > self.upper_bound:
            error_list.append( ParameterError( self, "Parameter '%s' must be a real value within [%d,%d]" % (self.fancy_name, self.lower_bound, self.upper_bound) ) )
            return True
            
        return False
    
    def get_value( self ):
        return float(self.value)
        
        
        
class Integer(Parameter):
    
    def __init__( self, name: str = "", fancy_name: str = "", lower_bound: int = -32768, upper_bound: int = 32767 ):
        
        if lower_bound <= upper_bound:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be less than 'upper_bound'" % (type(self).__name__) )
            
        elif type(lower_bound) != int:
            raise ValueError( "%s.__init__(): parameter 'lower_bound' must be an integer" % (type(self).__name__) )
            
        elif type(upper_bound) != int:
            raise ValueError( "%s.__init__(): parameter 'upper_bound' must be an integer" % (type(self).__name__) )
        
        super( Integer, self ).__init__( name, fancy_name )
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
    def error_check( self, error_list: List[Parameter.Error] ):
        
        if type(self.value)!=str or not TC.is_integer(self.value) or self.value < self.lower_bound or self.value > self.upper_bound:
            error_list.append( ParameterError( self, "Parameter '%s' must be an integer value within [%d,%d]" % (self.fancy_name, self.lower_bound, self.upper_bound) ) )
            return True
            
        return False
    
    def get_value( self ):
        return int(self.value)
        
        
class FilePath(Parameter):
    
    def __ini__( self, name: str = "", fancy_name: str = "", is_folder: bool = False ):
        
        super( FilePath, self ).__init__( name, fancy_name )
        self.is_folder = is_folder
        
    def error_check( self, error_list: List[Parameter.Error] ):
            
        if self.is_folder and not os.path.isdir(self.value):
            error_list.append( ParameterError( self, "Parameter '%s' must be a directory path" % (self.fancy_name) ) )
            return True
        
        if not self.is_folder and not os.path.isfile(self.value):    
            error_list.append( ParameterError( self, "Parameter '%s' must be a file path" % (self.fancy_name) ) )
            return True
        
        return False
    
    def get_value( self ):
        return self.value
    


