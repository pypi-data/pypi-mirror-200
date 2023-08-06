"""
Module rap_point_group_is


Defined at pwcom.fpp lines 209-230

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nsym_is():
    """
    Element nsym_is ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 213
    
    """
    return _qepy.f90wrap_rap_point_group_is__get__nsym_is()

def set_nsym_is(nsym_is):
    _qepy.f90wrap_rap_point_group_is__set__nsym_is(nsym_is)

def get_code_group_is():
    """
    Element code_group_is ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 215
    
    """
    return _qepy.f90wrap_rap_point_group_is__get__code_group_is()

def set_code_group_is(code_group_is):
    _qepy.f90wrap_rap_point_group_is__set__code_group_is(code_group_is)

def get_array_ft_is():
    """
    Element ft_is ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 218
    
    """
    global ft_is
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_is__array__ft_is(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ft_is = _arrays[array_handle]
    else:
        ft_is = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_is__array__ft_is)
        _arrays[array_handle] = ft_is
    return ft_is

def set_array_ft_is(ft_is):
    ft_is[...] = ft_is

def get_array_sr_is():
    """
    Element sr_is ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 220
    
    """
    global sr_is
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_is__array__sr_is(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sr_is = _arrays[array_handle]
    else:
        sr_is = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_is__array__sr_is)
        _arrays[array_handle] = sr_is
    return sr_is

def set_array_sr_is(sr_is):
    sr_is[...] = sr_is

def get_array_d_spin_is():
    """
    Element d_spin_is ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 223
    
    """
    global d_spin_is
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_is__array__d_spin_is(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d_spin_is = _arrays[array_handle]
    else:
        d_spin_is = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_is__array__d_spin_is)
        _arrays[array_handle] = d_spin_is
    return d_spin_is

def set_array_d_spin_is(d_spin_is):
    d_spin_is[...] = d_spin_is

def get_array_sname_is():
    """
    Element sname_is ftype=character(len=45) pytype=str
    
    
    Defined at pwcom.fpp line 226
    
    """
    global sname_is
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_is__array__sname_is(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        sname_is = _arrays[array_handle]
    else:
        sname_is = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_is__array__sname_is)
        _arrays[array_handle] = sname_is
    return sname_is

def set_array_sname_is(sname_is):
    sname_is[...] = sname_is

def get_gname_is():
    """
    Element gname_is ftype=character(len=11) pytype=str
    
    
    Defined at pwcom.fpp line 228
    
    """
    return _qepy.f90wrap_rap_point_group_is__get__gname_is()

def set_gname_is(gname_is):
    _qepy.f90wrap_rap_point_group_is__set__gname_is(gname_is)


_array_initialisers = [get_array_ft_is, get_array_sr_is, get_array_d_spin_is, \
    get_array_sname_is]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "rap_point_group_is".')

for func in _dt_array_initialisers:
    func()
