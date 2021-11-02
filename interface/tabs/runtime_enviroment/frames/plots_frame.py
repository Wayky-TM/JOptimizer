# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.runtime_enviroment.frames.runtime_frame import *


class PlotsFrame(RuntimeFrame):
        
    def __init__(self, master, engine_parameters: EngineParameters, *args, **kwargs):
        super(PlotsFrame, self).__init__(master=master, engine_parameters=engine_parameters, *args, **kwargs)
        
        tk.Label( master=self, text="#Runtime plots").place( relx=0.5, rely=0.5 )

