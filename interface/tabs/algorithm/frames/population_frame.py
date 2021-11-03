# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class PopulationFrame(AlgorithmFrame):
        
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(PopulationFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.population_frame = ttk.Frame(self)
        tk.Label( master=self.population_frame, text="Population size").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.population_size_entry = tk.Entry(master=self.population_frame, state=tk.NORMAL)
        self.population_size_entry.insert(0, self.algorithm_parameters.general_parameters["population_size"])
        self.population_size_entry.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.population_size_entry.config(state=tk.NORMAL)
        self.population_frame.grid( row=0, column=0, sticky="NSEW", pady=25, padx=25 )
        
        self.population_size_parameter = Integer(name="population_size", fancy_name="Population size", lower_bound=10, upper_bound=100000)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.population_size_parameter,
                                                          widget_read_lambda=lambda: self.population_size_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"population_size":var}),
                                                          error_set_lambda=EntryInvalidator(self.population_size_entry),
                                                          error_reset_lambda=EntryValidator(self.population_size_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.general_parameters["population_size"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.population_size_entry, str(var))) )