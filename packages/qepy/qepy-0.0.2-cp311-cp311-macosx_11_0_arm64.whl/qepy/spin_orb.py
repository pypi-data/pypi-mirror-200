"""
Module spin_orb


Defined at pwcom.fpp lines 463-484

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_lspinorb():
    """
    Element lspinorb ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 472
    
    """
    return _qepy.f90wrap_spin_orb__get__lspinorb()

def set_lspinorb(lspinorb):
    _qepy.f90wrap_spin_orb__set__lspinorb(lspinorb)

def get_lforcet():
    """
    Element lforcet ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 474
    
    """
    return _qepy.f90wrap_spin_orb__get__lforcet()

def set_lforcet(lforcet):
    _qepy.f90wrap_spin_orb__set__lforcet(lforcet)

def get_starting_spin_angle():
    """
    Element starting_spin_angle ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 476
    
    """
    return _qepy.f90wrap_spin_orb__get__starting_spin_angle()

def set_starting_spin_angle(starting_spin_angle):
    _qepy.f90wrap_spin_orb__set__starting_spin_angle(starting_spin_angle)

def get_domag():
    """
    Element domag ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 478
    
    """
    return _qepy.f90wrap_spin_orb__get__domag()

def set_domag(domag):
    _qepy.f90wrap_spin_orb__set__domag(domag)

def get_array_rot_ylm():
    """
    Element rot_ylm ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 480
    
    """
    global rot_ylm
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_spin_orb__array__rot_ylm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rot_ylm = _arrays[array_handle]
    else:
        rot_ylm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_spin_orb__array__rot_ylm)
        _arrays[array_handle] = rot_ylm
    return rot_ylm

def set_array_rot_ylm(rot_ylm):
    rot_ylm[...] = rot_ylm

def get_array_fcoef():
    """
    Element fcoef ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 482
    
    """
    global fcoef
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_spin_orb__array__fcoef(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        fcoef = _arrays[array_handle]
    else:
        fcoef = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_spin_orb__array__fcoef)
        _arrays[array_handle] = fcoef
    return fcoef

def set_array_fcoef(fcoef):
    fcoef[...] = fcoef


_array_initialisers = [get_array_rot_ylm, get_array_fcoef]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "spin_orb".')

for func in _dt_array_initialisers:
    func()
