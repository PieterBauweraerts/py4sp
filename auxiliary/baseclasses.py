import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import integrate
from scipy import ndimage
class WindFarm:
    """ A simple class to save different spwind fields
    """    
    def __init__(self, data, bounds, turbs):
        self.turbs  = turbs
        self.bounds = bounds
        self.fields = []
        for key in self.data:
            self.fields = Field(data[key], bounds)  

class Grid:
    """ A simple class to define your grid
    """
    def __init__(self, bounds, dims):
        self.min    = bounds['min']
        self.max    = bounds['max']

        self.resol  = tuple((np.array(self.max) - np.array(self.min))/(np.array(dims)-1))
        self.dims   = dims
        self.Ndim   = len(self.dims)

        self.coord = ()
        for i in range(self.Ndim):
            self.coord = self.coord + \
                        (np.linspace(self.min[i], 
                                     self.max[i],
                                     self.dims[i]),) 

class Field:
    """ A simple class to save spwind fields 
    """
    def __init__(self, data, bounds):
        # Initiate a Field object
        #
        self.data   = data
        self.dims   = data.shape
        self.bounds = bounds
        self.grid   = Grid(self.bounds, self.dims)
        self.Ndim   = len(self.dims)

    def __add__(self, other):
        dataAdd = self.data + other.data
        FieldClass = self.__class__
        return FieldClass(dataAdd, self.bounds)  

    def __radd__(self,other):
        return self.__add__(other) 

    def __sub__(self,other):
        dataAdd = self.data - other.data
        FieldClass = self.__class__
        return FieldClass(dataAdd, self.bounds)  

    def __mul__(self, other):
        if type(self) == type(other):
            dataMul = self.data * other.data
        elif (isinstance(other,float)) or (isinstance(other,int)):
            dataMul = self.data * other
        # print type(other)
        FieldClass = self.__class__
        return FieldClass(dataMul, self.bounds)  

    def __rmul__(self,other):
        return self.__mul__(other) 

    def __neg__(self):
        dataNeg = -self.data
        FieldClass = self.__class__
        return FieldClass(dataNeg, self.bounds)  

    def __div__(self, other):
        dataDiv = self.data / other
        FieldClass = self.__class__
        return FieldClass(dataDiv, self.bounds)  

    def diff(self, dim):
        # print self.grid.resol[dim]
        if self.Ndim == 1:
            diff = np.gradient(self.data, self.grid.resol[dim])
        else:  
            diff = np.gradient(self.data, self.grid.resol[dim])[dim]
        # print 'dim', dim
        # print 'diff', diff
        # print 'diff.shape', diff.shape
        FieldClass  = self.__class__
        return FieldClass(diff, self.bounds)

    def removeDim(self):
        # Converts a 3D object to a 2D object, object should first 
        # have a one value in one direction
        shape = self.data.shape
        bounds = self.bounds
        shapeNew = ()
        boundsNew = {}
        boundsNew['min'] = ()
        boundsNew['max'] = ()
        for i in range(self.Ndim):
            if shape[i] != 1:
                shapeNew = shapeNew + (shape[i],)
                boundsNew['min'] = boundsNew['min'] + (bounds['min'][i],)
                boundsNew['max'] = boundsNew['max'] + (bounds['max'][i],)
        dataNew = np.reshape(self.data, shapeNew, order='F')
        #print shapeNew
        if len(shapeNew) == 1:
            return Field1D(dataNew, boundsNew)
        elif len(shapeNew) == 2:
            return Field2D(dataNew, boundsNew)
        elif len(shapeNew) == 3:
            return Field3D(dataNew, boundsNew)

    def cutBU(self, boundsNew, dimsNew):
        # Changes the resolution of the field
        #
        gridNew = Grid(boundsNew, dimsNew)
        fieldNew = {}

        # Make an interpolation object for evaluating the field
        f = interpolate.RegularGridInterpolator(self.grid.coord, self.data)

        # Make full set of coordinates for the evaluation of the field 
        # at the new grid points
        gridCoordNewFull = np.meshgrid(*gridNew.coord, indexing = 'ij')

        coords = np.reshape(gridCoordNewFull,(self.Ndim,-1)).T

        dataCut = np.reshape(f(coords), dimsNew)

        FieldClass = self.__class__
        return FieldClass(dataCut, boundsNew).removeDim()

    def cut(self, boundsNew, dimsNew):
        # Changes the resolution of the field
        lboundNew = np.array(boundsNew['min'])
        uboundNew = np.array(boundsNew['max'])
        lboundOld = np.array(self.bounds['min'])
        uboundOld = np.array(self.bounds['max'])
        lowBound_MapCoord = tuple((lboundNew-lboundOld)/(uboundOld-lboundOld)*np.subtract(self.dims,1))
        upBound_MapCoord = tuple((uboundNew-lboundOld)/(uboundOld-lboundOld)*np.subtract(self.dims,1))

        boundsNew_MapCoord = {'min': lowBound_MapCoord,'max': upBound_MapCoord}
        gridNew = Grid(boundsNew_MapCoord, dimsNew)

        # Make full set of coordinates for the evaluation of the field 
        # at the new grid points
        gridCoordNewFull = np.meshgrid(*gridNew.coord, indexing = 'ij')
        coords = np.reshape(gridCoordNewFull,(self.Ndim,-1))

        # Interpolate data at coords
        dataCut = np.reshape(ndimage.map_coordinates(self.data, coords), dimsNew)

        # Make new field object
        FieldClass = self.__class__
        return FieldClass(dataCut, boundsNew).removeDim()
    
    def AV(self, dim):
        AV = np.average(self.data, axis = dim)
        dims = list(self.dims)
        dims[dim] = 1
        AV = np.reshape(AV, dims)

        AVObj = self.removeDim()
        FieldClass  = self.__class__
        AVObj = FieldClass(AV, self.bounds)
        return AVObj.removeDim()

    def integrate(self):
        integral = self.data
        # print 'shape', self.data.shape
        # print 'grid', self.grid.coord[0]
        for i in range(self.Ndim):
            integral = integrate.simps(integral, self.grid.coord[i], axis = 0)
            # print 'mean', mean
        return integral

    def periodAV(self, dim, period):
        shapePeriod = list(self.dims)
        shapePeriod[dim] = self.dims[dim]/period

        periodAV = np.zeros(shapePeriod)

        lowBound = np.zeros(self.Ndim)
        upBound  = list(shapePeriod)
        for i in range(period):
            fieldPartInd = []
            for j in range(self.Ndim):
                fieldPartInd.append(slice(lowBound[j],upBound[j]))
            # print self.data[fieldPartInd].shape, lowBound[dim], upBound[dim]
            periodAV    += self.data[fieldPartInd]

            lowBound[dim] += shapePeriod[dim]
            upBound[dim]  += shapePeriod[dim]

        periodAV /= period

        extension      = np.ones(self.Ndim)
        extension[dim] = period
        periodAV         = np.tile(periodAV, extension)

        # FrontInd = []
        # for i in range(self.Ndim):
        #     if i != dim:
        #         FrontInd.append(slice(0,self.dims[i]))
        #     else:
        #         FrontInd.append(slice(0,1))
        # periodAV = np.concatenate((periodAV, periodAV[FrontInd]), axis = dim )
        FieldClass  = self.__class__
        return FieldClass(periodAV, self.bounds)

    def cellAV(self, dim, period):

        shapeCell = list(self.dims)
        shapeCell[dim] = self.dims[dim]/period

        shapeCellAV = list(self.dims)
        shapeCellAV[dim] = period
        cellAV = np.zeros(shapeCellAV)
        cellAVInd = []
        for i in range(self.Ndim):
            cellAVInd.append(slice(0,shapeCellAV[i]))

        lowBound = np.zeros(self.Ndim)
        upBound  = list(shapeCell)
        boundsNew = {}
        boundsNew['min'] = self.bounds['min']
        boundsNew['max'] = list(self.bounds['max'])
        boundsNew['max'][dim] = (boundsNew['max'][dim]-boundsNew['min'][dim])*float((period-1))/period +\
                                boundsNew['min'][dim]
        boundsNew['max'] = tuple(boundsNew['max'])

        for i in range(period):
            fieldPartInd = []
            for j in range(self.Ndim):
                fieldPartInd.append(slice(lowBound[j],upBound[j]))
            cellAVInd[dim] = i

            # print fieldPartInd, cellAVInd
            # print self.data.shape
            # print self.Ndim, dim, np.mean(self.data[fieldPartInd], axis = dim).shape   
            cellAV[cellAVInd] = np.mean(self.data[fieldPartInd], axis = dim)    

            lowBound[dim] += shapeCell[dim]
            upBound[dim]  += shapeCell[dim]
        FieldClass  = self.__class__
        return FieldClass(cellAV, self.bounds)


class Field1D(Field):
    """ A simple class to save 1D fields 
    """
    def plot(self, ax = None, save = None, legend = None, 
             marker = None, limits = None, xlabel = None, ylabel = None, title = None, linestyle = None):
        if ax == None:
            fig = plt.figure()
	    ax = fig.add_subplot(111)
        # print 'ID', self.grid.coord[0], self.data
        ax.plot(self.grid.coord[0], self.data, label= legend, marker = marker, linestyle = linestyle)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if limits is not None:
            ax.set_xlim(limits[0:2])
            ax.set_ylim(limits[2:4])
        lgd = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., ncol = 3, columnspacing= -0.5, labelspacing = 0.25)
        # ax.set_title(title)
        if save is not None:
            plt.savefig(save['savedir'] + save['savename'], bbox_extra_artists=(lgd,), bbox_inches='tight', format='eps', dpi=1000)
        return 0

class Field2D(Field):
    """ A simple class to save 2D fields 
    """
    def plot(self, savedir, savename):
        plt.figure()

        plt.imshow(self.data.T, 
                   cmap = 'jet', 
                   aspect = 'auto',
                   origin = 'lower')
        plt.title(savename)
        plt.savefig(savedir + savename)
        return 0

    def plotContour(self, savedir, savename, color = 'k', xlabel = '$x/H$', ylabel = '$y/H$'):
        plt.figure()

        [meshdir1,meshdir2] = np.meshgrid(*self.grid.coord)
        levels =  np.array([12])
        plt.contour(meshdir1, meshdir2, self.data.T, levels,
                    colors = color)

        plt.xlabel(xlabel, fontsize=20)
        plt.ylabel(ylabel, fontsize=20)
        plt.savefig(savedir + savename)
        return 0


class Field3D(Field):
    """ A simple class to save 3D fields 
    """
    def convTo2D(self):
        # Converts a 3D object to a 2D object, object should first 
        # have a one value in one direction
        shape3D = self.data.shape
        bounds3D = self.bounds
        shape2D = ()
        bounds2D = {}
        bounds2D['min'] = ()
        bounds2D['max'] = ()
        for i in range(len(shape3D)):
            if shape3D[i] != 1:
                shape2D = shape2D + (shape3D[i],)
                bounds2D['min'] = bounds2D['min'] + (bounds3D['min'][i],)
                bounds2D['max'] = bounds2D['max'] + (bounds3D['max'][i],)
        data2D = np.reshape(self.data, shape2D)

        return Field2D(data2D, bounds2D)
    
def EnergyBalance(volBounds, fluxes_x, fluxes_z, vols):
    netFlux_x = {}
    for name, flux_x in fluxes_x.iteritems():
        dim_z = round((volBounds['max'][1]-volBounds['min'][1])/flux_x.grid.resol[1])

        flux_x1Bounds = {}
        flux_x1Bounds['min'] = (volBounds['min'][0], volBounds['min'][1])        
        flux_x1Bounds['max'] = (volBounds['min'][0], volBounds['max'][1])     
    
        flux_x1 = flux_x.cut(flux_x1Bounds, (1, dim_z)).integrate()

        flux_x2Bounds = {}
        flux_x2Bounds['min'] = (volBounds['max'][0], volBounds['min'][1])        
        flux_x2Bounds['max'] = (volBounds['max'][0], volBounds['max'][1]) 

        flux_x2 = flux_x.cut(flux_x2Bounds, (1, dim_z)).integrate()
        # print flux_x2
        netFlux_x[name] = flux_x2-flux_x1

    netFlux_z = {}
    for name, flux_z in fluxes_z.iteritems():
        dim_x = round((volBounds['max'][0]-volBounds['min'][0])/flux_z.grid.resol[0])

        flux_z1Bounds = {}
        flux_z1Bounds['min'] = (volBounds['min'][0], volBounds['min'][1])        
        flux_z1Bounds['max'] = (volBounds['max'][0], volBounds['min'][1])     
    
        flux_z1 = flux_z.cut(flux_z1Bounds, (dim_x, 1)).integrate()

        flux_z2Bounds = {}
        flux_z2Bounds['min'] = (volBounds['min'][0], volBounds['max'][1])        
        flux_z2Bounds['max'] = (volBounds['max'][0], volBounds['max'][1]) 

        flux_z2 = flux_z.cut(flux_z2Bounds, (dim_x, 1)).integrate()

        netFlux_z[name] =  flux_z2-flux_z1
    netVol = {}
    for name, vol in vols.iteritems():
        dim_x = round((volBounds['max'][0]-volBounds['min'][0])/vol.grid.resol[0])
        dim_z = round((volBounds['max'][1]-volBounds['min'][1])/vol.grid.resol[1])

        netVol[name] = vol.cut(volBounds, (dim_x, dim_z)).integrate()

    return netFlux_x, netFlux_z, netVol
