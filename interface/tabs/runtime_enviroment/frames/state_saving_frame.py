# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.runtime_enviroment.frames.runtime_frame import *


class StateSavingFrame(RuntimeFrame):
        
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(StateSavingFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
        
        tk.Label( master=self, text="#Runtime state saving").place( relx=0.5, rely=0.5 )
        
