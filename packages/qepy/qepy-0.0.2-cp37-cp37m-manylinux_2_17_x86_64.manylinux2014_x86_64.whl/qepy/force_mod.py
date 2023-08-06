"""
Module force_mod


Defined at pwcom.fpp lines 334-352

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_force():
    """
    Element force ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 342
    
    """
    global force
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_force_mod__array__force(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        force = _arrays[array_handle]
    else:
        force = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_force_mod__array__force)
        _arrays[array_handle] = force
    return force

def set_array_force(force):
    force[...] = force

def get_sumfor():
    """
    Element sumfor ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 344
    
    """
    return _qepy.f90wrap_force_mod__get__sumfor()

def set_sumfor(sumfor):
    _qepy.f90wrap_force_mod__set__sumfor(sumfor)

def get_array_sigma():
    """
    Element sigma ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 346
    
    """
    global sigma
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_force_mod__array__sigma(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sigma = _arrays[array_handle]
    else:
        sigma = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_force_mod__array__sigma)
        _arrays[array_handle] = sigma
    return sigma

def set_array_sigma(sigma):
    sigma[...] = sigma

def get_lforce():
    """
    Element lforce ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 348
    
    """
    return _qepy.f90wrap_force_mod__get__lforce()

def set_lforce(lforce):
    _qepy.f90wrap_force_mod__set__lforce(lforce)

def get_lstres():
    """
    Element lstres ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 350
    
    """
    return _qepy.f90wrap_force_mod__get__lstres()

def set_lstres(lstres):
    _qepy.f90wrap_force_mod__set__lstres(lstres)


_array_initialisers = [get_array_force, get_array_sigma]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "force_mod".')

for func in _dt_array_initialisers:
    func()
