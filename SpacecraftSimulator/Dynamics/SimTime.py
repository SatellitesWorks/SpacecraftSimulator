# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 05:17:52 2020

@author: EO
"""
from datetime import datetime

class SimTime(object):

    def __init__(self,
                 time_properties):

        start_string        = time_properties['StartTime']
        print(start_string)
        datetime_array      = datetime.strptime(start_string,
                                                '%Y/%m/%d %H:%M:%S')
        self.start          = datetime_array.timestamp()
        self.start_array    = self.get_array_time()
        self.end            = time_properties['EndTime']
        self.step           = time_properties['StepTime']
        self.orbstep        = time_properties['OrbStepTime']
        self.logperiod      = time_properties['LogPeriod']
        self.simspeed       = time_properties['SimulationSpeed']
        self.propagatestep  = time_properties['PropStepSec']
        self.countTime = 0

    def get_array_time(self):
        datetime_array = datetime.fromtimestamp(self.start)
        start_array = [datetime_array.year,
                       datetime_array.month,
                       datetime_array.day,
                       datetime_array.hour,
                       datetime_array.minute,
                       datetime_array.second + datetime_array.microsecond/1e6]
        #print(datetime_array.minute, datetime_array.second)
        return start_array

    def update_time(self):
        self.start += self.step
        self.countTime += self.step
        self.start_array = self.get_array_time()

    def progression(self):
        return print(round(100*self.countTime/self.end, 2), '%')

    def reset(self):
        self.countTime = 0
