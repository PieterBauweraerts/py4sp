import matplotlib.pyplot as plt
import numpy as np
import load_sp as lsp
from load_sp import load_plane

def plot_turbines_topview(filename):
    turbines = np.loadtxt(filename, skiprows=2)
    for turbine in turbines:
        xcoord = turbine[0]
        ycoord = turbine[1]
        radius = turbine[4]
        ycoords = np.array([ycoord - radius, ycoord + radius])
        plt.plot((xcoord, xcoord), ycoords, 'k', lw=2)

def plot_planexy(filename, Nx, Ny):
    # First read from setup
    return 0

def plot_planeyz(filename, Ny, Nz):
    return 0

def plot_planexz(filename, Nx, Nz):
    return 0

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


def make_movie(time_array,N1,N2):
    
    for t in time_array:
        plt.clf()
        tstr = "{:6.4f}".format(t)
        print 'Loading t = ', tstr
        basefilename = '_zplane_k013_t_'
        filenameu = 'u'+basefilename+tstr+'.dat'
        filenamev = 'v'+basefilename+tstr+'.dat'
        u = lsp.load_plane(filenameu, N1=N1, N2=N2)
        v = lsp.load_plane(filenamev, N1=N1, N2=N2)
        plt.pcolormesh(np.transpose(np.sqrt(u**2+v**2)))
        plt.clim((0, 30))
        plt.colorbar()
        plt.savefig('u_'+tstr+'.png')

