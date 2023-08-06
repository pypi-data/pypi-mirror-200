"""
Module uspp


Defined at uspp.fpp lines 95-320

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def aainit(lli):
    """
    aainit(lli)
    
    
    Defined at uspp.fpp lines 165-235
    
    Parameters
    ----------
    lli : int
    
    -----------------------------------------------------------------------
     this routine computes the coefficients of the expansion of the product
     of two real spherical harmonics into real spherical harmonics.
         Y_limi(r) * Y_ljmj(r) = \sum_LM  ap(LM,limi,ljmj)  Y_LM(r)
     On output:
     ap     the expansion coefficients
     lpx    for each input limi,ljmj is the number of LM in the sum
     lpl    for each input limi,ljmj points to the allowed LM
     The indices limi,ljmj and LM assume the order for real spherical
     harmonics given in routine ylmr2
    """
    _qepy.f90wrap_aainit(lli=lli)

def deallocate_uspp():
    """
    deallocate_uspp()
    
    
    Defined at uspp.fpp lines 297-318
    
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_deallocate_uspp()

def get_nlx():
    """
    Element nlx ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 114
    
    """
    return _qepy.f90wrap_uspp__get__nlx()

nlx = get_nlx()

def get_array_lpx():
    """
    Element lpx ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 117
    
    """
    global lpx
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__lpx(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpx = _arrays[array_handle]
    else:
        lpx = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__lpx)
        _arrays[array_handle] = lpx
    return lpx

def set_array_lpx(lpx):
    lpx[...] = lpx

def get_array_lpl():
    """
    Element lpl ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 117
    
    """
    global lpl
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__lpl(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        lpl = _arrays[array_handle]
    else:
        lpl = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__lpl)
        _arrays[array_handle] = lpl
    return lpl

def set_array_lpl(lpl):
    lpl[...] = lpl

def get_array_ap():
    """
    Element ap ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 119
    
    """
    global ap
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__ap(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ap = _arrays[array_handle]
    else:
        ap = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__ap)
        _arrays[array_handle] = ap
    return ap

def set_array_ap(ap):
    ap[...] = ap

def get_nkb():
    """
    Element nkb ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 123
    
    """
    return _qepy.f90wrap_uspp__get__nkb()

def set_nkb(nkb):
    _qepy.f90wrap_uspp__set__nkb(nkb)

def get_nkbus():
    """
    Element nkbus ftype=integer  pytype=int
    
    
    Defined at uspp.fpp line 123
    
    """
    return _qepy.f90wrap_uspp__get__nkbus()

def set_nkbus(nkbus):
    _qepy.f90wrap_uspp__set__nkbus(nkbus)

def get_array_indv():
    """
    Element indv ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 130
    
    """
    global indv
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__indv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        indv = _arrays[array_handle]
    else:
        indv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__indv)
        _arrays[array_handle] = indv
    return indv

def set_array_indv(indv):
    indv[...] = indv

def get_array_nhtol():
    """
    Element nhtol ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 130
    
    """
    global nhtol
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__nhtol(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtol = _arrays[array_handle]
    else:
        nhtol = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__nhtol)
        _arrays[array_handle] = nhtol
    return nhtol

def set_array_nhtol(nhtol):
    nhtol[...] = nhtol

def get_array_nhtolm():
    """
    Element nhtolm ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 130
    
    """
    global nhtolm
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__nhtolm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtolm = _arrays[array_handle]
    else:
        nhtolm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__nhtolm)
        _arrays[array_handle] = nhtolm
    return nhtolm

def set_array_nhtolm(nhtolm):
    nhtolm[...] = nhtolm

def get_array_ijtoh():
    """
    Element ijtoh ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 130
    
    """
    global ijtoh
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__ijtoh(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ijtoh = _arrays[array_handle]
    else:
        ijtoh = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__ijtoh)
        _arrays[array_handle] = ijtoh
    return ijtoh

def set_array_ijtoh(ijtoh):
    ijtoh[...] = ijtoh

def get_array_indv_ijkb0():
    """
    Element indv_ijkb0 ftype=integer pytype=int
    
    
    Defined at uspp.fpp line 130
    
    """
    global indv_ijkb0
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__indv_ijkb0(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        indv_ijkb0 = _arrays[array_handle]
    else:
        indv_ijkb0 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__indv_ijkb0)
        _arrays[array_handle] = indv_ijkb0
    return indv_ijkb0

def set_array_indv_ijkb0(indv_ijkb0):
    indv_ijkb0[...] = indv_ijkb0

def get_okvan():
    """
    Element okvan ftype=logical pytype=bool
    
    
    Defined at uspp.fpp line 134
    
    """
    return _qepy.f90wrap_uspp__get__okvan()

def set_okvan(okvan):
    _qepy.f90wrap_uspp__set__okvan(okvan)

def get_nlcc_any():
    """
    Element nlcc_any ftype=logical pytype=bool
    
    
    Defined at uspp.fpp line 134
    
    """
    return _qepy.f90wrap_uspp__get__nlcc_any()

def set_nlcc_any(nlcc_any):
    _qepy.f90wrap_uspp__set__nlcc_any(nlcc_any)

def get_array_vkb():
    """
    Element vkb ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 137
    
    """
    global vkb
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__vkb(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vkb = _arrays[array_handle]
    else:
        vkb = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__vkb)
        _arrays[array_handle] = vkb
    return vkb

def set_array_vkb(vkb):
    vkb[...] = vkb

def get_array_becsum():
    """
    Element becsum ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 139
    
    """
    global becsum
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__becsum(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        becsum = _arrays[array_handle]
    else:
        becsum = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__becsum)
        _arrays[array_handle] = becsum
    return becsum

def set_array_becsum(becsum):
    becsum[...] = becsum

def get_array_ebecsum():
    """
    Element ebecsum ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 141
    
    """
    global ebecsum
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__ebecsum(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ebecsum = _arrays[array_handle]
    else:
        ebecsum = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__ebecsum)
        _arrays[array_handle] = ebecsum
    return ebecsum

def set_array_ebecsum(ebecsum):
    ebecsum[...] = ebecsum

def get_array_dvan():
    """
    Element dvan ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 147
    
    """
    global dvan
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__dvan(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan = _arrays[array_handle]
    else:
        dvan = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__dvan)
        _arrays[array_handle] = dvan
    return dvan

def set_array_dvan(dvan):
    dvan[...] = dvan

def get_array_deeq():
    """
    Element deeq ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 147
    
    """
    global deeq
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__deeq(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        deeq = _arrays[array_handle]
    else:
        deeq = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__deeq)
        _arrays[array_handle] = deeq
    return deeq

def set_array_deeq(deeq):
    deeq[...] = deeq

def get_array_qq_nt():
    """
    Element qq_nt ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 147
    
    """
    global qq_nt
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__qq_nt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_nt = _arrays[array_handle]
    else:
        qq_nt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__qq_nt)
        _arrays[array_handle] = qq_nt
    return qq_nt

def set_array_qq_nt(qq_nt):
    qq_nt[...] = qq_nt

def get_array_qq_at():
    """
    Element qq_at ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 147
    
    """
    global qq_at
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__qq_at(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_at = _arrays[array_handle]
    else:
        qq_at = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__qq_at)
        _arrays[array_handle] = qq_at
    return qq_at

def set_array_qq_at(qq_at):
    qq_at[...] = qq_at

def get_array_nhtoj():
    """
    Element nhtoj ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 147
    
    """
    global nhtoj
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__nhtoj(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        nhtoj = _arrays[array_handle]
    else:
        nhtoj = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__nhtoj)
        _arrays[array_handle] = nhtoj
    return nhtoj

def set_array_nhtoj(nhtoj):
    nhtoj[...] = nhtoj

def get_array_qq_so():
    """
    Element qq_so ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 152
    
    """
    global qq_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__qq_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        qq_so = _arrays[array_handle]
    else:
        qq_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__qq_so)
        _arrays[array_handle] = qq_so
    return qq_so

def set_array_qq_so(qq_so):
    qq_so[...] = qq_so

def get_array_dvan_so():
    """
    Element dvan_so ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 152
    
    """
    global dvan_so
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__dvan_so(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dvan_so = _arrays[array_handle]
    else:
        dvan_so = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__dvan_so)
        _arrays[array_handle] = dvan_so
    return dvan_so

def set_array_dvan_so(dvan_so):
    dvan_so[...] = dvan_so

def get_array_deeq_nc():
    """
    Element deeq_nc ftype=complex(dp) pytype=complex
    
    
    Defined at uspp.fpp line 152
    
    """
    global deeq_nc
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__deeq_nc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        deeq_nc = _arrays[array_handle]
    else:
        deeq_nc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__deeq_nc)
        _arrays[array_handle] = deeq_nc
    return deeq_nc

def set_array_deeq_nc(deeq_nc):
    deeq_nc[...] = deeq_nc

def get_array_beta():
    """
    Element beta ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 158
    
    """
    global beta
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__beta(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        beta = _arrays[array_handle]
    else:
        beta = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__beta)
        _arrays[array_handle] = beta
    return beta

def set_array_beta(beta):
    beta[...] = beta

def get_array_dbeta():
    """
    Element dbeta ftype=real(dp) pytype=float
    
    
    Defined at uspp.fpp line 160
    
    """
    global dbeta
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_uspp__array__dbeta(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        dbeta = _arrays[array_handle]
    else:
        dbeta = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_uspp__array__dbeta)
        _arrays[array_handle] = dbeta
    return dbeta

def set_array_dbeta(dbeta):
    dbeta[...] = dbeta


_array_initialisers = [get_array_lpx, get_array_lpl, get_array_ap, \
    get_array_indv, get_array_nhtol, get_array_nhtolm, get_array_ijtoh, \
    get_array_indv_ijkb0, get_array_vkb, get_array_becsum, get_array_ebecsum, \
    get_array_dvan, get_array_deeq, get_array_qq_nt, get_array_qq_at, \
    get_array_nhtoj, get_array_qq_so, get_array_dvan_so, get_array_deeq_nc, \
    get_array_beta, get_array_dbeta]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "uspp".')

for func in _dt_array_initialisers:
    func()
