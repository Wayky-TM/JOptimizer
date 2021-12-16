# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class KappaFrame(AlgorithmFrame):
        
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(KappaFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.kappa_frame = ttk.Frame(self)
        tk.Label( master=self.kappa_frame, text="Kappa").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.kappa_entry = tk.Entry(master=self.kappa_frame, state=tk.NORMAL)
        self.kappa_entry.insert(0, self.algorithm_parameters.specific_options["kappa"])
        self.kappa_entry.grid( row=0, column=1, columnspan=2, padx=8, pady=2, sticky="NSEW" )
        self.kappa_entry.config(state=tk.NORMAL)
        self.kappa_frame.grid( row=0, column=0, sticky="NSEW", pady=25, padx=25 )
        
        self.kappa_parameter = Float(name="kappa", fancy_name="Kappa", lower_bound=0.0, upper_bound=100.0)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.kappa_parameter,
                                                          widget_read_lambda=lambda: self.kappa_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"kappa":var}),
                                                          error_set_lambda=EntryInvalidator(self.kappa_entry),
                                                          error_reset_lambda=EntryValidator(self.kappa_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["kappa"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.kappa_entry, str(var))) )