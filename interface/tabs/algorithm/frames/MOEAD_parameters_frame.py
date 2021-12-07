# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class MOEADParametersFrame(AlgorithmFrame):
        
    def _browse(self): 
        
        path = filedialog.askdirectory(title = "Select a folder to store weights", initialdir=os.getcwd() )
        
        self.weight_files_path_entry.config(state=tk.NORMAL)
        self.weight_files_path_entry.delete( 0, tk.END )
        self.weight_files_path_entry.insert( 0, path )
        self.weight_files_path_entry.config(state="readonly")
    
    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(MOEADParametersFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        self.neighborhood_selection_probability_frame = tk.Frame(self)
        tk.Label( master=self.neighborhood_selection_probability_frame, text="Neighbourhood selection probability").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.neighborhood_selection_probability_entry = tk.Entry(master=self.neighborhood_selection_probability_frame, state=tk.NORMAL)
        self.neighborhood_selection_probability_entry.insert(0, self.algorithm_parameters.specific_options["neighborhood_selection_probability"])
        self.neighborhood_selection_probability_entry.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1, ipadx=5 )
        self.neighborhood_selection_probability_entry.config(state=tk.NORMAL)
        self.neighborhood_selection_probability_frame.grid( row=0, column=0, sticky="NSEW", pady=10, padx=2 )
        
        self.neighborhood_selection_probability_frame.grid( row=0, column=0, sticky="NSW", pady=10, padx=2 )
        
        self.neighborhood_selection_probability_parameter = Float(name="neighborhood_selection_probability", fancy_name="Neighbourhood selection probability", lower_bound=0.0, upper_bound=1.0)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.neighborhood_selection_probability_parameter,
                                                          widget_read_lambda=lambda: self.neighborhood_selection_probability_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"neighborhood_selection_probability":var}),
                                                          error_set_lambda=EntryInvalidator(self.neighborhood_selection_probability_entry),
                                                          error_reset_lambda=EntryValidator(self.neighborhood_selection_probability_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["neighborhood_selection_probability"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.neighborhood_selection_probability_entry, str(var))) )
        
        
        self.max_number_of_replaced_solutions_frame = tk.Frame(self)
        tk.Label( master=self.max_number_of_replaced_solutions_frame, text="Max. number of replaced solutions").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.max_number_of_replaced_solutions_entry = tk.Entry(master=self.max_number_of_replaced_solutions_frame, state=tk.NORMAL)
        self.max_number_of_replaced_solutions_entry.insert(0, self.algorithm_parameters.specific_options["max_number_of_replaced_solutions"])
        self.max_number_of_replaced_solutions_entry.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1 )
        self.max_number_of_replaced_solutions_entry.config(state=tk.NORMAL)
        self.max_number_of_replaced_solutions_frame.grid( row=1, column=0, sticky="NSW", pady=10, padx=2 )
        
        self.max_number_of_replaced_solutions_parameter = Integer(name="max_number_of_replaced_solutions", fancy_name="Max. number of replaced solutions", lower_bound=1, upper_bound=100)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.max_number_of_replaced_solutions_parameter,
                                                          widget_read_lambda=lambda: self.max_number_of_replaced_solutions_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"max_number_of_replaced_solutions":var}),
                                                          error_set_lambda=EntryInvalidator(self.max_number_of_replaced_solutions_entry),
                                                          error_reset_lambda=EntryValidator(self.max_number_of_replaced_solutions_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["max_number_of_replaced_solutions"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.max_number_of_replaced_solutions_entry, str(var))) )
        
        
        self.neighbor_size_frame = tk.Frame(self)
        tk.Label( master=self.neighbor_size_frame, text="Neighborhood size").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.neighbor_size_entry = tk.Entry(master=self.neighbor_size_frame, state=tk.NORMAL)
        self.neighbor_size_entry.insert(0, self.algorithm_parameters.specific_options["neighborhood_size"])
        self.neighbor_size_entry.grid( row=0, column=1, sticky="NSEW", padx=8, pady=2, columnspan=1 )
        self.neighbor_size_entry.config(state=tk.NORMAL)
        self.neighbor_size_frame.grid( row=2, column=0, sticky="NSW", pady=10, padx=2 )
        
        self.neighbor_size_parameter = Integer(name="neighbor_size", fancy_name="Neighbourhood size", lower_bound=1, upper_bound=100)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.neighbor_size_parameter,
                                                          widget_read_lambda=lambda: self.neighbor_size_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"neighborhood_size":var}),
                                                          error_set_lambda=EntryInvalidator(self.neighbor_size_entry),
                                                          error_reset_lambda=EntryValidator(self.neighbor_size_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["neighborhood_size"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.neighbor_size_entry, str(var))) )
        
        
        self.weight_files_path_frame = tk.Frame(self)
        tk.Label( master=self.weight_files_path_frame, text="Weight files folder path").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.weight_files_path_entry = tk.Entry(master=self.weight_files_path_frame, state=tk.NORMAL)
        self.weight_files_path_entry.insert(0, self.algorithm_parameters.specific_options["weight_files_path"])
        self.weight_files_path_entry.grid( row=0, column=1, sticky="NSEW", padx=(8,2), pady=2, columnspan=6, ipadx=120 )
        self.weight_files_path_entry.config(state="readonly")
        self.button_browse_weight_files = ttk.Button( master=self.weight_files_path_frame,  text="Browse", command=lambda: self._browse() )
        self.button_browse_weight_files.grid( row=0, column=7, sticky="EW", padx=(3,2), pady=2, columnspan=1 )
        self.weight_files_path_frame.grid( row=3, column=0, sticky="NSW", pady=10, padx=2 )
        
        self.weight_files_path_parameter = FilePath(name="weight_files_path", fancy_name="Weight files path", is_folder=True)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.weight_files_path_parameter,
                                                          widget_read_lambda=lambda: self.weight_files_path_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"weight_files_path":var}),
                                                          error_set_lambda=EntryInvalidator(self.weight_files_path_entry),
                                                          error_reset_lambda=EntryValidator(self.weight_files_path_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["weight_files_path"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.weight_files_path_entry, str(var))) )
