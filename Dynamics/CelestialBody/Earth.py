
import numpy as np
from Library.sgp4.earth_gravity import wgs72, wgs72old, wgs84
from Library.math_sup.tools_reference_frame import gstime
twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0


class Earth(object):
    def __init__(self, wgs):
        self.historical_gst = []
        self.h_gst = {}
        self.current_sideral = 0
        self.radiusearthkm = 6378.315 #km
        if wgs == 0:
            self.radiusearthkm = 6378.135  # km
        elif wgs == 1:
            self.radiusearthkm = 6378.135  # km
        elif wgs == 2:
            self.radiusearthkm = 6378.137  # km
        else:
            print('wgs not used')

    def gst_Update(self):
        self.historical_gst.append(self.current_sideral)

    def getSideral(self, current_jd):
        self.current_sideral = gstime(current_jd)

    def create_report(self):
        self.h_gst = {'GST [rad]': self.historical_gst}



