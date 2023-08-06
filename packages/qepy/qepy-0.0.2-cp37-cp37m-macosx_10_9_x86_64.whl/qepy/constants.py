"""
Module constants


Defined at constants.fpp lines 13-124

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_pi():
    """
    Element pi ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 26
    
    """
    return _qepy.f90wrap_constants__get__pi()

pi = get_pi()

def get_tpi():
    """
    Element tpi ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 27
    
    """
    return _qepy.f90wrap_constants__get__tpi()

tpi = get_tpi()

def get_fpi():
    """
    Element fpi ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 28
    
    """
    return _qepy.f90wrap_constants__get__fpi()

fpi = get_fpi()

def get_sqrtpi():
    """
    Element sqrtpi ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 29
    
    """
    return _qepy.f90wrap_constants__get__sqrtpi()

sqrtpi = get_sqrtpi()

def get_sqrtpm1():
    """
    Element sqrtpm1 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 30
    
    """
    return _qepy.f90wrap_constants__get__sqrtpm1()

sqrtpm1 = get_sqrtpm1()

def get_sqrt2():
    """
    Element sqrt2 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 31
    
    """
    return _qepy.f90wrap_constants__get__sqrt2()

sqrt2 = get_sqrt2()

def get_h_planck_si():
    """
    Element h_planck_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 35
    
    """
    return _qepy.f90wrap_constants__get__h_planck_si()

H_PLANCK_SI = get_h_planck_si()

def get_k_boltzmann_si():
    """
    Element k_boltzmann_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 36
    
    """
    return _qepy.f90wrap_constants__get__k_boltzmann_si()

K_BOLTZMANN_SI = get_k_boltzmann_si()

def get_electron_si():
    """
    Element electron_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 37
    
    """
    return _qepy.f90wrap_constants__get__electron_si()

ELECTRON_SI = get_electron_si()

def get_electronvolt_si():
    """
    Element electronvolt_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 38
    
    """
    return _qepy.f90wrap_constants__get__electronvolt_si()

ELECTRONVOLT_SI = get_electronvolt_si()

def get_electronmass_si():
    """
    Element electronmass_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 39
    
    """
    return _qepy.f90wrap_constants__get__electronmass_si()

ELECTRONMASS_SI = get_electronmass_si()

def get_hartree_si():
    """
    Element hartree_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 40
    
    """
    return _qepy.f90wrap_constants__get__hartree_si()

HARTREE_SI = get_hartree_si()

def get_rydberg_si():
    """
    Element rydberg_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 41
    
    """
    return _qepy.f90wrap_constants__get__rydberg_si()

RYDBERG_SI = get_rydberg_si()

def get_bohr_radius_si():
    """
    Element bohr_radius_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 42
    
    """
    return _qepy.f90wrap_constants__get__bohr_radius_si()

BOHR_RADIUS_SI = get_bohr_radius_si()

def get_amu_si():
    """
    Element amu_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 43
    
    """
    return _qepy.f90wrap_constants__get__amu_si()

AMU_SI = get_amu_si()

def get_c_si():
    """
    Element c_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 44
    
    """
    return _qepy.f90wrap_constants__get__c_si()

C_SI = get_c_si()

def get_munought_si():
    """
    Element munought_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 45
    
    """
    return _qepy.f90wrap_constants__get__munought_si()

MUNOUGHT_SI = get_munought_si()

def get_epsnought_si():
    """
    Element epsnought_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 47
    
    """
    return _qepy.f90wrap_constants__get__epsnought_si()

EPSNOUGHT_SI = get_epsnought_si()

def get_k_boltzmann_au():
    """
    Element k_boltzmann_au ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 53
    
    """
    return _qepy.f90wrap_constants__get__k_boltzmann_au()

K_BOLTZMANN_AU = get_k_boltzmann_au()

def get_k_boltzmann_ry():
    """
    Element k_boltzmann_ry ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 54
    
    """
    return _qepy.f90wrap_constants__get__k_boltzmann_ry()

K_BOLTZMANN_RY = get_k_boltzmann_ry()

def get_autoev():
    """
    Element autoev ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 58
    
    """
    return _qepy.f90wrap_constants__get__autoev()

AUTOEV = get_autoev()

def get_rytoev():
    """
    Element rytoev ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 59
    
    """
    return _qepy.f90wrap_constants__get__rytoev()

RYTOEV = get_rytoev()

def get_amu_au():
    """
    Element amu_au ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 60
    
    """
    return _qepy.f90wrap_constants__get__amu_au()

AMU_AU = get_amu_au()

def get_amu_ry():
    """
    Element amu_ry ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 61
    
    """
    return _qepy.f90wrap_constants__get__amu_ry()

AMU_RY = get_amu_ry()

def get_au_sec():
    """
    Element au_sec ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 65
    
    """
    return _qepy.f90wrap_constants__get__au_sec()

AU_SEC = get_au_sec()

def get_au_ps():
    """
    Element au_ps ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 66
    
    """
    return _qepy.f90wrap_constants__get__au_ps()

AU_PS = get_au_ps()

def get_au_gpa():
    """
    Element au_gpa ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 71
    
    """
    return _qepy.f90wrap_constants__get__au_gpa()

AU_GPA = get_au_gpa()

def get_ry_kbar():
    """
    Element ry_kbar ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 72
    
    """
    return _qepy.f90wrap_constants__get__ry_kbar()

RY_KBAR = get_ry_kbar()

def get_debye_si():
    """
    Element debye_si ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 79
    
    """
    return _qepy.f90wrap_constants__get__debye_si()

DEBYE_SI = get_debye_si()

def get_au_debye():
    """
    Element au_debye ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 81
    
    """
    return _qepy.f90wrap_constants__get__au_debye()

AU_DEBYE = get_au_debye()

def get_ev_to_kelvin():
    """
    Element ev_to_kelvin ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 83
    
    """
    return _qepy.f90wrap_constants__get__ev_to_kelvin()

eV_to_kelvin = get_ev_to_kelvin()

def get_ry_to_kelvin():
    """
    Element ry_to_kelvin ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 84
    
    """
    return _qepy.f90wrap_constants__get__ry_to_kelvin()

ry_to_kelvin = get_ry_to_kelvin()

def get_evtonm():
    """
    Element evtonm ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 89
    
    """
    return _qepy.f90wrap_constants__get__evtonm()

EVTONM = get_evtonm()

def get_rytonm():
    """
    Element rytonm ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 90
    
    """
    return _qepy.f90wrap_constants__get__rytonm()

RYTONM = get_rytonm()

def get_c_au():
    """
    Element c_au ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 94
    
    """
    return _qepy.f90wrap_constants__get__c_au()

C_AU = get_c_au()

def get_eps4():
    """
    Element eps4 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 98
    
    """
    return _qepy.f90wrap_constants__get__eps4()

eps4 = get_eps4()

def get_eps6():
    """
    Element eps6 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 99
    
    """
    return _qepy.f90wrap_constants__get__eps6()

eps6 = get_eps6()

def get_eps8():
    """
    Element eps8 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 100
    
    """
    return _qepy.f90wrap_constants__get__eps8()

eps8 = get_eps8()

def get_eps12():
    """
    Element eps12 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 101
    
    """
    return _qepy.f90wrap_constants__get__eps12()

eps12 = get_eps12()

def get_eps14():
    """
    Element eps14 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 102
    
    """
    return _qepy.f90wrap_constants__get__eps14()

eps14 = get_eps14()

def get_eps16():
    """
    Element eps16 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 103
    
    """
    return _qepy.f90wrap_constants__get__eps16()

eps16 = get_eps16()

def get_eps24():
    """
    Element eps24 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 104
    
    """
    return _qepy.f90wrap_constants__get__eps24()

eps24 = get_eps24()

def get_eps32():
    """
    Element eps32 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 105
    
    """
    return _qepy.f90wrap_constants__get__eps32()

eps32 = get_eps32()

def get_gsmall():
    """
    Element gsmall ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 107
    
    """
    return _qepy.f90wrap_constants__get__gsmall()

gsmall = get_gsmall()

def get_e2():
    """
    Element e2 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 109
    
    """
    return _qepy.f90wrap_constants__get__e2()

e2 = get_e2()

def get_degspin():
    """
    Element degspin ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 110
    
    """
    return _qepy.f90wrap_constants__get__degspin()

degspin = get_degspin()

def get_bohr_radius_cm():
    """
    Element bohr_radius_cm ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 114
    
    """
    return _qepy.f90wrap_constants__get__bohr_radius_cm()

BOHR_RADIUS_CM = get_bohr_radius_cm()

def get_bohr_radius_angs():
    """
    Element bohr_radius_angs ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 115
    
    """
    return _qepy.f90wrap_constants__get__bohr_radius_angs()

BOHR_RADIUS_ANGS = get_bohr_radius_angs()

def get_angstrom_au():
    """
    Element angstrom_au ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 116
    
    """
    return _qepy.f90wrap_constants__get__angstrom_au()

ANGSTROM_AU = get_angstrom_au()

def get_dip_debye():
    """
    Element dip_debye ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 117
    
    """
    return _qepy.f90wrap_constants__get__dip_debye()

DIP_DEBYE = get_dip_debye()

def get_au_terahertz():
    """
    Element au_terahertz ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 118
    
    """
    return _qepy.f90wrap_constants__get__au_terahertz()

AU_TERAHERTZ = get_au_terahertz()

def get_au_to_ohmcmm1():
    """
    Element au_to_ohmcmm1 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 119
    
    """
    return _qepy.f90wrap_constants__get__au_to_ohmcmm1()

AU_TO_OHMCMM1 = get_au_to_ohmcmm1()

def get_ry_to_thz():
    """
    Element ry_to_thz ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 120
    
    """
    return _qepy.f90wrap_constants__get__ry_to_thz()

RY_TO_THZ = get_ry_to_thz()

def get_ry_to_ghz():
    """
    Element ry_to_ghz ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 121
    
    """
    return _qepy.f90wrap_constants__get__ry_to_ghz()

RY_TO_GHZ = get_ry_to_ghz()

def get_ry_to_cmm1():
    """
    Element ry_to_cmm1 ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 122
    
    """
    return _qepy.f90wrap_constants__get__ry_to_cmm1()

RY_TO_CMM1 = get_ry_to_cmm1()

def get_avogadro():
    """
    Element avogadro ftype=real(dp) pytype=float
    
    
    Defined at constants.fpp line 124
    
    """
    return _qepy.f90wrap_constants__get__avogadro()

AVOGADRO = get_avogadro()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "constants".')

for func in _dt_array_initialisers:
    func()
