""" 
Unit Tests for SAPR-VAD-VAP vad.quicklooks
and vad.vad modules. 
"""

import numpy as np
from numpy.testing import assert_equal
import vad
import glob
import os

def test_vad_profile():
    # Test vad.vad
    input_files = glob.glob('2017*', recursive=True)
    input_files.sort()

    vel_field = 'corrected_velocity'
    z_want = np.linspace(0, 10000, 101)
    config = 'xsaprvadI5'
    outdir = '.'

    test_vad = vad.vad(
        files=input_files, vel_field=vel_field, z_want=z_want)

    test_vad.write(file_directory=outdir, config=config)

    assert_equal(os.path.exists('sgpxsaprvadI5.c1.20171005.000000.nc'), True)

def test_vad_quicklooks():
    # Test vad.quicklooks
    input_file = 'example_vad.nc'
    config = 'xsaprvadI5'
    outdir = '.'

    vad.quicklooks(input_file, config, outdir)

    assert_equal(os.path.exists('sgpxsaprvadI5.c1.20171005.000000.png'), True)
