
import numpy as np

class Earth(object):
    def __init__(self):
        self.gst = []

    def gst_Update(self, addgst):
        self.gst.append(addgst)

    def get_gst(self):
        return np.array(self.gst)
