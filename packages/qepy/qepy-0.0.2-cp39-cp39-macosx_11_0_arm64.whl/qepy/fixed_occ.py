"""
Module fixed_occ


Defined at pwcom.fpp lines 442-458

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_array_f_inp():
    """
    Element f_inp ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 450
    
    """
    global f_inp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_fixed_occ__array__f_inp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        f_inp = _arrays[array_handle]
    else:
        f_inp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_fixed_occ__array__f_inp)
        _arrays[array_handle] = f_inp
    return f_inp

def set_array_f_inp(f_inp):
    f_inp[...] = f_inp

def get_tfixed_occ():
    """
    Element tfixed_occ ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 452
    
    """
    return _qepy.f90wrap_fixed_occ__get__tfixed_occ()

def set_tfixed_occ(tfixed_occ):
    _qepy.f90wrap_fixed_occ__set__tfixed_occ(tfixed_occ)

def get_one_atom_occupations():
    """
    Element one_atom_occupations ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 454
    
    """
    return _qepy.f90wrap_fixed_occ__get__one_atom_occupations()

def set_one_atom_occupations(one_atom_occupations):
    _qepy.f90wrap_fixed_occ__set__one_atom_occupations(one_atom_occupations)


_array_initialisers = [get_array_f_inp]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "fixed_occ".')

for func in _dt_array_initialisers:
    func()
