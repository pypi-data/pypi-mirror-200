"""
Module rap_point_group


Defined at pwcom.fpp lines 142-171

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_code_group():
    """
    Element code_group ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 146
    
    """
    return _qepy.f90wrap_rap_point_group__get__code_group()

def set_code_group(code_group):
    _qepy.f90wrap_rap_point_group__set__code_group(code_group)

def get_nclass():
    """
    Element nclass ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 148
    
    """
    return _qepy.f90wrap_rap_point_group__get__nclass()

def set_nclass(nclass):
    _qepy.f90wrap_rap_point_group__set__nclass(nclass)

def get_array_nelem():
    """
    Element nelem ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 150
    
    """
    global nelem
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__nelem(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nelem = _arrays[array_handle]
    else:
        nelem = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__nelem)
        _arrays[array_handle] = nelem
    return nelem

def set_array_nelem(nelem):
    nelem[...] = nelem

def get_array_elem():
    """
    Element elem ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 152
    
    """
    global elem
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__elem(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        elem = _arrays[array_handle]
    else:
        elem = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__elem)
        _arrays[array_handle] = elem
    return elem

def set_array_elem(elem):
    elem[...] = elem

def get_array_which_irr():
    """
    Element which_irr ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 154
    
    """
    global which_irr
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__which_irr(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        which_irr = _arrays[array_handle]
    else:
        which_irr = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__which_irr)
        _arrays[array_handle] = which_irr
    return which_irr

def set_array_which_irr(which_irr):
    which_irr[...] = which_irr

def get_array_char_mat():
    """
    Element char_mat ftype=complex(dp) pytype=complex
    
    
    Defined at pwcom.fpp line 157
    
    """
    global char_mat
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__char_mat(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        char_mat = _arrays[array_handle]
    else:
        char_mat = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__char_mat)
        _arrays[array_handle] = char_mat
    return char_mat

def set_array_char_mat(char_mat):
    char_mat[...] = char_mat

def get_array_name_rap():
    """
    Element name_rap ftype=character(len=15) pytype=str
    
    
    Defined at pwcom.fpp line 160
    
    """
    global name_rap
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__name_rap(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        name_rap = _arrays[array_handle]
    else:
        name_rap = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__name_rap)
        _arrays[array_handle] = name_rap
    return name_rap

def set_array_name_rap(name_rap):
    name_rap[...] = name_rap

def get_array_ir_ram():
    """
    Element ir_ram ftype=character(len=3) pytype=str
    
    
    Defined at pwcom.fpp line 162
    
    """
    global ir_ram
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__ir_ram(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ir_ram = _arrays[array_handle]
    else:
        ir_ram = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__ir_ram)
        _arrays[array_handle] = ir_ram
    return ir_ram

def set_array_ir_ram(ir_ram):
    ir_ram[...] = ir_ram

def get_gname():
    """
    Element gname ftype=character(len=11) pytype=str
    
    
    Defined at pwcom.fpp line 165
    
    """
    return _qepy.f90wrap_rap_point_group__get__gname()

def set_gname(gname):
    _qepy.f90wrap_rap_point_group__set__gname(gname)

def get_array_name_class():
    """
    Element name_class ftype=character(len=5) pytype=str
    
    
    Defined at pwcom.fpp line 167
    
    """
    global name_class
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__name_class(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        name_class = _arrays[array_handle]
    else:
        name_class = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__name_class)
        _arrays[array_handle] = name_class
    return name_class

def set_array_name_class(name_class):
    name_class[...] = name_class

def get_array_elem_name():
    """
    Element elem_name ftype=character(len=55) pytype=str
    
    
    Defined at pwcom.fpp line 169
    
    """
    global elem_name
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_rap_point_group__array__elem_name(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        elem_name = _arrays[array_handle]
    else:
        elem_name = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_rap_point_group__array__elem_name)
        _arrays[array_handle] = elem_name
    return elem_name

def set_array_elem_name(elem_name):
    elem_name[...] = elem_name


_array_initialisers = [get_array_nelem, get_array_elem, get_array_which_irr, \
    get_array_char_mat, get_array_name_rap, get_array_ir_ram, \
    get_array_name_class, get_array_elem_name]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "rap_point_group".')

for func in _dt_array_initialisers:
    func()
