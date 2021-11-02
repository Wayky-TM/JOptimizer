# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class CrossoverFrame(AlgorithmFrame):
        
    class FloatCrossoverFrame(ParameterLabelFrame):
        
        class SBXFrame(ParameterLabelFrame):
            
            def __update_probability__(self, var):
                self.probability_entry.configure( state=tk.NORMAL )
                ClearInsertEntry(self.probability_entry, str(var))
                
                if self.algorithm_parameters.float_crossover_choice != AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
                    self.probability_entry.configure( state=tk.DISABLED )
            
            def __update_distribution_index__(self, var):
                self.distribution_index_entry.configure( state=tk.NORMAL )
                ClearInsertEntry(self.distribution_index_entry, str(var))
                
                if self.algorithm_parameters.float_crossover_choice != AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
                    self.distribution_index_entry.configure( state=tk.DISABLED )
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(CrossoverFrame.FloatCrossoverFrame.SBXFrame,self).__init__(master=master, *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.probability_label = tk.Label( self, text="Probability" ).place( relx=0.01, rely=0.048 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["probability"])
                self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
                self.probability_entry.config(state=tk.NORMAL)
                
                self.distribution_index_label = tk.Label( self, text="Distribution index" ).place( relx=0.01, rely=0.448 )
                self.distribution_index_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.distribution_index_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["distribution_index"])
                self.distribution_index_entry.place(relx=0.23, rely=0.45+0.005, relwidth=0.08)
                self.distribution_index_entry.config(state=tk.NORMAL)
                
                self.probability_parameter = Float(name="probability", fancy_name="Probability (float crossover)", lower_bound=0.0, upper_bound=1.0)
                self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (float crossover)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
        
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["probability"],
                                                                  widget_update_lambda=lambda var: self.__update_probability__(var) ) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                                  widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"distribution_index":var}),
                                                                  error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                                  error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["distribution_index"],
                                                                  widget_update_lambda=lambda var: self.__update_distribution_index__(var) ) )
            
            def display(self):
                self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
                
            def disable(self):
                self.probability_entry.config(state=tk.DISABLED)
                self.distribution_index_entry.config(state=tk.DISABLED)
            
            def enable(self):
                self.probability_entry.config(state=tk.NORMAL)
                self.distribution_index_entry.config(state=tk.NORMAL)
        
        class DiffEvolFrame(ParameterLabelFrame):
            
            def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
                super(CrossoverFrame.FloatCrossoverFrame.DiffEvolFrame,self).__init__(master=master, *args, **kwargs)
                
                self.problem_parameters = problem_parameters
                self.algorithm_parameters = algorithm_parameters
                
                self.probability_label = tk.Label( self, text="Probability" ).place( relx=0.01, rely=0.048 )
                self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.probability_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["probability"])
                self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
                self.probability_entry.config(state=tk.NORMAL)
                
                self.F_label = tk.Label( self, text="F" ).place( relx=0.01, rely=0.348 )
                self.F_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.F_entry.place(relx=0.13, rely=0.35+0.005, relwidth=0.08)
                self.F_entry.config(state=tk.NORMAL)
                
                self.K_label = tk.Label( self, text="K" ).place( relx=0.01, rely=0.648 )
                self.K_entry = tk.Entry(master=self, state=tk.NORMAL)
                self.K_entry.place(relx=0.13, rely=0.65+0.005, relwidth=0.08)
                self.K_entry.config(state=tk.NORMAL)
                
                self.probability_parameter = Float(name="probability", fancy_name="Probability (float crossover)", lower_bound=0.0, upper_bound=1.0)
                self.F_parameter = Float(name="F", fancy_name="F", lower_bound=float("-Inf"), upper_bound=float("Inf"))
                self.K_parameter = Float(name="K", fancy_name="K", lower_bound=float("-Inf"), upper_bound=float("Inf"))
        
                self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                                  widget_read_lambda=lambda: self.probability_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"probability":var}),
                                                                  error_set_lambda=EntryInvalidator(self.probability_entry),
                                                                  error_reset_lambda=EntryValidator(self.probability_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["probability"],
                                                                  widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var))) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.F_parameter,
                                                                  widget_read_lambda=lambda: self.F_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"F":var}),
                                                                  error_set_lambda=EntryInvalidator(self.F_entry),
                                                                  error_reset_lambda=EntryValidator(self.F_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["F"],
                                                                  widget_update_lambda=lambda var: ClearInsertEntry(self.F_entry, str(var)) ) )
                
                self.parameters_bindings.append( ParameterBinding(parameter=self.K_parameter,
                                                                  widget_read_lambda=lambda: self.K_entry.get(),
                                                                  variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"K":var}),
                                                                  error_set_lambda=EntryInvalidator(self.K_entry),
                                                                  error_reset_lambda=EntryValidator(self.K_entry),
                                                                  variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["K"],
                                                                  widget_update_lambda=lambda var: ClearInsertEntry(self.K_entry, str(var)) ) )
                
            def display(self):
                self.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
            
            def disable(self):
                self.probability_entry.config(state=tk.DISABLED)
                self.F_entry.config(state=tk.DISABLED)
                self.K_entry.config(state=tk.DISABLED)
            
            def enable(self):
                self.probability_entry.config(state=tk.NORMAL)
                self.F_entry.config(state=tk.NORMAL)
                self.K_entry.config(state=tk.NORMAL)
           
        def __update_crossover_option__(self,var):
            self.CrossoverOption.set(var)
            self.option_change(var)
            
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(CrossoverFrame.FloatCrossoverFrame,self).__init__(master=master, text="Float crossover", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            self.crossover_options = [ option.value for option in AlgorithmParameters.FLOAT_CROSSOVER ]
            
            tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
            self.CrossoverOption = tk.StringVar(self)
            self.CrossoverOption.set( AlgorithmParameters.FLOAT_CROSSOVER.SBX.value )
            self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options, command=self.option_change)
            self.crossover_option.config( state=tk.NORMAL )
            self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
            
            self.frames = {}
            self.frames[AlgorithmParameters.FLOAT_CROSSOVER.SBX.value] = CrossoverFrame.FloatCrossoverFrame.SBXFrame(master=self,
                                                                                                                                  problem_parameters=self.problem_parameters,
                                                                                                                                  algorithm_parameters=self.algorithm_parameters)
            
            self.frames[AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION.value] = CrossoverFrame.FloatCrossoverFrame.DiffEvolFrame(master=self,
                                                                                                                                       problem_parameters=self.problem_parameters,
                                                                                                                                       algorithm_parameters=self.algorithm_parameters)
            
            self.selected_frame_key = AlgorithmParameters.FLOAT_CROSSOVER.SBX.value
            self.frames[self.selected_frame_key].display()
            
            self.crossover_option_parameter = Parameter( name="float_crossover_option", fancy_name="Float crossover option" )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                              widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                              variable_store_lambda=self.__store_float_crossover_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_choice,
                                                              widget_update_lambda=lambda var: self.__update_crossover_option__(var) ) )
            
        def __store_float_crossover_option(self, value):
            self.algorithm_parameters.float_crossover_choice = value
            
        def option_change(self, new_value):
            
            if new_value != self.selected_frame_key:
                self.frames[self.selected_frame_key].hide()
                self.selected_frame_key = new_value
                self.frames[self.selected_frame_key].display()
            
        def check_errors(self):
            error_list = super(CrossoverFrame.FloatCrossoverFrame,self).check_errors()
            error_list.extend( self.frames[self.selected_frame_key].check_errors() )
            
            return error_list
        
        def save_parameters(self):
            super(CrossoverFrame.FloatCrossoverFrame, self).save_parameters()
            self.frames[self.selected_frame_key].save_parameters()
            
        def load_parameters(self):
            super(CrossoverFrame.FloatCrossoverFrame, self).load_parameters()
            self.frames[self.selected_frame_key].load_parameters()
            
        def disable(self):
            self.configure(text="Float crossover (Disabled)")
            self.crossover_option.config(state=tk.DISABLED)
            self.frames[self.selected_frame_key].disable()
            
        def enable(self):
            self.configure(text="Float crossover")
            self.crossover_option.config(state=tk.NORMAL)
            self.frames[self.selected_frame_key].enable()
        
        
    class IntCrossoverFrame(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(CrossoverFrame.IntCrossoverFrame,self).__init__(master=master, text="Integer crossover", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            self.crossover_options = [AlgorithmParameters.INT_CROSSOVER.INT_SBX.value]
            
            tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
            self.CrossoverOption = tk.StringVar(self)
            self.CrossoverOption.set( AlgorithmParameters.INT_CROSSOVER.INT_SBX.value )
            self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
            self.crossover_option.config( state=tk.DISABLED )
            self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
            
            self.labelframe_params = tk.LabelFrame(master=self)
            
            tk.Label( master=self.labelframe_params, text="Probability" ).place( relx=0.01, rely=0.05 )
            self.probability_entry = tk.Entry(master=self.labelframe_params, state=tk.NORMAL)
            self.probability_entry.place(relx=0.155, rely=0.05+0.005, relwidth=0.08)
            self.probability_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["probability"])
            self.probability_entry.config(state=tk.NORMAL)
            
            self.distribution_index_label = tk.Label( self.labelframe_params, text="Distribution index" ).place( relx=0.01, rely=0.448 )
            self.distribution_index_entry = tk.Entry(master=self.labelframe_params, state=tk.NORMAL)
            self.distribution_index_entry.place(relx=0.23, rely=0.45+0.005, relwidth=0.08)
            self.distribution_index_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["distribution_index"])
            self.distribution_index_entry.config(state=tk.NORMAL)
            
            self.labelframe_params.place( relx=0.02, rely=0.28, relwidth=0.96, relheight=0.67 )
            
            self.crossover_option_parameter = Parameter( name="int_crossover_option", fancy_name="Integer crossover option" )
            self.probability_parameter = Float(name="probability", fancy_name="Probability (int crossover)", lower_bound=0.0, upper_bound=1.0)
            self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (int crossover)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
        
            self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                              widget_read_lambda=lambda: self.probability_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.int_crossover_parameters.update({"probability":var}),
                                                              error_set_lambda=EntryInvalidator(self.probability_entry),
                                                              error_reset_lambda=EntryValidator(self.probability_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_parameters["probability"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                              widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.int_crossover_parameters.update({"distribution_index":var}),
                                                              error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                              error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_parameters["distribution_index"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.distribution_index_entry, str(var)) ) )
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                              widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                              variable_store_lambda=self.__store_int_crossover_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.int_crossover_choice,
                                                              widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
            
        def __store_int_crossover_option(self, value):
            self.algorithm_parameters.int_crossover_choice = value
            
        def disable(self):
            self.configure(text="Integer crossover (Disabled)")
            self.crossover_option.config(state=tk.DISABLED)
            self.probability_entry.config(state=tk.DISABLED)
            self.distribution_index_entry.config(state=tk.DISABLED)
            
        def enable(self):
            self.configure(text="Integer crossover")
            self.crossover_option.config(state=tk.NORMAL)
            self.probability_entry.config(state=tk.NORMAL)
            self.distribution_index_entry.config(state=tk.NORMAL)
            
    class BinaryCrossoverFrame(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(CrossoverFrame.BinaryCrossoverFrame,self).__init__(master=master, text="Binary crossover", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            self.crossover_options = [AlgorithmParameters.BINARY_CROSSOVER.SPX.value]
            
            tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.3 )
            self.CrossoverOption = tk.StringVar(self)
            self.CrossoverOption.set( self.crossover_options[0] )
            self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
            self.crossover_option.config( state=tk.DISABLED )
            self.crossover_option.place( relx=0.15, rely=0.0425, relwidth=0.3 )
            
            tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
            self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
            self.probability_entry.insert(0, self.algorithm_parameters.binary_crossover_parameters["probability"])
            self.probability_entry.config(state=tk.NORMAL)
            
            
            self.crossover_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
            self.probability_parameter = Float(name="probability", fancy_name="Probability (binary crossover)", lower_bound=0.0, upper_bound=1.0)
        
            self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                              widget_read_lambda=lambda: self.probability_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.binary_crossover_parameters.update({"probability":var}),
                                                              error_set_lambda=EntryInvalidator(self.probability_entry),
                                                              error_reset_lambda=EntryValidator(self.probability_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.binary_crossover_parameters["distribution_index"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
            
                
            self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                              widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                              variable_store_lambda=self.__store_binary_crossover_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.binary_crossover_choice,
                                                              widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
            
        def __store_binary_crossover_option(self, value):
            self.algorithm_parameters.binary_crossover_choice = value
            
        def disable(self):
            self.configure(text="Binary crossover (Disabled)")
            self.crossover_option.config(state=tk.DISABLED)
            self.probability_entry.config(state=tk.DISABLED)
            
        def enable(self):
            self.configure(text="Binary crossover")
            self.crossover_option.config(state=tk.NORMAL)
            self.probability_entry.config(state=tk.NORMAL)
    
            
    class PermutationCrossoverFrame(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(CrossoverFrame.PermutationCrossoverFrame,self).__init__(master=master, text="Permutation crossover", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            self.crossover_options = [AlgorithmParameters.PERMUTATION_CROSSOVER.CXC.value, AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value]
            
            tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.35 )
            self.CrossoverOption = tk.StringVar(self)
            self.CrossoverOption.set( AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value )
            self.crossover_option = tk.OptionMenu(self, self.CrossoverOption, *self.crossover_options)
            self.crossover_option.config( state=tk.NORMAL )
            self.crossover_option.place( relx=0.15, rely=0.17, relwidth=0.3 )
            
            tk.Label( master=self, text="Probability" ).place( relx=0.5, rely=0.3 )
            self.probability_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.probability_entry.place(relx=0.65, rely=0.3, relwidth=0.08)
            self.probability_entry.insert(0, self.algorithm_parameters.permutation_crossover_parameters["probability"])
            self.probability_entry.config(state=tk.NORMAL)
            
            self.crossover_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
            self.probability_parameter = Float(name="probability", fancy_name="Probability (permutation crossover)", lower_bound=0.0, upper_bound=1.0)
        
            self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                              widget_read_lambda=lambda: self.probability_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.permutation_crossover_parameters.update({"probability":var}),
                                                              error_set_lambda=EntryInvalidator(self.probability_entry),
                                                              error_reset_lambda=EntryValidator(self.probability_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.permutation_crossover_parameters["probability"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var))) )
            
                
            self.parameters_bindings.append( ParameterBinding(parameter=self.crossover_option_parameter,
                                                              widget_read_lambda=lambda: self.CrossoverOption.get(),
                                                              variable_store_lambda=self.__store_permutation_crossover_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.permutation_crossover_choice,
                                                              widget_update_lambda=lambda var: self.CrossoverOption.set(var)) )
            
        def __store_permutation_crossover_option(self, value):
            self.algorithm_parameters.permutation_crossover_choice = value
            
        def disable(self):
            self.configure(text="Permutation crossover (Disabled)")
            self.crossover_option.config(state=tk.DISABLED)
            self.probability_entry.config(state=tk.DISABLED)
            
        def enable(self):
            self.configure(text="Permutation crossover")
            self.crossover_option.config(state=tk.NORMAL)
            self.probability_entry.config(state=tk.NORMAL)
        
    def check_errors(self):
        error_list = super(CrossoverFrame,self).check_errors()
        
        used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
        
        if variable_types.FloatVariable in used_variable_types:
            error_list.extend( self.float_frame.check_errors() )
        
        if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
            error_list.extend( self.int_frame.check_errors() )
        
        if variable_types.BinaryVariable in used_variable_types:
            error_list.extend( self.binary_frame.check_errors() )
        
        if variable_types.PermutationVariable in used_variable_types:
            error_list.extend( self.permutation_frame.check_errors() )
        
        return error_list
    
    
    def save_parameters(self):
        
        used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
        
        if variable_types.FloatVariable in used_variable_types:
            self.float_frame.save_parameters()
        
        if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
            self.int_frame.save_parameters()
        
        if variable_types.BinaryVariable in used_variable_types:
            self.binary_frame.save_parameters()
        
        if variable_types.PermutationVariable in used_variable_types:
            self.permutation_frame.save_parameters()
            
    def load_parameters(self):
        
        used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
        
        self.float_frame.load_parameters()
        self.int_frame.load_parameters()
        self.binary_frame.load_parameters()
        self.permutation_frame.load_parameters()
        
        # if variable_types.FloatVariable in used_variable_types:
        #     self.float_frame.load_parameters()
        
        # if variable_types.IntegerVariable in used_variable_types or variable_types.DiscretizedFloatVariable in used_variable_types:
        #     self.int_frame.load_parameters()
        
        # if variable_types.BinaryVariable in used_variable_types:
        #     self.binary_frame.load_parameters()
        
        # if variable_types.PermutationVariable in used_variable_types:
        #     self.permutation_frame.load_parameters()
            
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(CrossoverFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.float_frame = CrossoverFrame.FloatCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.int_frame = CrossoverFrame.IntCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.binary_frame = CrossoverFrame.BinaryCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.permutation_frame = CrossoverFrame.PermutationCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        
        self.float_frame.place( relx=0.025, rely=0.05, relwidth=0.4, relheight=0.3 )
        self.int_frame.place( relx=0.025, rely=0.38, relwidth=0.4, relheight=0.3 )
        self.binary_frame.place( relx=0.025, rely=0.71, relwidth=0.4, relheight=0.11 )
        self.permutation_frame.place( relx=0.025, rely=0.85, relwidth=0.4, relheight=0.11 )
        
        self.float_frame.disable()
        self.int_frame.disable()
        self.binary_frame.disable()
        self.permutation_frame.disable()
