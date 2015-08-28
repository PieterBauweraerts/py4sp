import matplotlib.pyplot as plt
import load_sp as lsp
import numpy as np

# Class velocityfield, could make this inherit from greater vectorfield class in future...
class VelocityField:
    def __init__(self, filename, *varargs):
        dum = lsp.load_BLfield_real(filename)
        self.Nx = dum['Nx2']
        self.Ny = dum['Ny']
        self.Nz = dum['Nz']
        self.u = dum['u']
        self.v = dum['v']
        self.w = dum['w']
        self.Lx = dum['Lx']
        self.Ly = dum['Ly']
        self.x = np.linspace(0, self.Lx, self.Nx, endpoint=True)
        self.y = np.linspace(0, self.Ly, self.Ny, endpoint=True)
        if('zmesh' in varargs):
            self.z = np.loadtxt(zmesh)[2::2]
            self.Lz = np.max(self.z)
        else:
            self.Lz = 1.
            self.z = np.linspace(0, self.Lz, self.Nz)

    def topview(self,z):
        k = np.max(np.where(self.z<=z))
        plt.figure()
        plt.pcolormesh(self.x, self.y, np.transpose(self.u[:,:,k]))
        plt.show()

    def sideview(self,y):
        j = np.max(np.where(self.y<=y))
        plt.figure()
        plt.pcolormesh(self.x, self.z, np.transpose(self.u[:,j,:]))
        plt.show()

    def frontview(self,x):
        i = np.max(np.where(self.x<=x))
        plt.figure()
        plt.pcolormesh(self.y, self.z, np.transpose(self.u[i,:,:]))
        plt.show()
