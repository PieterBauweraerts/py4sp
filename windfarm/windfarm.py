import load_sp as lsp
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

class Windfarm:
    def __init__(self, Nrows, Ncols, path='./', windpowerfile='Windpower.dat'):
        self.path                       = path
        self.Nrows                      = Nrows
        self.Ncols                      = Ncols
        self.turbines                   = load_windfarm(path+'windfarm.setup', self.Nrows, self.Ncols)
        self.wptime, self.windpower     = load_windpower(path+windpowerfile, self.Nrows, self.Ncols)
        self.meanwindpower              = np.mean(self.windpower, 2)
        self.totalpower                 = np.sum(np.sum(self.windpower,0),0)
        self.power_per_row              = np.mean(self.meanwindpower,1) 
        self.power_per_col              = np.mean(self.meanwindpower,0) 
        self.rows                       = np.arange(Nrows)
        self.cols                       = np.arange(Ncols)

        self.Sx = 0.
        self.Sy = 0.

    def plot_power_per_row(self, show=True):
        plt.plot(self.rows, self.power_per_row/self.power_per_row[0])
        plt.xlabel('rows')
        plt.ylabel('P')
        if show:
            plt.show()

    def plot_total_power(self, show=True):
        plt.plot(self.wptime, self.totalpower)
        plt.xlabel('rows')
        plt.ylabel('P_tot')
        if show:
            plt.show()

    def plot_turbines(self, show=True,color='k'):
        for turbine in self.turbines:
            plt.plot((turbine.x, turbine.x), (turbine.y-turbine.r, turbine.y+turbine.r),color,lw=2)
        if show:
            plt.show()


class Turbine:
    def __init__(self, turb, row, col):
        self.x = turb[0]
        self.y = turb[1]
        self.H = turb[2]
        self.r = turb[4]
        self.row = row
        self.col = col


def load_windfarm(filename, Nrows, Ncols):
    if os.path.exists(filename):
        dummy = np.loadtxt(filename, skiprows=2)
    #    rows, cols = get_rows_and_cols(dummy[0,:], dummy[1,:], Nrows, Ncols)
    #    Nrows = rows.size
    #    Ncols = cols.size
    #    print 'Amount of rows    = ', Nrows
    #    print 'Amount of columns = ', Ncols
        windfarm = [] # Empty list
        for index, turbine_data in enumerate(dummy):
            row, col = get_row_col(index, Ncols)
            windfarm.append(Turbine(turbine_data, row, col))
        return windfarm
    else:
        print 'windfarm.setup not found'
        return 0

def load_windpower(filename, Nrows, Ncols):
    if os.path.exists(filename):
        dummy = np.loadtxt(filename,comments='%')
        time = dummy[:,0]
        powerdum = -dummy[:,2::2]
        # Reshape data into windfarm format, this assumes the turbines are numbered row per row
        power = np.zeros((Nrows, Ncols, time.size))
        for num in range(Nrows*Ncols):
            row, col = get_row_col(num, Ncols)
            power[row, col, :] = powerdum[:, num]
        return time, power
    else:
        print 'Windpower file not found.'
        return np.zeros((1)), np.zeros((Nrows, Ncols, 1))

def get_row_col(index, Ncols):
    row = int(index)/int(Ncols)
    col = index - row*Ncols
    return row, col

#def get_rows_and_cols(x, y):
#    # Works only for regular windfarms!
#    xt1 = x[0]
#    yt1 = y[0]
#    Nrows = y.count(y1) # aka how many times does the same spanwise location occur?
#    Ncols = x.count(x1)
#    if not Nrows*Ncols == x.size: 
#        print 'Windfarm seems to be slightly irregular, row and column classification will be based on spanwise locations'
#        Ncols = x.size/Nrows
#    rows = np.zeros(Nrows)
#    cols = np.zeros(Ncols)

