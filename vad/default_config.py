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
        'instrument_name' : 'X_SAPR Velocity Azimuth Display',
        'command_line' : '',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I4 : Billings, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI4,c1',
        'doi' : '105439/190987',
        'input_datastream' : 'sgpadicmac2I4.c1',
        'history' : ''},
    
    #X-SAPR I5 VAD metadata
    'xsaprvadI5':{
        'Convention'     'Convention' : 'ARM-1.2',
        'vap_name' : 'vad',
        'instrument_name' : 'X_SAPR Velocity Azimuth Display',
        'command_line' : '',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I5 : Garber, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI5,c1',
        'doi' : '105439/190987',
        'input_datastream' : 'sgpadicmac2I5.c1',
        'history' : ''},
    
    #X-SAPR I6 VAD metadata
    'xsaprvadI6':{
        'Convention' : 'ARM-1.2',
        'vap_name' : 'vad',
        'instrument_name' : 'X_SAPR Velocity Azimuth Display',
        'command_line' : '',
        'process_version' : 'EVAL-0.5',
        'dod_version' : 'v1.0',
        'site_id' : 'SGP',
        'platform_id' : 'xsaprvad',
        'facility_id' : 'I6 : Deer Creek, OK',
        'data_level' : 'c1',
        'location_description' : (
            'Southern Great Plains (SGP)',
            'Garber, Oklahoma'),
        'datastream' : 'sgpxsaprvadI6,c1',
        'doi' : '105439/190987',
        'input_datastream' : 'sgpadicmac2I6.c1',
        'history' : ''}
}