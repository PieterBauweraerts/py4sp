import numpy as np
import matplotlib.pyplot as plt

Nx = 128 
Ny = 128
Nxtarget = 256
Nytarget = 256
Nz = 80

#-----------------------------------------------------------------------------------------------#
# Auxiliary function definitions                                                                #
#-----------------------------------------------------------------------------------------------#
def load_field(filename, N1, N2, N3):
    print 'Reading from file'
    dumr = np.loadtxt(filename, comments='%')
    dum = dumr[:,0] + 1j*dumr[:,1]
    amount = N1*N2*N3
    shape1 = (N1,N2,N3)
    shape2 = (N1,N2,N3-1)
    uu = dum[:amount].reshape(shape1,order='F')
    vv = dum[amount:2*amount].reshape(shape1,order='F')
    ww = dum[2*amount:].reshape(shape2,order='F')
    return uu,vv,ww

def write_field(filename, uu, vv, ww):
    print 'Writing to file...'
    with open(filename, 'w') as blfile:
        blfile.write('% \n')
        blfile.write('% \n')
        blfile.write('% \n')
        blfile.write('% \n')
        blfile.write('% \n')
        blfile.write('% \n')
        blfile.write('% \n')
        writearray = np.vstack([uu,vv,ww])
#        for entry in uu:
#            blfile.write(np.array_str(np.real(entry)).strip('[]') + '   '+ np.array_str(np.imag(entry)).strip('[]') + ' \n')
        np.savetxt(blfile, writearray, fmt=['%25.17f',  '%25.17f'])
#        for entry in vv
#            blfile.write(np.array_str(np.real(entry)).strip('[]') + '   '+ np.array_str(np.imag(entry)).strip('[]') + ' \n')
#        for entry in ww:
#            blfile.write(np.array_str(np.real(entry)).strip('[]') + '   '+ np.array_str(np.imag(entry)).strip('[]') + ' \n')


#-----------------------------------------------------------------------------------------------#
# Body of the interpolator script                                                               #
#-----------------------------------------------------------------------------------------------#

# Load the data
uu, vv, ww = load_field('BL_field.dat', Nx/2+1, Ny, Nz)

# Shift the field in y direction such that ky=0 lies in the middle..
uu = np.fft.fftshift(uu, axes=(1,))
vv = np.fft.fftshift(vv, axes=(1,))
ww = np.fft.fftshift(ww, axes=(1,))

# Expand 
print 'Expanding Fourier space fields.'
starty = (Nytarget-Ny)/2
stopy   = starty+Ny
field_big_uu = np.zeros((Nxtarget/2+1,Nytarget,Nz),dtype=np.complex128)
field_big_vv = np.zeros((Nxtarget/2+1,Nytarget,Nz),dtype=np.complex128)
field_big_ww = np.zeros((Nxtarget/2+1,Nytarget,Nz-1),dtype=np.complex128)
field_big_uu[:Nx/2+1, starty:stopy, :] = uu
field_big_vv[:Nx/2+1, starty:stopy, :] = vv
field_big_ww[:Nx/2+1, starty:stopy, :] = ww 

# Shift the field back again..
field_big_uu = np.fft.fftshift(field_big_uu, axes=(1,))
field_big_vv = np.fft.fftshift(field_big_vv, axes=(1,))
field_big_ww = np.fft.fftshift(field_big_ww, axes=(1,))

# Check if mean profiles are still intact...
uu = np.fft.fftshift(uu, axes=(1,))
plt.figure()
print uu[0,0,:]
print '--'
print field_big_uu[0,0,:]
plt.plot(uu[0,0,:], 'or', label='old')
plt.plot(field_big_uu[0,0,:],'k',label='new')
plt.legend()
plt.show()

# Reshape into a vector for writing..
field_big_uu = field_big_uu.reshape( (field_big_uu.size,1), order='F')
field_big_vv = field_big_vv.reshape( (field_big_vv.size,1), order='F')
field_big_ww = field_big_ww.reshape( (field_big_ww.size,1), order='F')

field_big_uu_write = np.zeros((field_big_uu.size,2))
field_big_uu_write[:,0] = np.real(field_big_uu)[:,0]
field_big_uu_write[:,1] = np.imag(field_big_uu)[:,0]
field_big_vv_write = np.zeros((field_big_vv.size,2))
field_big_vv_write[:,0] = np.real(field_big_vv)[:,0]
field_big_vv_write[:,1] = np.imag(field_big_vv)[:,0]
field_big_ww_write = np.zeros((field_big_ww.size,2))
field_big_ww_write[:,0] = np.real(field_big_ww)[:,0]
field_big_ww_write[:,1] = np.imag(field_big_ww)[:,0]
write_field('BL_field_interpolated.dat', field_big_uu_write, field_big_vv_write, field_big_ww_write )


