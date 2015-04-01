import numpy as np
import matplotlib.pyplot as plt
import load_sp as lsp
import sys

Nx = 1024
Nxtarget = 12*128
Ny = 192
Nz = 288

def load_BLfieldraw(filename, N1, N2, N3):
    print 'Start loading.'
    N1 = N1/2+1
    BL = {}
    with open(filename, 'rb') as binfile:
        BL['time'] = np.fromfile(binfile, dtype=np.float64, count=1)
        print 'time = ', BL['time']
        BL['Lx'] = np.fromfile(binfile, dtype=np.float64, count=1)
        print 'Lx = ', BL['Lx']
        BL['Ly'] = np.fromfile(binfile, dtype=np.float64, count=1)
        print 'Ly = ', BL['Ly']
        BL['Nx2'] = np.fromfile(binfile, dtype=np.int32, count=1)
        print 'Nx2 = ', BL['Nx2']
        BL['Ny'] = np.fromfile(binfile, dtype=np.int32, count=1)
        print 'Ny = ', BL['Ny']
        BL['Nz'] = np.fromfile(binfile, dtype=np.int32, count=1)
        print 'Nz = ', BL['Nz']
        BL['thetaground'] = np.fromfile(binfile, dtype=np.float64, count=1)
        dum = np.fromfile(binfile,dtype=np.complex128)

    amount = N1*N2*N3
    shape  = (N1, N2, N3)
    shape2 = (N1, N2, N3-1)
    BL['uu'] = dum[:amount].reshape(shape, order='F')
    BL['vv'] = dum[amount:2*amount].reshape(shape, order='F')
    BL['ww'] = dum[2*amount:].reshape(shape2, order='F')
    BL['kx'] = [(i)/BL['Lx']*(2*np.pi) for i in range(N1/2)]
    BL['ky'] = [(i)/BL['Ly']*(2*np.pi) for i in range(-N2/2+1, N2/2)]
    print 'Spectral field loaded.'
    return BL

oldfield = load_BLfieldraw('BL_field.dat', Nx, Ny, Nz)
time = np.array(oldfield['time'],dtype=np.float64)
Lx = np.array(oldfield['Lx'], dtype = np.float64)
Ly = np.array(oldfield['Ly'], dtype = np.float64)
Nxtarget = np.array(Nxtarget, dtype=np.int32)
Ny = np.array(Ny, dtype=np.int32)
Nz = np.array(Nz, dtype=np.int32)
thetaground = np.array(oldfield['thetaground'], dtype = np.float64)
u = np.zeros((Nxtarget/2+1,Ny,Nz), dtype= np.complex128)
v = np.zeros((Nxtarget/2+1,Ny,Nz), dtype= np.complex128)
w = np.zeros((Nxtarget/2+1,Ny,Nz-1), dtype= np.complex128)
Nx = oldfield['uu'].shape[0]
u[:Nx,:,:] = oldfield['uu']
v[:Nx,:,:] = oldfield['vv']
w[:Nx,:,:] = oldfield['ww']
shape = (u.size,1)
shape2 = (w.size,1)
u=u.reshape(shape,order='F')
v=v.reshape(shape,order='F')
w=w.reshape(shape2,order='F')


newfilename = 'BL_field_new.dat'
with open(newfilename, 'wb') as binfile:
    time.tofile(binfile)
    Lx.tofile(binfile)
    Ly.tofile(binfile)
    Nxtarget.tofile(binfile)
    Ny.tofile(binfile)
    Nz.tofile(binfile)
    thetaground.tofile(binfile)
    u.tofile(binfile)
    v.tofile(binfile)
    w.tofile(binfile)
    

