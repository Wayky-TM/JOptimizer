# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.problem.frames.problem_frame import *



class EvaluatorFrame(ProblemFrame):
        
    def _browse(self): 
        
        path = filedialog.askopenfilename(title = "Select a file which contains the evaluator", filetypes=[("Python script", "*.py")], initialdir=os.getcwd() )
        
        self.OperatorFilePath.config(state=tk.NORMAL)
        self.OperatorFilePath.delete( 0, tk.END )
        self.OperatorFilePath.insert( 0, path )
        self.OperatorFilePath.config(state="readonly")
    
    def _update_evaluator_path(self, var):
        self.OperatorFilePath.configure( state=tk.NORMAL )
        ClearInsertEntry(self.OperatorFilePath, str(var))
        self.OperatorFilePath.configure( state=tk.DISABLED )
        
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(EvaluatorFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        ttk.Label( master=self, text="Evaluator script path").place( relx=0.02, rely=0.05 )
        self.OperatorFilePath = ttk.Entry(master=self, state=tk.NORMAL)
        self.OperatorFilePath.insert(0, problem_parameters.options["evaluator_path"])
        self.OperatorFilePath.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
        self.OperatorFilePath.config(state=tk.DISABLED)
        self.button_browse_operator = ttk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
        
        self.evaluator_path_parameter = FilePath( fancy_name="Evaluator script path", extension=".py" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.evaluator_path_parameter,
                                                          widget_read_lambda=lambda: self.OperatorFilePath.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_path":var}),
                                                          error_set_lambda=EntryInvalidator(self.OperatorFilePath),
                                                          error_reset_lambda=EntryValidator(self.OperatorFilePath),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["evaluator_path"],
                                                          widget_update_lambda=lambda var: self._update_evaluator_path(var) ) )
        
        
        
        tk.Label( master=self, text="Evaluator class").place( relx=0.02, rely=0.15 )
        self.evaluator_class_entry = ttk.Entry( master=self , state=tk.NORMAL)
        self.evaluator_class_entry.place(relx=0.1, rely=0.15)
        
        self.evaluator_class_parameter = Parameter( fancy_name="Evaluator class", error_lambda=self.__is_evaluator_instance )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.evaluator_class_parameter,
                                                          widget_read_lambda=lambda: self.evaluator_class_entry.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var}),
                                                          error_set_lambda=EntryInvalidator(self.evaluator_class_entry),
                                                          error_reset_lambda=EntryValidator(self.evaluator_class_entry),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["evaluator_class"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.evaluator_class_entry, str(var)) ) )
        
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
