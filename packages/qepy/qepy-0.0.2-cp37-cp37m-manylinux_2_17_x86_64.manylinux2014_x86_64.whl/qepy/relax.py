"""
Module relax


Defined at pwcom.fpp lines 357-373

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_epse():
    """
    Element epse ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 365
    
    """
    return _qepy.f90wrap_relax__get__epse()

def set_epse(epse):
    _qepy.f90wrap_relax__set__epse(epse)

def get_epsf():
    """
    Element epsf ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 367
    
    """
    return _qepy.f90wrap_relax__get__epsf()

def set_epsf(epsf):
    _qepy.f90wrap_relax__set__epsf(epsf)

def get_epsp():
    """
    Element epsp ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 369
    
    """
    return _qepy.f90wrap_relax__get__epsp()

def set_epsp(epsp):
    _qepy.f90wrap_relax__set__epsp(epsp)

def get_starting_scf_threshold():
    """
    Element starting_scf_threshold ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 371
    
    """
    return _qepy.f90wrap_relax__get__starting_scf_threshold()

def set_starting_scf_threshold(starting_scf_threshold):
    _qepy.f90wrap_relax__set__starting_scf_threshold(starting_scf_threshold)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "relax".')

for func in _dt_array_initialisers:
    func()
