#!/usr/bin/env python3
"""This module contains the application functions for the calculation of the IBP index as well as the graphical visualization.
"""
from .ibpcalc import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from   matplotlib import cm

def calculateIBPindex(day_month=0, longitude=list(range(-180,180,5)), local_time=np.arange(-6,6.1,0.1), f107=150):
    '''Calculates the Ionospheric Bubble propability index based on the input parameters. 
    Returns a *pandas.DataFrame* with input parameters and IBP index. 

    Parameters
    ----------
    day_month : int or str or list, optional
        Day of year (*int*) or the month of the year (*str*). 
        *int*: Day of the year, ``0 <= doy <= 365``. The value 0 means it should be calculated based on every month.
        *str*: Abbreviated month name. ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        The default is 0.
    longitude : int or list of ints, optional
        The geographical longitude(s), ``-180 <= longitude <= 180``. The default is `list(range(-180,181,5))`.
    local_time : int or float or list, optional
        The local time, ``-6.0 <= local_time <= 24``. The default is `np.arange(-6,6.1,0.1)`.
    f107 : int or float or list, optional
        The Solar Radio Flux (F10.7 index), ``0.0 <= f107 <= 200.0``. The default is 150.

    Returns
    -------
    df : pandas.DataFrame
        contains the columns: Doy (Day(s) of the year), Month (Month(s) from the day of the year), 
        Lon (Longitude(s)), LT (Local Time(s)), F10.7 (solar index(es)), IBP (Ionospheric Bubble Index, value(s) between 0.0 and 1.0).
    '''

    
    df = pd.DataFrame(columns=['Doy','Month','Lon','LT','F10.7','IBP'])
    
    if day_month == 0:
        day_of_year = np.array([ doyFromMonth(i) for i in range(1,13) ])
    else:
        day_of_year = np.array(checkDoyMonth(day_month))
       
    longitude_range = range(-180,181)
    longitude = checkParameter(longitude, longitude_range).astype(int)
    longitude[longitude == 180] = -180

    local_time_range = range(-6,25)
    local_time = checkParameter(local_time, local_time_range) 

    f107_range = range(0,201)
    f107 = checkParameter(f107, f107_range)

    data = read_model_file()

    parts = tiler(day_of_year, longitude, local_time, f107)

    for i, c in enumerate(['Doy', 'Lon', 'LT', 'F10.7']):
        df[c] = parts[i]

    df['Month'] = [ monthFromDoy(i) for i in df['Doy'] ]

    df['IBP'] = compute_probability_exp(
        df['Doy'].to_numpy(), 
        df['Month'].to_numpy(), 
        df['Lon'].to_numpy(), 
        df['LT'].to_numpy(), 
        df['F10.7'].to_numpy(),
        data=data)

    df['IBP'] = df['IBP'].round(4)

    return df

def butterflyData(f107=150):
    '''Calculates the Ionospheric Bubble Propability Index for all months (using the center DOY of each month) and all integer longitudes (resolution of 5 degree)
    using Local_Time of range -5 to 1 and a fixed value of F10.7. IBP index is then averaged from the Local_Times.

    Parameters
    ----------
    f107 : int, optional
        The Solar Radio Flux (F10.7 index). The default is 150.

    Returns
    -------
    out_data : numpy.array
        [[month],[longitude],[IBP index]].

    '''
    month_range       = np.arange(   1,  13,    1)
    longitude_range   = np.arange(-180, 179,  5.0)
    local_time_range  = np.arange(  -5,   1, 0.01)

    month, longitude, local_time = tiler(
        np.array(month_range,dtype='int'),longitude_range,local_time_range)

    data = read_model_file()
    
    day_of_year = np.array([ doyFromMonth(t) for t in month ])
    result = compute_probability_exp(
        day_of_year,month,longitude,local_time,f107,data)

    out_data = np.array(tile_aggregate(result,month_range,longitude_range,local_time_range)).transpose()
    
    return out_data
    
def plotIBPindex(doy, f107=150, getFig=False):
    '''Create a contour plot of IBP index for the given day. The resolution along the longitude is 5 degree. Local time spans from 6 pm to 6 am with a resolution of 0.1 hours. 

    Parameters
    ----------
    doy : int
        Day of the year.
    f107 : int, optional
        The Solar Radio Flux (F10.7 index). The default is 150.
    getFig : bool, optional
        True: return matplotlib.axes, False: show picture. The default is False.

    Returns
    -------
    matplotlib.axes or bool

    '''
    df = calculateIBPindex(day_month=doy, f107=f107)
    
    value_size = np.unique(df['Lon'].to_numpy(), return_counts=True)
    value_size = ( len(value_size[0]), value_size[1][0] )
    
    x = np.transpose(df['Lon'].to_numpy().reshape(value_size))
    y = np.transpose(df['LT'].to_numpy().reshape(value_size))
    z = np.transpose(df['IBP'].to_numpy().reshape(value_size))
    
    levels = np.arange(0.0, 1.0, 0.05)
    
    fig, ax = plt.subplots(figsize = (6.4, 3.0))
    CS = ax.contourf(x, y, z, levels, cmap=cm.coolwarm)
    
    CS2 = ax.contour(CS, levels, colors = 'b', linewidths = 0.2)

    ax.set_title('IBP index at doy ' + str(doy)+' with F10.7 = ' + str(f107))
    ax.set_xlabel('Longitude in degree')
    ax.set_ylabel('Hours to Midnight')

    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('Ionospheric Bubble Probability')
    
    if getFig:
        return ax
    elif getFig == False:
        plt.show()
        return True
    else:
        return False
    
def plotButterflyData(f107=150, getFig=False):
    '''Create a contour plot of the result from function butterflyData(). 

    Parameters
    ----------
    f107 : int, optional
        The Solar Radio Flux (F10.7 index). The default is 150.
    getFig : bool, optional
        True: return matplotlib.axes, False: show picture. The default is False.

    Returns
    -------
    matplotlib.axes or bool

    '''
    d = butterflyData(f107)
    
    y = np.transpose(np.reshape(d[:, 0], (12, 72)))
    x = np.transpose(np.reshape(d[:, 1], (12, 72)))
    z = np.transpose(np.reshape(d[:, 2], (12, 72)))
    
    l = np.arange(0.0, 0.8, 0.05)
    
    fig, ax = plt.subplots(figsize = (6.2, 5.0))
        
    C = ax.contourf(x, y, z, l, cmap = cm.plasma_r)
    CS2 = ax.contour(C, levels=np.arange(0.05, 0.8, 0.05), colors = '#999900', linewidths = 0.2)
    
    ax.set_title('Monthly IBP index with F10.7 = '+str(f107))
    ax.set_xlabel('Longitude in degree')
    ax.set_ylabel('Month')
    
    cbar = fig.colorbar(C)
    cbar.ax.set_ylabel('Ionospheric Bubble Probability')
    
    if getFig:
        return ax
    elif getFig == False:
        plt.show()
        return True
    else:
        return False
    
if __name__ == "__main__":
    print("Laeuft!")
    