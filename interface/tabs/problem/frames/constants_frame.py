# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.problem.frames.problem_frame import *


class ConstantsFrame(ProblemFrame):
        
    class ConstantsParametersFrame(tk.Frame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ConstantsFrame.ConstantsParametersFrame, self).__init__(master=master, *args, **kwargs)
            
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
            super(ConstantsFrame.NumericConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
                
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
            super(ConstantsFrame.NumericConstantFrame, self).clear_errors()
            
            self._reset_entry_(self.value_entry)
            
        def clear_entries(self):
            super(ConstantsFrame.NumericConstantFrame, self).clear_entries()
            
            self.value_entry.delete(0, 'end')  
          
        def check_errors(self):
            
            error_list = super(ConstantsFrame.NumericConstantFrame, self).check_errors()
            
            if not self.is_type(self.value_entry.get()):
                error_list.append("Value of unsuitable type")
                self._invalidate_entry_(self.value_entry)
                
            return error_list
            
    class FloatConstantFrame(NumericConstantFrame):
    
        def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
            super(ConstantsFrame.FloatConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
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
            super(ConstantsFrame.IntegerConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
    
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
            super(ConstantsFrame.BinaryConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
    
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
            super(ConstantsFrame.PermutationConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
            
            self.permutation_label = tk.Label( master=self, text="Insert elements (comma separated):")
            self.permutation_label.place( relx=0.1, rely=0.3 )
            self.permutation_textbox = tk.Text( master=self )
            self.permutation_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
        
        def clear_entries(self):
            super(ConstantsFrame.PermutationConstantFrame, self).clear_entries()
            
            self.permutation_textbox.delete('1.0', tk.END)
        
        def check_errors(self):
            
            error_list = super(ConstantsFrame.PermutationConstantFrame, self).check_errors()
            
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
            super(ConstantsFrame.StringConstantFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
    
            self.string_label = tk.Label( master=self, text="Insert string:")
            self.string_label.place( relx=0.1, rely=0.3 )
            self.string_textbox = tk.Text( master=self )
            self.string_textbox.place( relx=0.1, rely=0.35, relwidth=0.8, relheight=0.55 )
        
        def clear_entries(self):
            super(ConstantsFrame.StringConstantFrame, self).clear_entries()
            
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
    
    def load_constants(self):
        
        self.clearall_constants()
        
        for constant in self.problem_parameters.constants:
            
            const_name = constant.keyword
            const_type = self.type_dict[type(constant)]
                
            const_value = str(constant.value)
        
            self.constants_tree.insert('', 'end', text=const_name, values=(const_type, const_value))
            
    def load_parameters(self):
        
        super(ConstantsFrame, self).load_parameters()
        
        self.load_constants()
    
    def update_type(self, new_value):
        self.selected_constant_frame.clear_errors()
        self.selected_constant_frame.clear_entries()
        self.selected_constant_frame.hide()
        self.selected_constant_frame = self.constant_frames[new_value]
        self.selected_constant_frame.show()
    
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ConstantsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
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
        self.constant_frames["Real"] = ConstantsFrame.FloatConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.constant_frames["Integer"] = ConstantsFrame.IntegerConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.constant_frames["Binary"] = ConstantsFrame.BinaryConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.constant_frames["Permutation"] = ConstantsFrame.PermutationConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        self.constant_frames["String"] = ConstantsFrame.StringConstantFrame(master=labelframe_add, problem_parameters=self.problem_parameters)
        
        self.constant_frames["Real"].show()
        self.selected_constant_frame = self.constant_frames["Real"]
        
        self.add_button.lift()