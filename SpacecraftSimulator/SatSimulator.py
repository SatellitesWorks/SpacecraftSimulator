# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:19:53 2020

@author: EO
"""

from MainSimulation.MainSimulation import MainSimulation
import sys
from PyQt5 import Qt
from Visualization.Viewer import Viewer

mainSim = MainSimulation()
dataLog = mainSim.run_simulation() # Datalog => *.Json

# Create a CSV file
mainSim.generate_report_csv()

# 3D and 2D visualization
app = Qt.QApplication(sys.argv)
window = Viewer(dataLog)
sys.exit(app.exec_())


