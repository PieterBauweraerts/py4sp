import numpy as np
import numpy.fft as fft

def c2r(field, N1, N2):
    res = np.fft.ifft(field, axis=1)
    res = np.fft.irfft(res, axis=0)
    res = res*N1*N2
    return res

def r2c(field, N1, N2):
    res = np.fft.rfft(field, axis=0)
    res = np.fft.fft(res, axis=1)
    return res
