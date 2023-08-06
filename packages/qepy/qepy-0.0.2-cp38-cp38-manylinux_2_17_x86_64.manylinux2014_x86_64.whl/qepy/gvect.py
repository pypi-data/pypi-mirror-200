"""
Module gvect


Defined at recvec.fpp lines 13-177

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def gvect_init(ngm_, comm):
    """
    gvect_init(ngm_, comm)
    
    
    Defined at recvec.fpp lines 66-96
    
    Parameters
    ----------
    ngm_ : int
    comm : int
    
    """
    _qepy.f90wrap_gvect_init(ngm_=ngm_, comm=comm)

def deallocate_gvect(vc=None):
    """
    deallocate_gvect([vc])
    
    
    Defined at recvec.fpp lines 98-118
    
    Parameters
    ----------
    vc : bool
    
    """
    _qepy.f90wrap_deallocate_gvect(vc=vc)

def deallocate_gvect_exx():
    """
    deallocate_gvect_exx()
    
    
    Defined at recvec.fpp lines 120-125
    
    
    """
    _qepy.f90wrap_deallocate_gvect_exx()

def gshells(vc):
    """
    gshells(vc)
    
    
    Defined at recvec.fpp lines 129-175
    
    Parameters
    ----------
    vc : bool
    
    ----------------------------------------------------------------------
     calculate number of G shells: ngl, and the index ng = igtongl(ig)
     that gives the shell index ng for(local) G-vector of index ig
    """
    _qepy.f90wrap_gshells(vc=vc)

def get_ngm():
    """
    Element ngm ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 23
    
    """
    return _qepy.f90wrap_gvect__get__ngm()

def set_ngm(ngm):
    _qepy.f90wrap_gvect__set__ngm(ngm)

def get_ngm_g():
    """
    Element ngm_g ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 25
    
    """
    return _qepy.f90wrap_gvect__get__ngm_g()

def set_ngm_g(ngm_g):
    _qepy.f90wrap_gvect__set__ngm_g(ngm_g)

def get_ngl():
    """
    Element ngl ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 27
    
    """
    return _qepy.f90wrap_gvect__get__ngl()

def set_ngl(ngl):
    _qepy.f90wrap_gvect__set__ngl(ngl)

def get_ngmx():
    """
    Element ngmx ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 28
    
    """
    return _qepy.f90wrap_gvect__get__ngmx()

def set_ngmx(ngmx):
    _qepy.f90wrap_gvect__set__ngmx(ngmx)

def get_ecutrho():
    """
    Element ecutrho ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 29
    
    """
    return _qepy.f90wrap_gvect__get__ecutrho()

def set_ecutrho(ecutrho):
    _qepy.f90wrap_gvect__set__ecutrho(ecutrho)

def get_gcutm():
    """
    Element gcutm ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 30
    
    """
    return _qepy.f90wrap_gvect__get__gcutm()

def set_gcutm(gcutm):
    _qepy.f90wrap_gvect__set__gcutm(gcutm)

def get_gstart():
    """
    Element gstart ftype=integer  pytype=int
    
    
    Defined at recvec.fpp line 31
    
    """
    return _qepy.f90wrap_gvect__get__gstart()

def set_gstart(gstart):
    _qepy.f90wrap_gvect__set__gstart(gstart)

def get_array_gg():
    """
    Element gg ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 36
    
    """
    global gg
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__gg(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        gg = _arrays[array_handle]
    else:
        gg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__gg)
        _arrays[array_handle] = gg
    return gg

def set_array_gg(gg):
    gg[...] = gg

def get_array_g():
    """
    Element g ftype=real(dp) pytype=float
    
    
    Defined at recvec.fpp line 45
    
    """
    global g
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        g = _arrays[array_handle]
    else:
        g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__g)
        _arrays[array_handle] = g
    return g

def set_array_g(g):
    g[...] = g

def get_array_mill():
    """
    Element mill ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 50
    
    """
    global mill
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__mill(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mill = _arrays[array_handle]
    else:
        mill = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__mill)
        _arrays[array_handle] = mill
    return mill

def set_array_mill(mill):
    mill[...] = mill

def get_array_ig_l2g():
    """
    Element ig_l2g ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 55
    
    """
    global ig_l2g
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__ig_l2g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ig_l2g = _arrays[array_handle]
    else:
        ig_l2g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__ig_l2g)
        _arrays[array_handle] = ig_l2g
    return ig_l2g

def set_array_ig_l2g(ig_l2g):
    ig_l2g[...] = ig_l2g

def get_array_mill_g():
    """
    Element mill_g ftype=integer pytype=int
    
    
    Defined at recvec.fpp line 59
    
    """
    global mill_g
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__mill_g(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        mill_g = _arrays[array_handle]
    else:
        mill_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__mill_g)
        _arrays[array_handle] = mill_g
    return mill_g

def set_array_mill_g(mill_g):
    mill_g[...] = mill_g

def get_array_eigts1():
    """
    Element eigts1 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 63
    
    """
    global eigts1
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__eigts1(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts1 = _arrays[array_handle]
    else:
        eigts1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__eigts1)
        _arrays[array_handle] = eigts1
    return eigts1

def set_array_eigts1(eigts1):
    eigts1[...] = eigts1

def get_array_eigts2():
    """
    Element eigts2 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 63
    
    """
    global eigts2
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__eigts2(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts2 = _arrays[array_handle]
    else:
        eigts2 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__eigts2)
        _arrays[array_handle] = eigts2
    return eigts2

def set_array_eigts2(eigts2):
    eigts2[...] = eigts2

def get_array_eigts3():
    """
    Element eigts3 ftype=complex(dp) pytype=complex
    
    
    Defined at recvec.fpp line 63
    
    """
    global eigts3
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_gvect__array__eigts3(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        eigts3 = _arrays[array_handle]
    else:
        eigts3 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_gvect__array__eigts3)
        _arrays[array_handle] = eigts3
    return eigts3

def set_array_eigts3(eigts3):
    eigts3[...] = eigts3


_array_initialisers = [get_array_gg, get_array_g, get_array_mill, \
    get_array_ig_l2g, get_array_mill_g, get_array_eigts1, get_array_eigts2, \
    get_array_eigts3]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "gvect".')

for func in _dt_array_initialisers:
    func()
