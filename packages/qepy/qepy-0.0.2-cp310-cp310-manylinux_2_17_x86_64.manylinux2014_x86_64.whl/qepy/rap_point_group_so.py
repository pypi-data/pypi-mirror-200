"""
Module rap_point_group_so


Defined at pwcom.fpp lines 176-204

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nrap():
    """
    Element nrap ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 180
    
    """
    return _qepy.f90wrap_rap_point_group_so__get__nrap()

def set_nrap(nrap):
    _qepy.f90wrap_rap_point_group_so__set__nrap(nrap)

def get_array_nelem_so():
    """
    Element nelem_so ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 182
    
    """
    global nelem_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__nelem_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nelem_so = _arrays[array_handle]
    else:
        nelem_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__nelem_so)
        _arrays[array_handle] = nelem_so
    return nelem_so

def set_array_nelem_so(nelem_so):
    nelem_so[...] = nelem_so

def get_array_elem_so():
    """
    Element elem_so ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 184
    
    """
    global elem_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__elem_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        elem_so = _arrays[array_handle]
    else:
        elem_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__elem_so)
        _arrays[array_handle] = elem_so
    return elem_so

def set_array_elem_so(elem_so):
    elem_so[...] = elem_so

def get_array_has_e():
    """
    Element has_e ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 186
    
    """
    global has_e
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__has_e(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        has_e = _arrays[array_handle]
    else:
        has_e = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__has_e)
        _arrays[array_handle] = has_e
    return has_e

def set_array_has_e(has_e):
    has_e[...] = has_e

def get_array_which_irr_so():
    """
    Element which_irr_so ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 188
    
    """
    global which_irr_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__which_irr_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        which_irr_so = _arrays[array_handle]
    else:
        which_irr_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__which_irr_so)
        _arrays[array_handle] = which_irr_so
    return which_irr_so

def set_array_which_irr_so(which_irr_so):
    which_irr_so[...] = which_irr_so

def get_array_char_mat_so():
    """
    Element char_mat_so ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 191
    
    """
    global char_mat_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__char_mat_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        char_mat_so = _arrays[array_handle]
    else:
        char_mat_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__char_mat_so)
        _arrays[array_handle] = char_mat_so
    return char_mat_so

def set_array_char_mat_so(char_mat_so):
    char_mat_so[...] = char_mat_so

def get_array_d_spin():
    """
    Element d_spin ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 193
    
    """
    global d_spin
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__d_spin(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        d_spin = _arrays[array_handle]
    else:
        d_spin = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__d_spin)
        _arrays[array_handle] = d_spin
    return d_spin

def set_array_d_spin(d_spin):
    d_spin[...] = d_spin

def get_array_name_rap_so():
    """
    Element name_rap_so ftype=character(len=15) pytype=str
    
    
    Defined at pwcom.fpp line 196
    
    """
    global name_rap_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__name_rap_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        name_rap_so = _arrays[array_handle]
    else:
        name_rap_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__name_rap_so)
        _arrays[array_handle] = name_rap_so
    return name_rap_so

def set_array_name_rap_so(name_rap_so):
    name_rap_so[...] = name_rap_so

def get_array_name_class_so():
    """
    Element name_class_so ftype=character(len=5) pytype=str
    
    
    Defined at pwcom.fpp line 198
    
    """
    global name_class_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__name_class_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        name_class_so = _arrays[array_handle]
    else:
        name_class_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__name_class_so)
        _arrays[array_handle] = name_class_so
    return name_class_so

def set_array_name_class_so(name_class_so):
    name_class_so[...] = name_class_so

def get_array_name_class_so1():
    """
    Element name_class_so1 ftype=character(len=5) pytype=str
    
    
    Defined at pwcom.fpp line 200
    
    """
    global name_class_so1
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__name_class_so1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        name_class_so1 = _arrays[array_handle]
    else:
        name_class_so1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__name_class_so1)
        _arrays[array_handle] = name_class_so1
    return name_class_so1

def set_array_name_class_so1(name_class_so1):
    name_class_so1[...] = name_class_so1

def get_array_elem_name_so():
    """
    Element elem_name_so ftype=character(len=55) pytype=str
    
    
    Defined at pwcom.fpp line 202
    
    """
    global elem_name_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group_so__array__elem_name_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        elem_name_so = _arrays[array_handle]
    else:
        elem_name_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group_so__array__elem_name_so)
        _arrays[array_handle] = elem_name_so
    return elem_name_so

def set_array_elem_name_so(elem_name_so):
    elem_name_so[...] = elem_name_so


_array_initialisers = [get_array_nelem_so, get_array_elem_so, get_array_has_e, \
    get_array_which_irr_so, get_array_char_mat_so, get_array_d_spin, \
    get_array_name_rap_so, get_array_name_class_so, get_array_name_class_so1, \
    get_array_elem_name_so]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "rap_point_group_so".')

for func in _dt_array_initialisers:
    func()
