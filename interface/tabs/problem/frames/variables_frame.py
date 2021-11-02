# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.problem.frames.problem_frame import *


class VariablesFrame(ProblemFrame):
        
    def check_errors(self):
        error_list = super(VariablesFrame, self).check_errors()
        
        if len(self.problem_parameters.variables) == 0:
            error_list.append("No optimization variable was specified")
        
        return error_list
    
    class VariableParametersFrame(tk.Frame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.VariableParametersFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            
            self.name_label = tk.Label( master=self, text="Name" )
            self.name_label.place( relx=0.1, rely=0.1 )
            self.name_entry = tk.Entry( master=self )
            self.name_entry.place( relx=0.26, rely=0.1, relwidth=0.5 )
            
        def check_name(self, error_list: List[str]):
            
            if not self.name_entry.get():
                error_list.append("Empty variable name")
                self._invalidate_entry_(self.name_entry)
            
            elif self.name_entry.get() in { var.keyword for var in self.problem_parameters.variables }:
                error_list.append("A variable with name '%s' was already defined" % self.name_entry.get())
                self._invalidate_entry_(self.name_entry)
        
        
        def _invalidate_entry_(self, entry):
            entry.config({"background":"#ffc7c8"})
            
            
        def _reset_entry_(self, entry):
            entry.config({"background":"White"})
            
        def clear_errors(self):
            self._reset_entry_(self.name_entry)
            
        def clear_entries(self):
            self.name_entry.delete(0, 'end')
            
        def show(self):
            self.place( relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8 )
        
        def hide(self):
            self.place_forget()
        
    class NumericParametersFrame(VariableParametersFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.NumericParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            self.lower_bound_label = tk.Label( master=self, text="Lower Bound" )
            self.lower_bound_label.place( relx=0.1, rely=0.3 )
            self.lower_bound_entry = tk.Entry( master=self )
            self.lower_bound_entry.place( relx=0.4, rely=0.3, relwidth=0.5 )
            
            self.upper_bound_label = tk.Label( master=self, text="Upper Bound" )
            self.upper_bound_label.place( relx=0.1, rely=0.4 )
            self.upper_bound_entry = tk.Entry( master=self )
            self.upper_bound_entry.place( relx=0.4, rely=0.4, relwidth=0.5 )
            
        
        def clear_errors(self):
            super(VariablesFrame.NumericParametersFrame, self).clear_errors()
            
            self._reset_entry_(self.lower_bound_entry)
            self._reset_entry_(self.upper_bound_entry)
            
        def clear_entries(self):
            super(VariablesFrame.NumericParametersFrame, self).clear_entries()
            
            self.lower_bound_entry.delete(0, 'end')
            self.upper_bound_entry.delete(0, 'end')
        
        
        def check_errors(self) -> bool:
            
            error_list = []
            
            self.check_name(error_list)
            
            # if len(error_list)>0:
            #     self._invalidate_entry_(self.lower_bound_entry)
            
            if not self.is_type(self.lower_bound_entry.get()):
                error_list.append("Lower bound of unsuitable type")
                self._invalidate_entry_(self.lower_bound_entry)
                
            if not self.is_type(self.upper_bound_entry.get()):
                error_list.append("Upper bound of unsuitable type")
                self._invalidate_entry_(self.upper_bound_entry)
            
            if len(error_list) == 0 and self.cast_type(self.lower_bound_entry.get()) >= self.cast_type(self.upper_bound_entry.get()):
                error_list.append("Lower bound must be smaller than Upper bound")
                self._invalidate_entry_(self.lower_bound_entry)
                
            return error_list
            
        
        @abstractmethod
        def cast_type(self, value: str):
            pass
        
        @abstractmethod
        def generate_variable(self):
            pass
            
        @abstractmethod
        def is_type(self, string: str):
            return
        
            
    class FloatParametersFrame(NumericParametersFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.FloatParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
        def is_type(self, string: str):
            return is_float(string)
        
        def cast_type(self, value: str):
            return float(value)
        
        def generate_variable(self):
            
            self.clear_errors()
            
            error_list = self.check_errors()
            
            if len(error_list)==0:
                
                variable = variable_types.FloatVariable(keyword=self.name_entry.get(), lower_bound=float(self.lower_bound_entry.get()), upper_bound=float(self.upper_bound_entry.get()))
                
                self.clear_entries()
                
                return variable
            
            else:
                tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                return None
            
    class IntegerParametersFrame(NumericParametersFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.IntegerParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        def is_type(self, string: str):
            return is_integer(string)
        
        def cast_type(self, value: str):
            return to_integer(value)
        
        def generate_variable(self):
            
            self.clear_errors()
            
            error_list = self.check_errors()
            
            if len(error_list)==0:
                
                variable = variable_types.IntegerVariable(keyword=self.name_entry.get(), lower_bound=to_integer(self.lower_bound_entry.get()), upper_bound=to_integer(self.upper_bound_entry.get()))
                
                self.clear_entries()
                
                return variable
            
            else:
                tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                return None
            
            
            
    class DiscretizedParametersFrame(NumericParametersFrame):
        
        def _radiobutton_command_(self, value):
        
            if value=="step":
                self.step_entry.config(state=tk.NORMAL)
                self.points_entry.delete(0, tk.END)
                self.points_entry.config(state=tk.DISABLED)
                self._reset_entry_(self.points_entry)
                
            elif value=="points":
                self.points_entry.config(state=tk.NORMAL)
                self.step_entry.delete(0, tk.END)
                self.step_entry.config(state=tk.DISABLED)
                self._reset_entry_(self.step_entry)
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.DiscretizedParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            self.ps = tk.StringVar()
            self.ps.set("none")
            self.step_radiobutton = tk.Radiobutton(master=self, text='Step', variable=self.ps, value="step", command=lambda: self._radiobutton_command_(self.ps.get()))
            self.step_entry = tk.Entry(master=self, state=tk.DISABLED)
            self.points_radiobutton = tk.Radiobutton(master=self, text='Nº of points', variable=self.ps, value="points", command=lambda: self._radiobutton_command_(self.ps.get()))
            self.points_entry = tk.Entry(master=self, state=tk.DISABLED)
            
            self.step_radiobutton.place( relx=0.1, rely=0.6 )
            self.step_entry.place( relx=0.4, rely=0.6 )
            
            self.points_radiobutton.place( relx=0.1, rely=0.7 )
            self.points_entry.place( relx=0.4, rely=0.7 )
            
        def is_type(self, string: str):
            return is_float(string)
        
        
        def cast_type(self, value: str):
            return float(value)
        
        def clear_errors(self):
            super(VariablesFrame.DiscretizedParametersFrame, self).clear_errors()
            
            self._reset_entry_(self.step_entry)
            self._reset_entry_(self.points_entry)
            
            
        def clear_entries(self):
            super(VariablesFrame.DiscretizedParametersFrame, self).clear_entries()
            
            self.step_entry.delete(0, 'end')
            self.points_entry.delete(0, 'end')
        
        
        def check_errors(self) -> bool:
            
            error_list = super(VariablesFrame.DiscretizedParametersFrame, self).check_errors()
            
            if self.ps.get() == "none":
                error_list.append( "No discretization criteria selected" )
                
            elif self.ps.get() == "step" and (not is_float(self.step_entry.get()) or float(self.step_entry.get())<= 0.0):
                error_list.append( "Invalid step value" )
                self._invalidate_entry_(self.step_entry)
                
            elif self.ps.get() == "points" and (not is_integer(self.points_entry.get()) or to_integer(self.points_entry.get()) < 1):
                error_list.append( "Invalid number of points" )
                self._invalidate_entry_(self.points_entry)
                
            return error_list
        
        
        def generate_variable(self):
            
            self.clear_errors()
            
            error_list = self.check_errors()
            
            if len(error_list)==0 and self.ps.get() == "step" and float(self.step_entry.get()) >= ( float(self.upper_bound_entry.get()) - float(self.lower_bound_entry.get()) ):
                error_list.append("Chosen step value exceeds the range of the variable")
                self._invalidate_entry_(self.step_entry)
                
            if len(error_list)==0:
                
                if self.ps.get() == "step":
                    step = float(self.step_entry.get())
                    
                elif self.ps.get() == "points":
                    step = (float(self.upper_bound_entry.get()) - float(self.lower_bound_entry.get()))/float(self.points_entry.get())
                
                variable = variable_types.DiscretizedFloatVariable(keyword=self.name_entry.get(), lower_bound=float(self.lower_bound_entry.get()), upper_bound=float(self.upper_bound_entry.get()), step=step)
                
                self.clear_entries()
                
                return variable
            
            else:
                tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                return None
            
    class BinaryParametersFrame(VariableParametersFrame):
        
        def generate_variable(self):
            
            self.clear_errors()
            
            error_list = []
            
            self.check_name(error_list)
            
            if len(error_list)==0:
                
                variable = variable_types.BinaryVariable(keyword=self.name_entry.get())
                
                self.clear_entries()
                
                return variable
            
            else:
                tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                return None
            
    class PermutationParametersFrame(VariableParametersFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(VariablesFrame.PermutationParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            self.permutation_label = tk.Label( master=self, text="Insert elements (comma separated):")
            self.permutation_label.place( relx=0.1, rely=0.3 )
            self.permutation_textbox = tk.Text( master=self )
            self.permutation_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
        
        def clear_entries(self):
            super(VariablesFrame.PermutationParametersFrame, self).clear_entries()
            
            self.permutation_textbox.delete('1.0', tk.END)
        
        def generate_variable(self):
            
            self.clear_errors()
            
            error_list = []
            
            self.check_name(error_list)
            
            string = self.permutation_textbox.get("1.0", tk.END)
            string = string.rstrip("\n")
            # string = string.rstrip(" ")
            string = remove_whitespaces(string)
            string = string.rstrip("\t")
            elements = string.split(",")
            
            if len(elements)<2:
                error_list.append("At least two elements are needed")
                
            elif not all( is_integer(e) for e in elements ):
                error_list.append("Non-integer values in permutation")
                
            else:
                elements_int = [ to_integer(e) for e in elements ]
                
            
            if len(error_list)==0:
                
                variable = variable_types.PermutationVariable(keyword=self.name_entry.get(), elements=elements_int)
                
                self.clear_entries()
                
                return variable
            
            else:
                tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join( ["-" + s for s in error_list] ))
                return None
    
    def add_variable(self):
        variable = self.selected_variable_frame.generate_variable()
        
        if variable != None:
            
            var_name = variable.keyword
            var_type = self.type_dict[type(variable)]
            
            if type(variable) in [variable_types.BinaryVariable, variable_types.PermutationVariable]:
                var_lower_bound = "-"
                var_upper_bound = "-"
                
            else:
                var_lower_bound = str(variable.lower_bound)
                var_upper_bound = str(variable.upper_bound)
        
            self.problem_parameters.variables.append( variable )
            self.parameters_tree.insert('', 'end', text=var_name, values=(var_type, var_lower_bound, var_upper_bound))
    
    def delete_variable(self):
        
        for iid in self.parameters_tree.selection():
            var_name = self.parameters_tree.item(iid)['text']
            self.parameters_tree.delete( iid )
            
            self.problem_parameters.variables = [ x for x in self.problem_parameters.variables if x.keyword!=var_name ]
            
    
    def clearall_variable(self):
        
        var_names = []
        
        for iid in self.parameters_tree.get_children():
            var_names.append( self.parameters_tree.item(iid)['text'] )
            self.parameters_tree.delete( iid )
            
        self.problem_parameters.variables = [ x for x in self.problem_parameters.variables if x.keyword not in var_names ]
    
    
    def update_type(self, new_value):
        self.selected_variable_frame.clear_errors()
        self.selected_variable_frame.clear_entries()
        self.selected_variable_frame.hide()
        self.selected_variable_frame = self.variable_frames[new_value]
        self.selected_variable_frame.show()
        
    def load_variables(self):
        
        self.clearall_variable()
        
        for variable in self.problem_parameters.variables:
            
            var_name = variable.keyword
            var_type = self.type_dict[type(variable)]
            
            if type(variable) in [variable_types.BinaryVariable, variable_types.PermutationVariable]:
                var_lower_bound = "-"
                var_upper_bound = "-"
                
            else:
                var_lower_bound = str(variable.lower_bound)
                var_upper_bound = str(variable.upper_bound)
        
            self.parameters_tree.insert('', 'end', text=var_name, values=(var_type, var_lower_bound, var_upper_bound))
        
    
    def load_parameters(self):
        
        super(VariablesFrame, self).load_parameters()
        
        self.load_variables()
    
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(VariablesFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        
        labelframe_list = tk.LabelFrame(master=self, text="Variable List")
        labelframe_list.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.65)
        
        self.variable_headers = ["Type", "Lower bound", "Upper bound"]
        self.parameters_tree = ttk.Treeview(master=labelframe_list, columns=self.variable_headers, selectmode="extended")
        
        self.parameters_tree.heading("#0", text="Name")
        self.parameters_tree.column("#0", minwidth=100, width=200, stretch=tk.NO)
        
        self.parameters_tree.heading( "Type", text="Type" )
        self.parameters_tree.column( "Type", minwidth=100, width=200, stretch=tk.NO )
        
        self.parameters_tree.heading( "Lower bound", text="Lower bound" )
        self.parameters_tree.column( "Lower bound", minwidth=100, width=200, stretch=tk.NO )
        
        self.parameters_tree.heading( "Upper bound", text="Upper bound" )
        self.parameters_tree.column( "Upper bound", minwidth=100, width=200 )
        
        self.parameters_tree.place(relx=0.02, rely=0.17, relwidth=0.955, relheight=0.8)
    
        
    
        delete = ttk.Button(labelframe_list, text="Delete", command=self.delete_variable)
        delete.place(relx=0.805, rely=0.025, relwidth=0.17, relheight=0.1 )         
    
        clearall = ttk.Button(labelframe_list, text="Clear All", command=self.clearall_variable)
        clearall.place(relx=0.62, rely=0.025, relwidth=0.17, relheight=0.1 ) 
    
        labelframe_add = tk.LabelFrame(master=self, text="Add Variables")
        labelframe_add.place(relx=0.69, rely=0.05, relheight=0.9, relwidth=0.29)
    
        tk.Label(labelframe_add, text = "Type").place(relx=0.1325,rely=0.05)
        optionList_Type = ["Real", "Integer", "Discretized real", "Binary", "Permutation"]
        optionType = tk.StringVar(labelframe_add)
        optionType.set("Real")
        option_type = tk.OptionMenu(labelframe_add, optionType, *optionList_Type, command=self.update_type)
        option_type.config(width=5)
        option_type.place(relx=0.28,rely=0.04, relwidth=0.45)
    
        self.add_button = ttk.Button(labelframe_add, text="Add", command=self.add_variable)
        self.add_button.place(relx=0.325, rely=0.86, relwidth=0.35, relheight=0.1)
        
        self.type_dict = { variable_types.FloatVariable:"Real",
                      variable_types.IntegerVariable:"Integer",
                      variable_types.DiscretizedFloatVariable:"Discretized real",
                      variable_types.BinaryVariable:"Binary",
                      variable_types.PermutationVariable:"Permutation" }
        
        self.variable_frames = {}
        self.variable_frames["Real"] = VariablesFrame.FloatParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.variable_frames["Integer"] = VariablesFrame.IntegerParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.variable_frames["Discretized real"] = VariablesFrame.DiscretizedParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.variable_frames["Binary"] = VariablesFrame.BinaryParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.variable_frames["Permutation"] = VariablesFrame.PermutationParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        
        self.variable_frames["Real"].show()
        self.selected_variable_frame = self.variable_frames["Real"]
        
        self.add_button.lift()