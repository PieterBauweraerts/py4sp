import numpy as np

import os

tstart = 0.
tend   = 0.3
dt     = 0.001
times = np.arange(tstart, tend+dt, dt)
print('Times = ', times)
print('Nt    = ', times.size)

# Create the vdf file
command = 'vdfcreate -extents 0:0:0:6.283185307179586:3.141592653589793:1 -periodic 1:1:0 -dimension 256x256x128 -numts '+str(times.size)+' -vars3d u mydata.vdf'
print('Command = ', command)
os.system(command)
# Populate the vdf file

for i, t in enumerate(times):
    command = 'raw2vdf -varname u -ts '+str(i)+' -dbl mydata.vdf u_t_'+"{:6.4f}".format(t)+'.dat'
    print('Command = ', command)
    os.system(command)

