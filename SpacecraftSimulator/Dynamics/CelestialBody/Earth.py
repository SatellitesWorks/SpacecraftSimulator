
import numpy as np
twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0;


class Earth(object):
    def __init__(self):
        self.gst = {}

    def gst_Update(self, current_gs):
        self.gst['GST [rad]'] = current_gs


