#import packages:
import numpy as np
import xarray as xr
import re
import glob

#calculate the area of each lat/lon grid:
latit = np.linspace(-90,90,num  = 181)
longit = np.linspace(-180,180,num = 360)
Area = np.ones([181,360])
for tick_lat in range(len(latit)):
    for tick_lon in range(len(longit)):
        latit_low = (latit[tick_lat]-0.5)*np.pi/180
        latit_high = (latit[tick_lat]+0.5)*np.pi/180
        longit_low = longit[tick_lon]-0.5
        longit_high = longit[tick_lon]+0.5
        Area[tick_lat,tick_lon] = np.pi/180*6378.1e3**2*abs(np.sin(latit_high)-np.sin(latit_low))*abs(longit_high-longit_low)
#sum(Area.ravel()) #gets 511182497306249.56 m^2 which is consistent with observations
#get the filenames initialize total lightning:
filenames  = glob.glob("geosgcm_prog/*.nc4")
filenames.sort()
filenames
tot_lght = 0.0

#sum up the lightning from each day:
for tick_f in range(len(filenames)):
    ds = xr.open_dataset(filenames[tick_f])
    a = ds['EMIS_NO_LGHT'].values
    b = Area
    c = np.multiply(a,b).ravel()
    lght_no =sum(c)
    tot_lght += lght_no

#get the amount per day:
TOT_lght = (tot_lght)/15 #kg/s/day 
print(str(TOT_lght)+' kg/s/day')


