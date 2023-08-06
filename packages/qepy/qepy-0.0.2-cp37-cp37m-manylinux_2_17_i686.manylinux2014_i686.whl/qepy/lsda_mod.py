"""
Module lsda_mod


Defined at pwcom.fpp lines 112-137

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_lsda():
    """
    Element lsda ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 123
    
    """
    return _qepy.f90wrap_lsda_mod__get__lsda()

def set_lsda(lsda):
    _qepy.f90wrap_lsda_mod__set__lsda(lsda)

def get_magtot():
    """
    Element magtot ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 125
    
    """
    return _qepy.f90wrap_lsda_mod__get__magtot()

def set_magtot(magtot):
    _qepy.f90wrap_lsda_mod__set__magtot(magtot)

def get_absmag():
    """
    Element absmag ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 127
    
    """
    return _qepy.f90wrap_lsda_mod__get__absmag()

def set_absmag(absmag):
    _qepy.f90wrap_lsda_mod__set__absmag(absmag)

def get_array_starting_magnetization():
    """
    Element starting_magnetization ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 129
    
    """
    global starting_magnetization
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_lsda_mod__array__starting_magnetization(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        starting_magnetization = _arrays[array_handle]
    else:
        starting_magnetization = \
            f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_lsda_mod__array__starting_magnetization)
        _arrays[array_handle] = starting_magnetization
    return starting_magnetization

def set_array_starting_magnetization(starting_magnetization):
    starting_magnetization[...] = starting_magnetization

def get_nspin():
    """
    Element nspin ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 131
    
    """
    return _qepy.f90wrap_lsda_mod__get__nspin()

def set_nspin(nspin):
    _qepy.f90wrap_lsda_mod__set__nspin(nspin)

def get_current_spin():
    """
    Element current_spin ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 133
    
    """
    return _qepy.f90wrap_lsda_mod__get__current_spin()

def set_current_spin(current_spin):
    _qepy.f90wrap_lsda_mod__set__current_spin(current_spin)

def get_array_isk():
    """
    Element isk ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 135
    
    """
    global isk
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_lsda_mod__array__isk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        isk = _arrays[array_handle]
    else:
        isk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_lsda_mod__array__isk)
        _arrays[array_handle] = isk
    return isk

def set_array_isk(isk):
    isk[...] = isk


_array_initialisers = [get_array_starting_magnetization, get_array_isk]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "lsda_mod".')

for func in _dt_array_initialisers:
    func()
