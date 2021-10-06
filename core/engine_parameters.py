# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 23:29:45 2021

@author: Wayky
"""

import sys
sys.path.append(r"./..")

import copy
import random
import math

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict



class EngineParameters:
    
    class SUPPORTED_MODES(Enum):
        SINGLE_THREAD="Single thread"
        # PARALLEL="Parallel"
        # MASTER_SLAVE="Master/Slave"
        # CLUSTER="Cluster"
    
    class TERMINATION_CRITERIA(Enum):
        EVALUATIONS="Evaluations"
        TIME="Time"
        
    class TIME_SCALE(Enum):
        SECONDS="Seconds"
        MINUTES="Minutes"
        HOURS="Hours"
        DAYS="Days"
        
    class SAVE_CRITERIA(Enum):
        PAUSE="Pause"
        EVALUATIONS="Evaluations"
        
    class RUNTIME_STATS_CRITERIA(Enum):
        BY_TIME="Time"
        BY_EVALUATIONS="Evaluations"
    
    def __init__(self):
        
        self.temination_criteria=[EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value]
        self.termination_parameters = defaultdict(lambda: "")
        self.termination_parameters["evaluations"] = 1000
        self.termination_parameters["time"] = 60
        self.termination_parameters["time_scale"] = EngineParameters.TIME_SCALE.SECONDS.value
        
        self.save_runtime_criteria = []
        self.save_runtime_status = defaultdict(lambda: "")
        self.save_runtime_status["on_pause"] = False
        self.save_runtime_status["every_pause"] = False
        self.save_runtime_status["folder_path"]
        
        self.runtime_statistics_criteria = [EngineParameters.RUNTIME_STATS_CRITERIA.BY_TIME.value]
        self.runtime_statistics = defaultdict(lambda: "")
        self.runtime_statistics["time"] = 10
        self.runtime_statistics["time_escale"] = EngineParameters.TIME_SCALE.SECONDS.value
        self.runtime_statistics["evaluations"] = 100
        
        
        
        