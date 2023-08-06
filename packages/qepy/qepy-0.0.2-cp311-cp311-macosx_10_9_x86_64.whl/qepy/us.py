"""
Module us


Defined at pwcom.fpp lines 414-437

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_nqxq():
    """
    Element nqxq ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 422
    
    """
    return _qepy.f90wrap_us__get__nqxq()

def set_nqxq(nqxq):
    _qepy.f90wrap_us__set__nqxq(nqxq)

def get_nqx():
    """
    Element nqx ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 424
    
    """
    return _qepy.f90wrap_us__get__nqx()

def set_nqx(nqx):
    _qepy.f90wrap_us__set__nqx(nqx)

def get_dq():
    """
    Element dq ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 426
    
    """
    return _qepy.f90wrap_us__get__dq()

dq = get_dq()

def get_array_qrad():
    """
    Element qrad ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 428
    
    """
    global qrad
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_us__array__qrad(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qrad = _arrays[array_handle]
    else:
        qrad = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_us__array__qrad)
        _arrays[array_handle] = qrad
    return qrad

def set_array_qrad(qrad):
    qrad[...] = qrad

def get_array_tab():
    """
    Element tab ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 430
    
    """
    global tab
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_us__array__tab(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tab = _arrays[array_handle]
    else:
        tab = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_us__array__tab)
        _arrays[array_handle] = tab
    return tab

def set_array_tab(tab):
    tab[...] = tab

def get_array_tab_at():
    """
    Element tab_at ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 432
    
    """
    global tab_at
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_us__array__tab_at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tab_at = _arrays[array_handle]
    else:
        tab_at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_us__array__tab_at)
        _arrays[array_handle] = tab_at
    return tab_at

def set_array_tab_at(tab_at):
    tab_at[...] = tab_at

def get_spline_ps():
    """
    Element spline_ps ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 434
    
    """
    return _qepy.f90wrap_us__get__spline_ps()

def set_spline_ps(spline_ps):
    _qepy.f90wrap_us__set__spline_ps(spline_ps)

def get_array_tab_d2y():
    """
    Element tab_d2y ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 435
    
    """
    global tab_d2y
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_us__array__tab_d2y(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tab_d2y = _arrays[array_handle]
    else:
        tab_d2y = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_us__array__tab_d2y)
        _arrays[array_handle] = tab_d2y
    return tab_d2y

def set_array_tab_d2y(tab_d2y):
    tab_d2y[...] = tab_d2y


_array_initialisers = [get_array_qrad, get_array_tab, get_array_tab_at, \
    get_array_tab_d2y]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "us".')

for func in _dt_array_initialisers:
    func()
