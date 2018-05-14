import numpy as np
import xarray as xr
import matplotlib.pyplot as plt # general plotting
import re
import scipy.interpolate
from scipy.interpolate import interp1d
#open nc file
ds = xr.open_dataset(".././initial_GEOSChem_rst.2x25_benchmark.nc")

#get list of molecules
molec = list()
pattern = "(SPC_\w+)"
for i, line in enumerate(open('../molecular_species.txt')):
    for match in re.finditer(pattern,line):
        molec.append(match.group())

#initialize new netcd4 file
dataset = xr.Dataset()
dataset.coords['time'] = ds.coords['time']
lev = np.linspace(1,132,num =132,dtype = 'float64')
dataset.coords['lev'] = (('lev'),lev)
dataset.coords['lat'] = ds.coords['lat'] 
dataset.coords['lon'] = ds.coords['lon']
dataset.attrs['title'] = 'GEOS-5 132 lvl restart'
dataset.attrs['history'] = 'created by Ada Shaw with initial_GEOSChem_rst.2x25_benchmark.nc'
dataset.attrs['format'] = "NetCDF-4"
dataset.attrs['conventions'] = 'COARDS'
dataset['AREA'] = ds['AREA']

#find lat lon dimensions
lon_dim = len(ds['lon'].values)
lat_dim = len(ds['lat'].values)

#initialize interpolation vectors
lev72 = np.reshape(np.repeat(np.linspace(1,72, num=72,dtype = 'float64'),lon_dim),[72,lon_dim])
lev132 = np.reshape(np.repeat(np.linspace(1,72, num=132,dtype = 'float64'),lon_dim),[132,lon_dim])
lon_i =np.transpose(np.reshape(np.repeat(np.linspace(1,lon_dim,num= lon_dim,dtype ='float64'),72),[lon_dim,72]))
lon_f = np.transpose(np.reshape(np.repeat(np.linspace(1,lon_dim,num= lon_dim,dtype ='float32'),132),[lon_dim,132]))
conc_interp = np.ndarray(shape=(1,132,lat_dim,lon_dim), dtype='f', order='F')

#loop through all molecules and latitudes to interpolate layers
for tick_molec in range(len(molec)):
    dr = ds[molec[tick_molec]].values
    for tick_lat in range(lat_dim):
        interp = scipy.interpolate.Rbf(lon_i,lev72 ,dr[0,:,tick_lat,:], function='linear')
        conc_interp[0,:,tick_lat,:] = interp(lon_f,lev132)
    dataset[molec[tick_molec]] = (('time','lev','lat','lon'),conc_interp)
    dataset.data_vars[molec[tick_molec]].attrs = ds.data_vars[molec[tick_molec]].attrs

#save to netcdf file
dataset.to_netcdf('132_lvl_rst.nc','w')
