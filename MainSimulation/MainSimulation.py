
from Spacecraft.Spacecraft import Spacecraft
from Dynamics.SimTime import SimTime
from initial_config import initial_config
from Dynamics.Main_Dynamics import main_dynamics
from Dynamics.CelestialBody.Ephemeris import Ephemeris
import numpy as np
import pandas as pd
import datetime

twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0
rad2deg     = 1 / deg2rad


class MainSimulation(main_dynamics):
    def __init__(self, initial_properties = initial_config()):

        self.main_spacecraft  = Spacecraft(initial_properties[1], None)
        propagetor_properties = initial_properties[2]
        orbit_properties      = self.main_spacecraft.orbit_dynamics
        simulation_time       = SimTime(initial_properties[0])
        main_dynamics.__init__(self, propagetor_properties, orbit_properties, simulation_time)
        self.earth = Ephemeris()
        date = datetime.datetime.now()
        self.filename = date.strftime('%Y-%m-%d %H-%M-%S')

    def run_simulation(self):
        self.set_propagator()
        # Loop
        self.simulation_time.reset()
        while self.simulation_time.countTime <= self.simulation_time.end:
            self.simulation_time.progression()

            pos, vel = self.update_orbit()
            quat, omega = self.update_attitude()

            array_time, str_time = self.simulation_time.get_array_time()
            lat, long, alt = self.orbit_propagate.TransECItoGeo()

            if self.simulation_time.log_flag:
                self.main_spacecraft.update_spacecraft_dynamics(pos, vel, quat, omega, lat, long, alt)

                self.main_spacecraft.update_spacecraft_state(str_time, self.simulation_time.countTime)
                self.earth.gst_Update(self.orbit_propagate.current_side)
                self.simulation_time.log_flag = False

            # update time
            self.simulation_time.updateSimtime()

        # Data report to create dictionary
        self.main_spacecraft.create_data()

        # Save Dataframe pandas in csv file
        self.save_data()
        print('Finished')

    def save_data(self):
        master_data = {**self.main_spacecraft.master_data_satellite, **self.earth.gst}
        database = pd.DataFrame(master_data, columns=master_data.keys())
        print(database)

        database.to_csv("./Data/log/"+self.filename+".csv", index=False, header=True)
        print("Data created")

