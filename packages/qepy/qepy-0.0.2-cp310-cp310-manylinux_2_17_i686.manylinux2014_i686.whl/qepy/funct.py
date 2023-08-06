"""
Module funct


Defined at funct.fpp lines 13-1353

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def set_dft_from_name(dft_):
    """
    set_dft_from_name(dft_)
    
    
    Defined at funct.fpp lines 385-729
    
    Parameters
    ----------
    dft_ : str
    
    -----------------------------------------------------------------------
     Translates a string containing the exchange-correlation name
     into internal indices iexch, icorr, igcx, igcc, inlc, imeta.
    """
    _qepy.f90wrap_set_dft_from_name(dft_=dft_)

def set_auxiliary_flags():
    """
    set_auxiliary_flags()
    
    
    Defined at funct.fpp lines 771-810
    
    
    -----------------------------------------------------------------------
     Set logical flags describing the complexity of the xc functional
     define the fraction of exact exchange used by hybrid fuctionals.
    """
    _qepy.f90wrap_set_auxiliary_flags()

def enforce_input_dft(dft_, nomsg=None):
    """
    enforce_input_dft(dft_[, nomsg])
    
    
    Defined at funct.fpp lines 838-865
    
    Parameters
    ----------
    dft_ : str
    nomsg : bool
    
    ---------------------------------------------------------------------
     Translates a string containing the exchange-correlation name
     into internal indices and force any subsequent call to
     \(\textrm{set_dft_from_name}\) to return without changing them.
    """
    _qepy.f90wrap_enforce_input_dft(dft_=dft_, nomsg=nomsg)

def enforce_dft_exxrpa():
    """
    enforce_dft_exxrpa()
    
    
    Defined at funct.fpp lines 870-888
    
    
    ---------------------------------------------------------------------
    """
    _qepy.f90wrap_enforce_dft_exxrpa()

def init_dft_exxrpa():
    """
    init_dft_exxrpa()
    
    
    Defined at funct.fpp lines 893-907
    
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_init_dft_exxrpa()

def start_exx():
    """
    start_exx()
    
    
    Defined at funct.fpp lines 912-915
    
    
    """
    _qepy.f90wrap_start_exx()

def stop_exx():
    """
    stop_exx()
    
    
    Defined at funct.fpp lines 918-921
    
    
    """
    _qepy.f90wrap_stop_exx()

def dft_force_hybrid(request=None):
    """
    dft_force_hybrid([request])
    
    
    Defined at funct.fpp lines 924-933
    
    Parameters
    ----------
    request : bool
    
    """
    _qepy.f90wrap_dft_force_hybrid(request=request)

def exx_is_active():
    """
    exx_is_active = exx_is_active()
    
    
    Defined at funct.fpp lines 936-938
    
    
    Returns
    -------
    exx_is_active : bool
    
    """
    exx_is_active = _qepy.f90wrap_exx_is_active()
    return exx_is_active

def set_exx_fraction(exxf_):
    """
    set_exx_fraction(exxf_)
    
    
    Defined at funct.fpp lines 941-945
    
    Parameters
    ----------
    exxf_ : float
    
    """
    _qepy.f90wrap_set_exx_fraction(exxf_=exxf_)

def set_screening_parameter(scrparm_):
    """
    set_screening_parameter(scrparm_)
    
    
    Defined at funct.fpp lines 948-953
    
    Parameters
    ----------
    scrparm_ : float
    
    """
    _qepy.f90wrap_set_screening_parameter(scrparm_=scrparm_)

def get_screening_parameter():
    """
    get_screening_parameter = get_screening_parameter()
    
    
    Defined at funct.fpp lines 956-959
    
    
    Returns
    -------
    get_screening_parameter : float
    
    """
    get_screening_parameter = _qepy.f90wrap_get_screening_parameter()
    return get_screening_parameter

def set_gau_parameter(gauparm_):
    """
    set_gau_parameter(gauparm_)
    
    
    Defined at funct.fpp lines 962-967
    
    Parameters
    ----------
    gauparm_ : float
    
    """
    _qepy.f90wrap_set_gau_parameter(gauparm_=gauparm_)

def get_gau_parameter():
    """
    get_gau_parameter = get_gau_parameter()
    
    
    Defined at funct.fpp lines 970-973
    
    
    Returns
    -------
    get_gau_parameter : float
    
    """
    get_gau_parameter = _qepy.f90wrap_get_gau_parameter()
    return get_gau_parameter

def get_iexch():
    """
    get_iexch = get_iexch()
    
    
    Defined at funct.fpp lines 976-979
    
    
    Returns
    -------
    get_iexch : int
    
    """
    get_iexch = _qepy.f90wrap_get_iexch()
    return get_iexch

def get_icorr():
    """
    get_icorr = get_icorr()
    
    
    Defined at funct.fpp lines 982-985
    
    
    Returns
    -------
    get_icorr : int
    
    """
    get_icorr = _qepy.f90wrap_get_icorr()
    return get_icorr

def get_igcx():
    """
    get_igcx = get_igcx()
    
    
    Defined at funct.fpp lines 988-991
    
    
    Returns
    -------
    get_igcx : int
    
    """
    get_igcx = _qepy.f90wrap_get_igcx()
    return get_igcx

def get_igcc():
    """
    get_igcc = get_igcc()
    
    
    Defined at funct.fpp lines 994-997
    
    
    Returns
    -------
    get_igcc : int
    
    """
    get_igcc = _qepy.f90wrap_get_igcc()
    return get_igcc

def get_meta():
    """
    get_meta = get_meta()
    
    
    Defined at funct.fpp lines 1000-1003
    
    
    Returns
    -------
    get_meta : int
    
    """
    get_meta = _qepy.f90wrap_get_meta()
    return get_meta

def get_metac():
    """
    get_metac = get_metac()
    
    
    Defined at funct.fpp lines 1006-1009
    
    
    Returns
    -------
    get_metac : int
    
    """
    get_metac = _qepy.f90wrap_get_metac()
    return get_metac

def get_inlc():
    """
    get_inlc = get_inlc()
    
    
    Defined at funct.fpp lines 1012-1015
    
    
    Returns
    -------
    get_inlc : int
    
    """
    get_inlc = _qepy.f90wrap_get_inlc()
    return get_inlc

def get_nonlocc_name():
    """
    get_nonlocc_name = get_nonlocc_name()
    
    
    Defined at funct.fpp lines 1018-1021
    
    
    Returns
    -------
    get_nonlocc_name : str
    
    """
    get_nonlocc_name = _qepy.f90wrap_get_nonlocc_name()
    return get_nonlocc_name

def dft_is_nonlocc():
    """
    dft_is_nonlocc = dft_is_nonlocc()
    
    
    Defined at funct.fpp lines 1024-1027
    
    
    Returns
    -------
    dft_is_nonlocc : bool
    
    """
    dft_is_nonlocc = _qepy.f90wrap_dft_is_nonlocc()
    return dft_is_nonlocc

def get_exx_fraction():
    """
    get_exx_fraction = get_exx_fraction()
    
    
    Defined at funct.fpp lines 1030-1034
    
    
    Returns
    -------
    get_exx_fraction : float
    
    """
    get_exx_fraction = _qepy.f90wrap_get_exx_fraction()
    return get_exx_fraction

def get_dft_name():
    """
    get_dft_name = get_dft_name()
    
    
    Defined at funct.fpp lines 1037-1040
    
    
    Returns
    -------
    get_dft_name : str
    
    """
    get_dft_name = _qepy.f90wrap_get_dft_name()
    return get_dft_name

def dft_is_gradient():
    """
    dft_is_gradient = dft_is_gradient()
    
    
    Defined at funct.fpp lines 1043-1046
    
    
    Returns
    -------
    dft_is_gradient : bool
    
    """
    dft_is_gradient = _qepy.f90wrap_dft_is_gradient()
    return dft_is_gradient

def dft_is_meta():
    """
    dft_is_meta = dft_is_meta()
    
    
    Defined at funct.fpp lines 1049-1052
    
    
    Returns
    -------
    dft_is_meta : bool
    
    """
    dft_is_meta = _qepy.f90wrap_dft_is_meta()
    return dft_is_meta

def dft_is_hybrid():
    """
    dft_is_hybrid = dft_is_hybrid()
    
    
    Defined at funct.fpp lines 1055-1058
    
    
    Returns
    -------
    dft_is_hybrid : bool
    
    """
    dft_is_hybrid = _qepy.f90wrap_dft_is_hybrid()
    return dft_is_hybrid

def igcc_is_lyp():
    """
    igcc_is_lyp = igcc_is_lyp()
    
    
    Defined at funct.fpp lines 1061-1064
    
    
    Returns
    -------
    igcc_is_lyp : bool
    
    """
    igcc_is_lyp = _qepy.f90wrap_igcc_is_lyp()
    return igcc_is_lyp

def dft_has_finite_size_correction():
    """
    dft_has_finite_size_correction = dft_has_finite_size_correction()
    
    
    Defined at funct.fpp lines 1067-1070
    
    
    Returns
    -------
    dft_has_finite_size_correction : bool
    
    """
    dft_has_finite_size_correction = _qepy.f90wrap_dft_has_finite_size_correction()
    return dft_has_finite_size_correction

def set_finite_size_volume(volume):
    """
    set_finite_size_volume(volume)
    
    
    Defined at funct.fpp lines 1073-1082
    
    Parameters
    ----------
    volume : float
    
    """
    _qepy.f90wrap_set_finite_size_volume(volume=volume)

def get_finite_size_cell_volume():
    """
    is_present, volume = get_finite_size_cell_volume()
    
    
    Defined at funct.fpp lines 1086-1091
    
    
    Returns
    -------
    is_present : bool
    volume : float
    
    """
    is_present, volume = _qepy.f90wrap_get_finite_size_cell_volume()
    return is_present, volume

def set_dft_from_indices(iexch_, icorr_, igcx_, igcc_, imeta_, inlc_):
    """
    set_dft_from_indices(iexch_, icorr_, igcx_, igcc_, imeta_, inlc_)
    
    
    Defined at funct.fpp lines 1098-1135
    
    Parameters
    ----------
    iexch_ : int
    icorr_ : int
    igcx_ : int
    igcc_ : int
    imeta_ : int
    inlc_ : int
    
    """
    _qepy.f90wrap_set_dft_from_indices(iexch_=iexch_, icorr_=icorr_, igcx_=igcx_, \
        igcc_=igcc_, imeta_=imeta_, inlc_=inlc_)

def get_dft_short():
    """
    get_dft_short = get_dft_short()
    
    
    Defined at funct.fpp lines 1140-1261
    
    
    Returns
    -------
    get_dft_short : str
    
    ---------------------------------------------------------------------
    """
    get_dft_short = _qepy.f90wrap_get_dft_short()
    return get_dft_short

def get_dft_long():
    """
    get_dft_long = get_dft_long()
    
    
    Defined at funct.fpp lines 1266-1281
    
    
    Returns
    -------
    get_dft_long : str
    
    ---------------------------------------------------------------------
    """
    get_dft_long = _qepy.f90wrap_get_dft_long()
    return get_dft_long

def write_dft_name():
    """
    write_dft_name()
    
    
    Defined at funct.fpp lines 1286-1292
    
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_write_dft_name()

def nlc(rho_valence, rho_core, nspin, enl, vnl, v):
    """
    nlc(rho_valence, rho_core, nspin, enl, vnl, v)
    
    
    Defined at funct.fpp lines 1301-1347
    
    Parameters
    ----------
    rho_valence : float array
    rho_core : float array
    nspin : int
    enl : float
    vnl : float
    v : float array
    
    -----------------------------------------------------------------------
         non-local contribution to the correlation energy
         input      :  rho_valence, rho_core
         definition :  E_nl = \int E_nl(rho',grho',rho'',grho'',|r'-r''|) dr
         output     :  enl = E^nl_c
                       vnl = D(E^nl_c)/D(rho)
                       v   = non-local contribution to the potential
    """
    _qepy.f90wrap_nlc(rho_valence=rho_valence, rho_core=rho_core, nspin=nspin, \
        enl=enl, vnl=vnl, v=v)

def get_array_is_libxc():
    """
    Element is_libxc ftype=logical pytype=bool
    
    
    Defined at funct.fpp line 340
    
    """
    global is_libxc
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_funct__array__is_libxc(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        is_libxc = _arrays[array_handle]
    else:
        is_libxc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_funct__array__is_libxc)
        _arrays[array_handle] = is_libxc
    return is_libxc

def set_array_is_libxc(is_libxc):
    is_libxc[...] = is_libxc

def get_scan_exx():
    """
    Element scan_exx ftype=logical pytype=bool
    
    
    Defined at funct.fpp line 351
    
    """
    return _qepy.f90wrap_funct__get__scan_exx()

def set_scan_exx(scan_exx):
    _qepy.f90wrap_funct__set__scan_exx(scan_exx)


_array_initialisers = [get_array_is_libxc]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "funct".')

for func in _dt_array_initialisers:
    func()
