# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from inspect import getmembers, isfunction
import copy
import random
import math
import yaml
import os

import imp
from pathlib import Path

from interface.tabs.problem.frames.problem_frame import *


class PythonFrame(ProblemFrame):
        
    def _browse(self): 
        
        path = filedialog.askopenfilename(title = "Select a script which contains the function", filetypes=[("Python script", "*.py")], initialdir=os.getcwd() )
        
        if path:
            try:
                function_module = imp.load_source(name=Path(path).stem, pathname=path)
                self.functions = getmembers(function_module, isfunction)
                self.function_list = [ function[0] for function in self.functions]
                
            
                self.ScriptFilePath.config(state=tk.NORMAL)
                self.ScriptFilePath.delete( 0, tk.END )
                self.ScriptFilePath.insert( 0, path )
                self.ScriptFilePath.config(state="readonly")
            
            except Exception as error:    
                tk.messagebox.showerror(title="Invalid script path", message="%s" % (error))
                
        else:
            tk.messagebox.showerror(title="Invalid script path", message="No script path was chosen")
    
    def _update_function_parameters(self, var):
        
        function_module = imp.load_source(name=Path(var).stem, pathname=var)
        self.functions = getmembers(function_module, isfunction)
        self.function_list = [ function[0] for function in self.functions]
        
        # try:
        self.ScriptFilePath.configure( state=tk.NORMAL )
        ClearInsertEntry(self.ScriptFilePath, str(var))
        self.ScriptFilePath.configure( state=tk.DISABLED )
        
        if self.problem_parameters.options["function_name"] not in self.function_list:
           self.problem_parameters.options["function_name"] = self.function_list[0]
           
        menu = self.function_option["menu"]
        menu.delete(0, "end")
        
        for string in self.function_list:
            menu.add_command(label=string, 
                             command=lambda value=string: self.FunctionOption.set(value))
        
        self.FunctionOption.set(self.problem_parameters.options["function_name"])
        
        # except:
        #     pass
        
        
    def _save_function_parameters(self, *args):
        self.problem_parameters.options["function_name"] = self.FunctionOption.get()
        self.problem_parameters.options["python_script_path"] = self.ScriptFilePath.get()
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(PythonFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        ttk.Label( master=self, text="Function script path").place( relx=0.02, rely=0.05 )
        self.ScriptFilePath = ttk.Entry(master=self, state=tk.NORMAL)
        self.ScriptFilePath.insert(0, problem_parameters.options["python_script_path"])
        self.ScriptFilePath.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
        self.ScriptFilePath.config(state=tk.DISABLED)
        self.button_browse_operator = ttk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
        
        self.function_options = ["none"]
        
        tk.Label( master=self, text="Function").place( relx=0.02, rely=0.15 )
        
        self.FunctionOption = tk.StringVar(self)
        self.FunctionOption.set(self.function_options[0])
        self.function_option = tk.OptionMenu(self, self.FunctionOption, *self.function_options )
        
        self.function_option.config( state=tk.DISABLED )
        self.function_option.place( relx=0.11, rely=0.045, relwidth=0.15 )
        
        self.function_option_parameter = Parameter(name="function_operator", fancy_name="Function operator")
        
        self.script_path_parameter = FilePath( fancy_name="Evaluator script path", extension=".py" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.script_path_parameter,
                                                          widget_read_lambda=lambda: self.ScriptFilePath.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"python_script_path":var}),
                                                          error_set_lambda=EntryInvalidator(self.ScriptFilePath),
                                                          error_reset_lambda=EntryValidator(self.ScriptFilePath),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["python_script_path"],
                                                          widget_update_lambda=lambda var: self._update_script_path(var) ) )
        
        
        # self.parameters_bindings.append( ParameterBinding(parameter=self.function_option_parameter,
        #                                                   widget_read_lambda=lambda: self.FunctionOption.get(),
        #                                                   variable_store_lambda=self.__store_selection_option,
        #                                                   variable_read_lambda=lambda: self.algorithm_parameters.selection_choice,
        #                                                   widget_update_lambda=lambda var: self.__update_operator_option__(var) ) )
       
    
        
    def __is_evaluator_instance(self, parameter: Parameter):
            
        error_list = []
        
        if len(self.evaluator_path_parameter.error_check()) == 0:
            evaluator_module = imp.load_source(name=Path(self.OperatorFilePath.get()).stem, pathname=self.OperatorFilePath.get())
            
            # if self.evaluator_class_entry.get() in inspect.getmembers(evaluator_module):
            if hasattr(evaluator_module, self.evaluator_class_entry.get()):
                evaluator_class = getattr(evaluator_module, self.evaluator_class_entry.get())
                
                if not issubclass(evaluator_class, Evaluator):
                    error_list.append("Parameter '%s' is not a subclass of Evaluator" % (self.evaluator_class_parameter.fancy_name))
                
            else:
                error_list.append("Parameter '%s' is not a class in specified file" % (self.evaluator_class_parameter.fancy_name))
        
        return error_list

