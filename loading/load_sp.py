import numpy as np
import fft_sp as fft

class Turbine:
    def __init__(self, turb):
        self.x = turb[0]
        self.y = turb[1]
        self.H = turb[2]
        self.r = turb[4]

def load_windfarm(filename):
    dummy = np.loadtxt(filename, skiprows=2)
    windfarm = [] # Empty list
    for turbine_data in dummy:
        windfarm.append(Turbine(turbine_data))
    return windfarm

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
    d = dummy[:,0] + dummy[:,1]*1j
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

def load_windpower(filename,Nrows,Ncols):
    dummy = np.loadtxt(filename,comments='%')
    time = dummy[:,0]
    powerdum = -dummy[:,2::2]
    # Reshape data into windfarm format, this assumes the turbines are numbered row per row
    power = np.zeros((Nrows, Ncols, time.size))
    for num in range(Nrows*Ncols):
        row = int(num)/int(Ncols)
        col = num - row*Ncols
        power[row, col, :] = powerdum[:, num]
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

def load_1D_spectrum(filename, L, N, Nz):
    dummy = np.loadtxt(filename, comments='%')
    spec = {}
    spec['k']  = np.array([(i)/L*(2*np.pi) for i in range(N/2)])
    spec['z']  = dummy[0:Nz-1,0]
    spec['uu'] = dummy[0:Nz-1,1:]
    spec['vv'] = dummy[Nz:2*Nz-1,1:]
    spec['zst']= dummy[2*Nz-1:,0]
    spec['ww'] = dummy[2*Nz-1:,1:]
#    if(np.size(spec['uu'][1,:]) > np.size(spec['k'])):
#        spec['uu'] = np.delete(spec['uu'],np.size(spec['uu'][1,:])-1, axis=1)
#        spec['vv'] = np.delete(spec['vv'],np.size(spec['uu'][1,:])-1, axis=1)
#        spec['ww'] = np.delete(spec['ww'],np.size(spec['uu'][1,:])-1, axis=1)
    return spec

def load_field_bin(filename, N1, N2, N3):
    stat = {}
    with open(filename, 'rb') as binfile:
        dumm = np.fromfile(binfile, dtype=np.float64)
        shape = (N1,N2,N3,3)
        dumm = dumm.reshape(shape, order='F')
        stat['u']   = dumm[:,:,:,0]
        stat['v']   = dumm[:,:,:,1]
        stat['w']   = dumm[:,:,:,2]
    return stat

def load_BLfieldstat_bin(filename, N1, N2, N3):
    N4 = 11
    stat = {}
    with open(filename, 'rb') as binfile:
        stat['nsamp'] = np.fromfile(binfile, dtype=np.int32, count=1)
        stat['time_interv'] = np.fromfile(binfile, dtype=np.float32, count=1)
        stat['time_incurr'] = np.fromfile(binfile, dtype=np.float32, count=1)
        dumm = np.fromfile(binfile, dtype=np.float64)
        shape = (N1,N2,N3,N4)
        dumm = dumm.reshape(shape, order='F')
        stat['u']   = dumm[:,:,:,0]
        stat['v']   = dumm[:,:,:,1]
        stat['w']   = dumm[:,:,:,2]
        stat['uu']  = dumm[:,:,:,3]
        stat['vv']  = dumm[:,:,:,4]
        stat['ww']  = dumm[:,:,:,5]
        stat['uv']  = dumm[:,:,:,6]
        stat['uw']  = dumm[:,:,:,7]
        stat['vw']  = dumm[:,:,:,8]
        stat['p']   = dumm[:,:,:,9]
        stat['wst'] = dumm[:,:,:,10]
    return stat

def load_BLfield_real(filename):
    #N1 = N1/2+1
    BL = {}
    with open(filename, 'rb') as binfile:
        BL['time'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Lx'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Ly'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Nx2'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['Ny'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['Nz'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['thetaground'] = np.fromfile(binfile, dtype=np.float64, count=1)
        dum = np.fromfile(binfile,dtype=np.complex128)
    print '######################'
    print 'BL_field.dat data:'
    print 'time         = ', BL['time']
    print 'Lx           = ', BL['Lx']
    print 'Ly           = ', BL['Ly']
    print 'Nx2          = ', BL['Nx2']
    print 'Ny           = ', BL['Ny']
    print 'Nz           = ', BL['Nz']
    print 'thetaground  = ', BL['thetaground']
    print 'restsize     = ', dum.size
    print '######################'

    N1 = BL['Nx2']/2+1
    N2 = BL['Ny']
    N3 = BL['Nz']

    amount = N1*N2*N3
    shape  = (N1, N2, N3)
    shape2 = (N1, N2, N3-1)
    uu = dum[:amount].reshape(shape, order='F')
    vv = dum[amount:2*amount].reshape(shape, order='F')
    ww = dum[2*amount:].reshape(shape2, order='F')
    
    BL['u']  = fft.c2r(uu, N1, N2)
    BL['v']  = fft.c2r(vv, N1, N2)
    BL['w']  = fft.c2r(ww, N1, N2)

    return BL

def load_BLfield_real_ascii(filename, N1, N2, N3):
    N1 = N1/2+1
    BL = {}
    dum = np.loadtxt(filename, comments='%')
    dum = dum[:,0] + 1j*dum[:,1]

    amount = N1*N2*N3
    shape  = (N1, N2, N3)
    shape2 = (N1, N2, N3-1)
    uu = dum[:amount].reshape(shape, order='F')
    vv = dum[amount:2*amount].reshape(shape, order='F')
    ww = dum[2*amount:].reshape(shape2, order='F')
    
    BL['u']  = fft.c2r(uu, N1, N2)
    BL['v']  = fft.c2r(vv, N1, N2)
    BL['w']  = fft.c2r(ww, N1, N2)

    return BL

def cube_show_slider(cube, axis=2, **kwargs):
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button, RadioButtons
    # check dim
    if not cube.ndim == 3:
        raise ValueError("cube should be an ndarray with ndim == 3")
    # generate figure
    fig = plt.figure()
    ax = plt.subplot(111)
    fig.subplots_adjust(left=0.25, bottom=0.25)

    # select first image
    s = [slice(0, 1) if i == axis else slice(None) for i in xrange(3)]
    im = cube[s].squeeze()

    # display image
    l = ax.imshow(im, **kwargs)
    axcolor = 'lightgoldenrodyellow'
    ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
        
    slider = Slider(ax, 'Axis %i index' % axis, 0, cube.shape[axis] - 1,
                                        valinit=0, valfmt='%i')
            
    def update(val):
        ind = int(slider.val)
        s = [slice(ind, ind + 1) if i == axis else slice(None) for i in xrange(3)]
        im = cube[s].squeeze()
        l.set_data(im, **kwargs)
        fig.canvas.draw()
        
    slider.on_changed(update)
                                                                
    plt.show()

def load_BLfield(filename, post=False):
    BL = {}
    with open(filename, 'rb') as binfile:
        BL['time'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Lx'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Ly'] = np.fromfile(binfile, dtype=np.float64, count=1)
        BL['Nx2'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['Ny'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['Nz'] = np.fromfile(binfile, dtype=np.int32, count=1)
        BL['thetaground'] = np.fromfile(binfile, dtype=np.float64, count=1)
        dum = np.fromfile(binfile,dtype=np.complex128)

    N1 = BL['Nx2']/2+1
    N2 = BL['Ny']
    N3 = BL['Nz']

    amount = N1*N2*N3
    shape  = (N1, N2, N3)
    shape2 = (N1, N2, N3-1)
    BL['uu'] = dum[:amount].reshape(shape, order='F')
    BL['vv'] = dum[amount:2*amount].reshape(shape, order='F')
    BL['ww'] = dum[2*amount:].reshape(shape2, order='F')
    BL['kx'] = [(i)/BL['Lx']*(2*np.pi) for i in range(N1/2)]
    BL['ky'] = [(i)/BL['Ly']*(2*np.pi) for i in range(-N2/2+1, N2/2)]
    
    BLpostkeys = ['uu','vv','ww']
    if post:
        for key in BLpostkeys:
        # Take the logs
            BL[key] = np.log(np.abs(BL[key]))   
        # Shift spectrum to match correct locations
            BL[key] = np.fft.fftshift(BL[key],axes=(1,))
        # Remove the defunct wavenumbers
            BL[key] = BL[key][:N1-1, 1:] 

    return BL

def head_BLfield(filename):
    head = {}
    with open(filename, 'rb') as binfile:
        head['time'] = np.fromfile(binfile, dtype=np.float64, count=1)
        head['Lx'] = np.fromfile(binfile, dtype=np.float64, count=1)
        head['Ly'] = np.fromfile(binfile, dtype=np.float64, count=1)
        head['Nx2'] = np.fromfile(binfile, dtype=np.int32, count=1)
        head['Ny'] = np.fromfile(binfile, dtype=np.int32, count=1)
        head['Nz'] = np.fromfile(binfile, dtype=np.int32, count=1)
        head['thetaground'] = np.fromfile(binfile, dtype=np.float64, count=1)
    return head
