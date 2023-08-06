"""
Module vlocal


Defined at pwcom.fpp lines 235-250

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_strf():
    """
    Element strf ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 244
    
    """
    global strf
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_vlocal__array__strf(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        strf = _arrays[array_handle]
    else:
        strf = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_vlocal__array__strf)
        _arrays[array_handle] = strf
    return strf

def set_array_strf(strf):
    strf[...] = strf

def get_array_vloc():
    """
    Element vloc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 246
    
    """
    global vloc
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_vlocal__array__vloc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vloc = _arrays[array_handle]
    else:
        vloc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_vlocal__array__vloc)
        _arrays[array_handle] = vloc
    return vloc

def set_array_vloc(vloc):
    vloc[...] = vloc

def get_array_starting_charge():
    """
    Element starting_charge ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 248
    
    """
    global starting_charge
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_vlocal__array__starting_charge(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        starting_charge = _arrays[array_handle]
    else:
        starting_charge = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_vlocal__array__starting_charge)
        _arrays[array_handle] = starting_charge
    return starting_charge

def set_array_starting_charge(starting_charge):
    starting_charge[...] = starting_charge


_array_initialisers = [get_array_strf, get_array_vloc, \
    get_array_starting_charge]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "vlocal".')

for func in _dt_array_initialisers:
    func()
