import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
import xarray
import datetime
import os

from .config import get_plot_values

def quicklooks(file, config, image_directory=None):
    """
    Quicklook, produces a single image using a VAD object netCDF file.
    
    Parameters
    ----------
    file : str
        File path to the VAD NetCDF file
    config : str
        A string of the radar name found from config.py that contains values
        for writing, specific to that radar
    
    Other Parameters
    ----------------
    image_directory : str
        File path to the image folder to save the VAD image. If no
        image file path is given, image path deafults to users home directory.
        
    """
    if image_directory is None:
        image_directory = os.path.expanduser('~')
    plot_values = get_plot_values(config)
    vad = xarray.open_dataset(file)
    
    u = vad.u_wind.data[::6,::5]/0.514444
    v = vad.v_wind.data[::6,::5]/0.514444
    z = vad.height.data[::5]/1000
    C = vad.speed.data[::6,::5]/0.514444
    t = vad.time[::6].data
    date = pd.to_datetime(vad.time[0].data).strftime('%Y%m%d')
    ts = datetime.datetime.strptime(date, '%Y%m%d')
    
    
    fig = plt.figure(figsize=[25,12])
    font = {'family': 'normal',
            'size': 20}
    matplotlib.rc('font', **font)
    matplotlib.rcParams.update({'font.size': 20})
    matplotlib.rcParams.update({'axes.titlesize': 20})
    
    for i in range(len(t)):
        Xq, Yq = np.meshgrid(t[i], z)
        img = plt.barbs(Xq[:,0], Yq[:,0], u[i], v[i],
                        C[i], cmap = plot_values['cmap'],
                        norm=plot_values['norm'],
                        sizes=dict(emptybarb=0.1), rounding=False,
                        length=7, clip_on=False)

    cb = plt.colorbar(img, cmap=plot_values['cmap'], norm=plot_values['norm'],
                      boundaries=plot_values['ticks'], ticks=plot_values['ticks'])
    cb.set_label('Speed (kts)')
    plt.title(plot_values['title'] + str(ts) + ' - '
              + str(ts + datetime.timedelta(days=1)))
    plt.xlim(ts, (ts + datetime.timedelta(days=1)))
    plt.xticks(rotation=45)
    plt.ylim(0,10)
    plt.ylabel('Height (km)')
    plt.xlabel('Time (UTC)')
    
    plt.savefig(image_directory + '/' + plot_values['save_name']
                + '.' + str(date) + '.000000.png', bbox_inches='tight') 
    
    
    