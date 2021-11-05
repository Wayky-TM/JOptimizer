# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./..")

from core.evaluator import Evaluator

class PythonFunctionEvaluator(Evaluator):
    
    def __init__( self,
                  number_of_variables: int,
                  number_of_objectives: int,
                  script_path: str,
                  function_name: str ):
        
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        
        function_module = imp.load_source(name=Path(script_path).stem, pathname=script_path)
        self.python_function = getattr(function_module, function_name)
    
    def evaluate( **kwargs, *args ):
        
        objectives = self.python_function( **kwargs, *args )
        
        if len(objectives) != self.number_of_objectives:
            raise ValueError("Function '%s' returned an inappropiate number of values: expected %d, received %d" % (function_name, self.number_of_objectives, len(objectives)))
        
        return objectives
