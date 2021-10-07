# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:25:11 2021

@author: Álvaro
"""

import sys
sys.path.append(r"./../..")

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    # from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter.ttk import Notebook
    from tkinter import messagebox    
    from tkinter import scrolledtext
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
    
    
from win32api import GetSystemMetrics
from collections import defaultdict
from typing import List

import core.variable as variable_types
import core.constant as constant_types
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float, to_integer
from util.string_utils import remove_whitespaces

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding



class ProblemTab(ttk.Frame):
    
    class ProblemFrame(tk.LabelFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ProblemFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.parameters_bindings = []
            
        def check_errors(self):
            
            error_list = []
            
            for binding in self.parameters_bindings:
                error_list.extend(binding.error_check())
                
            return error_list
                
        def save_parameters(self):
            
            for binding in self.parameters_bindings:
                binding.store_value()
                
        def display(self):
            self.place( relx=0.18, rely=0.045, relwidth=0.81, relheight=0.715 )
            
        def hide(self):
            self.place_forget()
            
            
            
    class EvaluatorFrame(ProblemFrame):
        
        def _browse(self): 
            
            path = filedialog.askopenfilename(title = "Select a file which contains the evaluator")
            
            self.OperatorFilePath.config(state=tk.NORMAL)
            self.OperatorFilePath.insert( 0, path )
            self.OperatorFilePath.config(state="readonly")
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.EvaluatorFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Evaluator script path").place( relx=0.02, rely=0.05 )
            self.OperatorFilePath = tk.Entry(master=self, state=tk.NORMAL)
            self.OperatorFilePath.insert(0, problem_parameters.options["evaluator_classname"])
            self.OperatorFilePath.place(relx=0.12, rely=0.05+0.005, relwidth=0.3)
            self.OperatorFilePath.config(state=tk.DISABLED)
            self.button_browse_operator = tk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
            
            self.evaluator_path_parameter = FilePath( fancy_name="Evaluator script path" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.evaluator_path_parameter,
                                                              widget_read_lambda=lambda: self.evaluator_class_entry.get(),
                                                              variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var})) )
            
            
            
            tk.Label( master=self, text="Evaluator class").place( relx=0.02, rely=0.15 )
            self.evaluator_class_entry = tk.Entry( master=self , state=tk.NORMAL)
            self.evaluator_class_entry.place(relx=0.1, rely=0.15)
            
            evaluator_class_parameter = Parameter( fancy_name="Evaluator class" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=evaluator_class_parameter,
                                                              widget_read_lambda=lambda: self.evaluator_class_entry.get(),
                                                              variable_store_lambda=lambda var: self.problem_parameters.options.update({"evaluator_class":var})) )
            
            
        
    class VariablesFrame(ProblemFrame):
        
        def check_errors(self):
            error_list = super(ProblemTab.VariablesFrame, self).check_errors()
            
            if len(self.problem_parameters.variables) == 0:
                error_list.append("No optimization variable was specified")
            
            return error_list
        
        class VariableParametersFrame(tk.Frame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.VariablesFrame.VariableParametersFrame, self).__init__(master=master, *args, **kwargs)
                
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
                super(ProblemTab.VariablesFrame.NumericParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
                self.lower_bound_label = tk.Label( master=self, text="Lower Bound" )
                self.lower_bound_label.place( relx=0.1, rely=0.3 )
                self.lower_bound_entry = tk.Entry( master=self )
                self.lower_bound_entry.place( relx=0.4, rely=0.3, relwidth=0.5 )
                
                self.upper_bound_label = tk.Label( master=self, text="Upper Bound" )
                self.upper_bound_label.place( relx=0.1, rely=0.4 )
                self.upper_bound_entry = tk.Entry( master=self )
                self.upper_bound_entry.place( relx=0.4, rely=0.4, relwidth=0.5 )
                
            
            def clear_errors(self):
                super(ProblemTab.VariablesFrame.NumericParametersFrame, self).clear_errors()
                
                self._reset_entry_(self.lower_bound_entry)
                self._reset_entry_(self.upper_bound_entry)
                
            def clear_entries(self):
                super(ProblemTab.VariablesFrame.NumericParametersFrame, self).clear_entries()
                
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
                super(ProblemTab.VariablesFrame.FloatParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
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
                super(ProblemTab.VariablesFrame.IntegerParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
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
                super(ProblemTab.VariablesFrame.DiscretizedParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
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
                super(ProblemTab.VariablesFrame.DiscretizedParametersFrame, self).clear_errors()
                
                self._reset_entry_(self.step_entry)
                self._reset_entry_(self.points_entry)
                
                
            def clear_entries(self):
                super(ProblemTab.VariablesFrame.DiscretizedParametersFrame, self).clear_entries()
                
                self.step_entry.delete(0, 'end')
                self.points_entry.delete(0, 'end')
            
            
            def check_errors(self) -> bool:
                
                error_list = super(ProblemTab.VariablesFrame.DiscretizedParametersFrame, self).check_errors()
                
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
                super(ProblemTab.VariablesFrame.PermutationParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
                self.permutation_label = tk.Label( master=self, text="Insert elements (comma separated):")
                self.permutation_label.place( relx=0.1, rely=0.3 )
                self.permutation_textbox = tk.Text( master=self )
                self.permutation_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
            
            def clear_entries(self):
                super(ProblemTab.VariablesFrame.PermutationParametersFrame, self).clear_entries()
                
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
        
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.VariablesFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            
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
            self.variable_frames["Real"] = ProblemTab.VariablesFrame.FloatParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.variable_frames["Integer"] = ProblemTab.VariablesFrame.IntegerParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.variable_frames["Discretized real"] = ProblemTab.VariablesFrame.DiscretizedParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.variable_frames["Binary"] = ProblemTab.VariablesFrame.BinaryParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.variable_frames["Permutation"] = ProblemTab.VariablesFrame.PermutationParametersFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            
            self.variable_frames["Real"].show()
            self.selected_variable_frame = self.variable_frames["Real"]
            
            self.add_button.lift()
            
         
            
    class ConstantsFrame(ProblemFrame):
        
        class ConstantsParametersFrame(tk.Frame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.ConstantsParametersFrame, self).__init__(master=master, *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                
                self.name_label = tk.Label( master=self, text="Name" )
                self.name_label.place( relx=0.1, rely=0.1 )
                self.name_entry = tk.Entry( master=self )
                self.name_entry.place( relx=0.26, rely=0.1, relwidth=0.5 )
                
            def check_name(self, error_list: List[str]):
                
                if not self.name_entry.get():
                    error_list.append("Empty constant name")
                    self._invalidate_entry_(self.name_entry)
                
                elif self.name_entry.get() in { const.keyword for const in self.problem_parameters.constants }:
                    error_list.append("A constant with name '%s' was already defined" % self.name_entry.get())
                    self._invalidate_entry_(self.name_entry)
            
            def check_errors(self):
                
                error_list = []
                
                self.check_name(error_list)
                
                return error_list
            
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
                
        class NumericConstantFrame(ConstantsParametersFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.NumericConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                    
                self.value_label = tk.Label( master=self, text="Value" )
                self.value_label.place( relx=0.1, rely=0.2 )
                self.value_entry = tk.Entry( master=self )
                self.value_entry.place( relx=0.26, rely=0.2, relwidth=0.5 )
               
            @abstractmethod
            def is_type(self, string: str):
                pass
            
            @abstractmethod
            def cast_type(self, value: str):
                pass
              
            def clear_errors(self):
                super(ProblemTab.ConstantsFrame.NumericConstantFrame, self).clear_errors()
                
                self._reset_entry_(self.value_entry)
                
            def clear_entries(self):
                super(ProblemTab.ConstantsFrame.NumericConstantFrame, self).clear_entries()
                
                self.value_entry.delete(0, 'end')  
              
            def check_errors(self):
                
                error_list = super(ProblemTab.ConstantsFrame.NumericConstantFrame, self).check_errors()
                
                if not self.is_type(self.value_entry.get()):
                    error_list.append("Value of unsuitable type")
                    self._invalidate_entry_(self.value_entry)
                    
                return error_list
                
        class FloatConstantFrame(NumericConstantFrame):
        
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.FloatConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
            def is_type(self, string: str):
                return is_float(string)
            
            def cast_type(self, value: str):
                return float(value)
            
            def generate_constant(self):
                
                self.clear_errors()
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    
                    variable = constant_types.FloatConstant(keyword=self.name_entry.get(), value=self.cast_type(self.value_entry.get()))
                    
                    self.clear_entries()
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding constant", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                    return None
        
        
        class IntegerConstantFrame(NumericConstantFrame):
        
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.IntegerConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
            def is_type(self, string: str):
                return is_integer(string)
            
            def cast_type(self, value: str):
                return to_integer(value)
            
            def generate_constant(self):
                
                self.clear_errors()
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    
                    variable = constant_types.IntegerConstant(keyword=self.name_entry.get(), value=self.cast_type(self.value_entry.get()))
                    
                    self.clear_entries()
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding constant", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                    return None
             
                
        class BinaryConstantFrame(ConstantsParametersFrame):
        
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.BinaryConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
                self.value_label = tk.Label(master=self, text = "Value")
                options = ["True", "False"]
                self.value_option = tk.StringVar(master=self)
                self.value_option.set("True")
                self.option_menu = tk.OptionMenu(self, self.value_option, *options)
                
                self.value_label.place( relx=0.1, rely=0.2 )
                self.option_menu.place( relx=0.26, rely=0.2, relwidth=0.5 )
            
            def cast_type(self, value: str):
                
                if value=="True":
                    return True
                
                return False
            
            def generate_constant(self):
                
                self.clear_errors()
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    
                    variable = constant_types.BinaryConstant(keyword=self.name_entry.get(), value=self.cast_type(self.value_option.get()))
                    
                    self.clear_entries()
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding constant", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                    return None
        
        
        class PermutationConstantFrame(ConstantsParametersFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.PermutationConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
                self.permutation_label = tk.Label( master=self, text="Insert elements (comma separated):")
                self.permutation_label.place( relx=0.1, rely=0.3 )
                self.permutation_textbox = tk.Text( master=self )
                self.permutation_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
            
            def clear_entries(self):
                super(ProblemTab.ConstantsFrame.PermutationConstantFrame, self).clear_entries()
                
                self.permutation_textbox.delete('1.0', tk.END)
            
            def check_errors(self):
                
                error_list = super(ProblemTab.ConstantsFrame.PermutationConstantFrame, self).check_errors()
                
                string = self.permutation_textbox.get("1.0", tk.END)
                string = string.rstrip("\n")
                string = remove_whitespaces(string)
                string = string.rstrip("\t")
                self.elements = string.split(",")
                
                if len(self.elements)<2:
                    error_list.append("At least two elements are needed")
                    
                elif not all( is_integer(e) for e in self.elements ):
                    error_list.append("Non-integer values in permutation")
                    
                return error_list
                
            
            def generate_constant(self):
                
                self.clear_errors()
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    elements_int = [ to_integer(e) for e in self.elements ]
                    variable = constant_types.PermutationConstant(keyword=self.name_entry.get(), value=elements_int)
                    
                    self.clear_entries()
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding constant", message="The following errors where found:\n\n" + "\n".join( ["-" + s for s in error_list] ))
                    return None
                
            
        class StringConstantFrame(ConstantsParametersFrame):
    
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.ConstantsFrame.StringConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
                self.string_label = tk.Label( master=self, text="Insert string:")
                self.string_label.place( relx=0.1, rely=0.3 )
                self.string_textbox = tk.Text( master=self )
                self.string_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
            
            def clear_entries(self):
                super(ProblemTab.ConstantsFrame.StringConstantFrame, self).clear_entries()
                
                self.string_textbox.delete('1.0', tk.END)
            
            def generate_constant(self):
                
                self.clear_errors()
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    
                    variable = constant_types.StringConstant(keyword=self.name_entry.get(), value=self.string_textbox.get("1.0", tk.END))
                    
                    self.clear_entries()
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding constant", message="The following errors where found:\n\n" + "\n".join(["-" + s for s in error_list]))
                    return None
        
        
        def add_constant(self):
            constant = self.selected_constant_frame.generate_constant()
            
            if constant != None:
                
                const_name = constant.keyword
                const_type = self.type_dict[type(constant)]
                    
                const_value = str(constant.value)
            
                self.problem_parameters.constants.append( constant )
                self.constants_tree.insert('', 'end', text=const_name, values=(const_type, const_value))
        
        def delete_constant(self):
            
            for iid in self.constants_tree.selection():
                const_name = self.constants_tree.item(iid)['text']
                self.constants_tree.delete( iid )
                
                self.problem_parameters.constants = [ x for x in self.problem_parameters.constants if x.keyword!=const_name ]
                
        
        def clearall_constants(self):
            
            const_names = []
            
            for iid in self.constants_tree.get_children():
                const_names.append( self.constants_tree.item(iid)['text'] )
                self.constants_tree.delete( iid )
                
            self.problem_parameters.constants = [ x for x in self.problem_parameters.constants if x.keyword not in const_names ]
        
        def update_type(self, new_value):
            self.selected_constant_frame.clear_errors()
            self.selected_constant_frame.clear_entries()
            self.selected_constant_frame.hide()
            self.selected_constant_frame = self.constant_frames[new_value]
            self.selected_constant_frame.show()
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstantsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            labelframe_list = tk.LabelFrame(master=self, text="Constants List")
            labelframe_list.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.65)
            
            self.variable_headers = ["Type", "Value"]
            self.constants_tree = ttk.Treeview(master=labelframe_list, columns=self.variable_headers, selectmode="extended")
            
            self.constants_tree.heading("#0", text="Name")
            self.constants_tree.column("#0", minwidth=100, width=200, stretch=tk.NO)
            
            self.constants_tree.heading( "Type", text="Type" )
            self.constants_tree.column( "Type", minwidth=100, width=200, stretch=tk.NO )
            
            self.constants_tree.heading( "Value", text="Value" )
            self.constants_tree.column( "Value", minwidth=100, width=200, stretch=tk.NO )
            
            self.constants_tree.place(relx=0.02, rely=0.17, relwidth=0.955, relheight=0.8)
        
            
        
            delete = ttk.Button(labelframe_list, text="Delete", command=self.delete_constant)
            delete.place(relx=0.805, rely=0.025, relwidth=0.17, relheight=0.1 )         
        
            clearall = ttk.Button(labelframe_list, text="Clear All", command=self.clearall_constants)
            clearall.place(relx=0.62, rely=0.025, relwidth=0.17, relheight=0.1 ) 
        
            labelframe_add = tk.LabelFrame(master=self, text="Add Constants")
            labelframe_add.place(relx=0.69, rely=0.05, relheight=0.9, relwidth=0.29)
        
            tk.Label(labelframe_add, text = "Type").place(relx=0.1325,rely=0.05)
            optionList_Type = ["Real", "Integer", "Binary", "Permutation", "String"]
            optionType = tk.StringVar(labelframe_add)
            optionType.set("Real")
            option_type = tk.OptionMenu(labelframe_add, optionType, *optionList_Type, command=self.update_type)
            option_type.config(width=5)
            option_type.place(relx=0.28,rely=0.04, relwidth=0.45)
        
            self.add_button = ttk.Button(labelframe_add, text="Add", command=self.add_constant)
            self.add_button.place(relx=0.325, rely=0.86, relwidth=0.35, relheight=0.1)
            
            self.type_dict = { constant_types.FloatConstant:"Real",
                          constant_types.IntegerConstant:"Integer",
                          constant_types.BinaryConstant:"Binary",
                          constant_types.PermutationConstant:"Permutation",
                          constant_types.StringConstant:"String" }
            
            self.constant_frames = {}
            self.constant_frames["Real"] = ProblemTab.ConstantsFrame.FloatConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.constant_frames["Integer"] = ProblemTab.ConstantsFrame.IntegerConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.constant_frames["Binary"] = ProblemTab.ConstantsFrame.BinaryConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.constant_frames["Permutation"] = ProblemTab.ConstantsFrame.PermutationConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            self.constant_frames["String"] = ProblemTab.ConstantsFrame.StringConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
            
            self.constant_frames["Real"].show()
            self.selected_constant_frame = self.constant_frames["Real"]
            
            self.add_button.lift()
            
            
    class ConstraintsFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstraintsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Constraints").place( relx=0.5, rely=0.5 )
            
        
    
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            # print(data)
            self.selected_frame.hide()
            self.selected_frame = self.frames[data]
            self.selected_frame.display()
        
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ProblemTab, self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        
        templates_optionlist = [ option.value for option in ProblemParameters.PROBLEM_TEMPLATES ]
        
        tk.Label( self, text="Template", font=('URW Gothic L','11','bold') ).place( relx=0.01, rely=0.048 )
        self.TemplateOption = tk.StringVar(self)
        self.TemplateOption.set(templates_optionlist[0])
        template_option = tk.OptionMenu(self, self.TemplateOption, *templates_optionlist)
        template_option.config( font=('URW Gothic L','11') )
        template_option.config( state=tk.DISABLED )
        template_option.place( relx=0.065, rely=0.045, relwidth=0.105 )
        
        self.frames = {}
        self.frames["Evaluator"] = ProblemTab.EvaluatorFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Variables"] = ProblemTab.VariablesFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constants"] = ProblemTab.ConstantsFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constraints"] = ProblemTab.ConstraintsFrame( master=self, problem_parameters=self.problem_parameters )
        
        self.generic_problem_items = [ "Evaluator", "Variables", "Constants", "Constraints" ]
        self.matlab_problem_items = [ "Script", "Variables", "Constants", "Constraints" ]
        self.CST_problem_items = [ "CST", "Variables", "Constants", "Constraints" ]
        
        self.selected_problem_items = self.generic_problem_items
        
        self.selected_frame = self.frames["Evaluator"]
        self.selected_frame.display()
        
        self.parameters_listbox = tk.Listbox( master=self)
        self.parameters_listbox.config( font=('URW Gothic L','11','bold') )
        self.parameters_listbox.insert(0, "Evaluator")
        self.parameters_listbox.insert(tk.END, "Variables")
        self.parameters_listbox.insert(tk.END, "Constants")
        self.parameters_listbox.insert(tk.END, "Constraints")
        
        self.parameters_listbox.place( relx=0.01, rely=0.115, relwidth=0.16, relheight=0.86 )
        self.parameters_listbox.bind( '<<ListboxSelect>>', self.__listbox_selection_handler__ )
        self.parameters_listbox.activate(0)
        
        self.parameters_frame = tk.Frame(master=self)
        self.parameters_frame.place()
        
        self.console = Console(master=self, font=("Times New Roman", 10, 'bold'))
        self.console.place( relx=0.18, rely=0.775, relwidth=0.81, relheight=0.2 )
        self.console.print_message("Mensaje\n")
        self.console.print_warning("Advertencia\n")
        self.console.print_error("Error\n")
        
        
    def check_errors(self):
        
        error_list = []
        
        for key in self.selected_problem_items:
            #TODO: check if specified evaluator class name is correct
            error_list.extend( self.frames[key].check_errors() )
        
        return error_list
    
    def console_print_error(self, string: str):
        self.console.print_error( string+"\n" )
        
    def console_print_warning(self, string: str):
        self.console.print_warning( string+"\n" )
        
    def console_print_message(self, string: str):
        self.console.print_message( string+"\n" )
        
    def console_clear(self):
        self.console.clear_all()
        
        
        