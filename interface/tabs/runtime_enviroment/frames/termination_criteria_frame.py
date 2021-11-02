# -*- coding: utf-8 -*-


import sys
sys.path.append(r"./../../../../../")

from interface.tabs.runtime_enviroment.frames.runtime_frame import *


class TerminationCriteriaFrame(RuntimeFrame):
        
    def __update_time__(self, var):
        self.time_entry.configure( state=tk.NORMAL )
        
        ClearInsertEntry(self.time_entry, str(var))
        
        if EngineParameters.TERMINATION_CRITERIA.TIME.value not in self.engine_parameters.temination_criteria:
            self.time_entry.configure( state=tk.DISABLED )
        
    def __update_timescale__(self, var):
        self.TimescaleOption.set(var)
        
        if EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
            self.timescale_option.configure( state=tk.NORMAL )
            
        else:
            self.timescale_option.configure( state=tk.DISABLED )
        
    def __update_evaluations__(self, var):
        self.eval_entry.configure( state=tk.NORMAL )
        ClearInsertEntry(self.eval_entry, str(var))
        
        if EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value not in self.engine_parameters.temination_criteria:
            self.eval_entry.configure( state=tk.DISABLED )
        
    
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(TerminationCriteriaFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
        
        tk.Label( master=self, text="Stop by:").place( relx=0.02, rely=0.05 )
        
        self.time_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.time_entry.insert(0, self.engine_parameters.termination_parameters["time"])
        self.time_entry.place(relx=0.10, rely=0.11+0.005, relwidth=0.06)
        self.time_entry.config(state=tk.DISABLED)
        
        self.timescale_optionlist = [ option.value for option in EngineParameters.TIME_SCALE ]
        self.TimescaleOption = tk.StringVar(master=self)
        self.TimescaleOption.set( self.timescale_optionlist[0] )
        self.timescale_option = tk.OptionMenu(self, self.TimescaleOption, *self.timescale_optionlist)
        self.timescale_option.place(relx=0.17,rely=0.11-0.005, relwidth=0.07)
        self.timescale_option.config(state=tk.DISABLED)
        
        self.time_checkbox_var = tk.BooleanVar(master=self)
        self.time_checkbox = ttk.Checkbutton(master=self, text="Time", variable=self.time_checkbox_var, command=self._time_checkbox_command_)
        self.time_checkbox.config( state=tk.NORMAL )
        self.time_checkbox.place( relx=0.05,rely=0.11 )
        
        self.eval_entry = tk.Entry(master=self, state=tk.NORMAL)
        self.eval_entry.insert(0, self.engine_parameters.termination_parameters["evaluations"])
        self.eval_entry.place(relx=0.12, rely=0.17+0.005, relwidth=0.04)
        self.eval_entry.config(state=tk.DISABLED)
        
        self.eval_checkbox_var = tk.BooleanVar(master=self)
        self.eval_checkbox = ttk.Checkbutton(master=self, text="Evaluations", variable=self.eval_checkbox_var, command=self._eval_checkbox_command_)
        self.eval_checkbox.config( state=tk.NORMAL )
        self.eval_checkbox.place( relx=0.05,rely=0.17 )
        
        self.by_time_parameter = Parameter( name="by_time" )
        self.by_eval_parameter = Parameter( name="by_eval" )
        self.time_parameter = Integer( name="time", fancy_name="Time", lower_bound=1, upper_bound=99999999 )
        self.eval_parameter = Integer( name="evaluations", fancy_name="Evaluations", lower_bound=1, upper_bound=99999999 )
        self.time_scale_parameter = Parameter( name="time_scale" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.by_time_parameter,
                                                          widget_read_lambda=lambda: self.time_checkbox_var.get(),
                                                          variable_store_lambda=self._save_time_boolean,
                                                          variable_read_lambda=lambda: EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria,
                                                          widget_update_lambda=lambda var: self.time_checkbox_var.set(var)) )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.by_eval_parameter,
                                                          widget_read_lambda=lambda: self.eval_checkbox_var.get(),
                                                          variable_store_lambda=self._save_eval_boolean,
                                                          variable_read_lambda=lambda: EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria,
                                                          widget_update_lambda=lambda var: self.eval_checkbox_var.set(var)) )
        
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.eval_parameter,
                                                          widget_read_lambda=lambda: self.eval_entry.get(),
                                                          variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"evaluations":var}),
                                                          error_set_lambda=EntryInvalidator(self.eval_entry),
                                                          error_reset_lambda=EntryValidator(self.eval_entry),
                                                          variable_read_lambda=lambda: self.engine_parameters.termination_parameters["evaluations"],
                                                          widget_update_lambda=lambda var: self.__update_evaluations__(var)) )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.time_parameter,
                                                          widget_read_lambda=lambda: self.time_entry.get(),
                                                          variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"time":var}),
                                                          error_set_lambda=EntryInvalidator(self.time_entry),
                                                          error_reset_lambda=EntryValidator(self.time_entry),
                                                          variable_read_lambda=lambda: self.engine_parameters.termination_parameters["time"],
                                                          widget_update_lambda=lambda var: self.__update_time__(var)) )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.time_scale_parameter,
                                                          widget_read_lambda=lambda: self.TimescaleOption.get(),
                                                          variable_store_lambda=lambda var:self.engine_parameters.termination_parameters.update({"time_scale":var}),
                                                          variable_read_lambda=lambda: self.engine_parameters.termination_parameters["time_scale"],
                                                          widget_update_lambda=lambda var: self.__update_timescale__(var)) )
    
    
    def _save_time_boolean(self, var):
        
        if var:
            self.engine_parameters.temination_criteria.add( EngineParameters.TERMINATION_CRITERIA.TIME.value )
        else:
            if EngineParameters.TERMINATION_CRITERIA.TIME.value in self.engine_parameters.temination_criteria:
                self.engine_parameters.temination_criteria.remove( EngineParameters.TERMINATION_CRITERIA.TIME.value )
            
    def _save_eval_boolean(self, var):
        
        if var:
            self.engine_parameters.temination_criteria.add( EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value )
        else:
            if EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.engine_parameters.temination_criteria:
                self.engine_parameters.temination_criteria.remove( EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value )
        
    def _time_checkbox_command_(self):
        
        if self.time_checkbox_var.get():
            self.timescale_option.configure( state=tk.NORMAL )
            self.time_entry.configure( state=tk.NORMAL )
        else:
            self.timescale_option.configure( state=tk.DISABLED )
            self.time_entry.configure( state=tk.DISABLED )
            
    def _eval_checkbox_command_(self):
        
        if self.eval_checkbox_var.get():
            self.eval_entry.configure( state=tk.NORMAL )
        else:
            self.eval_entry.configure( state=tk.DISABLED )
