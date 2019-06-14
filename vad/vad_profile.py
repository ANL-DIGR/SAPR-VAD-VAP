import numpy as np
import pyart
import xarray
import netCDF4
import datetime
import sys
import socket

from .config import get_metadata
class vad():
    
    def __init__(self, files, vel_field=None, z_want=None):
        
        self.u_wind = []
        self.v_wind = []
        self.speed = []
        self.direction = []
        self.time = []
        
        if vel_field is None:
            self.vel_field = 'corrected_velocity'
        else:
            self.vel_field = vel_field
        
        if z_want is None:
            self.z_want = np.linspace(0, 10000, 101)
        else:
            self.z_want = z_want
        
        self.create_vad(files)
        
    def create_vad(self, files, **kwargs):
        """

        """
        files.sort()
        for file in files:
            try:
                radar = pyart.io.read(file)
            except TypeError:
                continue


            radar_time = netCDF4.num2date(radar.time['data'][0],
                                          radar.time['units'])
            rtime = datetime.datetime.strftime(
                radar_time, '%Y-%m-%dT%H:%M:%S')
            vad = pyart.retrieve.velocity_azimuth_display(
                radar, vel_field=self.vel_field,
                z_want=self.z_want, **kwargs)

            self.u_wind.append(vad.u_wind)
            self.v_wind.append(vad.v_wind)
            self.time.append(rtime)
            self.speed.append(vad.speed)
            self.direction.append(vad.direction)

            altitude = radar.altitude['data']
            longitude = radar.longitude['data']
            latitude = radar.latitude['data']
            height = self.z_want

        self.uwind = np.array(self.u_wind)
        self.vwind = np.array(self.v_wind)
        self.t = np.array(self.time, dtype='datetime64[ns]')
        self.dir = np.array(self.direction)
        self.hght = np.array(height)
        self.spd = np.array(self.speed)
        self.alt = np.array(altitude)
        self.lon = np.array(longitude)
        self.lat = np.array(latitude)
        
        dt = netCDF4.num2date(radar.time['data'][0],
                      radar.time['units'])
        td = dt - datetime.datetime.utcfromtimestamp(0)
        td = td.seconds + td.days * 24 * 3600
        
    def write(self, filename, config):
        ds = xarray.Dataset()
        ds['base_time'] = xarray.Variable('base_time', np.array(np.array([td], dtype=np.int32)),
                                          attrs={'string': dt.strftime('%d-%b-%Y,%H:%M:%S GMT'),
                                                 'units': 'seconds since 1970-1-1 0:00:00 0:00',
                                                 'long_name': 'Base time in Epoch',
                                                 'ancillary_variables': 'time_offset',
                                                 'calendar': 'gregorian'})
        ds['time_offset'] = xarray.Variable('time', self.t,
                                            attrs={'long_name': 'Time offset from base_time',
                                                   'units': 'seconds since ' + self.t[0],
                                                   'ancillary_variables': 'base_time',
                                                   'calendar': 'gregorian'})
        ds['time'] = xarray.Variable(['time'], self.t, 
                                     attrs={'standard_name': 'time',
                                            'units': 'seconds since ' + self.t[0],
                                            'long_name': 'Time offset from midnight',
                                            'calendar': 'gregorian'})
        ds['height'] = xarray.Variable(['height'], self.hght, 
                                        attrs={'standard_name': 'height', 
                                               'units': 'meter', 
                                               'long_name': 'Height above ground',
                                               '_FillValue': -9999})
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
                                           '_FillValue': -9999})
        ds['lat'] = xarray.Variable('latitude', self.lat, 
                                    attrs={'standard_name': 'latitude',
                                           'units': 'degree_N', 
                                           'long_name': 'North latitude',
                                           'valid_min': -90, 
                                           'valid_max': 90,
                                           '_Fillvalue': -9999})
        
        ds['alt'] = xarray.Variable('altitude', self.alt,
                                    attrs={'standard_name': 'altitude', 
                                           'units': 'm', 
                                           'long_name': 'Altitude above mean sea level',
                                           '_FillValue': -9999})
        ds.attrs=get_metadata(config)
        command_line = ''
        for item in sys.argv:
            command_line = command_line + '' + item
        ds.attrs['command_line'] = command_line
        ds.attrs['history'] = ('Created by jhemedinger on ' 
                               + socket.gethostname() + ' at' 
                               + datetime.datetime.utcnow().strftime(
                                   '%Y-%m-%dT%H:%M:%S.%f')
                               + ' using PyART')
        ds.squeeze(dim=None, drop=False).to_netcdf(path=filename,
                                                   unlimited_dims='time')