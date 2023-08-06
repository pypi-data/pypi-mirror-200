"""
Module ener


Defined at pwcom.fpp lines 287-329

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_etot():
    """
    Element etot ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 295
    
    """
    return _qepy.f90wrap_ener__get__etot()

def set_etot(etot):
    _qepy.f90wrap_ener__set__etot(etot)

def get_hwf_energy():
    """
    Element hwf_energy ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 297
    
    """
    return _qepy.f90wrap_ener__get__hwf_energy()

def set_hwf_energy(hwf_energy):
    _qepy.f90wrap_ener__set__hwf_energy(hwf_energy)

def get_eband():
    """
    Element eband ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 299
    
    """
    return _qepy.f90wrap_ener__get__eband()

def set_eband(eband):
    _qepy.f90wrap_ener__set__eband(eband)

def get_deband():
    """
    Element deband ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 301
    
    """
    return _qepy.f90wrap_ener__get__deband()

def set_deband(deband):
    _qepy.f90wrap_ener__set__deband(deband)

def get_ehart():
    """
    Element ehart ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 303
    
    """
    return _qepy.f90wrap_ener__get__ehart()

def set_ehart(ehart):
    _qepy.f90wrap_ener__set__ehart(ehart)

def get_etxc():
    """
    Element etxc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 305
    
    """
    return _qepy.f90wrap_ener__get__etxc()

def set_etxc(etxc):
    _qepy.f90wrap_ener__set__etxc(etxc)

def get_vtxc():
    """
    Element vtxc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 307
    
    """
    return _qepy.f90wrap_ener__get__vtxc()

def set_vtxc(vtxc):
    _qepy.f90wrap_ener__set__vtxc(vtxc)

def get_etxcc():
    """
    Element etxcc ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 309
    
    """
    return _qepy.f90wrap_ener__get__etxcc()

def set_etxcc(etxcc):
    _qepy.f90wrap_ener__set__etxcc(etxcc)

def get_ewld():
    """
    Element ewld ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 311
    
    """
    return _qepy.f90wrap_ener__get__ewld()

def set_ewld(ewld):
    _qepy.f90wrap_ener__set__ewld(ewld)

def get_elondon():
    """
    Element elondon ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 313
    
    """
    return _qepy.f90wrap_ener__get__elondon()

def set_elondon(elondon):
    _qepy.f90wrap_ener__set__elondon(elondon)

def get_edftd3():
    """
    Element edftd3 ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 315
    
    """
    return _qepy.f90wrap_ener__get__edftd3()

def set_edftd3(edftd3):
    _qepy.f90wrap_ener__set__edftd3(edftd3)

def get_exdm():
    """
    Element exdm ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 317
    
    """
    return _qepy.f90wrap_ener__get__exdm()

def set_exdm(exdm):
    _qepy.f90wrap_ener__set__exdm(exdm)

def get_demet():
    """
    Element demet ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 319
    
    """
    return _qepy.f90wrap_ener__get__demet()

def set_demet(demet):
    _qepy.f90wrap_ener__set__demet(demet)

def get_epaw():
    """
    Element epaw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 321
    
    """
    return _qepy.f90wrap_ener__get__epaw()

def set_epaw(epaw):
    _qepy.f90wrap_ener__set__epaw(epaw)

def get_ef():
    """
    Element ef ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 323
    
    """
    return _qepy.f90wrap_ener__get__ef()

def set_ef(ef):
    _qepy.f90wrap_ener__set__ef(ef)

def get_ef_up():
    """
    Element ef_up ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 325
    
    """
    return _qepy.f90wrap_ener__get__ef_up()

def set_ef_up(ef_up):
    _qepy.f90wrap_ener__set__ef_up(ef_up)

def get_ef_dw():
    """
    Element ef_dw ftype=real(dp) pytype=float
    
    
    Defined at pwcom.fpp line 327
    
    """
    return _qepy.f90wrap_ener__get__ef_dw()

def set_ef_dw(ef_dw):
    _qepy.f90wrap_ener__set__ef_dw(ef_dw)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "ener".')

for func in _dt_array_initialisers:
    func()
