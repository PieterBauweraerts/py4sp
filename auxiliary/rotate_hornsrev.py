import numpy as np
import matplotlib.pyplot as plt
import load_sp as lsp

wf = lsp.load_windfarm('hornsrev.setup')

wf = np.loadtxt('hornsrev.setup', skiprows=2)

wfmx = np.mean(wf[:,0])
wfmy = np.mean(wf[:,1])

wfx = wf[:,0]
wfy = wf[:,1]

dx_tower = .004

print 'wfmx = ', wfmx
print 'wfmy = ', wfmy

theta = 3.
thetas = (3, -3, 5, -5, 7.5, -7.5, 10, -10, 15, -15, 20, -20, 25, -25, 30, -30 )

for theta in thetas:
    thetarad = theta*np.pi/180.
    R = np.array(([np.cos(thetarad), -np.sin(thetarad)], 
        [np.sin(thetarad), np.cos(thetarad)]))
    
    # Re-origin
    wfx = wfx - wfmx
    wfy = wfy - wfmy
    
    # Rotate
    wfxnew = wfx*R[0,0] + wfy*R[0,1] + wfmx
    wfynew = wfx*R[1,0] + wfy*R[1,1] + wfmy
    
    wfx += wfmx
    wfy += wfmy
    
    for i in range(wfxnew.size):
        plt.plot(wfxnew, wfynew, 'or')
        plt.plot(wfx, wfy, 'ob')
    
    
    # Write
    # Now we generate the file
    Ct = 4./3.
    Ct_tow = 1.2
    Ct = 1.527864045
    dx_turb = .004
    timeconstant = .00
    powerconstant = 0.
    turbinescaling = 1000.
    plt.figure()
    Nturb = 80
    Ncols = 8
    Nrows = 10
    zhub = .07
    D = .08
    Ly = 10.
    Lx = 10.
    with open('HR/hornsrev_'+str(theta)+'.setup','w') as windfarmfile:
        windfarmfile.write(str(Nturb)+'\n')
        windfarmfile.write("{:10.7f}".format(Ct) + "{:15.7f}".format(powerconstant) + "{:15.7f}".format(timeconstant) + "{:15.4f}".format(turbinescaling)+'\n')
        for turbine in range(Nturb):
            row = turbine/Ncols
            col = turbine - row*Ncols
            xt = wfxnew[turbine]
            yt = wfynew[turbine]
            windfarmfile.write("{:10.7f}".format(xt) + "{:15.7f}".format(yt) + "{:15.7f}".format(zhub) + "{:15.7f}".format(.015)+"{:15.7f}".format(D/2)+"{:15.7f}".format(20.)+"{:15.7f}".format(0.)+"{:15.7f}".format(1.5)+'\n')
            plt.plot((xt, xt), (yt-D/2, yt+D/2), 'k', lw=2)
    
    plt.ylim((0,Ly))
    plt.xlim((0,Lx))
    plt.savefig('hornsrev_'+str(theta)+'.png')

    with open('HR/tower_hornsrev_'+str(theta)+'.setup','w') as windfarmfile:
        windfarmfile.write(str(Nturb)+'\n')
        windfarmfile.write("{:10.7f}".format(Ct_tow) + "{:15.7f}".format(timeconstant)+'\n')
        for turbine in range(Nturb):
            row = turbine/Ncols
            col = turbine - row*Ncols
            xt = wfxnew[turbine]+dx_turb
            yt = wfynew[turbine]
            windfarmfile.write("{:10.7f}".format(xt) + "{:15.7f}".format(yt) + "{:15.7f}".format(zhub) + "{:15.7f}".format(.0045000)+"{:15.7f}".format(zhub)+"{:15.7f}".format(1.5)+'\n')

# Plot
