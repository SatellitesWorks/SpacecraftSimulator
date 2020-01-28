
from Spacecraft.Spacecraft import spacecraft
from Dynamics.SimTime import SimTime
from initial_config import initial_config
from Dynamics.Main_Dynamics import main_dynamics
from Dynamics.CelestialBody.Ephemeris import Ephemeris
import numpy as np

twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0
rad2deg     = 1 / deg2rad


class MainSimulation(main_dynamics):
    def __init__(self, initial_properties = initial_config()):

        self.main_spacecraft  = spacecraft(initial_properties[1], None)
        propagetor_properties = initial_properties[2]
        orbit_properties      = self.main_spacecraft.orbit_dynamics
        simtime_class       = SimTime(initial_properties[0])
        main_dynamics.__init__(self, propagetor_properties, orbit_properties, simtime_class)
        self.earth_gst = Ephemeris()

    def run_simulation(self):
        self.set_propagator()
        # Loop
        self.simtime.reset()

        while self.simtime.countTime <= self.simtime.end:
            self.simtime.progression()

            pos, vel = self.update_orbit()
            quat, omega = self.update_attitude()

            lat, long, alt = self.orbit_propagate.TransECItoGeo(self.simtime.get_array_time())

            self.main_spacecraft.save_dynamics(pos, vel, quat, omega, lat, long, alt)
            self.earth_gst.gst_Update(rad2deg*self.orbit_propagate.current_side)

            self.main_spacecraft.Update_state()


            # update time
            self.simtime.countTime += self.simtime.step
            self.simtime.update_time()

        # Data report
        self.generate_report_csv()
        return self.simtime, self.main_spacecraft.get_dynamics(), self.earth_gst.get_gst()

    def generate_report_csv(self):
        return 0