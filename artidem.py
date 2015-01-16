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
        nc_x = root_grp.createVariable('x value', 'f4', ('x',))
        nc_y = root_grp.createVariable('y value', 'f4', ('y',))

        # geometry
        nc_surface = root_grp.createVariable('surf', 'f4', ('x', 'y',))
        nc_surface.units = 'm'
        nc_bed = root_grp.createVariable('bed', 'f4', ('x', 'y',))
        nc_bed.units = 'm'
        nc_thickness = root_grp.createVariable('thickness', 'f4', ('x', 'y',))
        nc_thickness.units = 'm'

        nc_meltrates = root_grp.createVariable('meltrates', 'f4', ('x', 'y',))
        nc_meltrates.units = 'm/s Water equivalent'
        nc_base_temp = root_grp.createVariable('base_temp', 'f4', ('x', 'y',))
        nc_base_temp.units = 'K'


        # assign to netcdf
        nc_x[:] = self.xvals
        nc_y[:] = self.yvals

        nc_surface[:]   = self.H_s
        nc_bed[:]       = self.H_b
        nc_thickness[:] = self.H
        nc_meltrates[:] = self.A
        nc_base_temp[:] = self.T_b


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




# generate grid
nx = 256
ny = 256
xvals =  np.arange(0,nx)
yvals =  np.arange(0,ny)
X, Y = np.meshgrid(xvals, yvals)


# generate different geometries
# This is very weird and we really need a better solution!
geoms = np.array([X, -X+9, Y, -Y+9,
                  (X+Y)/2, (X-Y+9)/2, (-X+Y+9)/2, (-X-Y+18)/2])

melts_y = np.array([8, 1, 4, 4, 8, 8, 1, 1])
melts_x = np.array([4, 4, 8, 1, 8, 1, 8, 1])


octaves = 5
freq = 16.0*octaves

H = np.zeros((nx, ny))
for y in range(ny):
    for x in range(nx):
        H[x,y] = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128)


# make island
bump = makeGaussian(nx,nx/2)
H = H*bump


gdata = GeometryData()
gdata.InitFromSurface(H)
gdata.SetMeltPos(int(nx/2),int(ny/2))
gdata.WriteNC('./artidemisland.nc')







