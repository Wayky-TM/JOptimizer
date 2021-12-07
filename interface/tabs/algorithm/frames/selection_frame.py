# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.algorithm.frames.algorithm_frame import *


class SelectionFrame(AlgorithmFrame):
    
    class SelectionParametersPane(ParameterLabelFrame):
        
        def __init__(self, master, algorithm_parameters, *args, **kwargs):
            super(SelectionFrame.SelectionParametersPane,self).__init__(master=master, *args, **kwargs)
            
            self.algorithm_parameters = algorithm_parameters
            
        def display(self):
            # self.place( relx=0.05, rely=0.16, relwidth=0.9, relheight=0.79 )
            self.grid( row=1, column=0, sticky="NSEW", pady=25, padx=25 )
            
        def hide(self):
            # self.place( relx=0.05, rely=0.16, relwidth=0.9, relheight=0.79 )
            self.grid_forget()
                
            
    class NaryParametersPane(SelectionParametersPane):
        
        def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(SelectionFrame.NaryParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)
            
            tk.Label( master=self, text="Number of solutions to select").place( relx=0.02, rely=0.05 )
            
            self.n_solutions_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.n_solutions_entry.insert(0, self.algorithm_parameters.selection_parameters["number_of_solutions_to_be_returned"])
            self.n_solutions_entry.place(relx=0.185, rely=0.05+0.005, relwidth=0.06)
            self.n_solutions_entry.config(state=tk.NORMAL)
            
            self.n_solutions_parameter = Integer(name="number_of_solutions_to_be_returned", fancy_name="Number of solutions to select", lower_bound=1, upper_bound=10000)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.n_solutions_parameter,
                                                              widget_read_lambda=lambda: self.n_solutions_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.selection_parameters.update({"number_of_solutions_to_be_returned":var}),
                                                              error_set_lambda=EntryInvalidator(self.n_solutions_entry),
                                                              error_reset_lambda=EntryValidator(self.n_solutions_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.selection_parameters["number_of_solutions_to_be_returned"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.n_solutions_entry, str(var)) ) )        
            
    
    class RankingAndCrowdingParametersPane(SelectionParametersPane):
        
        def __init__(self, master, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
            super(SelectionFrame.RankingAndCrowdingParametersPane,self).__init__(master=master, algorithm_parameters=algorithm_parameters, *args, **kwargs)

            tk.Label( master=self, text="Max. population size").place( relx=0.02, rely=0.05 )
            
            self.max_population_entry = tk.Entry(master=self, state=tk.NORMAL)
            self.max_population_entry.insert(0, self.algorithm_parameters.selection_parameters["max_population_size"])
            self.max_population_entry.place(relx=0.15, rely=0.05+0.005, relwidth=0.06)
            self.max_population_entry.config(state=tk.NORMAL)
            
            self.max_population_parameter = Integer(name="max_population_size", fancy_name="Max. population size", lower_bound=1, upper_bound=1000)
            
            self.parameters_bindings.append( ParameterBinding(parameter=self.max_population_parameter,
                                                              widget_read_lambda=lambda: self.max_population_entry.get(),
                                                              variable_store_lambda=lambda var: self.algorithm_parameters.selection_parameters.update({"max_population_size":var}),
                                                              error_set_lambda=EntryInvalidator(self.max_population_entry),
                                                              error_reset_lambda=EntryValidator(self.max_population_entry),
                                                              variable_read_lambda=lambda: self.algorithm_parameters.selection_parameters["max_population_size"],
                                                              widget_update_lambda=lambda var: ClearInsertEntry(self.max_population_entry, str(var)) ) )        

    def update_operator(self, new_value):
        # self.frames[self.selected_frame_key].clear_errors()
        # self.frames[self.selected_frame_key].clear_entries()
        self.frames[self.selected_frame_key].hide()
        self.selected_frame_key = new_value
        self.frames[self.selected_frame_key].display()

    def __update_operator_option__(self, var):
        self.SelectionOption.set(var)
        self.update_operator( var )

    def __init__(self, master, problem_parameters: ProblemParameters, algorithm_parameters: AlgorithmParameters, *args, **kwargs):
        super(SelectionFrame, self).__init__(master=master, problem_parameters=problem_parameters, algorithm_parameters=algorithm_parameters, *args, **kwargs)
        
        paceholder_frame = SelectionFrame.SelectionParametersPane( master=self, algorithm_parameters=self.algorithm_parameters, borderwidth=0, highlightthickness=0 )
        
        self.selection_options = [ option.value for option in AlgorithmParameters.SELECTION ]
        
        self.frames = {}
        self.frames[ AlgorithmParameters.SELECTION.ROULETTE.value ] = paceholder_frame
        self.frames[ AlgorithmParameters.SELECTION.BINARY_TOURNAMENT.value ] = paceholder_frame
        self.frames[ AlgorithmParameters.SELECTION.BEST_SOLUTION.value ] = paceholder_frame
        self.frames[ AlgorithmParameters.SELECTION.NARY_RANDOM.value ] = SelectionFrame.NaryParametersPane(master=self, algorithm_parameters=self.algorithm_parameters, text="Parameters")
        self.frames[ AlgorithmParameters.SELECTION.DIFF_EVOLUTION.value ] = paceholder_frame
        self.frames[ AlgorithmParameters.SELECTION.RANDOM.value ] = paceholder_frame
        self.frames[ AlgorithmParameters.SELECTION.RANKING_AND_CROWDING.value ] = SelectionFrame.RankingAndCrowdingParametersPane(master=self, algorithm_parameters=self.algorithm_parameters, text="Parameters")
        
        
        self.selection_frame = ttk.Frame(self)
        # tk.Label( master=self.selection_frame, text="Selection operator").place( relx=0.02, rely=0.05 )
        tk.Label( master=self.selection_frame, text="Selection operator").grid( row=0, column=0, sticky="NSEW", padx=2, pady=2 )
        self.SelectionOption = tk.StringVar(self)
        self.SelectionOption.set(self.selection_options[1])
        self.selected_frame_key = self.selection_options[1]
        self.frames[self.selected_frame_key].display()
        self.selection_option = tk.OptionMenu(self.selection_frame, self.SelectionOption, *self.selection_options, command=self.update_operator)
        # selection_option.config( font=('URW Gothic L','11') )
        self.selection_option.config( state=tk.NORMAL )
        self.selection_option.grid( row=0, column=1, columnspan=2, padx=8, pady=2, sticky="NSEW" )
        self.selection_frame.grid( row=0, column=0, sticky="NSEW", pady=25, padx=25 )
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.selection_option_parameter = Parameter(name="selection_operator", fancy_name="Selection operator")
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.selection_option_parameter,
                                                          widget_read_lambda=lambda: self.SelectionOption.get(),
                                                          variable_store_lambda=self.__store_selection_option,
                                                          variable_read_lambda=lambda: self.algorithm_parameters.selection_choice,
                                                          widget_update_lambda=lambda var: self.__update_operator_option__(var) ) )
        
    def __store_selection_option(self, value):
        self.algorithm_parameters.selection_choice = value
        
    def check_errors(self):
        
        error_list = super(SelectionFrame, self).check_errors()
        error_list.extend( self.frames[self.selected_frame_key].check_errors() )
            
        return error_list
            
    def save_parameters(self):
        
        super(SelectionFrame, self).save_parameters()
        self.frames[self.selected_frame_key].save_parameters()
        
    def load_parameters(self):
        
        super(SelectionFrame, self).load_parameters()
        self.frames[self.selected_frame_key].load_parameters()
