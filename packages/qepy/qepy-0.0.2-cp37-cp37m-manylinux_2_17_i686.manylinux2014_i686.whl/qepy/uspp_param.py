"""
Module uspp_param


Defined at uspp.fpp lines 12-92

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def n_atom_wfc(nat, ityp, noncolin=None):
    """
    n_atom_wfc = n_atom_wfc(nat, ityp[, noncolin])
    
    
    Defined at uspp.fpp lines 39-91
    
    Parameters
    ----------
    nat : int
    ityp : int array
    noncolin : bool
    
    Returns
    -------
    n_atom_wfc : int
    
    ----------------------------------------------------------------------------
     ... Find number of starting atomic orbitals
    """
    n_atom_wfc = _qepy.f90wrap_n_atom_wfc(nat=nat, ityp=ityp, noncolin=noncolin)
    return n_atom_wfc

def get_array_nh():
    """
    Element nh ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 28
    
    """
    global nh
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp_param__array__nh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nh = _arrays[array_handle]
    else:
        nh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp_param__array__nh)
        _arrays[array_handle] = nh
    return nh

def set_array_nh(nh):
    nh[...] = nh

def get_nhm():
    """
    Element nhm ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 28
    
    """
    return _qepy.f90wrap_uspp_param__get__nhm()

def set_nhm(nhm):
    _qepy.f90wrap_uspp_param__set__nhm(nhm)

def get_nbetam():
    """
    Element nbetam ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 28
    
    """
    return _qepy.f90wrap_uspp_param__get__nbetam()

def set_nbetam(nbetam):
    _qepy.f90wrap_uspp_param__set__nbetam(nbetam)

def get_array_iver():
    """
    Element iver ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 28
    
    """
    global iver
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp_param__array__iver(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        iver = _arrays[array_handle]
    else:
        iver = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp_param__array__iver)
        _arrays[array_handle] = iver
    return iver

def set_array_iver(iver):
    iver[...] = iver

def get_lmaxkb():
    """
    Element lmaxkb ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 31
    
    """
    return _qepy.f90wrap_uspp_param__get__lmaxkb()

def set_lmaxkb(lmaxkb):
    _qepy.f90wrap_uspp_param__set__lmaxkb(lmaxkb)

def get_lmaxq():
    """
    Element lmaxq ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 31
    
    """
    return _qepy.f90wrap_uspp_param__get__lmaxq()

def set_lmaxq(lmaxq):
    _qepy.f90wrap_uspp_param__set__lmaxq(lmaxq)

def get_nvb():
    """
    Element nvb ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 34
    
    """
    return _qepy.f90wrap_uspp_param__get__nvb()

def set_nvb(nvb):
    _qepy.f90wrap_uspp_param__set__nvb(nvb)

def get_array_ish():
    """
    Element ish ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 34
    
    """
    global ish
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp_param__array__ish(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ish = _arrays[array_handle]
    else:
        ish = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp_param__array__ish)
        _arrays[array_handle] = ish
    return ish

def set_array_ish(ish):
    ish[...] = ish


_array_initialisers = [get_array_nh, get_array_iver, get_array_ish]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "uspp_param".')

for func in _dt_array_initialisers:
    func()
