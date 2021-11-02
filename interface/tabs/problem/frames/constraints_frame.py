# -*- coding: utf-8 -*-

import sys
sys.path.append(r"./../../../../../")

from interface.tabs.problem.frames.problem_frame import *


class ConstraintsFrame(ProblemFrame):
        
    def __init__(self, master, problem_parameters: ProblemParameters, *args, **kwargs):
        super(ConstraintsFrame, self).__init__(master=master, problem_parameters=problem_parameters, *args, **kwargs)
        
        tk.Label( master=self, text="#Constraints").place( relx=0.5, rely=0.5 )

