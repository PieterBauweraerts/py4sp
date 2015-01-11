import numpy as np

def load_NSp(filename):
    dummy = np.loadtxt(filename, skiprows=1)
    NSp = {}
    NSp['t'] = dummy[:,0]
    NSp['U'] = dummy[:,1]
    NSp['V'] = dummy[:,2]
    NSp['W'] = dummy[:,3]
    NSp['Etot'] = dummy[:,4]
    NSp['Eturb'] = dummy[:,5]
    NSp['sf_mean_x'] = dummy[:,6]
    NSp['sf_Um'] = dummy[:,6]
    NSp['sf_sgs'] = dummy[:,6]
    return NSp

def load_BLcc(filename):
    dummy = np.loadtxt(filename, skiprows=2)
    BLinst = {}
    BLinst['z']  = dummy[:,0]
    BLinst['U']  = dummy[:,1]
    BLinst['V']  = dummy[:,2]
    BLinst['W']  = dummy[:,3]
    BLinst['uu'] = dummy[:,4]
    BLinst['vv'] = dummy[:,5]
    BLinst['ww'] = dummy[:,6]
    BLinst['uv'] = dummy[:,7]
    BLinst['uw'] = dummy[:,8]
    BLinst['vw'] = dummy[:,9]
    return BLinst

def load_plane(filename, N1, N2):
    # Load the data into memory
    u = np.loadtxt(filename)
    # Cast into vector
    u = np.reshape(u, [np.size(u), 1])
    # Rearrange, taking into account Fortran memory layout
    u = np.reshape(u, [N1, N2], order='F')
    return u

def load_spectral_field(filename, N1, N2, N3, N4):
    dummy = np.loadtxt(filename, skiprows=7)
    spectral = {}
    d = dummy[:,1] + dummy[:,1]*1j
    spectral['u'] = np.reshape(d[0:N1*N2*N3], [N1, N2, N3], order='F')
    spectral['v'] = np.reshape(d[N1*N2*N3:2*N1*N2*N3], [N1, N2, N3], order='F')
    spectral['w'] = np.reshape(d[2*N1*N2*N3:], [N1, N2, N3-1], order='F')
    return spectral

def load_field(filename, N1, N2, N3, N4):
    # Load the data into memory
    u = np.loadtxt(filename)
    # Cast into vector
    u = np.reshape(u, [np.size(u), 1])
    # Rearrange, taking into account Fortran memory layout
    u = np.reshape(u, [N1, N2, N3, N4], order='F')
    return u

def load_windpower(filename):
    dummy = np.loadtxt(filename)
    time = dummy[:,0]
    power = dummy[:,2::2]
    return time, power

def load_BLfieldstat(filename, N1, N2, N3):
    N4 = 11
    # Load the data into memory
    u = np.loadtxt(filename, skiprows=1)
    # Cast into vector
    u = np.reshape(u, [np.size(u), 1])
    # Create dictionary
    stat = {}
    u = np.reshape(u, [N1, N2, N3, N4], order='F')
    stat['u'] = u[:,:,:,0]
    stat['v'] = u[:,:,:,1]
    stat['w'] = u[:,:,:,2]
    stat['uu'] = u[:,:,:,3]
    stat['vv'] = u[:,:,:,4]
    stat['ww'] = u[:,:,:,5]
    stat['uv'] = u[:,:,:,6]
    stat['uw'] = u[:,:,:,7]
    stat['vw'] = u[:,:,:,8]
    stat['p'] = u[:,:,:,9]
    stat['wst'] = u[:,:,:,10]
    return stat

def load_stream_spec(filename, Lx, Nx2, Nz):
    dummy = np.loadtxt(filename, comments='%')
    spec = {}
    spec['k']  = [(i)/Lx*(2*np.pi) for i in range(Nx2/2)]
    spec['z']  = dummy[0:Nz-1,0]
    spec['uu'] = dummy[0:Nz-1,1:]
    spec['vv'] = dummy[Nz:2*Nz-1,1:]
    spec['ww'] = dummy[2*Nz-1:,1:]
    spec['zst'] = dummy[2*Nz-1:,0]
    return spec

