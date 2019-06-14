"""
===
VAD
===

VAD functions for creating a vad profile and for plotting.

    vad
    quicklooks
    get_metadata
 
 
 """

from .vad_profile import vad
from .comfig import get_metadata

__all__ = [s for s in dir() if not s.startswith('_')