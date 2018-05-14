import numpy as np
import xarray as xr
import matplotlib.pyplot as plt # general plotting
import re
import scipy.interpolate
from scipy.interpolate import interp1d
#open nc file
ds = xr.open_dataset(".././initial_GEOSChem_rst.c48_CO2.nc")

#get list of molecules
molec = list()
pattern = "(SPC_\w+)"
for i, line in enumerate(open('../molecular_species.txt')):
    for match in re.finditer(pattern,line):
        molec.append(match.group())
lev = np.linspace(1,132,num =132,dtype = 'float')

#initialize new netcd4 file
dataset = xr.Dataset()
dataset.coords['time'] = ds.coords['time']
dataset.coords['lev'] = (('lev'),lev)
dataset.coords['lat'] = ds.coords['lat'] 
dataset.coords['lon'] = ds.coords['lon']
dataset.attrs['title'] = 'GEOS-5 132 lvl restart'
dataset.attrs['history'] = 'created by Ada Shaw with initial_GEOSChem_rst.2x25_benchmark.nc'
dataset.attrs['format'] = "NetCDF-4"
dataset.attrs['conventions'] = 'COARDS'

#find lat lon dimensions
lon_dim = len(ds['lon'].values)
lat_dim = len(ds['lat'].values)

#47 layer model
tru_layer = 72

#initialize interpolation vectors
lev46 = np.reshape(np.repeat(np.linspace(1,tru_layer, num=tru_layer,dtype = 'float64'),lon_dim),[tru_layer,lon_dim])
lev132 = np.reshape(np.repeat(np.linspace(1,tru_layer, num=132,dtype = 'float64'),lon_dim),[132,lon_dim])
lon_i =np.transpose(np.reshape(np.repeat(np.linspace(1,lon_dim,num= lon_dim,dtype ='float64'),tru_layer),[lon_dim,tru_layer]))
lon_f = np.transpose(np.reshape(np.repeat(np.linspace(1,lon_dim,num= lon_dim,dtype ='float32'),132),[lon_dim,132]))
conc_interp = np.ndarray(shape=(1,132,lat_dim,lon_dim), dtype='f', order='F')

#loop through all molecules and latitudes to interpolate layers
dr = ds["SPC_CO2"].values
for tick_lat in range(lat_dim):
    interp = scipy.interpolate.Rbf(lon_i,lev46 ,dr[0,:,tick_lat,:], function='linear')
    conc_interp[0,:,tick_lat,:] = interp(lon_f,lev132)
dataset[molec[tick_molec]] = (('time','lev','lat','lon'),conc_interp)
dataset.data_vars[molec[tick_molec]].attrs = ds.data_vars[molec[tick_molec]].attrs

#save to netcdf file
dataset.to_netcdf('c48_132_lvl_CO2_rst.nc','w')
