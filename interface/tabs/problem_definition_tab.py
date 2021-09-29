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
from core.algorithm_parameters import AlgorithmParameters
from core.problem_parameters import ProblemParameters
from util.type_check import is_integer, is_float

from interface.parameter import *
from interface.console import Console
from interface.parameter_binding import ParameterBinding



class ProblemTab(ttk.Frame):
    
    class ProblemFrame(tk.LabelFrame):
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ProblemFrame, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.parameters_bindings = []
            
        def error_check(self, error_list: List[str]):
            
            for binding in self.parameters_bindings:
                binding.error_check(error_list)
                
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
            self.OperatorFilePath.place(relx=0.11, rely=0.05+0.005, relwidth=0.3)
            self.OperatorFilePath.config(state=tk.DISABLED)
            self.button_browse_operator = tk.Button( master=self,  text="Browse", command=lambda: self._browse() ).place(relx=0.43, rely=0.05, relwidth=0.06)
            
            evaluator_path_parameter = FilePath( fancy_name="Evaluator script path" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=evaluator_path_parameter,
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
        
        class VariableParametersFrame(tk.Frame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.VariablesFrame.VariableParametersFrame, self).__init__(master=master, *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                
                self.name_label = tk.Label( master=self, text="Name" )
                self.name_label.place( relx=0.1, rely=0.1 )
                self.name_entry = tk.Entry( master=self )
                self.name_entry.place( relx=0.3, rely=0.1, relwidth=0.5 )
                
            def check_name(self, error_list: List[str]):
                
                if not self.name_entry.get():
                    error_list.append("Empty variable name")
                
                elif self.name_entry.get() in { var.keyword for var in self.problem_parameters.variables }:
                    error_list.append("A variable with name '%s' was already defined" % self.name_entry.get())
            
            
            def _invalidate_entry_(self, entry):
                entry.config({"background":"Red"})
                
                
            def _reset_entry_(self, entry):
                entry.config({"background":"White"})
                
                
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
                
            
            
            def check_errors(self) -> bool:
                
                error_list = []
                
                self.check_name(error_list)
                
                if len(error_list)>0:
                    self._invalidate_entry_(self.lower_bound_entry)
                
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
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    self._reset_entry_(self.name_entry)
                    self._reset_entry_(self.lower_bound_entry)
                    self._reset_entry_(self.upper_bound_entry)
                    
                    variable = variable_types.FloatVariable(keyword=self.name_entry.get(), lower_bound=float(self.lower_bound_entry.get()), upper_bound=float(self.upper_bound_entry.get()))
                    
                    self.name_entry.delete(0, 'end')
                    self.lower_bound_entry.delete(0, 'end')
                    self.upper_bound_entry.delete(0, 'end')
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(error_list))
                    return None
                
        class IntegerParametersFrame(NumericParametersFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.VariablesFrame.IntegerParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            def is_type(self, string: str):
                return is_integer(string)
            
            def cast_type(self, value: str):
                return int(value)
            
            def generate_variable(self):
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    self._reset_entry_(self.name_entry)
                    self._reset_entry_(self.lower_bound_entry)
                    self._reset_entry_(self.upper_bound_entry)
                    
                    variable = variable_types.IntegerVariable(keyword=self.name_entry.get(), lower_bound=int(self.lower_bound_entry.get()), upper_bound=int(self.upper_bound_entry.get()))
                    
                    self.name_entry.delete(0, 'end')
                    self.lower_bound_entry.delete(0, 'end')
                    self.upper_bound_entry.delete(0, 'end')
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(error_list))
                    return None
                
                
                
        class DiscretizedParametersFrame(NumericParametersFrame):
            
            def _radiobutton_command_(self, value):
            
                if value=="step":
                    self.step_entry.config(state=tk.NORMAL)
                    self.points_entry.delete(0, tk.END)
                    self.points_entry.config(state=tk.DISABLED)
                    
                elif value=="points":
                    self.points_entry.config(state=tk.NORMAL)
                    self.step_entry.delete(0, tk.END)
                    self.step_entry.config(state=tk.DISABLED)
            
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
            
            
            def check_errors(self) -> bool:
                
                error_list = super(ProblemTab.VariablesFrame.DiscretizedParametersFrame, self).check_errors()
                
                if self.ps.get() == "none":
                    error_list.append( "No discretization criteria selected" )
                    
                elif self.ps.get() == "step" and (not is_float(self.step_entry.get()) or float(self.step_entry.get())<= 0.0):
                    error_list.append( "Invalid step value" )
                    self._invalidate_entry_(self.step_entry)
                    
                elif self.ps.get() == "points" and (not is_integer(self.points_entry.get()) or int(self.points_entry.get()) < 1):
                    error_list.append( "Invalid number of points" )
                    self._invalidate_entry_(self.step_entry)
                    
                return error_list
            
            
            def generate_variable(self):
                
                error_list = self.check_errors()
                
                if len(error_list)==0:
                    self._reset_entry_(self.name_entry)
                    self._reset_entry_(self.lower_bound_entry)
                    self._reset_entry_(self.upper_bound_entry)
                    self._reset_entry_(self.step_entry)
                    self._reset_entry_(self.points_entry)
                    
                    if self.ps.get() == "step":
                        step = float(self.step_entry.get())
                        
                    elif self.ps.get() == "points":
                        step = (float(self.upper_bound_entry.get()) - float(self.lower_bound_entry.get()))/float(self.points_entry.get())
                    
                    variable = variable_types.DiscretizedFloatVariable(keyword=self.name_entry.get(), lower_bound=float(self.lower_bound_entry.get()), upper_bound=float(self.upper_bound_entry.get()), step=step)
                    
                    self.name_entry.delete(0, 'end')
                    self.lower_bound_entry.delete(0, 'end')
                    self.upper_bound_entry.delete(0, 'end')
                    self.step_entry.delete(0, 'end')
                    self.points_entry.delete(0, 'end')
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(error_list))
                    return None
                
        class BinaryParametersFrame(VariableParametersFrame):
            
            def generate_variable(self):
                
                error_list = []
                
                self.check_name(error_list)
                
                if len(error_list)==0:
                    self._reset_entry_(self.name_entry)
                    
                    variable = variable_types.BinaryVariable(keyword=self.name_entry.get())
                    
                    self.name_entry.delete(0, 'end')
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(error_list))
                    return None
                
        class PermutationParametersFrame(VariableParametersFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
                super(ProblemTab.VariablesFrame.PermutationParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
                self.permutation_label = tk.Label( master=self, text="Insert elements (comma separated):")
                self.permutation_label.place( relx=0.1, rely=0.3 )
                self.permutation_textbox = tk.Text( master=self )
                self.permutation_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
            
            def generate_variable(self):
                
                error_list = []
                
                self.check_name(error_list)
                
                string = self.permutation_textbox.get("1.0", tk.END)
                string = string.rstrip("\n")
                string = string.rstrip(" ")
                string = string.rstrip("\t")
                elements = string.split(",")
                
                if all( is_integer(e) for e in elements ) and len(elements)>1:
                    elements_int = [ int(e) for e in elements ]
                    
                else:
                    error_list.append("Non-integer values in permutation")
                    
                
                if len(error_list)==0:
                    self._reset_entry_(self.name_entry)
                    
                    self.name_entry.delete(0, 'end')
                    
                    variable = variable_types.PermutationVariable(keyword=self.name_entry.get(), elements=elements_int)
                    
                    self.permutation_textbox.delete('1.0', END)
                    
                    return variable
                
                else:
                    tk.messagebox.showerror(title="Error adding variable", message="The following errors where found:\n\n" + "\n".join(error_list))
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
            pass
        
        def clearall_variable(self):
            pass
        
        def show_variables(self):
            pass
        
        def updateType(self, new_value):
            self.selected_variable_frame.hide()
            self.selected_variable_frame = self.variable_frames[new_value]
            self.selected_variable_frame.show()
        
        def radiobutton_StepPoints(self, value):
            pass
        
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
        
            labelframe_add = tk.LabelFrame(master=self, text="Add Design Variables")
            labelframe_add.place(relx=0.69, rely=0.05, relheight=0.9, relwidth=0.29)
        
            tk.Label(labelframe_add, text = "Type").place(relx=0.05,rely=0.05)
            optionList_Type = ["Real", "Integer", "Discretized real", "Binary", "Permutation"]
            optionType = tk.StringVar(labelframe_add)
            optionType.set("Real")
            option_type = tk.OptionMenu(labelframe_add, optionType, *optionList_Type, command=self.updateType)
            option_type.config(width=5)
            option_type.place(relx=0.18,rely=0.04, relwidth=0.3)
        
            # label_bounds_IntFloat = tk.Label(labelframe_add, text = "If not specified, bounds will be taken as \u00B1\u221E")
            # label_bounds_Binary = tk.Label(labelframe_add, text = "As a binary type, variable will be 0 or 1")
        
            add = ttk.Button(labelframe_add, text="Add", command=self.add_variable)
            add.place(relx=0.275, rely=0.9, relwidth=0.35)
            
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
            
            
    class ConstantsFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstantsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Constants").place( relx=0.5, rely=0.5 )
            
            
    class ConstraintsFrame(ProblemFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ProblemTab.ConstraintsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="#Constraints").place( relx=0.5, rely=0.5 )
            
        
    
    def __listbox_selection_handler__(self, event):
        
        selection = event.widget.curselection()
        
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            print(data)
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
        template_option.place( relx=0.055, rely=0.045, relwidth=0.115 )
        
        self.frames = {}
        self.frames["Evaluator"] = ProblemTab.EvaluatorFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Variables"] = ProblemTab.VariablesFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constants"] = ProblemTab.ConstantsFrame( master=self, problem_parameters=self.problem_parameters )
        self.frames["Constraints"] = ProblemTab.ConstraintsFrame( master=self, problem_parameters=self.problem_parameters )
        
        self.selected_frame = self.frames["Evaluator"]
        self.selected_frame.display()
        
        self.generic_problem_items = [ "Evaluator", "Variables", "Constants", "Contraints" ]
        self.matlab_problem_items = [ "Script", "Variables", "Constants", "Contraints" ]
        self.CST_problem_items = [ "CST", "Variables", "Constants", "Contraints" ]
        
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
        
        # self.prueba = ProblemTab.ProblemFrame(master=self, problem_parameters=self.problem_parameters)
        # self.prueba.display()
        
    def check_errors(self):
        pass
        
        