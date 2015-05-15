import numpy as np
import fft_sp as fft
import load_sp as lsp

# Class velocityfield, could make this inherit from greater vectorfield class in future...
class VelocityField:
    def __init__(self, filename):
        dum = lsp.load_BLfield_real(filename)
        self.Nx = dum['Nx2']
        self.Ny = dum['Ny']
        self.Nz = dum['Nz']
        self.u = dum['u']
        self.v = dum['v']
        self.w = dum['w']
        self.x = np.linspace(0, dum['Lx'], self.Nx, endpoint=True)
        self.y = np.linspace(0, dum['Ly'], self.Ny, endpoint=True)

#    def divergence(self):
#        dum = np.zeros(self.Nx, self.Ny, self.Nz, 3)
#        dum[:,:,:,0] = self.u
#        dum[:,:,:,1] = self.y
#        dum[:,:,:,2] = self.w
#        grad = np.gradient(dum)
#        return 
