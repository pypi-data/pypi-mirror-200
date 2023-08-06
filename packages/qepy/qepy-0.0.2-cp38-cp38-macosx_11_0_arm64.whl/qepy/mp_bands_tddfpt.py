"""
Module mp_bands_tddfpt


Defined at mp_bands.fpp lines 71-79

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_ibnd_start():
    """
    Element ibnd_start ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 77
    
    """
    return _qepy.f90wrap_mp_bands_tddfpt__get__ibnd_start()

def set_ibnd_start(ibnd_start):
    _qepy.f90wrap_mp_bands_tddfpt__set__ibnd_start(ibnd_start)

def get_ibnd_end():
    """
    Element ibnd_end ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 78
    
    """
    return _qepy.f90wrap_mp_bands_tddfpt__get__ibnd_end()

def set_ibnd_end(ibnd_end):
    _qepy.f90wrap_mp_bands_tddfpt__set__ibnd_end(ibnd_end)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mp_bands_tddfpt".')

for func in _dt_array_initialisers:
    func()
