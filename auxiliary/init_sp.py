"""Initialization functions for python postprocessing

Author : W. Munters
Date   : December 30 2014

"""

import numpy as np

def read_setup():
    #Function reading values from NS.setup file
    with open('NS.setup', 'r') as file:
        raw = file.readlines()
    #Strip the trailing characters etc.
    for lineno, text in enumerate(raw):
        raw[lineno] = raw[lineno].rstrip()
    #Put data in dictionary
    setup = dict()
    setup['case'] = raw[1]
    setup['therm'] = raw[3]
    setup['ekman'] = raw[5]
    setup['Nx2'] = int(raw[7].split()[0])
    setup['Ny'] = int(raw[7].split()[1]) 
    setup['Lx'] = float(raw[9].split()[0].replace('d0',''))
    setup['Ly'] = float(raw[9].split()[1].replace('d0',''))
    setup['Re'] = raw[11]
    if setup['case'] == 'Windfarm' or setup['case'] == 'BL':
        setup['Re'] = 'inf'
    # setup['drive'] = raw[13] ' Driving force'
    setup['tstart'] = float(raw[15].replace('d0','')) 
    setup['tstop']  = float(raw[17].replace('d0',''))
    setup['tpost']  = float(raw[19].replace('d0',''))
    setup['tpost2'] = float(raw[21].replace('d0',''))
    setup['tpost3'] = float(raw[23].replace('d0',''))
    setup['zmesh']  = raw[25]
    # setup['uinit'] = raw[27] ' Initial profile'
    setup['uinit']  = raw[29].split()[0]
    setup['upinit'] = raw[29].split()[1]
    setup['bc']     = raw[31]
    setup['model']  = int(raw[33])
    setup['Cs']     = float(raw[35].replace('d0',''))
    # setup['case'] = raw[37] ' Dealiasing '
    setup['CFLc']   = float(raw[39].replace('d0',''))
    setup['CFLd']   = float(raw[41].replace('d0',''))
    setup['stats']  = raw[43]
    # setup['case'] = raw[45]
    # setup['case'] = raw[47]
    setup['tseries'] = raw[49]
    setup['turbmod'] = int(raw[51])
    # setup['case'] = raw[53]
    # setup['case'] = raw[55]
    # setup['case'] = raw[57]
    # setup['case'] = raw[59]
    # setup['case'] = raw[61]
    return setup

def meshxy(setup):
    x = linspace(0,setup['Lx'],setup['Nx2'])
    y = linspace(0,setup['Ly'],setup['Ny'])
    return x,y
