"""
Module klist


Defined at pwcom.fpp lines 13-107

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def init_igk(npwx, ngm, g, gcutw):
    """
    init_igk(npwx, ngm, g, gcutw)
    
    
    Defined at pwcom.fpp lines 69-96
    
    Parameters
    ----------
    npwx : int
    ngm : int
    g : float array
    gcutw : float
    
    --------------------------------------------------------------
     Initialize indices igk_k and number of plane waves per k-point:
     * (k_ik + G)_i = k_ik + G_igk;
     * i = 1, ngk(ik);
     * igk = igk_k(i,ik).
    """
    _qepy.f90wrap_init_igk(npwx=npwx, ngm=ngm, g=g, gcutw=gcutw)

def deallocate_igk():
    """
    deallocate_igk()
    
    
    Defined at pwcom.fpp lines 100-104
    
    
    """
    _qepy.f90wrap_deallocate_igk()

def get_smearing():
    """
    Element smearing ftype=character(len=32) pytype=str
    
    
    Defined at pwcom.fpp line 24
    
    """
    return _qepy.f90wrap_klist__get__smearing()

def set_smearing(smearing):
    _qepy.f90wrap_klist__set__smearing(smearing)

def get_array_xk():
    """
    Element xk ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 26
    
    """
    global xk
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_klist__array__xk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        xk = _arrays[array_handle]
    else:
        xk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_klist__array__xk)
        _arrays[array_handle] = xk
    return xk

def set_array_xk(xk):
    xk[...] = xk

def get_array_wk():
    """
    Element wk ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 28
    
    """
    global wk
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_klist__array__wk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        wk = _arrays[array_handle]
    else:
        wk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_klist__array__wk)
        _arrays[array_handle] = wk
    return wk

def set_array_wk(wk):
    wk[...] = wk

def get_array_xqq():
    """
    Element xqq ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 30
    
    """
    global xqq
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_klist__array__xqq(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        xqq = _arrays[array_handle]
    else:
        xqq = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_klist__array__xqq)
        _arrays[array_handle] = xqq
    return xqq

def set_array_xqq(xqq):
    xqq[...] = xqq

def get_degauss():
    """
    Element degauss ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 32
    
    """
    return _qepy.f90wrap_klist__get__degauss()

def set_degauss(degauss):
    _qepy.f90wrap_klist__set__degauss(degauss)

def get_nelec():
    """
    Element nelec ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 34
    
    """
    return _qepy.f90wrap_klist__get__nelec()

def set_nelec(nelec):
    _qepy.f90wrap_klist__set__nelec(nelec)

def get_nelup():
    """
    Element nelup ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 36
    
    """
    return _qepy.f90wrap_klist__get__nelup()

def set_nelup(nelup):
    _qepy.f90wrap_klist__set__nelup(nelup)

def get_neldw():
    """
    Element neldw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 38
    
    """
    return _qepy.f90wrap_klist__get__neldw()

def set_neldw(neldw):
    _qepy.f90wrap_klist__set__neldw(neldw)

def get_tot_magnetization():
    """
    Element tot_magnetization ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 40
    
    """
    return _qepy.f90wrap_klist__get__tot_magnetization()

def set_tot_magnetization(tot_magnetization):
    _qepy.f90wrap_klist__set__tot_magnetization(tot_magnetization)

def get_tot_charge():
    """
    Element tot_charge ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 42
    
    """
    return _qepy.f90wrap_klist__get__tot_charge()

def set_tot_charge(tot_charge):
    _qepy.f90wrap_klist__set__tot_charge(tot_charge)

def get_qnorm():
    """
    Element qnorm ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 44
    
    """
    return _qepy.f90wrap_klist__get__qnorm()

def set_qnorm(qnorm):
    _qepy.f90wrap_klist__set__qnorm(qnorm)

def get_array_igk_k():
    """
    Element igk_k ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 46
    
    """
    global igk_k
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_klist__array__igk_k(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        igk_k = _arrays[array_handle]
    else:
        igk_k = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_klist__array__igk_k)
        _arrays[array_handle] = igk_k
    return igk_k

def set_array_igk_k(igk_k):
    igk_k[...] = igk_k

def get_array_ngk():
    """
    Element ngk ftype=integer pytype=int
    
    
    Defined at pwcom.fpp line 48
    
    """
    global ngk
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_klist__array__ngk(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ngk = _arrays[array_handle]
    else:
        ngk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_klist__array__ngk)
        _arrays[array_handle] = ngk
    return ngk

def set_array_ngk(ngk):
    ngk[...] = ngk

def get_nks():
    """
    Element nks ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 51
    
    """
    return _qepy.f90wrap_klist__get__nks()

def set_nks(nks):
    _qepy.f90wrap_klist__set__nks(nks)

def get_nkstot():
    """
    Element nkstot ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 53
    
    """
    return _qepy.f90wrap_klist__get__nkstot()

def set_nkstot(nkstot):
    _qepy.f90wrap_klist__set__nkstot(nkstot)

def get_ngauss():
    """
    Element ngauss ftype=integer  pytype=int
    
    
    Defined at pwcom.fpp line 55
    
    """
    return _qepy.f90wrap_klist__get__ngauss()

def set_ngauss(ngauss):
    _qepy.f90wrap_klist__set__ngauss(ngauss)

def get_lgauss():
    """
    Element lgauss ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 57
    
    """
    return _qepy.f90wrap_klist__get__lgauss()

def set_lgauss(lgauss):
    _qepy.f90wrap_klist__set__lgauss(lgauss)

def get_ltetra():
    """
    Element ltetra ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 59
    
    """
    return _qepy.f90wrap_klist__get__ltetra()

def set_ltetra(ltetra):
    _qepy.f90wrap_klist__set__ltetra(ltetra)

def get_lxkcry():
    """
    Element lxkcry ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 61
    
    """
    return _qepy.f90wrap_klist__get__lxkcry()

def set_lxkcry(lxkcry):
    _qepy.f90wrap_klist__set__lxkcry(lxkcry)

def get_two_fermi_energies():
    """
    Element two_fermi_energies ftype=logical pytype=bool
    
    
    Defined at pwcom.fpp line 63
    
    """
    return _qepy.f90wrap_klist__get__two_fermi_energies()

def set_two_fermi_energies(two_fermi_energies):
    _qepy.f90wrap_klist__set__two_fermi_energies(two_fermi_energies)


_array_initialisers = [get_array_xk, get_array_wk, get_array_xqq, \
    get_array_igk_k, get_array_ngk]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "klist".')

for func in _dt_array_initialisers:
    func()
