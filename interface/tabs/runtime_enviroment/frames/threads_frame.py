# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.runtime_enviroment.frames.runtime_frame import *

class ThreadsFrame(RuntimeFrame):
        
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(ThreadsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
        
        self.threads_label = tk.Label(master=self, text="Threads")
        self.threads_label.place( relx=0.02, rely=0.05 )
        
        self.threads_optionlist = [i for i in range(1,multiprocessing.cpu_count()+1)]
        self.ThreadsOption = tk.IntVar(master=self)
        self.ThreadsOption.set( self.threads_optionlist[0] )
        self.threads_option = tk.OptionMenu(self, self.ThreadsOption, *self.threads_optionlist)
        self.threads_option.place(relx=0.08,rely=0.05-0.005, relwidth=0.06)
        self.threads_option.config(state=tk.NORMAL)
        
        self.threads_parameter = Parameter( name="threads", fancy_name="Threads" )
        
        self.parameters_bindings.append( ParameterBinding(parameter=self.threads_parameter,
                                                          widget_read_lambda=lambda: self.ThreadsOption.get(),
                                                          variable_store_lambda=lambda var: self.engine_parameters.mode_parameters.update( {"threads":var} ),
                                                          variable_read_lambda=lambda: self.engine_parameters.termination_parameters["threads"],
                                                          widget_update_lambda=lambda var: self.ThreadsOption.set(var)) )
        
