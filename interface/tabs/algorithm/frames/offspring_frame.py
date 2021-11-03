# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *



class OffspringFrame(AlgorithmFrame):
        
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(OffspringFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.offspring_frame = ttk.Frame(self)
        tk.Label( master=self.offspring_frame, text="Offspring size").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.offspring_size_entry = tk.Entry(master=self.offspring_frame, state=tk.NORMAL)
        self.offspring_size_entry.insert(0, self.algorithm_parameters.general_parameters["offspring_size"])
        self.offspring_size_entry.grid( row=0, column=1, columnspan=2, padx=2, pady=2, sticky="NSEW" )
        self.offspring_size_entry.config(state=tk.NORMAL)
        self.offspring_frame.grid( row=0, column=0, sticky="NSEW", pady=25, padx=25 )
        
        self.offspring_size_parameter = Integer(name="offspring_size", fancy_name="Offspring size", lower_bound=3, upper_bound=100000)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.offspring_size_parameter,
                                                          widget_read_lambda=lambda: self.offspring_size_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.general_parameters.update({"offspring_size":var}),
                                                          error_set_lambda=EntryInvalidator(self.offspring_size_entry),
                                                          error_reset_lambda=EntryValidator(self.offspring_size_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.general_parameters["offspring_size"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.offspring_size_entry, str(var))) )