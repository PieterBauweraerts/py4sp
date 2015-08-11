"""
    Script for making a BL_field file twice as long by periodic repetition.

    Date: 08 Aug 2015

"""

import write_sp as wsp
import load_sp as lsp
import numpy as np
import matplotlib.pyplot as plt

bl_old = lsp.load_BLfield_real('BL_field_precursor.dat')

# Double the size and gridpoints
bl_new = bl_old.copy()
bl_new['Nx2'] = 2*bl_old['Nx2']
bl_new['Lx'] = 2*bl_old['Lx']

print bl_old['Nx2']
dumu = np.zeros((bl_new['Nx2'], bl_new['Ny'], bl_new['Nz']))
dumv = np.zeros((bl_new['Nx2'], bl_new['Ny'], bl_new['Nz']))
dumw = np.zeros((bl_new['Nx2'], bl_new['Ny'], bl_new['Nz']-1))

dumu[:bl_old['Nx2'],:,:] = bl_old['u']
dumv[:bl_old['Nx2'],:,:] = bl_old['v']
dumw[:bl_old['Nx2'],:,:] = bl_old['w']
dumu[bl_old['Nx2']:,:,:] = bl_old['u']
dumv[bl_old['Nx2']:,:,:] = bl_old['v']
dumw[bl_old['Nx2']:,:,:] = bl_old['w']

bl_new['u'] = dumu
bl_new['v'] = dumv
bl_new['w'] = dumw

wsp.write_BLfield(bl_new,'BL_field_precursor_4pi.dat')
