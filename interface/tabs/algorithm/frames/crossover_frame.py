# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *

class FloatCrossoverGenericFrame(ParameterLabelFrame):
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(FloatCrossoverGenericFrame,self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.probability_frame = ttk.Frame(self)
        self.probability_label = tk.Label( self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["probability"])
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.probability_parameter = Float(name="probability", fancy_name="Probability (float crossover)", lower_bound=0.0, upper_bound=1.0)

        self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                          widget_read_lambda=lambda: self.probability_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.float_crossover_parameters.update({"probability":var}),
                                                          error_set_lambda=EntryInvalidator(self.probability_entry),
                                                          error_reset_lambda=EntryValidator(self.probability_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.float_crossover_parameters["probability"],
                                                          widget_update_lambda=lambda var: self.__update_probability__(var) ) )
    
    def __update_probability__(self, var):
        self.probability_entry.configure( state=tk.NORMAL )
        ClearInsertEntry(self.probability_entry, str(var))
        
        if self.algorithm_parameters.float_crossover_choice != AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
            self.probability_entry.configure( state=tk.DISABLED )
    
    def display(self):
        self.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
    def hide(self):
        self.grid_forget()
        
    def disable(self):
        self.probability_entry.config(state=tk.DISABLED)
    
    def enable(self):
        self.probability_entry.config(state=tk.NORMAL)


class FloatCrossoverFrame(ParameterLabelFrame):
        
    class SBXFrame(FloatCrossoverGenericFrame):
        
        def __update_distribution_index__(self, var):
            self.distribution_index_entry.configure( state=tk.NORMAL )
            ClearInsertEntry(self.distribution_index_entry, str(var))
            
            if self.algorithm_parameters.float_crossover_choice != AlgorithmParameters.FLOAT_CROSSOVER.SBX.value:
                self.distribution_index_entry.configure( state=tk.DISABLED )
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(FloatCrossoverFrame.SBXFrame,self).__init__(master=master,
                                                                             problem_parameters=problem_parameters,
                                                                             algorithm_parameters=algorithm_parameters,
                                                                             *args, **kwargs)
            
            self.distribution_index_frame = ttk.Frame(self)
            self.distribution_index_label = tk.Label( self.distribution_index_frame, text="Distribution index" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.distribution_index_entry = tk.Entry(master=self.distribution_index_frame, state=tk.NORMAL)
            self.distribution_index_entry.insert(0, self.algorithm_parameters.float_crossover_parameters["distribution_index"])
            self.distribution_index_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.distribution_index_entry.config(state=tk.NORMAL)
            self.distribution_index_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
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
            
        def disable(self):
            super(FloatCrossoverFrame.SBXFrame,self).disable()
            self.distribution_index_entry.config(state=tk.DISABLED)
        
        def enable(self):
            super(FloatCrossoverFrame.SBXFrame,self).enable()
            self.distribution_index_entry.config(state=tk.NORMAL)
    
    class DiffEvolFrame(FloatCrossoverGenericFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(FloatCrossoverFrame.DiffEvolFrame,self).__init__(master=master,
                                                                                  problem_parameters=problem_parameters,
                                                                                  algorithm_parameters=algorithm_parameters,
                                                                                  *args, **kwargs)
            
            self.F_frame = ttk.Frame(self)
            self.F_label = tk.Label( self.F_frame, text="F" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.F_entry = tk.Entry(master=self.F_frame, state=tk.NORMAL)
            self.F_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.F_entry.config(state=tk.NORMAL)
            self.F_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.K_frame = ttk.Frame(self)
            self.K_label = tk.Label( self.K_frame, text="K" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.K_entry = tk.Entry(master=self.K_frame, state=tk.NORMAL)
            self.K_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.K_entry.config(state=tk.NORMAL)
            self.K_frame.grid( row=2, column=0, sticky="NSEW", padx=3, pady=6 )
            
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
        
        
        def disable(self):
            super(CrossoverFrame.FloatCrossoverFrame.SBXFrame,self).disable()
            self.F_entry.config(state=tk.DISABLED)
            self.K_entry.config(state=tk.DISABLED)
        
        def enable(self):
            super(CrossoverFrame.FloatCrossoverFrame.SBXFrame,self).enable()
            self.F_entry.config(state=tk.NORMAL)
            self.K_entry.config(state=tk.NORMAL)
            
       
    def __update_crossover_option__(self,var):
        self.CrossoverOption.set(var)
        self.option_change(var)
        
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(FloatCrossoverFrame,self).__init__(master=master, text="Float crossover", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.crossover_options = [ option.value for option in AlgorithmParameters.FLOAT_CROSSOVER ]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.CrossoverOption = tk.StringVar(self)
        self.CrossoverOption.set( AlgorithmParameters.FLOAT_CROSSOVER.SBX.value )
        self.crossover_option = tk.OptionMenu(self.operator_frame, self.CrossoverOption, *self.crossover_options, command=self.option_change)
        self.crossover_option.config( state=tk.NORMAL )
        self.crossover_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.frames = {}
        self.frames[AlgorithmParameters.FLOAT_CROSSOVER.SBX.value] = FloatCrossoverFrame.SBXFrame(master=self,
                                                                                                                              problem_parameters=self.problem_parameters,
                                                                                                                              algorithm_parameters=self.algorithm_parameters)
        
        self.frames[AlgorithmParameters.FLOAT_CROSSOVER.DIFF_EVOLUTION.value] = FloatCrossoverFrame.DiffEvolFrame(master=self,
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
        error_list = super(FloatCrossoverFrame,self).check_errors()
        error_list.extend( self.frames[self.selected_frame_key].check_errors() )
        
        return error_list
    
    def save_parameters(self):
        super(FloatCrossoverFrame, self).save_parameters()
        self.frames[self.selected_frame_key].save_parameters()
        
    def load_parameters(self):
        super(FloatCrossoverFrame, self).load_parameters()
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
        super(IntCrossoverFrame,self).__init__(master=master, text="Integer crossover", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.crossover_options = [AlgorithmParameters.INT_CROSSOVER.INT_SBX.value]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.CrossoverOption = tk.StringVar(self)
        self.CrossoverOption.set( AlgorithmParameters.INT_CROSSOVER.INT_SBX.value )
        self.crossover_option = tk.OptionMenu(self.operator_frame, self.CrossoverOption, *self.crossover_options)
        self.crossover_option.config( state=tk.DISABLED )
        self.crossover_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.labelframe_params = tk.LabelFrame(master=self)
        
        self.probability_frame = ttk.Frame(self.labelframe_params)
        tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["probability"])
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.distribution_index_frame = ttk.Frame(self.labelframe_params)
        self.distribution_index_label = tk.Label( self.distribution_index_frame, text="Distribution index" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.distribution_index_entry = tk.Entry(master=self.distribution_index_frame, state=tk.NORMAL)
        self.distribution_index_entry.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.distribution_index_entry.insert(0, self.algorithm_parameters.int_crossover_parameters["distribution_index"])
        self.distribution_index_entry.config(state=tk.NORMAL)
        self.distribution_index_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
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
        super(BinaryCrossoverFrame,self).__init__(master=master, text="Binary crossover", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.crossover_options = [AlgorithmParameters.BINARY_CROSSOVER.SPX.value]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.CrossoverOption = tk.StringVar(self)
        self.CrossoverOption.set( AlgorithmParameters.BINARY_CROSSOVER.SPX.value )
        self.crossover_option = tk.OptionMenu(self.operator_frame, self.CrossoverOption, *self.crossover_options)
        self.crossover_option.config( state=tk.DISABLED )
        self.crossover_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.labelframe_params = tk.LabelFrame(master=self)
        
        self.probability_frame = ttk.Frame(self.labelframe_params)
        tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.insert(0, self.algorithm_parameters.binary_crossover_parameters["probability"])
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
        
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
        super(PermutationCrossoverFrame,self).__init__(master=master, text="Permutation crossover", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.crossover_options = [AlgorithmParameters.PERMUTATION_CROSSOVER.CXC.value, AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.CrossoverOption = tk.StringVar(self)
        self.CrossoverOption.set( AlgorithmParameters.PERMUTATION_CROSSOVER.PMX.value )
        self.crossover_option = tk.OptionMenu(self.operator_frame, self.CrossoverOption, *self.crossover_options)
        self.crossover_option.config( state=tk.DISABLED )
        self.crossover_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.labelframe_params = tk.LabelFrame(master=self)
        
        self.probability_frame = ttk.Frame(self.labelframe_params)
        tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.insert(0, self.algorithm_parameters.permutation_crossover_parameters["probability"])
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
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


class CrossoverFrame(AlgorithmFrame):

    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(CrossoverFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.float_frame = FloatCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.int_frame = IntCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.binary_frame = BinaryCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.permutation_frame = PermutationCrossoverFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        
        # self.float_frame.place( relx=0.025, rely=0.05, relwidth=0.4, relheight=0.3 )
        # self.int_frame.place( relx=0.025, rely=0.38, relwidth=0.4, relheight=0.3 )
        # self.binary_frame.place( relx=0.025, rely=0.71, relwidth=0.4, relheight=0.11 )
        # self.permutation_frame.place( relx=0.025, rely=0.85, relwidth=0.4, relheight=0.11 )
        
        self.grid_columnconfigure((0,1), weight=1, uniform="column")
        self.grid_rowconfigure((0,1), weight=1, uniform="row" )
        
        self.float_frame.grid( row=0, column=0, sticky="SNWE", padx=30, pady=20 )
        self.int_frame.grid( row=0, column=1, sticky="SNWE", padx=30, pady=20 )
        self.binary_frame.grid( row=1, column=0, sticky="SNWE", padx=30, pady=20 )
        self.permutation_frame.grid( row=1, column=1, sticky="SNWE", padx=30, pady=20 )
        
        self.float_frame.disable()
        self.int_frame.disable()
        self.binary_frame.disable()
        self.permutation_frame.disable()    

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
        
        # used_variable_types = [ type(x) for x in self.problem_parameters.variables ]
        
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
        
