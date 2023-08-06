"""
Module cellmd


Defined at pwcom.fpp lines 378-409

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_press():
    """
    Element press ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 386
    
    """
    return _qepy.f90wrap_cellmd__get__press()

def set_press(press):
    _qepy.f90wrap_cellmd__set__press(press)

def get_cmass():
    """
    Element cmass ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 388
    
    """
    return _qepy.f90wrap_cellmd__get__cmass()

def set_cmass(cmass):
    _qepy.f90wrap_cellmd__set__cmass(cmass)

def get_array_at_old():
    """
    Element at_old ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 390
    
    """
    global at_old
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_cellmd__array__at_old(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        at_old = _arrays[array_handle]
    else:
        at_old = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_cellmd__array__at_old)
        _arrays[array_handle] = at_old
    return at_old

def set_array_at_old(at_old):
    at_old[...] = at_old

def get_omega_old():
    """
    Element omega_old ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 392
    
    """
    return _qepy.f90wrap_cellmd__get__omega_old()

def set_omega_old(omega_old):
    _qepy.f90wrap_cellmd__set__omega_old(omega_old)

def get_cell_factor():
    """
    Element cell_factor ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 394
    
    """
    return _qepy.f90wrap_cellmd__get__cell_factor()

def set_cell_factor(cell_factor):
    _qepy.f90wrap_cellmd__set__cell_factor(cell_factor)

def get_nzero():
    """
    Element nzero ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 397
    
    """
    return _qepy.f90wrap_cellmd__get__nzero()

def set_nzero(nzero):
    _qepy.f90wrap_cellmd__set__nzero(nzero)

def get_ntimes():
    """
    Element ntimes ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 399
    
    """
    return _qepy.f90wrap_cellmd__get__ntimes()

def set_ntimes(ntimes):
    _qepy.f90wrap_cellmd__set__ntimes(ntimes)

def get_ntcheck():
    """
    Element ntcheck ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 401
    
    """
    return _qepy.f90wrap_cellmd__get__ntcheck()

def set_ntcheck(ntcheck):
    _qepy.f90wrap_cellmd__set__ntcheck(ntcheck)

def get_lmovecell():
    """
    Element lmovecell ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 403
    
    """
    return _qepy.f90wrap_cellmd__get__lmovecell()

def set_lmovecell(lmovecell):
    _qepy.f90wrap_cellmd__set__lmovecell(lmovecell)

def get_calc():
    """
    Element calc ftype=character(len=2) pytype=str
    
    
    Defined at pwcom.fpp line 406
    
    """
    return _qepy.f90wrap_cellmd__get__calc()

def set_calc(calc):
    _qepy.f90wrap_cellmd__set__calc(calc)


_array_initialisers = [get_array_at_old]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "cellmd".')

for func in _dt_array_initialisers:
    func()
