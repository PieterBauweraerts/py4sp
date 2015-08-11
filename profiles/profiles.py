import load_sp as lsp
import numpy as np
import matplotlib.pyplot as plt

class Profile:
    def __init__(self, filename):
        dum = lsp.load_BLcc(filename)
        self.z = dum['z']
        self.U = dum['U']
        self.V = dum['V']
        self.W = dum['W']
        self.uu = dum['uu']
        self.vv = dum['vv']
        self.ww = dum['ww']
        self.uv = dum['uv']
        self.uw = dum['uw']
        self.vw = dum['vw']
        
    def plot_loglaw(self, **kwargs):
        if('utau' in kwargs):
            ut = kwargs['utau']
        else:
            ut = 1
        if('label' in kwargs):
            lbl = kwargs['label']
        else:
            lbl = ''
        plt.semilogx( self.z / self.z.max(), self.U/ut, label=lbl)

    def calc_TI(self, **kwargs):
        if('ref' in kwargs):
            r = kwargs['ref']
        else:
            r = 1
        return np.sqrt(1./3.*(self.uu+self.vv+self.ww))/r

    def plot_TI(self, **kwargs):
        if ('ref' in kwargs):
            r = ref
        elif ('zhub' in kwargs):
            k1 = np.max(np.where(self.z <= kwargs['zhub']))
	    u1 = self.U[k1]
	    u2 = self.U[k1+1]
	    z1 = self.z[k1]
	    z2 = self.z[k1+1]
	    # Linear interpolation to exact hub height
            r = u1 + (kwargs['zhub'] - z1)/(z2 - z1)*(u2 - u1)
        else:
            r = 1.

        TI = self.calc_TI(ref=r)    

        if 'label' in kwargs:
            lab = kwargs['label']
        else:
            lab = ''

        if ('fmt' in kwargs):
            plt.plot(TI, self.z, fmt, label=lab)
        else:
            plt.plot(TI, self.z, label=lab)



