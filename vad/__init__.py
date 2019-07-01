"""
===
VAD
===

VAD functions for creating a vad profile and for plotting.

    vad
    quicklooks
    get_metadata
    get_plot_values
 
 """

from .vad_profile import vad
from .vad_quicklooks import quicklooks
from .config import get_metadata, get_plot_values

__all__ = [s for s in dir() if not s.startswith('_')]