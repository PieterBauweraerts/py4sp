import numpy as np
import fft_sp as fft

def write_BLfield(field, filename, spectral=False):
    """
    function write_BLfield

    Parameters
    ------------
    field: dict
        structure produced by load_BLfield function from load_sp.py
    filename: str
        filename to which the current field data should be written
    spectral: bool, optional
        flag whether field data is in Fourier space (default is False)
    """
    print('##########################################')
    print('# Writing field to file ', filename)
    print('# Input field is spectral? ', spectral)
    print('# ------------------------------------------')
    print('# Field information')
    print('# ------------------------------------------')
    print('# time  = ', field['time'])
    print('# Lx    = ', field['Lx'])
    print('# Ly    = ', field['Ly'])
    print('# Nx2   = ', field['Nx2'])
    print('# Ny    = ', field['Ny'])
    print('# Nz    = ', field['Nz'])
    print('# theta = ', field['thetaground'])
    print('##########################################')

    with open(filename,'wb') as binfile:
        field['time'].astype(dtype=np.float64).tofile(binfile)
        field['Lx'].astype(dtype=np.float64).tofile(binfile)
        field['Ly'].astype(dtype=np.float64).tofile(binfile)
        field['Nx2'].astype(dtype=np.int32).tofile(binfile)
        field['Ny'].astype(dtype=np.int32).tofile(binfile)
        field['Nz'].astype(dtype=np.int32).tofile(binfile)
        field['thetaground'].astype(dtype=np.float64).tofile(binfile)

        if spectral:
            field['uu'].reshape((field['uu'].size,1), order='F').tofile(binfile)
            field['vv'].reshape((field['vv'].size,1), order='F').tofile(binfile)
            field['ww'].reshape((field['ww'].size,1), order='F').tofile(binfile)

        else:
            # Convert to wavenumber space
            uu =fft.r2c(field['u'], field['Nx2'], field['Ny']).astype(np.complex128)
            vv =fft.r2c(field['v'], field['Nx2'], field['Ny']).astype(np.complex128)
            ww =fft.r2c(field['w'], field['Nx2'], field['Ny']).astype(np.complex128)
            # Reshape and write to file
            uu = uu.reshape((uu.size,1), order='F').tofile(binfile)
            vv = vv.reshape((vv.size,1), order='F').tofile(binfile)
            ww = ww.reshape((ww.size,1), order='F').tofile(binfile)



