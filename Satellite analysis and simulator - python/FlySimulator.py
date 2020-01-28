# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:19:53 2020

@author: EO
"""

from MainSimulation.MainSimulation import MainSimulation
import sys
from PyQt5 import Qt
from Visualization.visualization3D import Main3D

mainSim = MainSimulation()
dataLog = mainSim.run_simulation()

# Create a CSV file
mainSim.generate_report_csv()

# 3D and 2D visualization
app = Qt.QApplication(sys.argv)
window = Main3D(dataLog)
sys.exit(app.exec_())


