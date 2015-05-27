#!/usr/bin/env python

## generates a random (beautiful perlin noise) DEM as netcdf file
## to be used with fluxrouting

## generated fields are
## x,y      coordinates
## geometry
## surface, bed, thickness
##
## meltrates, base_temp

from __future__ import division
from netCDF4 import Dataset
import numpy as np
import time
import os

from noise import pnoise2, snoise2

class GeometryData:
    """Class that contains geometry data for fluxrouting"""

    def InitFromSurface(self,H_s):
        """ assumes base is zero"""

        self.nx = H_s.shape[0]
        self.ny = H_s.shape[1]
        self.xvals = np.arange(0,self.nx)
        self.yvals = np.arange(0,self.ny)

        self.X, self.Y = np.meshgrid(self.xvals,self.yvals)

        self.H_s = H_s
        # base is at zero
        self.H_b = np.zeros((self.nx, self.ny))
        # thickness is computed as
        self.H = H_s - self.H_b
        # meltrates
        self.A = np.zeros((self.nx, self.ny))
        # just one cell is melting
        #self.A[5,5] = 1
        # temperature at base is 0
        self.T_b = np.zeros((self.nx, self.ny))

    def SetMeltPos(self,x,y):
        self.A[x,y] = 1

    def setMask(self,mask):
        self.mask = mask

    def WriteNC(self,ncfile):
        """Writes the data to netcdf file"""

        root_grp = Dataset(ncfile, 'w', format='NETCDF4')
        root_grp.description = 'Input data for flux routing'
        root_grp.history = 'Created ' + time.ctime(time.time())
        root_grp.source = 'Generated from ' + os.path.basename(__file__)
        # dimensions
        root_grp.createDimension('x', self.nx)
        root_grp.createDimension('y', self.ny)

        # variables
        nc_x = root_grp.createVariable('x', 'f4', ('x',))
        nc_x.units = 'm'
        nc_x.axis = 'X'
        nc_x.long_name = 'X-coordinate in Cartesian system'
        nc_x.standard_name = 'projection_x_coordinate'
        nc_y = root_grp.createVariable('y', 'f4', ('y',))
        nc_y.units = 'm'
        nc_y.axis = 'Y'
        nc_y.long_name = 'Y-coordinate in Cartesian system'
        nc_y.standard_name = 'projection_y_coordinate'

        # geometry
        nc_surface = root_grp.createVariable('surf', 'f4', ('y', 'x',))
        nc_surface.units = 'm'
        nc_surface.standard_name = 'surface_altitude'
        nc_surface.long_name = 'ice upper surface elevation'
        nc_bed = root_grp.createVariable('bed', 'f4', ('y', 'x',))
        nc_bed.units = 'm'
        nc_bed.standard_name = 'ice_base_altitude'
        nc_bed.long_name = 'ice lower surface elevation'
        nc_thickness = root_grp.createVariable('thickness', 'f4', ('y', 'x',))
        nc_thickness.units = 'm'
        nc_thickness.standard_name = 'land_ice_thickness'
        nc_thickness.long_name = 'land ice thickness'

        nc_meltrates = root_grp.createVariable('meltrates', 'f4', ('y', 'x',))
        nc_meltrates.units = 'm/s'
        nc_meltrates.comment = 'Water equivalent'
        nc_meltrates.standard_name = 'land_ice_basal_melt_rate'
        nc_meltrates.long_name = 'ice basal melt rate in m/s water equivalent (rho_w = 1000)'
        nc_base_temp = root_grp.createVariable('base_temp', 'f4', ('y', 'x',))
        nc_base_temp.units = 'C_deg'
        nc_base_temp.standard_name = 'basal_temperature'
        nc_base_temp.long_name = 'ice temperature at base'

        # mask
        nc_mask = root_grp.createVariable('mask', 'i4', ('y', 'x',))
        nc_mask.long_name = "ice-type (ice-free/grounded/floating/ocean) integer mask"
        nc_mask.flag_meanings = "ice_free_bedrock grounded_ice floating_ice ice_free_ocean"
        nc_mask.flag_values = "1 2 3 4"

        # assign to netcdf
        nc_x[:] = self.xvals
        nc_y[:] = self.yvals

        nc_surface[:]   = self.H_s
        nc_bed[:]       = self.H_b
        nc_thickness[:] = self.H
        nc_meltrates[:] = self.A
        nc_base_temp[:] = self.T_b
        nc_mask[:] = self.mask

        root_grp.close()


def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def makeMask(H, level=0):
    """ Make a mask, of grounded ice and no ice
        1 - ice_free_bedrock
        2 - grounded_ice
        3 - floating_ice
        4 - ice_free_ocean
        (same as pism 0.6) """
    ocean = (H <= level).astype(int)*4
    grounded = (H > level).astype(int)*2
    return ocean + grounded


# generate grid
nx = 7
ny = 7
xvals =  np.arange(0,nx)
yvals =  np.arange(0,ny)
X, Y = np.meshgrid(xvals, yvals)


octaves = 5
freq = 16.0*octaves

H = np.ones((nx, ny))
H[0,:] = 2
H[6,:] = 2
H[:,0] = 2
H[:,6] = 2
H[0,2] = 0





#for y in range(ny):
#    for x in range(nx):
#        H[x,y] = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128)


# make island
#bump = makeGaussian(nx,nx/2)
#H = H*bump
# lower everything by 20m to make it a real island
#H = H-20

#generate mask
mask = makeMask(H)


gdata = GeometryData()
gdata.InitFromSurface(H)
gdata.SetMeltPos(int(nx/2),int(ny/2))
gdata.setMask(mask)
gdata.WriteNC('./artidemisland.nc')







