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
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        if('zmesh' in varargs):
            self.z = np.loadtxt(zmesh)[2::2]
            self.Lz = np.max(self.z)
        else:
            self.Lz = 1.
            self.z = np.linspace(0, self.Lz, self.Nz)
            self.dz = self.z[1] - self.z[0]

    def dudx(self, field):
        dudx = np.zeros(field.shape)
        # Central scheme
        for i in range(dudx.shape[0]):
            # Periodic boundary conditions,  wrap around
            indices = (i-1, i+1-(i+1)//dudx.shape[0])
            dudx[i,:,:] = (field[indices[1],:,:] - field[indices[0],:,:])/(2*self.dx)
        return dudx

    def dudx_spectral(self, field):
        spec = np.fft.fft(field, axis=0)
        kx   = np.fft.fftfreq(field.shape[0], self.dx)
        dudx_spec = np.zeros(spec.shape)
        for i in range(spec.shape[0]):
            dudx_spec[i,:,:] = 1j*kx[i]*spec[i,:,:]
        dudx = np.fft.ifft(dudx_spec, axis=0)*np.sqrt(field.shape[0])
        return dudx

    def dudy(self, field):
        dudy = np.zeros(field.shape)
        # Central scheme
        for j in range(dudy.shape[1]):
            indices = (j-1, j+1-(j+1)//dudy.shape[1])
            dudy[:,j,:] = (field[:,indices[1],:] - field[:,indices[0],:])/(2*self.dy)
        return dudy

    def dudz(self, field):
        dudz = np.zeros(field.shape)
        # Interior: central sceme
        for k in range(1,dudz.shape[2]-1):
            dudz[:,:,k] = (field[:,:,k+1] - field[:,:,k-1])/(2*self.dz)
        # Bottom: use a forward scheme
        dudz[:,:,0] = (field[:,:,1] - field[:,:,0])/(self.dz)
        # Top: use a backward scheme
        dudz[:,:,dudz.shape[2]-1] = (field[:,:,dudz.shape[2]-1] - field[:,:,dudz.shape[2]-2])/(self.dz)
        return dudz


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
