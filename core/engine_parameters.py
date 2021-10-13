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
import yaml
import os

from enum import Enum
from abc import *
from typing import List
from collections import defaultdict

from jmetal.util.termination_criterion import TerminationCriterion, StoppingByEvaluations, StoppingByTime
from jmetal.util.evaluator import Evaluator, SequentialEvaluator, MultiprocessEvaluator, MapEvaluator
import datetime

import util.type_check as TC


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
        
        """ Mode """
        self.mode = EngineParameters.SUPPORTED_MODES.SINGLE_THREAD.value
        self.mode_parameters = defaultdict(lambda: "")
        self.mode_parameters["threads"] = 2
        
        """ Termination """
        self.temination_criteria={EngineParameters.TERMINATION_CRITERIA.EVALUATIONS.value}
        self.termination_parameters = defaultdict(lambda: "")
        self.termination_parameters["evaluations"] = 1000
        self.termination_parameters["time"] = 60
        self.termination_parameters["time_scale"] = EngineParameters.TIME_SCALE.SECONDS.value
        self.termination_parameters["datetime"] = datetime.datetime.now()
        
        """ Runtime save """
        self.save_runtime_criteria = []
        self.save_runtime_status = defaultdict(lambda: "")
        self.save_runtime_status["on_pause"] = False
        self.save_runtime_status["every_pause"] = False
        self.save_runtime_status["folder_path"] = ""
        
        """ Runtime stats """
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
    
    def save_state(self,
                   dir_path: str,
                   file_name: str = "engine_parameters.yaml"):
        
        if TC.is_dir( dir_path ):
            
            output = {}
            
            """ Mode """
            output["mode"] = {}
            output["mode"]["option"] = self.mode
            output["mode"]["parameters"] = {}
            
            for key, value in self.mode_parameters.items():
                output["mode"]["parameters"][key] = value
                
            """ Termination """
            output["termination"] = {}
            output["termination"]["criteria"] = self.temination_criteria
            output["termination"]["parameters"] = {}
            
            for key, value in self.termination_parameters.items():
                output["termination"]["parameters"][key] = value
            
            """ Runtime save """
            output["save_runtime"] = {}
            output["save_runtime"]["criteria"] = self.save_runtime_criteria
            output["save_runtime"]["parameters"] = {}
            
            for key, value in self.save_runtime_status.items():
                output["save_runtime"]["parameters"][key] = value
            
            """ Runtime stats """
            output["runtime_statistics"] = {}
            output["runtime_statistics"]["criteria"] = self.runtime_statistics_criteria
            output["runtime_statistics"]["parameters"] = {}
            
            for key, value in self.runtime_statistics.items():
                output["runtime_statistics"]["parameters"][key] = value
                
                
            with open( os.path.join(dir_path, file_name), 'w') as file:
                documents = yaml.dump(output, file)
        
        else:
            raise ValueError("Path '%s' is not a valid directory" % (dir_path))
            
    def load_state(self,
                   dir_path: str,
                   file_name: str = "engine_parameters.yaml"):
        
        if TC.is_file( os.path.join(dir_path, file_name) ):
            
            yaml_file = open( os.path.join(dir_path, file_name), 'r')
            yaml_content = yaml.safe_load(yaml_file)
            
            """ Mode """
            self.mode = yaml_content["mode"]["option"]
            
            for key, value in yaml_content["mode"]["parameters"].items():
                self.mode_parameters[key] = value
                
            """ Termination """
            self.temination_criteria = yaml_content["termination"]["criteria"]
            
            for key, value in yaml_content["termination"]["parameters"].items():
                self.termination_parameters[key] = value
                
            """ Runtime save """
            self.save_runtime_criteria = yaml_content["save_runtime"]["criteria"]
            
            for key, value in yaml_content["save_runtime"]["parameters"].items():
                self.save_runtime_status[key] = value
                
            """ Runtime stats """
            self.runtime_statistics_criteria = yaml_content["runtime_statistics"]["criteria"]
            
            for key, value in yaml_content["runtime_statistics"]["parameters"].items():
                self.runtime_statistics[key] = value    
            
        
        else:
            raise ValueError("File '%s' is not a valid file" % (os.path.join(dir_path, file_name)))
        