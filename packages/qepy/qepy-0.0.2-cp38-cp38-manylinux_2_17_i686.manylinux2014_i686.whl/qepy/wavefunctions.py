"""
Module wavefunctions


Defined at wavefunctions.fpp lines 13-48

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def deallocate_wavefunctions():
    """
    deallocate_wavefunctions()
    
    
    Defined at wavefunctions.fpp lines 39-46
    
    
    """
    _qepy.f90wrap_deallocate_wavefunctions()

def get_array_evc():
    """
    Element evc ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 20
    
    """
    global evc
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__evc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        evc = _arrays[array_handle]
    else:
        evc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__evc)
        _arrays[array_handle] = evc
    return evc

def set_array_evc(evc):
    evc[...] = evc

def get_array_psic():
    """
    Element psic ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 26
    
    """
    global psic
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__psic(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        psic = _arrays[array_handle]
    else:
        psic = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__psic)
        _arrays[array_handle] = psic
    return psic

def set_array_psic(psic):
    psic[...] = psic

def get_array_psic_nc():
    """
    Element psic_nc ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 26
    
    """
    global psic_nc
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__psic_nc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        psic_nc = _arrays[array_handle]
    else:
        psic_nc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__psic_nc)
        _arrays[array_handle] = psic_nc
    return psic_nc

def set_array_psic_nc(psic_nc):
    psic_nc[...] = psic_nc

def get_array_c0_bgrp():
    """
    Element c0_bgrp ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 33
    
    """
    global c0_bgrp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__c0_bgrp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        c0_bgrp = _arrays[array_handle]
    else:
        c0_bgrp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__c0_bgrp)
        _arrays[array_handle] = c0_bgrp
    return c0_bgrp

def set_array_c0_bgrp(c0_bgrp):
    c0_bgrp[...] = c0_bgrp

def get_array_cm_bgrp():
    """
    Element cm_bgrp ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 34
    
    """
    global cm_bgrp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__cm_bgrp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cm_bgrp = _arrays[array_handle]
    else:
        cm_bgrp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__cm_bgrp)
        _arrays[array_handle] = cm_bgrp
    return cm_bgrp

def set_array_cm_bgrp(cm_bgrp):
    cm_bgrp[...] = cm_bgrp

def get_array_phi_bgrp():
    """
    Element phi_bgrp ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 35
    
    """
    global phi_bgrp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__phi_bgrp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        phi_bgrp = _arrays[array_handle]
    else:
        phi_bgrp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__phi_bgrp)
        _arrays[array_handle] = phi_bgrp
    return phi_bgrp

def set_array_phi_bgrp(phi_bgrp):
    phi_bgrp[...] = phi_bgrp

def get_array_cv0():
    """
    Element cv0 ftype=complex(dp) pytype=complex
    
    
    Defined at wavefunctions.fpp line 37
    
    """
    global cv0
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_wavefunctions__array__cv0(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cv0 = _arrays[array_handle]
    else:
        cv0 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_wavefunctions__array__cv0)
        _arrays[array_handle] = cv0
    return cv0

def set_array_cv0(cv0):
    cv0[...] = cv0


_array_initialisers = [get_array_evc, get_array_psic, get_array_psic_nc, \
    get_array_c0_bgrp, get_array_cm_bgrp, get_array_phi_bgrp, get_array_cv0]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "wavefunctions".')

for func in _dt_array_initialisers:
    func()
