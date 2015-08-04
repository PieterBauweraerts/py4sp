import numpy as np
import fft_sp as fft

def write_BLfield(field, filename, spectral=False):
    print '##########################################'
    print '# Reading field to file ', filename
    print '# Input field is spectral? ', spectral
    print '# ------------------------------------------'
    print '# Field information'
    print '# ------------------------------------------'
    print '# time  = ', field['time']
    print '# Lx    = ', field['Lx']
    print '# Ly    = ', field['Ly']
    print '# Nx2   = ', field['Nx2']
    print '# Ny    = ', field['Ny']
    print '# Nz    = ', field['Nz']
    print '# theta = ', field['thetaground']
    print '##########################################'

    with open(filename,'wb') as binfile:
        field['time'].tofile(binfile)
        field['Lx'].tofile(binfile)
        field['Ly'].tofile(binfile)
        field['Nx2'].tofile(binfile)
        field['Ny'].tofile(binfile)
        field['Nz'].tofile(binfile)
        field['thetaground'].tofile(binfile)

        if spectral:
            field['uu'].tofile(binfile)
            field['vv'].tofile(binfile)
            field['ww'].tofile(binfile)

        else:
            fft.r2c(field['u'], field['Nx2'], field['Ny']).tofile(binfile)
            fft.r2c(field['v'], field['Nx2'], field['Ny']).tofile(binfile)
            fft.r2c(field['w'], field['Nx2'], field['Ny']).tofile(binfile)

