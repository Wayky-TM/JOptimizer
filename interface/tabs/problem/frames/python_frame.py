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

from util.arg_parsing import *

class PythonFrame(ProblemFrame):
        
    def _browse(self): 
        
        path = filedialog.askopenfilename(title = "Select a script which contains the function", filetypes=[("Python script", "*.py")], initialdir=os.getcwd() )
        
        if path:
            try:
                function_module = imp.load_source(name=Path(path).stem, pathname=path)
                self.functions = getmembers(function_module, isfunction)
                self.function_list = [ function[0] for function in self.functions]
                
                if len(self.function_list)>0:
                    self.ScriptFilePath.config(state=tk.NORMAL)
                    self.ScriptFilePath.delete( 0, tk.END )
                    self.ScriptFilePath.insert( 0, path )
                    self.ScriptFilePath.config(state="readonly")
                    
                    menu = self.function_option["menu"]
                    menu.delete(0, "end")
                    
                    for string in self.function_list:
                        menu.add_command(label=string, 
                                         command=lambda value=string: self.FunctionOption.set(value))
                        
                    self.FunctionOption.set( self.function_list[0] )
                    
                else:
                    menu = self.function_option["menu"]
                    menu.delete(0, "end")
                    self.FunctionOption.set( "none" )
            
            except Exception as error:    
                tk.messagebox.showerror(title="Invalid script path", message="%s" % (error))
                
        else:
            tk.messagebox.showerror(title="Invalid script path", message="No script path was chosen")
    
    def _update_function_parameters(self, var):
        
        function_module = imp.load_source(name=Path(var).stem, pathname=var)
        self.functions = getmembers(function_module, isfunction)
        self.function_list = [ function[0] for function in self.functions]
        
        if len(self.function_list)>0:
        
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
            
        else:
            self.master.console_print_error("Loaded file doesn't include any function definition")
        
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
        
        self.function_option.config( state=tk.NORMAL )
        self.function_option.place( relx=0.09, rely=0.15-0.005, relwidth=0.15 )
        
        # self.function_option_parameter = Parameter(name="function_operator", fancy_name="Function operator")
        
        self.script_path_parameter = FilePath( fancy_name="Function script path", extension=".py" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.script_path_parameter,
                                                          widget_read_lambda=lambda: None,
                                                          variable_store_lambda=lambda var: self._save_function_parameters(var),
                                                          # error_set_lambda=EntryInvalidator(self.ScriptFilePath),
                                                          # error_reset_lambda=EntryValidator(self.ScriptFilePath),
                                                          variable_read_lambda=lambda: None,
                                                          widget_update_lambda=lambda var: self._update_function_parameters(var) ) )
        
        tk.Label( master=self, text="Number of objectives").place( relx=0.02, rely=0.25 )
        self.ObjectivesEntry = ttk.Entry(master=self, state=tk.NORMAL)
        self.ObjectivesEntry.insert(0, self.problem_parameters.options["objectives"])
        self.ObjectivesEntry.place( relx=0.14, rely=0.25-0.005, relwidth=0.1 )
        
        self.objectives_parameter = Integer(name="number_of_objectives", fancy_name="Number of objectives", lower_bound=1, upper_bound=1000)
            
        self.parameters_bindings.append( ParameterBinding(parameter=self.objectives_parameter,
                                                          widget_read_lambda=lambda: self.ObjectivesEntry.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"objectives":var}),
                                                          error_set_lambda=EntryInvalidator(self.ObjectivesEntry),
                                                          error_reset_lambda=EntryValidator(self.ObjectivesEntry),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["objectives"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.ObjectivesEntry, str(var)) ) )        
       
    
        tk.Label( master=self, text="Call argument format").place( relx=0.02, rely=0.35 )
        self.ArgsEntry = ttk.Entry(master=self, state=tk.NORMAL)
        self.ArgsEntry.insert(0, self.problem_parameters.options["call_args"])
        self.ArgsEntry.place( relx=0.14, rely=0.35-0.005, relwidth=0.3 )
    
        
    def check_args(self):
        
        arg_string = su.remove_whitespaces( self.ArgsEntry.get() )
        arg_tokens = arg_string.split(',')
        
        keywargs_started = False
        already_warned = False
        error_list = []
        
        for token in arg_tokens:
            
            ret = token_is_kwarg(token)
            
            
            if ret != None:
                
                keywargs_started = True
                
                if (ret[1] not in normal_vars) and (ret[1] not in vector_vars) and (ret[1] not in matrix_vars):
                    # print( "Variable '%s' not defined" % ret[1] )
                    error_list.append( "Variable '%s' not defined" % ret[1] )
                    # break
                    
                else:
                    keyword_symbols[ret[0]] = ret[1]
                    
                    
            else:
    
                ret = token_is_unpacked_arg(token)
                
                if keywargs_started and not already_warned:
                    error_list.append( "args must preceed kwargs: %s" % token )
                    already_warned = True
                    # break
                
                elif ret!=None:
                    
                    if ret not in vector_vars:
                        # print( "Variable '%s' is not defined or of an unpackable type" % ret )
                        error_list.append( "Variable '%s' is not defined or of an unpackable type" % ret )
                        # break
                        
                    else:
                        unpack_symbols.add( ret )
                        
                else:
                    
                    if token_is_arg(token) and (token in normal_vars or token in vector_vars or token in matrix_vars):
                        simple_symbols.add(token)
                        
                    else:
                        # print( "Variable '%s' is not defined or is syntactically incorrect" % token )
                        error_list.append( "Variable '%s' is not defined or is syntactically incorrect" % token )
                        # break

        return error_list
    
    def check_errors(self):
        error_list = super(PythonFrame,self).check_errors()
        error_list.extend(self.check_args())
        return error_list
            
    def save_parameters(self):
        super(PythonFrame,self).save_parameters()
        self.problem_parameters.options["call_args"] = self.ArgsEntry.get()
            
    def load_parameters(self):
        super(PythonFrame,self).load_parameters()
        self.ArgsEntry.set(self.problem_parameters.options["call_args"])
    
    # def __is_evaluator_instance(self, parameter: Parameter):
            
    #     error_list = []
        
    #     if len(self.evaluator_path_parameter.error_check()) == 0:
    #         evaluator_module = imp.load_source(name=Path(self.OperatorFilePath.get()).stem, pathname=self.OperatorFilePath.get())
            
    #         # if self.evaluator_class_entry.get() in inspect.getmembers(evaluator_module):
    #         if hasattr(evaluator_module, self.evaluator_class_entry.get()):
    #             evaluator_class = getattr(evaluator_module, self.evaluator_class_entry.get())
                
    #             if not issubclass(evaluator_class, Evaluator):
    #                 error_list.append("Parameter '%s' is not a subclass of Evaluator" % (self.evaluator_class_parameter.fancy_name))
                
    #         else:
    #             error_list.append("Parameter '%s' is not a class in specified file" % (self.evaluator_class_parameter.fancy_name))
        
    #     return error_list

