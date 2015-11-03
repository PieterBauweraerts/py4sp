#!/usr/bin/env python

"""
transform_inflow_data.py: Python script used to transform a precursor inflow library to cases with other processor distributions.
"""

import numpy as np
import matplotlib.pyplot as plt
import load_sp as lsp

def print_summary():
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%        PARAMETER SUMMARY        %')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('   Lx = ', Lx, '   Lxfringe = ', Lxfringe)
    print('   Ly = ', Ly)
    print('   Nx = ', Nx)
    print('   Ny = ', Ny)
    print('   Nx32 = ', Nx32, '  i_start_glob = ', i_start_glob_fort)
    print('   Ny32 = ', Ny32)
    print('')
    print('-----------------------------------')
    print('    Original distribution           ')
    print('-----------------------------------')
    print('   no_procsx = ', npx_orig)
    print('   no_procsy = ', npy_orig)
    print('   orig: Nx32py = ', Nx32py_orig, ' Ny32px = ', Ny32px_orig)
    print(' offset Nx32py ')
    print(i32offsetpy_orig)
    print(' offset Ny32px ')
    print(j32offsetpx_orig)
    print('')
    print('-----------------------------------')
    print('    New distribution                ')
    print('-----------------------------------')
    print('   no_procsx = ', npx_new)
    print('   no_procsy = ', npy_new)
    print('   NEW: Nx32py = ', Nx32py_new, ' Ny32px = ', Ny32px_new)
    print(' offset Nx32py ')
    print(i32offsetpy_new)
    print(' offset Ny32px ')
    print(j32offsetpx_new)
    print('')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

Lx = 10.
Ly = 3.6
Nx = 384
Ny = 256
Nz = 200

Nx32 = int(3/2*Nx)
Ny32 = int(3/2*Ny)

npx_orig = 8
npy_orig = 24
npx_new = 16
npy_new = 16

Nx32py_orig = Nx32/npy_orig
Ny32px_orig = Ny32/npx_orig
Nx32py_new = Nx32/npy_new
Ny32px_new = Ny32/npx_new

if not (np.ceil([Nx32py_orig, Ny32px_orig]) == np.floor([int(Nx32py_orig), int(Ny32px_orig)])).all(): 
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('% UNEVEN DATA DISTRIBUTION ON OLD SIDE !     %')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
else:
    Nx32py_orig, Ny32px_orig = [int(Nx32py_orig), int(Ny32px_orig)]
if not (np.ceil([Nx32py_new, Ny32px_new]) == np.floor([Nx32py_new, Ny32px_new])).all(): 
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('% UNEVEN DATA DISTRIBUTION ON NEW SIDE !     %')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
else:
    Nx32py_new, Ny32px_new = [int(Nx32py_new), int(Ny32px_new)]

def generate_offset_array(nproc,N):
    offset = np.zeros(nproc,dtype=np.int32)
    for p in range(nproc):
        offset[p] = p*N
    return offset

j32offsetpx_orig = generate_offset_array(npx_orig, Ny32px_orig)
j32offsetpx_new = generate_offset_array(npx_new, Ny32px_new)
i32offsetpy_orig = generate_offset_array(npy_orig, Nx32py_orig)
i32offsetpy_new = generate_offset_array(npy_new, Nx32py_new)


percent_fringe = 10.
Lxfringe = Lx*(1 - percent_fringe/100)
dx32 = Lx/Nx32
dy32 = Ly/Ny32
i_start_glob_fort = int(np.ceil(Lxfringe/dx32))+1
i_start_glob_py = i_start_glob_fort-1

x = np.arange(start=0, stop=Lx, step=dx32)
y = np.arange(start=0, stop=Ly, step=dy32)

#---------------------------------------------------------------
# From here on we start the fringe region calculations..

# Orig side

# First, we determine the recycling procs
yranks = []
for py in range(npy_orig):
    if i32offsetpy_orig[py]+Nx32py_orig >= i_start_glob_py:
        yranks.append(py)

nxloc  = np.zeros(npy_orig,dtype=np.int32)
for py in yranks:
    if not i_start_glob_py <= i32offsetpy_orig[py]:
        print('n')
        nxloc[py] = int(Nx32py_orig - (i_start_glob_py - i32offsetpy_orig[py]))
    else:
        print('y')
        nxloc[py] = int(Nx32py_orig)
print('nxloc = ', nxloc)


procs_orig = []
for py in yranks:
    for px in range(npx_orig):
        procs_orig.append(py*npx_orig+px)


#print_summary()
#---------------------------------------------------------------

def loadfield(name, nx):
    with open(name, 'rb') as binfile:
        t = np.fromfile(binfile, dtype=np.float64, count=1)
        i = np.fromfile(binfile, dtype=np.int32, count=1)
        nx_file = np.fromfile(binfile, dtype=np.int32, count=1)
        print(t)
        print(i)
        print(nx_file)
        if not nx == nx_file:
            print('ERROR')
        print([nx, Ny32px_orig, Nz])
        field = np.fromfile(binfile, dtype=np.float64, count=nx*Ny32px_orig*Nz).reshape([nx, Ny32px_orig, Nz], order='F')
        print(field.size)
    return field


print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
print('Start loading data')
print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
srcdir = '/scratch/leuven/306/vsc30627/precursor_optim/'
destdir = '/scratch/leuven/306/vsc30627/precursor_optim_new/'
for py in yranks:
    for px in range(npx_orig):
        proc = py*npx_orig+px
        filename = srcdir+'u_precursor_rank_'+'{:04}'.format(proc)+'_t_0000010.dat'
        print('Filename = ', filename)
        xsize = nxloc[py]
        field = loadfield(filename, xsize)






