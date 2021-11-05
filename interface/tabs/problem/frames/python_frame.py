# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from inspect import getmembers, isfunction

from interface.tabs.problem.frames.problem_frame import *


class PythonFrame(ProblemFrame):
        
    def _browse(self): 
        
        path = filedialog.askopenfilename(title = "Select a script which contains the function", filetypes=[("Python script", "*.py")], initialdir=os.getcwd() )
        
        if path:
            try:
                function_module = imp.load_source(name=Path(path).stem, pathname=path)
                getmembers(function_module, isfunction)
            
                self.ScriptFilePath.config(state=tk.NORMAL)
                self.ScriptFilePath.delete( 0, tk.END )
                self.ScriptFilePath.insert( 0, path )
                self.ScriptFilePath.config(state="readonly")
            
            except Exception as error:    
                tk.messagebox.showerror(title="Invalid script path", message="%s" % (error))
                
        else:
            tk.messagebox.showerror(title="Invalid script path", message="No script path was chosen")
    
    def _update_script_path(self, var):
        self.ScriptFilePath.configure( state=tk.NORMAL )
        ClearInsertEntry(self.ScriptFilePath, str(var))
        self.ScriptFilePath.configure( state=tk.DISABLED )
    
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(PythonFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        ttk.Label( master=self, text="Function script path").place( relx=0.02, rely=0.05 )
        self.ScriptFilePath = ttk.Entry(master=self, state=tk.NORMAL)
        self.ScriptFilePath.insert(0, problem_parameters.options["python_script_path"])
        self.ScriptFilePath.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
        self.ScriptFilePath.config(state=tk.DISABLED)
        self.button_browse_operator = ttk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
        
        self.script_path_parameter = FilePath( fancy_name="Evaluator script path", extension=".py" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.script_path_parameter,
                                                          widget_read_lambda=lambda: self.ScriptFilePath.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"python_script_path":var}),
                                                          error_set_lambda=EntryInvalidator(self.ScriptFilePath),
                                                          error_reset_lambda=EntryValidator(self.ScriptFilePath),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["python_script_path"],
                                                          widget_update_lambda=lambda var: self._update_script_path(var) ) )
        
        
        
        # tk.Label( master=self, text="Evaluator class").place( relx=0.02, rely=0.15 )
        # self.evaluator_class_entry = ttk.Entry( master=self , state=tk.NORMAL)
        # self.evaluator_class_entry.place(relx=0.1, rely=0.15)
        
        # self.evaluator_class_parameter = Parameter( fancy_name="Evaluator class", error_lambda=self.__is_evaluator_instance )
        
        # self.parameters_bindings.append( ParameterBinding(parameter=self.evaluator_class_parameter,
        #                                                   widget_read_lambda=lambda: self.evaluator_class_entry.get(),
        #                                                   variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var}),
        #                                                   error_set_lambda=EntryInvalidator(self.evaluator_class_entry),
        #                                                   error_reset_lambda=EntryValidator(self.evaluator_class_entry),
        #                                                   variable_read_lambda=lambda: self.problem_parameters.options["evaluator_class"],
        #                                                   widget_update_lambda=lambda var: ClearInsertEntry(self.evaluator_class_entry, str(var)) ) )
        
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

