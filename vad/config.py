"""
vad.config
==========
VAD Configuration

    get_metadata
    get_plot_values

"""

from .default_config import _DEFAULT_METADATA, _DEFAULT_PLOT_VALUES




def get_metadata(radar):
    """
    Return a dictonary of metadata for a given radar. An empty dictonary
    will be returned if no metadata dictonary exists for parameter radar.
    """
    if radar in _DEFAULT_METADATA:
        return _DEFAULT_METADATA[radar].copy()
    else:
        return {}
    
def get_plot_values(radar):
    """
    Return the values specific to a radar for plotting the radar fields.
    """
    return _DEFAULT_PLOT_VALUES[radar].copy()