import matplotlib.pyplot as plt
import numpy as np
from load_sp import load_plane

def plot_turbines_topview(filename):
    turbines = np.loadtxt(filename, skiprows=2)
    for turbine in turbines:
        xcoord = turbine[0]
        ycoord = turbine[1]
        radius = turbine[4]
        ycoords = np.array([ycoord - radius, ycoord + radius])
        plt.plot((xcoord, xcoord), ycoords, 'k', lw=2)

def plot_planexy(filename, Nx, Ny):
    # First read from setup
    return 0

def plot_planeyz(filename, Ny, Nz):
    return 0

def plot_planexz(filename, Nx, Nz):
    return 0




