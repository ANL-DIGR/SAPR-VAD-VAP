"""
vad.config
==========
VAD Configuration

    get_metadata




"""

from .default_config import _DEFAULT_METADATA




def get_metadata(radar):
    """
    Return a dictonary of metadata for a given radar. An empty dictonary
    will be returned if no metadata dictonary exists for parameter radar.
    """
    if radar in _DEFAULT_METADATA:
        return _DEFAULT_METADATA[radar].copy()
    else:
        return {}