"""
Configuration file for the Velocity Azimuth Display (VAD)

The values for a number of parameters that change depending on which radar is
being used.

"""



#############################################################################
# Default metadata
# 
# The DEFAULT_METADATA dictionary contains dictionaries which provide the
# default metadata for each vad file.
#############################################################################

_DEFAULT_METADATA = {
    #X-SAPR I4 VAD metadata
    'xsaprvadI4': {
        'Convention' : 'ARM-1.2',
        'vap_name' : 'vad',
        'instrument_name' : 'X-SAPR Velocity Azimuth Display',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I4 : Billings, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI4.c1',
        'doi' : '10.5439/190987',
        'input_datastream' : 'sgpadicmac2I4.c1'},
    
    #X-SAPR I5 VAD metadata
    'xsaprvadI5':{
        'Convention'     'Convention' : 'ARM-1.2',
        'vap_name' : 'vad',
        'instrument_name' : 'X-SAPR Velocity Azimuth Display',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I5 : Garber, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI5.c1',
        'doi' : '10.5439/190987',
        'input_datastream' : 'sgpadicmac2I5.c1'},
    
    #X-SAPR I6 VAD metadata
    'xsaprvadI6':{
        'Convention' : 'ARM-1.2',
        'vap_name' : 'vad',
        'instrument_name' : 'X-SAPR Velocity Azimuth Display',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I6 : Deer Creek, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI6.c1',
        'doi' : '10.5439/190987',
        'input_datastream' : 'sgpadicmac2I6.c1'}
}

###########################################################################
# Default plot values
#
# The DEFAULT_PLOT_VALUES dictionary contains dictionaries for radars that
# contains parameter values in the VAD quicklooks. Values in these radar
# dictionaries are used for defininf specifications for plotting specific
# radars. These values are all used within vad_quicklooks.py.
###########################################################################
import numpy as np
import matplotlib

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    "vadbarbcolors", ['black', 'cyan', 'blue', 
                      'darkblue', 'lime', 'green',
                      'darkgreen', 'yellow', 'orange', 
                      'darkorange', 'red', 'firebrick', 
                      'maroon', 'purple', 'mediumpurple', 
                      'rebeccapurple', 'hotpink', 'deeppink', 
                      'magenta', 'pink', 'gray'])

bounds = np.arange(0, 105, 5)
ticks = np.arange(5, 105, 5)
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

_DEFAULT_PLOT_VALUES = {
    # X_SAPR I4 VAD plot values
    'xsaprvadI4':{
        'save_name': 'sgpxsaprvadI4.c1',
        'facility': 'I4',
        'title': 'SGP X-SAPR I4 VAD Profile ',
        'cmap': cmap,
        'bounds': bounds,
        'ticks': ticks,
        'norm': norm},
    
    # X-SAPR I5 VAD plot values
    'xsaprvadI5':{
        'save_name': 'sgpxsaprvadI5.c1',
        'facility': 'I5',
        'title': 'SGP X-SAPR I5 VAD Profile ',
        'cmap': cmap,
        'bounds': bounds,
        'ticks': ticks,
        'norm': norm},
    
    # X-SAPR I6 VAD plot values
    'xsaprvadI6':{
        'save_name': 'sgpxsaprvadI6.c1',
        'facility': 'I6',
        'title': 'SGP X-SAPR I6 VAD Profile ',
        'cmap': cmap,
        'bounds': bounds,
        'ticks': ticks,
        'norm': norm}
}