# -*- coding: utf-8 -*-


# import matlab.engine
import os

"""
    Description:
        Runs a Matlab script from python.
    
    Considerations:
        -Requires Matlab Python API
        -Function name must match that of the script where it's defined!!!
        -Script path is added to Matlab's during initialization
""" 

class MatlabFunction:
   
    """
    Params:
        'script_path' - path of the script that contains the function
        'nargin' - # of arguments expected by Matlab function
        'nargout' - # of return values expected
        'mat_eng' - initialized Matlab engine
    """
    def __init__( self, script_path, nargin, nargout, mat_engine ):
        
        self.engine = mat_engine
        self.script_path = os.path.dirname(script_path)
        self.function_name = os.path.splitext( os.path.basename(script_path) )[0]
        self.nargin = nargin
        self.nargout = nargout
        
        s = self.engine.genpath(self.script_path)
        self.engine.addpath( s, nargout=0 )
        
        # self.command = "self.engine.%s( *args, nargout=self.nargout )" % (self.function_name)
        self.function_ref = eval("self.engine.%s" % (self.function_name))
        
        
    def call( self, *args ): #TODO: Proper argument checking
        # return eval(self.command)
        return self.function_ref( *args, nargout=self.nargout )
    

