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
        
        tk.Label( master=self, text="Neighbourhood selection probability").place( relx=0.02, rely=0.05 )
        self.neighborhood_selection_probability_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.neighborhood_selection_probability_entry.insert(0, self.algorithm_parameters.specific_options["neighborhood_selection_probability"])
        self.neighborhood_selection_probability_entry.place(relx=0.19, rely=0.05+0.005, relwidth=0.08)
        self.neighborhood_selection_probability_entry.config(state=tk.NORMAL)
        
        self.neighborhood_selection_probability_parameter = Float(name="neighborhood_selection_probability", fancy_name="Neighbourhood selection probability", lower_bound=0.0, upper_bound=1.0)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.neighborhood_selection_probability_parameter,
                                                          widget_read_lambda=lambda: self.neighborhood_selection_probability_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"neighborhood_selection_probability":var}),
                                                          error_set_lambda=EntryInvalidator(self.neighborhood_selection_probability_entry),
                                                          error_reset_lambda=EntryValidator(self.neighborhood_selection_probability_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["neighborhood_selection_probability"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.neighborhood_selection_probability_entry, str(var))) )
        
        
        tk.Label( master=self, text="Max. number of replaced solutions").place( relx=0.02, rely=0.1 )
        self.max_number_of_replaced_solutions_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.max_number_of_replaced_solutions_entry.insert(0, self.algorithm_parameters.specific_options["max_number_of_replaced_solutions"])
        self.max_number_of_replaced_solutions_entry.place(relx=0.19, rely=0.1+0.005, relwidth=0.08)
        self.max_number_of_replaced_solutions_entry.config(state=tk.NORMAL)
        
        self.max_number_of_replaced_solutions_parameter = Integer(name="max_number_of_replaced_solutions", fancy_name="Max. number of replaced solutions", lower_bound=1, upper_bound=100)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.max_number_of_replaced_solutions_parameter,
                                                          widget_read_lambda=lambda: self.max_number_of_replaced_solutions_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"max_number_of_replaced_solutions":var}),
                                                          error_set_lambda=EntryInvalidator(self.max_number_of_replaced_solutions_entry),
                                                          error_reset_lambda=EntryValidator(self.max_number_of_replaced_solutions_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["max_number_of_replaced_solutions"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.max_number_of_replaced_solutions_entry, str(var))) )
        
        
        tk.Label( master=self, text="Neighborhood size").place( relx=0.02, rely=0.15 )
        self.neighbor_size_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.neighbor_size_entry.insert(0, self.algorithm_parameters.specific_options["neighborhood_size"])
        self.neighbor_size_entry.place(relx=0.115, rely=0.15+0.005, relwidth=0.08)
        self.neighbor_size_entry.config(state=tk.NORMAL)
        
        self.neighbor_size_parameter = Integer(name="neighbor_size", fancy_name="Neighbourhood size", lower_bound=1, upper_bound=100)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.neighbor_size_parameter,
                                                          widget_read_lambda=lambda: self.neighbor_size_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"neighborhood_size":var}),
                                                          error_set_lambda=EntryInvalidator(self.neighbor_size_entry),
                                                          error_reset_lambda=EntryValidator(self.neighbor_size_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["neighborhood_size"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.neighbor_size_entry, str(var))) )
        
        
        tk.Label( master=self, text="Weight files folder path").place( relx=0.02, rely=0.2 )
        self.weight_files_path_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.weight_files_path_entry.insert(0, self.algorithm_parameters.specific_options["weight_files_path"])
        self.weight_files_path_entry.place(relx=0.105, rely=0.2+0.005, relwidth=0.3)
        self.weight_files_path_entry.config(state="readonly")
        self.button_browse_weight_files = ttk.Button( master=self,  text="Browse", command=lambda: self._browse() )
        self.button_browse_weight_files.place(relx=0.41, rely=0.2, relwidth=0.06)
        
        self.weight_files_path_parameter = FilePath(name="weight_files_path", fancy_name="Weight files path", is_folder=True)
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.weight_files_path_parameter,
                                                          widget_read_lambda=lambda: self.weight_files_path_entry.get(),
                                                          variable_store_lambda=lambda var: self.algorithm_parameters.specific_options.update({"weight_files_path":var}),
                                                          error_set_lambda=EntryInvalidator(self.weight_files_path_entry),
                                                          error_reset_lambda=EntryValidator(self.weight_files_path_entry),
                                                          variable_read_lambda=lambda: self.algorithm_parameters.specific_options["weight_files_path"],
                                                          widget_update_lambda=lambda var: ClearInsertEntry(self.weight_files_path_entry, str(var))) )
