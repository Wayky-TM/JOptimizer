# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class AggregativeFrame(AlgorithmFrame):
        
    class Tschebycheff(ParameterLabelFrame):
        
        def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(AggregativeFrame.Tschebycheff, self).__init__(master=master, *args, **kwargs)
            
            self.problem_parameters = problem_parameters
            self.algorithm_parameters = algorithm_parameters
            
            tk.Label( master=self, text="Dimension").place( relx=0.02, rely=0.05 )
            
            self.dimension_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.dimension_entry.insert(0, self.algorithm_parameters.specific_parameters["aggregative"]["dimension"])
            self.dimension_entry.place(relx=0.105, rely=0.05+0.005, relwidth=0.06)
            self.dimension_entry.config(state=tk.NORMAL)
            
            self.dimension_parameter = Integer(name="dimension", fancy_name="Dimension", lower_bound=1, upper_bound=100)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.dimension_parameter,
                                                              widget_read_lambda=lambda: self.dimension_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.specific_parameters["aggregative"].update({"dimension":var}),
                                                              error_set_lambda=EntryInvalidator(self.dimension_entry),
                                                              error_reset_lambda=EntryValidator(self.dimension_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.specific_parameters["aggregative"]["dimension"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.dimension_entry, str(var)) ) )
            
        def display(self):
            self.place( relx=0.05, rely=0.16, relwidth=0.9, relheight=0.79 )
    
    def _option_update(self, new_key):
        self.frames[self.selected_frame_key].hide()
        self.selected_frame_key = new_key
        self.frames[self.selected_frame_key].display()
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(AggregativeFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
    
        self.aggregative_option_list = [ option.value for option in AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION ]
    
        tk.Label( self, text="Operator" ).place( relx=0.02, rely=0.05 )
        self.AggregativeOption = tk.StringVar(self)
        self.AggregativeOption.set( AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.WEIGHTED_SUM.value )
        self.aggregative_option = tk.OptionMenu(self, self.AggregativeOption, *self.aggregative_option_list, command=self._option_update)
        self.aggregative_option.config( state=tk.NORMAL )
        self.aggregative_option.place( relx=0.07, rely=0.045, relwidth=0.1 )
        
        self.frames = {}
        self.frames[AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.TSCHEBYCHEFF.value] = AggregativeFrame.Tschebycheff(master=self,
                                                                                                                                    problem_parameters=problem_parameters,
                                                                                                                                    algorithm_parameters=algorithm_parameters)
        self.frames[AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.WEIGHTED_SUM.value] = NullParameterFrame(master=self)
        
        self.selected_frame_key = AlgorithmParameters.MOEAD_AGGREGATIVE_FUNCTION.WEIGHTED_SUM.value
        
        self.function_parameter = Parameter(name="Aggregative function", fancy_name="aggregative_function")
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.function_parameter,
                                                            widget_read_lambda=lambda: self.AggregativeOption.get(),
                                                            variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"aggregative":var}),
                                                            variable_read_lambda=lambda: self.algorithm_parameters.specific_options["aggregative"],
                                                            widget_update_lambda=lambda var: self.AggregativeOption.set(str(var)) ) )
