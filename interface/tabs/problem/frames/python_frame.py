# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from inspect import getmembers, isfunction
import copy
import random
import math
import yaml
import os
import re

import imp
from pathlib import Path

from interface.tabs.problem.frames.problem_frame import *
from core.variable import *

from util.arg_parsing import *

class PythonFrame(ProblemFrame):
        
    NUMBER_OF_SUPPORTED_OBJECTIVES=10
    
    class ObjectiveDoubleclickPopup:
        
        def __init__( self, controller, event ):
        
            self.controller = controller    
            
            self.entry_item = self.controller.objectives_tree.selection()[0]
        
            self.selection_index = to_integer(self.controller.objectives_tree.item( self.entry_item, "text" ))
            self.original_selection_values = self.controller.objectives_tree.item( self.entry_item, "values" )
        
            self.objective_popup_win = tk.Toplevel( master=self.controller )
            self.objective_popup_win.wm_title("Change objective parameters")
            self.objective_popup_win.resizable(False,False)
            self.objective_popup_win.iconbitmap( os.path.join(os.getcwd(), 'interface', 'resources', 'images', 'joptimizer_icon.ico') )
            
            screen_width = self.objective_popup_win.winfo_screenwidth()
            screen_height = self.objective_popup_win.winfo_screenheight()
            
            window_width = 230
            window_height = 170
            
            window_x_offset = screen_width//2 - window_width//2
            window_y_offset = screen_height//2 - window_height//2
            
            self.objective_popup_win.wm_geometry("%dx%d+%d+%d" % (window_width, window_height, window_x_offset, window_y_offset))
            self.objective_popup_win.grab_set()
            
            name_label = tk.Label( master=self.objective_popup_win, text="Name" )
            name_label.grid( row=0, column=0, sticky="NSEW", padx=(30,0), pady=(30,0), columnspan=1 )
            
            self.name_entry = tk.Entry( master=self.objective_popup_win )
            self.name_entry.grid( row=0, column=1, sticky="NSEW", padx=(10,10), pady=(30,0), columnspan=2 )
            self.name_entry.insert( 0, self.original_selection_values[0] )
            
            mode_label = tk.Label( master=self.objective_popup_win, text="Mode" )
            mode_label.grid( row=1, column=0, sticky="NSEW", padx=(30,0), pady=(10,0), columnspan=1 )
            
            objective_option_list = [ ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE.value, ProblemParameters.OPTIMIZATION_TYPE.MAXIMIZE.value ]
            
            self.ObjectiveOption = tk.StringVar(self.objective_popup_win)
            self.ObjectiveOption.set( self.original_selection_values[1] )
            self.objective_option = tk.OptionMenu(self.objective_popup_win, self.ObjectiveOption, *objective_option_list )
            self.objective_option.grid( row=1, column=1, sticky="NSEW", padx=(10,10), pady=(10,0), columnspan=2 )
            
            self.save_close_button = tk.Button( master=self.objective_popup_win, text="Close", command=self._close)
            self.save_close_button.grid( row=2, column=0, sticky="NSEW", padx=(30,10), pady=(10,30), columnspan=3 )
            
        def _close(self):
            
            if not re.match("[a-zA-Z0-9][a-zA-Z0-9_]*", self.name_entry.get()):
                tk.messagebox.showerror(title="Invalid objective name", message="Objective name contains invalid characters")
                
            elif self.original_selection_values[0] != self.name_entry.get() and \
                ((self.name_entry.get() in self.controller.reserved_objective_names and self.name_entry.get() != "O"+str(self.selection_index)) or \
                 self.name_entry.get() in self.controller.objectives_dict):
                     
                tk.messagebox.showerror(title="Invalid objective name", message="Objective name already exists or is a reserved word")
                
            else:
                name = self.name_entry.get()
                index = self.controller.objectives.index( self.controller.objectives_dict.pop( self.original_selection_values[0] ) )
                new_objective = (name, ProblemParameters.OPTIMIZATION_TYPE(self.ObjectiveOption.get()))
                self.controller.objectives[index] = new_objective
                self.controller.objectives_dict[name] = new_objective
                self.controller.objectives_tree.item( self.entry_item, values=(name,self.ObjectiveOption.get()) )
                
                self.objective_popup_win.destroy()
                
                
    
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
    
    
    def _update_objectives(self, new_value):
        
        new_objective_count = to_integer(new_value)
        
        if new_objective_count > self.current_objectives:
            
            for i in range(new_objective_count - self.current_objectives):
                self.objectives_tree.insert('', 'end', text=str(self.current_objectives + i + 1), values=("O"+str(self.current_objectives + i + 1),ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE.value))
                new_objective = ("O"+str(self.current_objectives + i + 1), ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE)
                self.objectives.append( new_objective )
                self.objectives_dict[ new_objective[0] ] = new_objective
            
        
        elif new_objective_count < self.current_objectives:
            
            for i in range(self.current_objectives - new_objective_count):
                objective = self.objectives.pop()
                self.objectives_dict.pop(objective[0])
                self.objectives_tree.delete(self.objectives_tree.get_children()[-1])
            
            
        self.current_objectives = new_objective_count
        
        
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(PythonFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        
        # Script path
        self.script_file_path_frame = tk.Frame(self)
        ttk.Label( master=self.script_file_path_frame, text="Function script path").grid( row=0, column=0, sticky="NSEW", padx=0, pady=0 )
        self.ScriptFilePath = tk.Entry(master=self.script_file_path_frame, state=tk.NORMAL)
        self.ScriptFilePath.insert(0, problem_parameters.options["python_script_path"])
        self.ScriptFilePath.grid( row=0, column=1, sticky="NSEW", padx=8, pady=0, columnspan=1, ipadx=150 )
        self.ScriptFilePath.config(state=tk.DISABLED)
        self.button_browse_operator = ttk.Button( master=self.script_file_path_frame,  text="Browse", command=lambda: self._browse() )
        self.button_browse_operator.grid( row=0, column=2, sticky="NSEW", padx=8, pady=0, columnspan=1 )
        
        self.script_file_path_frame.grid( row=0, column=0, sticky="NSW", pady=(30,0), padx=25 )
        
        
        # Function choice
        self.function_options = ["none"]
        
        self.function_frame = tk.Frame(self)
        tk.Label( master=self.function_frame, text="Function").grid( row=0, column=0, sticky="NSEW", padx=0, pady=2 )
        self.FunctionOption = tk.StringVar(self.function_frame)
        self.FunctionOption.set(self.function_options[0])
        self.function_option = tk.OptionMenu(self.function_frame, self.FunctionOption, *self.function_options )
        
        self.function_option.config( state=tk.NORMAL )
        self.function_option.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1, ipadx=60 )
        self.function_frame.grid( row=1, column=0, sticky="NSEW", pady=(30,0), padx=25 )
        
        # self.function_option_parameter = Parameter(name="function_operator", fancy_name="Function operator")
        
        self.script_path_parameter = FilePath( fancy_name="Function script path", extension=".py" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.script_path_parameter,
                                                          widget_read_lambda=lambda: self.ScriptFilePath.get(),
                                                          variable_store_lambda=lambda var: self._save_function_parameters(var),
                                                          # error_set_lambda=EntryInvalidator(self.ScriptFilePath),
                                                          # error_reset_lambda=EntryValidator(self.ScriptFilePath),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["python_script_path"],
                                                          widget_update_lambda=lambda var: self._update_function_parameters(var) ) )
        
        
        
        # Call args
        self.call_args_frame = tk.Frame(self)
        tk.Label( master=self.call_args_frame, text="Call argument format").grid( row=0, column=0, sticky="NSEW", padx=0, pady=2 )
        self.ArgsEntry = tk.Entry(master=self.call_args_frame, state=tk.NORMAL)
        self.ArgsEntry.insert(0, self.problem_parameters.options["call_args"])
        self.ArgsEntry.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1, ipadx=145 )
        self.call_args_frame.grid( row=2, column=0, sticky="NSEW", pady=(30,0), padx=25 )
   
    
        # Number of objectives
        self.number_of_objectives_frame = tk.Frame(self)
        objective_option_list = [i for i in range(1,PythonFrame.NUMBER_OF_SUPPORTED_OBJECTIVES+1)]
        tk.Label( master=self.number_of_objectives_frame, text="Number of objectives").grid( row=0, column=0, sticky="NSEW", padx=0, pady=2 )
        self.ObjectiveOption = tk.StringVar(self)
        # self.ObjectiveOption.set( to_integer(self.problem_parameters.options["objectives"]) )
        self.ObjectiveOption.set( objective_option_list[0] )
        self.objective_option = tk.OptionMenu(self.number_of_objectives_frame, self.ObjectiveOption, *objective_option_list, command=self._update_objectives )
        self.objective_option.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1, ipadx=40 )
        self.number_of_objectives_frame.grid( row=3, column=0, sticky="NSEW", pady=(30,0), padx=25 )
        
        # self.ObjectivesEntry = tk.Entry(master=self, state=tk.NORMAL)
        # self.ObjectivesEntry.insert(0, self.problem_parameters.options["objectives"])
        # self.ObjectivesEntry.place( relx=0.14, rely=0.25-0.005, relwidth=0.1 )
        
        self.objectives_parameter = Integer(name="number_of_objectives", fancy_name="Number of objectives", lower_bound=1, upper_bound=1000)
            
        self.parameters_bindings.append( ParameterBinding(parameter=self.objectives_parameter,
                                                          widget_read_lambda=lambda: self.ObjectiveOption.get(),
                                                          variable_store_lambda=lambda var: self.problem_parameters.options.update({"objectives":var}),
                                                          # error_set_lambda=EntryInvalidator(self.ObjectivesEntry),
                                                          # error_reset_lambda=EntryValidator(self.ObjectivesEntry),
                                                          variable_read_lambda=lambda: self.problem_parameters.options["objectives"],
                                                          widget_update_lambda=lambda var: self.ObjectiveOption.set( str(var)) ) )        
        
        self.objectives_headers = ["Name", "Type"]
        self.objectives_tree = ttk.Treeview(master=self, columns=self.objectives_headers, selectmode="extended")
        
        self.objectives_tree.heading("#0", text="Index")
        self.objectives_tree.column("#0", minwidth=100, width=200, stretch=tk.NO)
        
        self.objectives_tree.heading( "Name", text="Name" )
        self.objectives_tree.column( "Name", minwidth=100, width=200, stretch=tk.NO )
        
        self.objectives_tree.heading( "Type", text="Type" )
        self.objectives_tree.column( "Type", minwidth=100, width=200, stretch=tk.NO )
        
        self.objectives_tree.grid( row=4, column=0, sticky="NSEW", pady=(30,15), padx=25 )
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
        self.reserved_objective_names = { "O"+str(i) for i in range(1,PythonFrame.NUMBER_OF_SUPPORTED_OBJECTIVES+1) }
        self.current_objectives = 1
        self.objectives = [("O1",ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE)]
        self.objectives_dict = { "O1" : self.objectives[0] }
        
        for i, objective in enumerate(self.objectives,1):
            self.objectives_tree.insert('', 'end', text=str(i), values=(objective[0], objective[1].value))
            
        self.objectives_tree.bind("<Double-1>", lambda event: PythonFrame.ObjectiveDoubleclickPopup(controller=self, event=event))
    
    # def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
    #     super(PythonFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
    #     ttk.Label( master=self, text="Function script path").place( relx=0.02, rely=0.05 )
    #     self.ScriptFilePath = tk.Entry(master=self, state=tk.NORMAL)
    #     self.ScriptFilePath.insert(0, problem_parameters.options["python_script_path"])
    #     self.ScriptFilePath.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
    #     self.ScriptFilePath.config(state=tk.DISABLED)
    #     self.button_browse_operator = ttk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
        
    #     self.function_options = ["none"]
        
    #     tk.Label( master=self, text="Function").place( relx=0.02, rely=0.15 )
        
    #     self.FunctionOption = tk.StringVar(self)
    #     self.FunctionOption.set(self.function_options[0])
    #     self.function_option = tk.OptionMenu(self, self.FunctionOption, *self.function_options )
        
    #     self.function_option.config( state=tk.NORMAL )
    #     self.function_option.place( relx=0.09, rely=0.15-0.005, relwidth=0.15 )
        
    #     # self.function_option_parameter = Parameter(name="function_operator", fancy_name="Function operator")
        
    #     self.script_path_parameter = FilePath( fancy_name="Function script path", extension=".py" )
        
    #     self.parameters_bindings.append( ParameterBinding(parameter=self.script_path_parameter,
    #                                                       widget_read_lambda=lambda: self.ScriptFilePath.get(),
    #                                                       variable_store_lambda=lambda var: self._save_function_parameters(var),
    #                                                       # error_set_lambda=EntryInvalidator(self.ScriptFilePath),
    #                                                       # error_reset_lambda=EntryValidator(self.ScriptFilePath),
    #                                                       variable_read_lambda=lambda: self.problem_parameters.options["python_script_path"],
    #                                                       widget_update_lambda=lambda var: self._update_function_parameters(var) ) )
        
        
    #     tk.Label( master=self, text="Call argument format").place( relx=0.02, rely=0.25 )
    #     self.ArgsEntry = tk.Entry(master=self, state=tk.NORMAL)
    #     self.ArgsEntry.insert(0, self.problem_parameters.options["call_args"])
    #     self.ArgsEntry.place( relx=0.14, rely=0.25, relwidth=0.3 )
        
    #     objective_option_list = [i for i in range(1,PythonFrame.NUMBER_OF_SUPPORTED_OBJECTIVES+1)]
    #     tk.Label( master=self, text="Number of objectives").place( relx=0.02, rely=0.35 )
    #     self.ObjectiveOption = tk.StringVar(self)
    #     # self.ObjectiveOption.set( to_integer(self.problem_parameters.options["objectives"]) )
    #     self.ObjectiveOption.set( objective_option_list[0] )
    #     self.objective_option = tk.OptionMenu(self, self.ObjectiveOption, *objective_option_list, command=self._update_objectives )
    #     self.objective_option.place( relx=0.14, rely=0.35-0.005, relwidth=0.1 )
        
    #     # self.ObjectivesEntry = tk.Entry(master=self, state=tk.NORMAL)
    #     # self.ObjectivesEntry.insert(0, self.problem_parameters.options["objectives"])
    #     # self.ObjectivesEntry.place( relx=0.14, rely=0.25-0.005, relwidth=0.1 )
        
    #     self.objectives_parameter = Integer(name="number_of_objectives", fancy_name="Number of objectives", lower_bound=1, upper_bound=1000)
            
    #     self.parameters_bindings.append( ParameterBinding(parameter=self.objectives_parameter,
    #                                                       widget_read_lambda=lambda: self.ObjectiveOption.get(),
    #                                                       variable_store_lambda=lambda var: self.problem_parameters.options.update({"objectives":var}),
    #                                                       # error_set_lambda=EntryInvalidator(self.ObjectivesEntry),
    #                                                       # error_reset_lambda=EntryValidator(self.ObjectivesEntry),
    #                                                       variable_read_lambda=lambda: self.problem_parameters.options["objectives"],
    #                                                       widget_update_lambda=lambda var: self.ObjectiveOption.set( str(var)) ) )        
        
    #     self.objectives_headers = ["Name", "Type"]
    #     self.objectives_tree = ttk.Treeview(master=self, columns=self.objectives_headers, selectmode="extended")
        
    #     self.objectives_tree.heading("#0", text="Index")
    #     self.objectives_tree.column("#0", minwidth=100, width=200, stretch=tk.NO)
        
    #     self.objectives_tree.heading( "Name", text="Name" )
    #     self.objectives_tree.column( "Name", minwidth=100, width=200, stretch=tk.NO )
        
    #     self.objectives_tree.heading( "Type", text="Type" )
    #     self.objectives_tree.column( "Type", minwidth=100, width=200, stretch=tk.NO )
        
    #     self.objectives_tree.place(relx=0.02, rely=0.45, relwidth=0.955, relheight=0.5)
    
    #     self.reserved_objective_names = { "O"+str(i) for i in range(1,PythonFrame.NUMBER_OF_SUPPORTED_OBJECTIVES+1) }
    #     self.current_objectives = 1
    #     self.objectives = [("O1",ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE)]
    #     self.objectives_dict = { "O1" : self.objectives[0] }
        
    #     for i, objective in enumerate(self.objectives,1):
    #         self.objectives_tree.insert('', 'end', text=str(i), values=(objective[0], objective[1].value))
            
    #     self.objectives_tree.bind("<Double-1>", lambda event: PythonFrame.ObjectiveDoubleclickPopup(controller=self, event=event))
    
        
    def check_args(self):
        
        arg_string = su.remove_whitespaces( self.ArgsEntry.get() )
        arg_tokens = arg_string.split(',')
        
        keywargs_started = False
        already_warned = False
        error_list = []
        
        # vector_vars = { var.keyword:var for var in self.problem_parameters.variables if isinstance(var,VectorVariable) }
        # scalar_vars = { var.keyword:var for var in self.problem_parameters.variables if not isinstance(var,VectorVariable) }
        # scalar_vars = set.union( scalar_vars, { var.keyword:var for var in self.problem_parameters.constants if not isinstance(var,VectorVariable) })
        
        for token in arg_tokens:
            
            ret = token_is_kwarg(token)
            
            
            if ret != None:
                
                keywargs_started = True
                
                # if (ret[1] not in scalar_vars) and (ret[1] not in vector_vars) and (ret[1] not in matrix_vars):
                if ret[1] not in self.problem_parameters.defined_symbols:
                    error_list.append( "Variable '%s' not defined" % ret[1] )
                    
                    
            else:
    
                ret = token_is_unpacked_arg(token)
                
                if keywargs_started and not already_warned:
                    error_list.append( "args must preceed kwargs: %s" % token )
                    already_warned = True
                
                elif ret!=None:
                    
                    # if ret not in vector_vars:
                    if ret not in self.problem_parameters.defined_symbols or not (isinstance(self.problem_parameters.defined_symbols[ret],VectorVariable) or \
                                                                                  isinstance(self.problem_parameters.defined_symbols[ret],PermutationVariable)):
                        error_list.append( "Variable '%s' is not defined or not of an unpackable type" % ret )
                        
                else:
                    
                    if not token_is_arg(token) or (token not in self.problem_parameters.defined_symbols):
                        error_list.append( "Variable '%s' is not defined or is syntactically incorrect" % token )

        return error_list
    
    def check_errors(self):
        error_list = super(PythonFrame,self).check_errors()
        error_list.extend(self.check_args())
        return error_list
            
    def save_parameters(self):
        super(PythonFrame,self).save_parameters()
        self.problem_parameters.options["call_args"] = self.ArgsEntry.get()
        self.problem_parameters.options["objectives"] = len(self.objectives)
        self.problem_parameters.options["objectives_names"] = [ objective[0] for objective in self.objectives]
        self.problem_parameters.options["objectives_minimize"] = [ objective[1]==ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE for objective in self.objectives]
            
    def load_parameters(self):
        super(PythonFrame,self).load_parameters()
        self.ArgsEntry.set(self.problem_parameters.options["call_args"])
        
        self.objectives = []
        self.objectives_dict = {}
        
        for name, minimize in zip(self.problem_parameters.options["objectives_names"],self.problem_parameters.options["objectives_minimize"]):
            
            if minimize:
                objective_type = ProblemParameters.OPTIMIZATION_TYPE.MINIMIZE
            else:
                objective_type = ProblemParameters.OPTIMIZATION_TYPE.MAXIMIZE
            
            objective = (name,objective_type)
            self.objectives.append(objective)
            self.objectives_dict[name] = objective
        
        for iid in self.objectives_tree.get_children():
            self.objectives_tree.delete( iid )
        
        for i, objective in enumerate(self.objectives,1):
            self.objectives_tree.insert('', 'end', text=str(i), values=(objective[0], objective[1].value))
        
    
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

