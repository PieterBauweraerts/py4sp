import numpy as np
import matplotlib.pyplot as plt

def generate(dx_turb=.004, Ct_tower=1.2, 
        Ct=4./3., timeconstant=.005, powerconstant=0., turbinescaling=1000., 
        plot=False, **kwargs):


    # Domain parameters
    Lfringe = np.pi/2
    Lx = np.pi+Lfringe
    Ly = 2*np.pi
    H = 1.
    Nx = Lx/np.pi*128
    Ny = 256
    
    # Turbine parameters
    D = .1
    zhub = .1
    
    # Farm parameters
    Nrows = 4
    Ncols = 12
    
    # Spacing
    if 'xturb' in kwargs:
        print('Taking turbine location from input values')
        Ncols = kwargs['Ncols']
        Nrows = kwargs['Nrows']
        xlocs = kwargs['xturb']
        ylocs = kwargs['yturb']
        Nturb = xlocs.size
        if not Nturb==Ncols*Nrows:
            print('Something wrong in input turbine locations!')
    else:
        print('Using default turbine locations')
        Nturb = Nrows*Ncols
        Sx = 7.85*D
        
        Sy = Ly/Ncols
        
        print(Sx/Sy)
        
        ylocs = np.zeros(Ncols)
        for col in range(Ncols):
            offset = Sy/2
            ylocs[col] = offset+col*Sy
        
        print('Y locations: ')
        print(ylocs)
        
        xlocs = np.zeros(Nrows)
        offset = Sx/2
        for row in range(Nrows):
            xlocs[row] = offset+row*Sx
        
        print('X locations: ')
        print(xlocs)
    
    # Now we generate the file
    
    if plot:
        plt.figure()

    # Windfarm file
    if 'filename_farm' in kwargs:
        filenamef = kwargs['filename_farm']
    else:
        filenamef = 'windfarm.setup'
    with open(filenamef,'w') as windfarmfile:
        windfarmfile.write(str(Nturb)+'\n')
        windfarmfile.write("{:10.7f}".format(Ct) + "{:15.7f}".format(powerconstant) + "{:15.7f}".format(timeconstant) + "{:15.4f}".format(turbinescaling)+'\n')
        for turbine in range(Nturb):
            row = int(turbine//Ncols)
            col = turbine - row*Ncols
            xt = xlocs[row]
            yt = ylocs[col]
            windfarmfile.write("{:10.7f}".format(xt) + "{:15.7f}".format(yt) + "{:15.7f}".format(zhub) + "{:15.7f}".format(.015)+"{:15.7f}".format(D/2)+"{:15.7f}".format(20.)+"{:15.7f}".format(0.)+"{:15.7f}".format(1.5)+'\n')
            if plot:
                plt.plot((xt, xt), (yt-D/2, yt+D/2), 'k', lw=2)
    
    # Towerfarm file
    if 'filename_tower' in kwargs:
        filenamet = kwargs['filename_tower']
    else:
        filenamet = 'tower.setup'
    with open(filenamet, 'w') as towerfile:
        towerfile.write(str(Nturb)+'\n')
        towerfile.write("{:10.7f}".format(Ct_tower) + "{:15.7f}".format(timeconstant)+'\n')
        for tower in range(Nturb):
            row = int(tower//Ncols)
            col = tower - row*Ncols
            xt = xlocs[row]+dx_turb
            yt = ylocs[col]
            towerfile.write("{:10.7f}".format(xt) + "{:15.7f}".format(yt) + "{:15.7f}".format(zhub) + "{:15.7f}".format(.0045000)+"{:15.7f}".format(zhub)+"{:15.7f}".format(1.5)+'\n')
            if plot:
                plt.plot((xt, yt),(xt,yt),'or',mec='r')

    if plot:
        plt.ion()
        plt.show()
        plt.ylim((0,Ly))
        plt.xlim((0,Lx))



# Default generator...
# generate()
