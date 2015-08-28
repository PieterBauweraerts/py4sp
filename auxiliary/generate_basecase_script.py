import os
import sys

cases = [ -3, 5, -5, 10, -10, 15, -15, 20, -20, 30, -30 ]
cases = [-3 , 5]

srcfolder = '/user/leuven/306/vsc30627/PYTHON/py4sp/auxiliary/HR/'
dstfolder = '/scratch/leuven/306/vsc30627/HORNS/HR'

for case in cases:
    casestr = str(case)
    print '###############################################################'
    print 'Generating case = ', casestr
    print '###############################################################'


    if casestr[0]=='-':
        sign = 'min'
        casestr_reduce = casestr[1:]
    else:
        sign = 'plus'
        casestr_reduce = casestr
    destination_folder = dstfolder+'_'+sign+casestr_reduce

    if os.path.exists(destination_folder):
        print 'Directory already exists!'
        sys.exit()
    command = 'cp -i -v -r HR_basecase '+destination_folder
    print 'Command copy = ', command
    os.system(command)

# First the windfarm
    command = 'cp '+srcfolder+'hornsrev_'+casestr+'.setup ' + destination_folder
    print 'Command windfarm = ', command
    os.system(command)
# Then the towerfarm
    command = 'cp '+srcfolder+'tower_hornsrev_'+casestr+'.setup ' +destination_folder
    print 'Command towerfarm = ', command
    os.system(command)

# Make the precursor folder
    command = 'cd '+destination_folder+' && mkdir precursor && cp BL_field_precursor.dat precursor/ && mv BL_field_precursor BL_field.dat && cd -'
    print 'Command BL_field = ', command
    os.system(command)
