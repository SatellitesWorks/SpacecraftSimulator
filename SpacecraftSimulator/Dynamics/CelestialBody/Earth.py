
import numpy as np

class Earth(object):
    def __init__(self):
        self.gst = {}

    def gst_Update(self, addgst):
        self.gst['GST [grad]'] = addgst

