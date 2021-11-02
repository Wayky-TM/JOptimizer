# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.runtime_enviroment.frames.runtime_frame import *


class StatisticsFrame(RuntimeFrame):
        
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(StatisticsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
        
        tk.Label( master=self, text="#Runtime Statistics").place( relx=0.5, rely=0.5 )
            
