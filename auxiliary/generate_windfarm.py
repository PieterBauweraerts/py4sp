import numpy as np
import matplotlib.pyplot as plt

# Domain parameters
Lfringe = np.pi/2
Lx = np.pi+Lfringe
Ly = 2*np.pi
H = 1.
Nx = Lx/np.pi*128
Ny = 256

# Turbine parameters
D = .1
zhub = .1

# Farm parameters
Nrows = 4
Ncols = 12
Nturb = Nrows*Ncols

# Spacing
Sx = 7.85*D

Sy = Ly/Ncols

print Sx/Sy

ylocs = np.zeros(Ncols)
for col in range(Ncols):
    offset = Sy/2
    ylocs[col] = offset+col*Sy

print 'Y locations: '
print ylocs

xlocs = np.zeros(Nrows)
offset = Sx/2
for row in range(Nrows):
    xlocs[row] = offset+row*Sx

print 'X locations: '
print xlocs

# Now we generate the file
Ct = 4./3.
timeconstant = .05
powerconstant = 0.
turbinescaling = 1000.
plt.figure()
with open('windfarm.setup.gen','w') as windfarmfile:
    windfarmfile.write(str(Nturb)+'\n')
    windfarmfile.write("{:10.7f}".format(Ct) + "{:15.7f}".format(powerconstant) + "{:15.7f}".format(timeconstant) + "{:15.4f}".format(turbinescaling)+'\n')
    for turbine in range(Nturb):
        row = turbine/Ncols
        col = turbine - row*Ncols
        xt = xlocs[row]
        yt = ylocs[col]
        windfarmfile.write("{:10.7f}".format(xt) + "{:15.7f}".format(yt) + "{:15.7f}".format(zhub) + "{:15.7f}".format(.015)+"{:15.7f}".format(D/2)+"{:15.7f}".format(20.)+"{:15.7f}".format(0.)+"{:15.7f}".format(1.5)+'\n')
        plt.plot((xt, xt), (yt-D/2, yt+D/2), 'k', lw=2)

plt.ylim((0,Ly))
plt.xlim((0,Lx))
plt.ion()
plt.show()
