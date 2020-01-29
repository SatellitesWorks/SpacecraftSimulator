
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd


def read_data(file_path):
    df = pd.read_csv(file_path, delimiter=',')
    sim_data = df
    return sim_data

Tk().withdraw()
filename = askopenfilename()
dataLog = read_data(filename)
print(dataLog[['sat_position_i(X)[m]', 'sat_position_i(Y)[m]', 'sat_position_i(Z)[m]']].values)