# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np
from .SubSystems import SubSystems
from Dynamics.Dynamics import Dynamics
from Dynamics.ClockGenerator import ClockGenerator


class Spacecraft(SubSystems):
    def __init__(self, dynamics_properties, components_properties, simtime):

        self.simtime = simtime
        self.dynamics = Dynamics(dynamics_properties, self.simtime)

        self.master_data_satellite = {}
        print('Spacecraft name: ' + str(dynamics_properties['Attitude']['spacecraft_name']))
        # Add components
        print('Spacecraft components:')
        SubSystems.__init__(self, components_properties, self.dynamics, self.simtime.stepsimTime)
        self.clockgenerator = ClockGenerator(self.subsystems, self.system_name)

    def update(self):
        # Dynamics updates
        self.dynamics.update()

        # Tick the time on component
        for i_ in range(int(self.simtime.stepsimTime*1000)):
            self.clockgenerator.tick_to_components()
        return

    def update_data(self):
        # Historical data
        self.save_log_values()
        self.dynamics.attitude.save_attitude_data()
        self.dynamics.orbit.save_orbit_data()
        self.dynamics.ephemeris.save_ephemeris_data()
        self.simtime.save_simtime_data()
        self.subsystems['ADCS'].save_data()

    def create_report(self):
        report_attitude = self.dynamics.attitude.get_log_values()
        report_orbit = self.dynamics.orbit.get_log_values()
        report_ephemerides = self.dynamics.ephemeris.earth.get_log_values()
        report_timelog = self.simtime.get_log_values()
        report_subsystems = {}

        for subsys in self.system_name:
            if self.subsystems[subsys] is not None:
                report_subsystems = {**report_subsystems,
                                     **self.subsystems[subsys].get_log_values(subsys)}

        self.master_data_satellite = {**report_timelog,
                                      **report_attitude,
                                      **report_orbit,
                                      **report_subsystems,
                                      **report_ephemerides}
