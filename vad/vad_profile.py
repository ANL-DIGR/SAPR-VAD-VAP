import numpy as np
import pandas as pd
import pyart
import xarray
import netCDF4
import datetime
import sys
import socket

from .config import get_metadata
class vad():
    """ Class for creating VAD objects for ploting. """
    
    def __init__(self, files, vel_field=None, z_want=None, gatefilter=None):
        """
        Velocity Azimuth Display
        
        Parameters
        ----------
        files : str
            list of radar file path.
        vel_field : string, optional
            Velocity field used for VAD calculation
        z_want : array. optional
            Heights for where to sample vads from.
            None will default to np.linspace(0, 10000, 101).
        
        Optional Parameters
        -------------------
        gatefilter : GateFilter
            A GateFilter indicating radar gates that should be excluded
            from the import vad calculation.
        
        """
        self.u_wind = []
        self.v_wind = []
        self.speed = []
        self.direction = []
        self.time = []
        self.base_time = []
        
        if vel_field is None:
            self.vel_field = 'corrected_velocity'
        else:
            self.vel_field = vel_field
        
        if z_want is None:
            self.z_want = np.linspace(0, 10000, 100)
        else:
            self.z_want = z_want
        
        self.create_vad(files)
        
    def create_vad(self, files, **kwargs):
        """
        Creates a VAD object containing u & v wind components,
        wind speed, direction, and height.
        
        """
        for file in files:
            try:
                radar = pyart.io.read(file)
            except TypeError:
                continue


            time = netCDF4.num2date(radar.time['data'][0],
                                    radar.time['units'])
            rtime = datetime.datetime.strftime(
                time, '%Y-%m-%dT%H:%M:%S')
            vad = pyart.retrieve.velocity_azimuth_display(
                radar, vel_field=self.vel_field,
                z_want=self.z_want, **kwargs)

            self.u_wind.append(vad.u_wind)
            self.v_wind.append(vad.v_wind)
            self.time.append(rtime)
            self.speed.append(vad.speed)
            self.direction.append(vad.direction)
            self.base_time.append(time)
            altitude = radar.altitude['data']
            longitude = radar.longitude['data']
            latitude = radar.latitude['data']
            height = self.z_want

        self.uwind = np.array(self.u_wind)
        self.vwind = np.array(self.v_wind)
        self.t = np.array(self.time, dtype='datetime64[ns]')
        self.bt = np.array([netCDF4.date2num(self.base_time[0],
                                             'seconds since 1970-1-1 0:00:00 0:00')],
                           dtype=np.int32)
        self.dir = np.array(self.direction)
        self.hght = np.array(height)
        self.spd = np.array(self.speed)
        self.alt = np.array(altitude)
        self.lon = np.array(longitude)
        self.lat = np.array(latitude)
        
    def write(self, config, file_directory=None):
        """
        Writes VAD file to a netCDF output
        
        Parameters
        ----------
        config : str
            A string of the radar name found from config.py that contains values
            for writing, specific to that radar.
        
        Optional Parameter
        ------------------
        file_directory : str
            File path to the file output folder of which to save the VAD netCDF files.
            If no file path is given, file path defaults to users home directory.
            
        """
        if file_directory is None:
            file_directory = os.path.expanduser('~')
        
        attributes = get_metadata(config)
        
        ds = xarray.Dataset()
        ds['base_time'] = xarray.Variable('base_time', self.bt,
                                          attrs={'string': datetime.datetime.strftime(
                                              self.base_time[0], '%d-%b-%Y,%H:%M:%S GMT'),
                                                 'units': 'seconds since 1970-1-1 0:00:00 0:00',
                                                 'long_name': 'Base time in Epoch',
                                                 'ancillary_variables': 'time_offset',
                                                 'calendar': 'gregorian'})
        ds['time_offset'] = xarray.Variable('time', self.t,
                                            attrs={'long_name': 'Time offset from base_time',
                                                   'ancillary_variables': 'base_time'})
        ds['time'] = xarray.Variable(['time'], self.t, 
                                     attrs={'standard_name': 'time',
                                            'long_name': 'Time offset from midnight'})
        ds['height'] = xarray.Variable(['height'], self.hght, 
                                        attrs={'standard_name': 'height', 
                                               'units': 'meter', 
                                               'long_name': 'Height above ground',
                                               '_FillValue': False})
        ds['u_wind'] = xarray.Variable(['time', 'height'], self.uwind, 
                                       attrs={'standard_name': 'eastward_wind', 
                                              'units': 'm/s', 
                                              'long_name': 'Eastward wind component',
                                              '_FillValue': -9999})
        ds['v_wind'] = xarray.Variable(['time', 'height'], self.vwind, 
                                       attrs={'standard_name': 'northward_wind', 
                                              'units': 'm/s', 
                                              'long_name': 'Northward wind component',
                                              '_FillValue': -9999})
        ds['speed'] = xarray.Variable(['time', 'height'], self.spd, 
                                      attrs={'standard_name': 'wind_speed', 
                                             'units': 'm/s', 
                                             'long_name': 'Horizontal wind speed',
                                             '_FillValue': -9999})
        ds['direction'] = xarray.Variable(['time', 'height'], self.dir, 
                                          attrs={'standard_name': 'wind_to_direction', 
                                                 'units': 'degree', 
                                                 'long_name': 'Horizontal wind direction',
                                                 '_FillValue': -9999})
        ds['lon'] = xarray.Variable('longitude', self.lon,
                                    attrs={'standard_name': 'longitude',
                                           'units': 'degree_E', 
                                           'long_name': "East longitude",
                                           'valid_min': -180, 
                                           'valid_max': 180,
                                           '_FillValue': False})
        ds['lat'] = xarray.Variable('latitude', self.lat, 
                                    attrs={'standard_name': 'latitude',
                                           'units': 'degree_N', 
                                           'long_name': 'North latitude',
                                           'valid_min': -90, 
                                           'valid_max': 90,
                                           '_FillValue': False})
        
        ds['alt'] = xarray.Variable('altitude', self.alt,
                                    attrs={'standard_name': 'altitude', 
                                           'units': 'm', 
                                           'long_name': 'Altitude above mean sea level',
                                           '_FillValue': False})
        
        encoding = {'time': {'units': 'seconds since ' + str(self.t[0]),
                             'calendar': 'gregorian'},
                    'time_offset': {'units': 'seconds since ' + str(self.t[0]),
                                    'calendar': 'gregorian'}}
        
        ds.attrs=attributes
        date = pd.to_datetime(
            np.array(self.time[0], dtype='datetime64[ns]')).strftime('%Y%m%d')
        
        
        command_line = ''
        for item in sys.argv:
            command_line = command_line + '' + item
        ds.attrs['command_line'] = command_line
        ds.attrs['history'] = ('Created by jhemedinger on ' 
                               + socket.gethostname() + ' at' 
                               + datetime.datetime.utcnow().strftime(
                                   '%Y-%m-%dT%H:%M:%S.%f')
                               + ' using PyART')
        ds.squeeze(dim=None, drop=False).to_netcdf(path= file_directory + '/' + attributes['datastream'] 
                                                   + '.' + str(date) + '.000000.nc', encoding=encoding,
                                                   unlimited_dims='time')