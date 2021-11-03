# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class FloatGenericMutationFrame(ParameterLabelFrame):
            
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        
        super(FloatGenericMutationFrame,self).__init__(master=master, *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.probability_frame = ttk.Frame(master=self)
        tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.insert(0, self.algorithm_parameters.float_mutation_parameters["probability"])
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.probability_parameter = Float(name="probability", fancy_name="probability", lower_bound=0.0, upper_bound=1.0)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                      widget_read_lambda=lambda: self.probability_entry.get(),
                                                      variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"probability":var}),
                                                      error_set_lambda=EntryInvalidator(self.probability_entry),
                                                      error_reset_lambda=EntryValidator(self.probability_entry),
                                                      variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["probability"],
                                                      widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
        
    def display(self):
        self.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
    def hide(self):
        self.grid_forget()
        
    def disable(self):
        self.probability_entry.config(state=tk.DISABLED)
    
    def enable(self):
        self.probability_entry.config(state=tk.NORMAL)



class FloatMutationFrame(ParameterLabelFrame):
        
    class PolynomialMutation(FloatGenericMutationFrame):
    
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(FloatMutationFrame.PolynomialMutation,self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            self.distribution_index_frame = ttk.Frame(master=self)
            self.distribution_index_label = tk.Label( master=self.distribution_index_frame, text="Distribution index" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.distribution_index_entry = tk.Entry(master=self.distribution_index_frame, state=tk.NORMAL)
            self.distribution_index_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.distribution_index_entry.insert(0, self.algorithm_parameters.float_mutation_parameters["distribution_index"])
            self.distribution_index_entry.config(state=tk.NORMAL)
            self.distribution_index_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (float mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                              widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"distribution_index":var}),
                                                              error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                              error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["distribution_index"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.distribution_index_entry, str(var)) ) )
        
            
        def disable(self):
            super(FloatMutationFrame.PolynomialMutation,self).disable()
            self.distribution_index_entry.config(state=tk.DISABLED)
        
        def enable(self):
            super(FloatMutationFrame.PolynomialMutation,self).enable()
            self.distribution_index_entry.config(state=tk.NORMAL)
    
    class UniformMutation(FloatGenericMutationFrame):
    
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(FloatMutationFrame.UniformMutation,self).__init__(master=master,
                                                                                  problem_parameters=problem_parameters,
                                                                                  algorithm_parameters=algorithm_parameters,
                                                                                  *args, **kwargs)
            
            
            self.perturbation_frame = ttk.Frame(self)
            self.perturbation_label = tk.Label( self.perturbation_frame, text="Perturbation" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.perturbation_entry = tk.Entry(master=self.perturbation_frame, state=tk.NORMAL)
            self.perturbation_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.perturbation_entry.config(state=tk.NORMAL)
            self.perturbation_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.perturbation_parameter = Float(name="perturbation", fancy_name="Perturbation (float mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.perturbation_parameter,
                                                              widget_read_lambda=lambda: self.perturbation_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"perturbation":var}),
                                                              error_set_lambda=EntryInvalidator(self.perturbation_entry),
                                                              error_reset_lambda=EntryValidator(self.perturbation_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["perturbation"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.perturbation_entry, str(var)) ) )
            
        def disable(self):
            super(FloatMutationFrame.UniformMutation,self).disable()
            self.perturbation_entry.config(state=tk.DISABLED)
        
        def enable(self):
            super(FloatMutationFrame.UniformMutation,self).enable()
            self.perturbation_entry.config(state=tk.NORMAL)
            
            
    class NonUniformMutation(UniformMutation):
    
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(FloatMutationFrame.NonUniformMutation,self).__init__(master=master,
                                                                                      problem_parameters=problem_parameters,
                                                                                      algorithm_parameters=algorithm_parameters,
                                                                                      *args, **kwargs)
            
            self.max_iter_frame = ttk.Frame(self)
            self.max_iter_label = tk.Label( self.max_iter_frame, text="Max. iterations" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.max_iter_entry = tk.Entry(master=self.max_iter_frame, state=tk.NORMAL)
            self.max_iter_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.max_iter_entry.config(state=tk.NORMAL)
            self.max_iter_frame.grid( row=2, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.max_iter_parameter = Integer(name="max_iterations", fancy_name="Max. iterations (float mutation)", lower_bound=1, upper_bound=100)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.max_iter_parameter,
                                                              widget_read_lambda=lambda: self.max_iter_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.float_mutation_parameters.update({"max_iterations":var}),
                                                              error_set_lambda=EntryInvalidator(self.max_iter_entry),
                                                              error_reset_lambda=EntryValidator(self.max_iter_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_parameters["max_iterations"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.max_iter_entry, str(var)) ) )
        
            
        def disable(self):
            super(FloatMutationFrame.NonUniformMutation,self).disable()
            self.max_iter_entry.config(state=tk.DISABLED)
        
        def enable(self):
            super(FloatMutationFrame.NonUniformMutation,self).enable()
            self.max_iter_entry.config(state=tk.NORMAL)
            
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(FloatMutationFrame,self).__init__(master=master, text="Float mutation", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.mutation_options = [ option.value for option in AlgorithmParameters.FLOAT_MUTATION ]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(master=self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.MutationOption = tk.StringVar(self)
        self.MutationOption.set( self.mutation_options[0] )
        self.mutation_option = tk.OptionMenu(self.operator_frame, self.MutationOption, *self.mutation_options, command=self.option_change)
        self.mutation_option.config( state=tk.NORMAL )
        self.mutation_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.frames = {}
        self.frames[AlgorithmParameters.FLOAT_MUTATION.SIMPLE_RANDOM.value] = FloatGenericMutationFrame(master=self,
                                                                                                        problem_parameters=self.problem_parameters,
                                                                                                        algorithm_parameters=self.algorithm_parameters)
        
        self.frames[AlgorithmParameters.FLOAT_MUTATION.POLYNOMIAL.value] = FloatMutationFrame.PolynomialMutation(master=self,
                                                                                                                                problem_parameters=self.problem_parameters,
                                                                                                                                algorithm_parameters=self.algorithm_parameters)
        
        self.frames[AlgorithmParameters.FLOAT_MUTATION.UNIFORM.value] = FloatMutationFrame.UniformMutation(master=self,
                                                                                                                            problem_parameters=self.problem_parameters,
                                                                                                                            algorithm_parameters=self.algorithm_parameters)
        
        self.frames[AlgorithmParameters.FLOAT_MUTATION.NON_UNIFORM.value] = FloatMutationFrame.NonUniformMutation(master=self,
                                                                                                                                            problem_parameters=self.problem_parameters,
                                                                                                                                            algorithm_parameters=self.algorithm_parameters)
        
        self.selected_frame_key = self.mutation_options[0]
        self.frames[self.selected_frame_key].display()
        
        self.mutation_option_parameter = Parameter( name="float_mutation_option", fancy_name="Float mutation option" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                          widget_read_lambda=lambda: self.MutationOption.get(),
                                                          variable_store_lambda=self.__store_float_mutation_option,
                                                          variable_read_lambda=lambda: self.algorithm_parameters.float_mutation_choice,
                                                          widget_update_lambda=lambda var: self.MutationOption.set(var)) )
        
    def __store_float_mutation_option(self, value):
        self.algorithm_parameters.float_mutation_choice = value
        
        
    def option_change(self, new_value):
        
        if new_value != self.selected_frame_key:
            self.frames[self.selected_frame_key].hide()
            self.selected_frame_key = new_value
            self.frames[self.selected_frame_key].display()
        
    def check_errors(self):
        error_list = super(FloatMutationFrame,self).check_errors()
        error_list.extend( self.frames[self.selected_frame_key].check_errors() )
        
        return error_list
    
    def save_parameters(self):
        
        super(FloatMutationFrame,self).save_parameters()
        self.frames[self.selected_frame_key].save_parameters()
        
    def load_parameters(self):
        
        super(FloatMutationFrame,self).load_parameters()
        self.frames[self.selected_frame_key].load_parameters()
        
    def disable(self):
        self.configure(text="Float mutation (Disabled)")
        self.mutation_option.config(state=tk.DISABLED)
        # self.probability_entry.config(state=tk.DISABLED)
        self.frames[self.selected_frame_key].disable()
        
    def enable(self):
        self.configure(text="Float mutation")
        self.mutation_option.config(state=tk.NORMAL)
        # self.probability_entry.config(state=tk.NORMAL)
        self.frames[self.selected_frame_key].enable()


class IntMutationFrame(ParameterLabelFrame):
        
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(IntMutationFrame,self).__init__(master=master, text="Integer mutation", *args, **kwargs)
        
        self.problem_parameters = problem_parameters
        self.algorithm_parameters = algorithm_parameters
        
        self.mutation_options = [AlgorithmParameters.INT_MUTATION.INT_POLYNOMIAL.value]
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,2,3,4),weight=1)
        
        self.operator_frame = ttk.Frame(master=self)
        tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.MutationOption = tk.StringVar(self)
        self.MutationOption.set( self.mutation_options[0] )
        self.mutation_option = tk.OptionMenu(self.operator_frame, self.MutationOption, *self.mutation_options )
        self.mutation_option.config( state=tk.NORMAL )
        self.mutation_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.labelframe_params = tk.LabelFrame(master=self)
        
        self.probability_frame = ttk.Frame(master=self.labelframe_params)
        tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
        self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.probability_entry.insert(0, self.algorithm_parameters.int_mutation_parameters["probability"])
        self.probability_entry.config(state=tk.NORMAL)
        self.probability_frame.grid( row=0, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.distribution_index_frame = ttk.Frame(master=self.labelframe_params)
        self.distribution_index_label = tk.Label( master=self.distribution_index_frame, text="Distribution index" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
        self.distribution_index_entry = tk.Entry(master=self.distribution_index_frame, state=tk.NORMAL)
        self.distribution_index_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
        self.distribution_index_entry.insert(0, self.algorithm_parameters.int_mutation_parameters["distribution_index"])
        self.distribution_index_entry.config(state=tk.NORMAL)
        self.distribution_index_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
        
        self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
        
        self.mutation_option_parameter = Parameter( name="int_mutation_option", fancy_name="Integer mutation option" )
        self.probability_parameter = Float(name="probability", fancy_name="Probability (int mutation)", lower_bound=0.0, upper_bound=1.0)
        self.distribution_index_parameter = Float(name="distribution_index", fancy_name="Distribution index (int mutation)", lower_bound=float("-Inf"), upper_bound=float("Inf"))
    
        self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                          widget_read_lambda=lambda: self.probability_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.int_mutation_parameters.update({"probability":var}),
                                                          error_set_lambda=EntryInvalidator(self.probability_entry),
                                                          error_reset_lambda=EntryValidator(self.probability_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_parameters["probability"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.distribution_index_parameter,
                                                          widget_read_lambda=lambda: self.distribution_index_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.int_mutation_parameters.update({"distribution_index":var}),
                                                          error_set_lambda=EntryInvalidator(self.distribution_index_entry),
                                                          error_reset_lambda=EntryValidator(self.distribution_index_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_parameters["distribution_index"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.distribution_index_entry, str(var)) ) )
        
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                          widget_read_lambda=lambda: self.MutationOption.get(),
                                                          variable_store_lambda=self.__store_int_mutation_option,
                                                          variable_read_lambda=lambda: self.algorithm_parameters.int_mutation_choice,
                                                          widget_update_lambda=lambda var: self.MutationOption.set(var)) )

    def __store_int_mutation_option(self, value):
        self.algorithm_parameters.int_mutation_choice = value
        
    def disable(self):
        self.configure(text="Integer mutation (Disabled)")
        self.mutation_option.config(state=tk.DISABLED)
        self.probability_entry.config(state=tk.DISABLED)
        self.distribution_index_entry.config(state=tk.DISABLED)
        
    def enable(self):
        self.configure(text="Integer mutation")
        self.mutation_option.config(state=tk.NORMAL)
        self.probability_entry.config(state=tk.NORMAL)
        self.distribution_index_entry.config(state=tk.NORMAL)


class MutationFrame(AlgorithmFrame):
        
    
            
    class BinaryMutationFrame(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(MutationFrame.BinaryMutationFrame,self).__init__(master=master, text="Binary mutation", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            self.mutation_options = [AlgorithmParameters.BINARY_MUTATION.BIT_FLIP.value]
            
            self.grid_columnconfigure((0), weight=1)
            self.grid_rowconfigure((1,2,3,4),weight=1)
            
            self.labelframe_params = tk.LabelFrame(master=self)
            
            self.operator_frame = ttk.Frame(master=self)
            tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
            self.MutationOption = tk.StringVar(self)
            self.MutationOption.set( self.mutation_options[0] )
            self.mutation_option = tk.OptionMenu(self.operator_frame, self.MutationOption, *self.mutation_options)
            self.mutation_option.config( state=tk.DISABLED )
            self.mutation_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
            self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
            
            self.probability_frame = ttk.Frame(master=self.labelframe_params)
            tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
            self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.probability_entry.insert(0, self.algorithm_parameters.binary_mutation_parameters["probability"])
            self.probability_entry.config(state=tk.NORMAL)
            self.probability_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
            
            self.mutation_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
            self.probability_parameter = Float(name="probability", fancy_name="Probability (Binary mutation)", lower_bound=0.0, upper_bound=1.0)
        
            self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                              widget_read_lambda=lambda: self.probability_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.binary_mutation_parameters.update({"probability":var}),
                                                              error_set_lambda=EntryInvalidator(self.probability_entry),
                                                              error_reset_lambda=EntryValidator(self.probability_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.binary_mutation_parameters["probability"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
        
                
            self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                              widget_read_lambda=lambda: self.MutationOption.get(),
                                                              variable_store_lambda=self.__store_binary_mutation_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.binary_mutation_choice,
                                                              widget_update_lambda=lambda var: self.MutationOption.set(var)) )
            
        
        def __store_binary_mutation_option(self, value):
            self.algorithm_parameters.binary_mutation_choice = value
            
        def disable(self):
            self.configure(text="Binary mutation (Disabled)")
            self.mutation_option.config(state=tk.DISABLED)
            self.probability_entry.config(state=tk.DISABLED)
            
        def enable(self):
            self.configure(text="Binary mutation")
            self.mutation_option.config(state=tk.NORMAL)
            self.probability_entry.config(state=tk.NORMAL)
    
            
    class PermutationMutationFrame(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(MutationFrame.PermutationMutationFrame,self).__init__(master=master, text="Permutation mutation", *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            # self.rowconfigure(1)
            # self.grid_columnconfigure(5, {'minsize': 150})
            self.grid_columnconfigure((0), weight=1)
            self.grid_rowconfigure((1,2,3,4),weight=1)
            # self.grid_rowconfigure((0,1), weight=1, uniform="row" )
            
            self.mutation_options = [option.value for option in AlgorithmParameters.PERMUTATION_MUTATION]
            
            self.labelframe_params = tk.LabelFrame(master=self)
            
            self.operator_frame = ttk.Frame(master=self)
            tk.Label( self.operator_frame, text="Operator" ).grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
            self.MutationOption = tk.StringVar(self)
            self.MutationOption.set( self.mutation_options[0] )
            self.mutation_option = tk.OptionMenu(self.operator_frame, self.MutationOption, *self.mutation_options)
            self.mutation_option.config( state=tk.NORMAL )
            self.mutation_option.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
            self.operator_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
            
            self.probability_frame = ttk.Frame(master=self.labelframe_params)
            tk.Label( master=self.probability_frame, text="Probability" ).grid( row=0, column=0, padx=2, pady=2, sticky="WENS" )
            self.probability_entry = tk.Entry(master=self.probability_frame, state=tk.NORMAL)
            self.probability_entry.grid( row=0, column=1, padx=2, pady=2, sticky="NSEW" )
            self.probability_entry.insert(0, self.algorithm_parameters.permutation_mutation_parameters["probability"])
            self.probability_entry.config(state=tk.NORMAL)
            self.probability_frame.grid( row=1, column=0, sticky="NSEW", padx=3, pady=6 )
            
            self.labelframe_params.grid( row=1, column=0, columnspan=3, rowspan=4, sticky="NSEW", padx=5, pady=5 )
            
            self.mutation_option_parameter = Parameter( name="binary_crossover_option", fancy_name="Binary crossover option" )
            self.probability_parameter = Float(name="probability", fancy_name="Probability (Permutation mutation)", lower_bound=0.0, upper_bound=1.0)
        
            self.parameters_bindings.append( ParameterBinding(parameter=self.probability_parameter,
                                                              widget_read_lambda=lambda: self.probability_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.permutation_mutation_parameters.update({"probability":var}),
                                                              error_set_lambda=EntryInvalidator(self.probability_entry),
                                                              error_reset_lambda=EntryValidator(self.probability_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.permutation_mutation_parameters["probability"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.probability_entry, str(var)) ) )
            
                
            self.parameters_bindings.append( ParameterBinding(parameter=self.mutation_option_parameter,
                                                              widget_read_lambda=lambda: self.MutationOption.get(),
                                                              variable_store_lambda=self.__store_permutation_mutation_option,
                                                              variable_read_lambda=lambda: self.algorithm_parameters.permutation_mutation_choice,
                                                              widget_update_lambda=lambda var: self.MutationOption.set(var)) )
            
        def __store_permutation_mutation_option(self, value):
            self.algorithm_parameters.permutation_mutation_choice = value
            
        def disable(self):
            self.configure(text="Permutation mutation (Disabled)")
            self.mutation_option.config(state=tk.DISABLED)
            self.probability_entry.config(state=tk.DISABLED)
            
        def enable(self):
            self.configure(text="Permutation mutation")
            self.mutation_option.config(state=tk.NORMAL)
            self.probability_entry.config(state=tk.NORMAL)
            
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(MutationFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.float_frame = FloatMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.int_frame = IntMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.binary_frame = MutationFrame.BinaryMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        self.permutation_frame = MutationFrame.PermutationMutationFrame( master=self, problem_parameters=self.problem_parameters, algorithm_parameters=self.algorithm_parameters )
        
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
        error_list = super(MutationFrame,self).check_errors()
        
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
