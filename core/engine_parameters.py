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

from jmetal.util.termination_criterion import TerminationCriterion, StoppingByEvaluations, StoppingByTime
from jmetal.util.evaluator import Evaluator, SequentialEvaluator, MultiprocessEvaluator, MapEvaluator
import datetime



class StoppingByDateTime(TerminationCriterion):
    
    def __init__(self, date_time: datetime.datetime):
        self.date_time = date_time

    def update(self, *args, **kwargs):
        pass
    
    @property
    def is_met(self):
        current_date = datetime.datetime.now()
        return self.date_time < current_date



class CompositeTerminationCriterion(TerminationCriterion):
    
    def __init__(self, criteria: List[TerminationCriterion]):
        self.termination_criteria = copy.deepcopy(criteria)
        
    def update(self, *args, **kwargs):
        
        for criterion in self.termination_criteria:
            criterion.update(*args, **kwargs)

    @property
    def is_met(self):
        return any( [ criterion.is_met() for criterion in self.termination_criteria ] )
        
        


class EngineParameters:
    
    class SUPPORTED_MODES(Enum):
        SINGLE_THREAD="Single thread"
        MULTITHREADED="Multithreaded"
        # MASTER_SLAVE="Master/Slave"
        # CLUSTER="Cluster"
    
    class TERMINATION_CRITERIA(Enum):
        EVALUATIONS="Evaluations"
        TIME="Time"
        DATE="Date"
        
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
        self.mode = EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value
        self.mode_parameters = defaultdict(lambda: "")
        self.mode_parameters["threads"] = 2
        
        self.temination_criteria={EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value}
        self.termination_parameters = defaultdict(lambda: "")
        self.termination_parameters["evaluations"] = 1000
        self.termination_parameters["time"] = 60
        self.termination_parameters["time_scale"] = EngineParameters.TIME_SCALE.SECONDS.value
        self.termination_parameters["datetime"] = datetime.datetime.now()
        
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
        
        
    def compile_termination_criterion(self) -> TerminationCriterion:
        
        if len( self.temination_criteria ) == 0:
            raise Exception("EngineParameters.compile_termination_criteria(): no termination criteria available")
            
        else:
            criteria = []
            
            if EngineParameters.TERMINATION_CRITERIA.TIME.value in self.temination_criteria:
                
                time = int(self.termination_parameters["time"])
                
                if self.termination_parameters["time_scale"] == EngineParameters.TIME_SCALE.MINUTES.value:
                    time *= 60
                    
                elif self.termination_parameters["time_scale"] == EngineParameters.TIME_SCALE.HOURS.value:
                    time *= 3600
                    
                elif self.termination_parameters["time_scale"] == EngineParameters.TIME_SCALE.DAYS.value:
                    time *= 86400
                
                criteria.append( StoppingByTime( max_seconds=time ) )
                
            if EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value in self.temination_criteria:
                criteria.append( StoppingByEvaluations( max_evaluations=int(self.termination_parameters["evaluations"]) ) )
                
            if EngineParameters.TERMINATION_CRITERIA.DATE.value in self.temination_criteria:
                criteria.append( StoppingByDateTime( date_time=self.termination_parameters["datetime"]) )
                
            
            if len(criteria)>1:
                return CompositeTerminationCriterion( criteria=criteria )
            
            return criteria[0]
            
            
    def compile_evaluator(self) -> TerminationCriterion:
            
        if EngineParameters.SUPPORTED_MODES.MULTITHREADED.value == self.mode:
            return MapEvaluator( processes=self.mode_parameters["threads"] )
        
        # elif EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value == self.mode:
        #     return SequentialEvaluator()
        
        return SequentialEvaluator()