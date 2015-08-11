"""
    
    Script for generating a PSP-Wind compatible vertical grid using linspace (so no special grids or so...)

    Date: 07 Aug 2015

"""

import numpy as np

Lz = 0.5
Nz = 192/2
Nz2 = 2*Nz+1

z = np.linspace(0,Lz,Nz2)

filename = 'ZMESH_96'
with open(filename, 'w') as file:
    file.write(str(Nz2)+'\n')
    for k in range(z.size):
        file.write(str(z[k])+'\n')

