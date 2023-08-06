"""
Module control_flags


Defined at control_flags.fpp lines 13-349

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy.convergence_criteria")
class convergence_criteria(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=convergence_criteria)
    
    
    Defined at control_flags.fpp lines 29-36
    
    """
    def __init__(self, handle=None):
        """
        self = Convergence_Criteria()
        
        
        Defined at control_flags.fpp lines 29-36
        
        
        Returns
        -------
        this : Convergence_Criteria
        	Object to be constructed
        
        
        Automatically generated constructor for convergence_criteria
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_convergence_criteria_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Convergence_Criteria
        
        
        Defined at control_flags.fpp lines 29-36
        
        Parameters
        ----------
        this : Convergence_Criteria
        	Object to be destructed
        
        
        Automatically generated destructor for convergence_criteria
        """
        if self._alloc:
            _qepy.f90wrap_convergence_criteria_finalise(this=self._handle)
    
    @property
    def active(self):
        """
        Element active ftype=logical pytype=bool
        
        
        Defined at control_flags.fpp line 31
        
        """
        return _qepy.f90wrap_convergence_criteria__get__active(self._handle)
    
    @active.setter
    def active(self, active):
        _qepy.f90wrap_convergence_criteria__set__active(self._handle, active)
    
    @property
    def nstep(self):
        """
        Element nstep ftype=integer   pytype=int
        
        
        Defined at control_flags.fpp line 32
        
        """
        return _qepy.f90wrap_convergence_criteria__get__nstep(self._handle)
    
    @nstep.setter
    def nstep(self, nstep):
        _qepy.f90wrap_convergence_criteria__set__nstep(self._handle, nstep)
    
    @property
    def ekin(self):
        """
        Element ekin ftype=real(dp) pytype=float
        
        
        Defined at control_flags.fpp line 33
        
        """
        return _qepy.f90wrap_convergence_criteria__get__ekin(self._handle)
    
    @ekin.setter
    def ekin(self, ekin):
        _qepy.f90wrap_convergence_criteria__set__ekin(self._handle, ekin)
    
    @property
    def derho(self):
        """
        Element derho ftype=real(dp) pytype=float
        
        
        Defined at control_flags.fpp line 34
        
        """
        return _qepy.f90wrap_convergence_criteria__get__derho(self._handle)
    
    @derho.setter
    def derho(self, derho):
        _qepy.f90wrap_convergence_criteria__set__derho(self._handle, derho)
    
    @property
    def force(self):
        """
        Element force ftype=real(dp) pytype=float
        
        
        Defined at control_flags.fpp line 35
        
        """
        return _qepy.f90wrap_convergence_criteria__get__force(self._handle)
    
    @force.setter
    def force(self, force):
        _qepy.f90wrap_convergence_criteria__set__force(self._handle, force)
    
    def __str__(self):
        ret = ['<convergence_criteria>{\n']
        ret.append('    active : ')
        ret.append(repr(self.active))
        ret.append(',\n    nstep : ')
        ret.append(repr(self.nstep))
        ret.append(',\n    ekin : ')
        ret.append(repr(self.ekin))
        ret.append(',\n    derho : ')
        ret.append(repr(self.derho))
        ret.append(',\n    force : ')
        ret.append(repr(self.force))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def fix_dependencies():
    """
    fix_dependencies()
    
    
    Defined at control_flags.fpp lines 281-324
    
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_fix_dependencies()

def check_flags():
    """
    check_flags()
    
    
    Defined at control_flags.fpp lines 328-347
    
    
    ------------------------------------------------------------------------
     ...  do some checks for consistency
    """
    _qepy.f90wrap_check_flags()

def get_trhor():
    """
    Element trhor ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 53
    
    """
    return _qepy.f90wrap_control_flags__get__trhor()

def set_trhor(trhor):
    _qepy.f90wrap_control_flags__set__trhor(trhor)

def get_trhow():
    """
    Element trhow ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 54
    
    """
    return _qepy.f90wrap_control_flags__get__trhow()

def set_trhow(trhow):
    _qepy.f90wrap_control_flags__set__trhow(trhow)

def get_tksw():
    """
    Element tksw ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 55
    
    """
    return _qepy.f90wrap_control_flags__get__tksw()

def set_tksw(tksw):
    _qepy.f90wrap_control_flags__set__tksw(tksw)

def get_tfirst():
    """
    Element tfirst ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 56
    
    """
    return _qepy.f90wrap_control_flags__get__tfirst()

def set_tfirst(tfirst):
    _qepy.f90wrap_control_flags__set__tfirst(tfirst)

def get_tlast():
    """
    Element tlast ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 57
    
    """
    return _qepy.f90wrap_control_flags__get__tlast()

def set_tlast(tlast):
    _qepy.f90wrap_control_flags__set__tlast(tlast)

def get_tprint():
    """
    Element tprint ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 58
    
    """
    return _qepy.f90wrap_control_flags__get__tprint()

def set_tprint(tprint):
    _qepy.f90wrap_control_flags__set__tprint(tprint)

def get_tsde():
    """
    Element tsde ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 63
    
    """
    return _qepy.f90wrap_control_flags__get__tsde()

def set_tsde(tsde):
    _qepy.f90wrap_control_flags__set__tsde(tsde)

def get_tzeroe():
    """
    Element tzeroe ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 64
    
    """
    return _qepy.f90wrap_control_flags__get__tzeroe()

def set_tzeroe(tzeroe):
    _qepy.f90wrap_control_flags__set__tzeroe(tzeroe)

def get_trescalee():
    """
    Element trescalee ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 65
    
    """
    return _qepy.f90wrap_control_flags__get__trescalee()

def set_trescalee(trescalee):
    _qepy.f90wrap_control_flags__set__trescalee(trescalee)

def get_tfor():
    """
    Element tfor ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 66
    
    """
    return _qepy.f90wrap_control_flags__get__tfor()

def set_tfor(tfor):
    _qepy.f90wrap_control_flags__set__tfor(tfor)

def get_tsdp():
    """
    Element tsdp ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 67
    
    """
    return _qepy.f90wrap_control_flags__get__tsdp()

def set_tsdp(tsdp):
    _qepy.f90wrap_control_flags__set__tsdp(tsdp)

def get_tzerop():
    """
    Element tzerop ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 68
    
    """
    return _qepy.f90wrap_control_flags__get__tzerop()

def set_tzerop(tzerop):
    _qepy.f90wrap_control_flags__set__tzerop(tzerop)

def get_tprnfor():
    """
    Element tprnfor ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 69
    
    """
    return _qepy.f90wrap_control_flags__get__tprnfor()

def set_tprnfor(tprnfor):
    _qepy.f90wrap_control_flags__set__tprnfor(tprnfor)

def get_taurdr():
    """
    Element taurdr ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 70
    
    """
    return _qepy.f90wrap_control_flags__get__taurdr()

def set_taurdr(taurdr):
    _qepy.f90wrap_control_flags__set__taurdr(taurdr)

def get_tv0rd():
    """
    Element tv0rd ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 71
    
    """
    return _qepy.f90wrap_control_flags__get__tv0rd()

def set_tv0rd(tv0rd):
    _qepy.f90wrap_control_flags__set__tv0rd(tv0rd)

def get_tpre():
    """
    Element tpre ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 72
    
    """
    return _qepy.f90wrap_control_flags__get__tpre()

def set_tpre(tpre):
    _qepy.f90wrap_control_flags__set__tpre(tpre)

def get_thdyn():
    """
    Element thdyn ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 73
    
    """
    return _qepy.f90wrap_control_flags__get__thdyn()

def set_thdyn(thdyn):
    _qepy.f90wrap_control_flags__set__thdyn(thdyn)

def get_tsdc():
    """
    Element tsdc ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 74
    
    """
    return _qepy.f90wrap_control_flags__get__tsdc()

def set_tsdc(tsdc):
    _qepy.f90wrap_control_flags__set__tsdc(tsdc)

def get_tzeroc():
    """
    Element tzeroc ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 75
    
    """
    return _qepy.f90wrap_control_flags__get__tzeroc()

def set_tzeroc(tzeroc):
    _qepy.f90wrap_control_flags__set__tzeroc(tzeroc)

def get_tstress():
    """
    Element tstress ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 76
    
    """
    return _qepy.f90wrap_control_flags__get__tstress()

def set_tstress(tstress):
    _qepy.f90wrap_control_flags__set__tstress(tstress)

def get_tortho():
    """
    Element tortho ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 77
    
    """
    return _qepy.f90wrap_control_flags__get__tortho()

def set_tortho(tortho):
    _qepy.f90wrap_control_flags__set__tortho(tortho)

def get_timing():
    """
    Element timing ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 78
    
    """
    return _qepy.f90wrap_control_flags__get__timing()

def set_timing(timing):
    _qepy.f90wrap_control_flags__set__timing(timing)

def get_memchk():
    """
    Element memchk ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 79
    
    """
    return _qepy.f90wrap_control_flags__get__memchk()

def set_memchk(memchk):
    _qepy.f90wrap_control_flags__set__memchk(memchk)

def get_tscreen():
    """
    Element tscreen ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 80
    
    """
    return _qepy.f90wrap_control_flags__get__tscreen()

def set_tscreen(tscreen):
    _qepy.f90wrap_control_flags__set__tscreen(tscreen)

def get_force_pairing():
    """
    Element force_pairing ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 81
    
    """
    return _qepy.f90wrap_control_flags__get__force_pairing()

def set_force_pairing(force_pairing):
    _qepy.f90wrap_control_flags__set__force_pairing(force_pairing)

def get_lecrpa():
    """
    Element lecrpa ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 82
    
    """
    return _qepy.f90wrap_control_flags__get__lecrpa()

def set_lecrpa(lecrpa):
    _qepy.f90wrap_control_flags__set__lecrpa(lecrpa)

def get_tddfpt():
    """
    Element tddfpt ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 83
    
    """
    return _qepy.f90wrap_control_flags__get__tddfpt()

def set_tddfpt(tddfpt):
    _qepy.f90wrap_control_flags__set__tddfpt(tddfpt)

def get_smallmem():
    """
    Element smallmem ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 84
    
    """
    return _qepy.f90wrap_control_flags__get__smallmem()

def set_smallmem(smallmem):
    _qepy.f90wrap_control_flags__set__smallmem(smallmem)

def get_tionstep():
    """
    Element tionstep ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 94
    
    """
    return _qepy.f90wrap_control_flags__get__tionstep()

def set_tionstep(tionstep):
    _qepy.f90wrap_control_flags__set__tionstep(tionstep)

def get_nstepe():
    """
    Element nstepe ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 95
    
    """
    return _qepy.f90wrap_control_flags__get__nstepe()

def set_nstepe(nstepe):
    _qepy.f90wrap_control_flags__set__nstepe(nstepe)

def get_nbeg():
    """
    Element nbeg ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 98
    
    """
    return _qepy.f90wrap_control_flags__get__nbeg()

def set_nbeg(nbeg):
    _qepy.f90wrap_control_flags__set__nbeg(nbeg)

def get_ndw():
    """
    Element ndw ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 99
    
    """
    return _qepy.f90wrap_control_flags__get__ndw()

def set_ndw(ndw):
    _qepy.f90wrap_control_flags__set__ndw(ndw)

def get_ndr():
    """
    Element ndr ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 100
    
    """
    return _qepy.f90wrap_control_flags__get__ndr()

def set_ndr(ndr):
    _qepy.f90wrap_control_flags__set__ndr(ndr)

def get_nomore():
    """
    Element nomore ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 101
    
    """
    return _qepy.f90wrap_control_flags__get__nomore()

def set_nomore(nomore):
    _qepy.f90wrap_control_flags__set__nomore(nomore)

def get_iprint():
    """
    Element iprint ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 102
    
    """
    return _qepy.f90wrap_control_flags__get__iprint()

def set_iprint(iprint):
    _qepy.f90wrap_control_flags__set__iprint(iprint)

def get_max_xml_steps():
    """
    Element max_xml_steps ftype=integer   pytype=int
    
    
    Defined at control_flags.fpp line 103
    
    """
    return _qepy.f90wrap_control_flags__get__max_xml_steps()

def set_max_xml_steps(max_xml_steps):
    _qepy.f90wrap_control_flags__set__max_xml_steps(max_xml_steps)

def get_isave():
    """
    Element isave ftype=integer  pytype=int
    
    
    Defined at control_flags.fpp line 104
    
    """
    return _qepy.f90wrap_control_flags__get__isave()

def set_isave(isave):
    _qepy.f90wrap_control_flags__set__isave(isave)

def get_gamma_only():
    """
    Element gamma_only ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 108
    
    """
    return _qepy.f90wrap_control_flags__get__gamma_only()

def set_gamma_only(gamma_only):
    _qepy.f90wrap_control_flags__set__gamma_only(gamma_only)

def get_dt_old():
    """
    Element dt_old ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 112
    
    """
    return _qepy.f90wrap_control_flags__get__dt_old()

def set_dt_old(dt_old):
    _qepy.f90wrap_control_flags__set__dt_old(dt_old)

def get_trane():
    """
    Element trane ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 116
    
    """
    return _qepy.f90wrap_control_flags__get__trane()

def set_trane(trane):
    _qepy.f90wrap_control_flags__set__trane(trane)

def get_ampre():
    """
    Element ampre ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 117
    
    """
    return _qepy.f90wrap_control_flags__get__ampre()

def set_ampre(ampre):
    _qepy.f90wrap_control_flags__set__ampre(ampre)

def get_array_tranp():
    """
    Element tranp ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 121
    
    """
    global tranp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_control_flags__array__tranp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tranp = _arrays[array_handle]
    else:
        tranp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_control_flags__array__tranp)
        _arrays[array_handle] = tranp
    return tranp

def set_array_tranp(tranp):
    tranp[...] = tranp

def get_array_amprp():
    """
    Element amprp ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 122
    
    """
    global amprp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_control_flags__array__amprp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        amprp = _arrays[array_handle]
    else:
        amprp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_control_flags__array__amprp)
        _arrays[array_handle] = amprp
    return amprp

def set_array_amprp(amprp):
    amprp[...] = amprp

def get_tbeg():
    """
    Element tbeg ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 126
    
    """
    return _qepy.f90wrap_control_flags__get__tbeg()

def set_tbeg(tbeg):
    _qepy.f90wrap_control_flags__set__tbeg(tbeg)

def get_tnosee():
    """
    Element tnosee ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 130
    
    """
    return _qepy.f90wrap_control_flags__get__tnosee()

def set_tnosee(tnosee):
    _qepy.f90wrap_control_flags__set__tnosee(tnosee)

def get_tnoseh():
    """
    Element tnoseh ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 134
    
    """
    return _qepy.f90wrap_control_flags__get__tnoseh()

def set_tnoseh(tnoseh):
    _qepy.f90wrap_control_flags__set__tnoseh(tnoseh)

def get_tnosep():
    """
    Element tnosep ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 138
    
    """
    return _qepy.f90wrap_control_flags__get__tnosep()

def set_tnosep(tnosep):
    _qepy.f90wrap_control_flags__set__tnosep(tnosep)

def get_tcap():
    """
    Element tcap ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 139
    
    """
    return _qepy.f90wrap_control_flags__get__tcap()

def set_tcap(tcap):
    _qepy.f90wrap_control_flags__set__tcap(tcap)

def get_tcp():
    """
    Element tcp ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 140
    
    """
    return _qepy.f90wrap_control_flags__get__tcp()

def set_tcp(tcp):
    _qepy.f90wrap_control_flags__set__tcp(tcp)

def get_tolp():
    """
    Element tolp ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 141
    
    """
    return _qepy.f90wrap_control_flags__get__tolp()

def set_tolp(tolp):
    _qepy.f90wrap_control_flags__set__tolp(tolp)

def get_ekin_conv_thr():
    """
    Element ekin_conv_thr ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 146
    
    """
    return _qepy.f90wrap_control_flags__get__ekin_conv_thr()

def set_ekin_conv_thr(ekin_conv_thr):
    _qepy.f90wrap_control_flags__set__ekin_conv_thr(ekin_conv_thr)

def get_etot_conv_thr():
    """
    Element etot_conv_thr ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 146
    
    """
    return _qepy.f90wrap_control_flags__get__etot_conv_thr()

def set_etot_conv_thr(etot_conv_thr):
    _qepy.f90wrap_control_flags__set__etot_conv_thr(etot_conv_thr)

def get_forc_conv_thr():
    """
    Element forc_conv_thr ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 146
    
    """
    return _qepy.f90wrap_control_flags__get__forc_conv_thr()

def set_forc_conv_thr(forc_conv_thr):
    _qepy.f90wrap_control_flags__set__forc_conv_thr(forc_conv_thr)

def get_ekin_maxiter():
    """
    Element ekin_maxiter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 150
    
    """
    return _qepy.f90wrap_control_flags__get__ekin_maxiter()

def set_ekin_maxiter(ekin_maxiter):
    _qepy.f90wrap_control_flags__set__ekin_maxiter(ekin_maxiter)

def get_etot_maxiter():
    """
    Element etot_maxiter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 150
    
    """
    return _qepy.f90wrap_control_flags__get__etot_maxiter()

def set_etot_maxiter(etot_maxiter):
    _qepy.f90wrap_control_flags__set__etot_maxiter(etot_maxiter)

def get_forc_maxiter():
    """
    Element forc_maxiter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 150
    
    """
    return _qepy.f90wrap_control_flags__get__forc_maxiter()

def set_forc_maxiter(forc_maxiter):
    _qepy.f90wrap_control_flags__set__forc_maxiter(forc_maxiter)

def get_lscf():
    """
    Element lscf ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lscf()

def set_lscf(lscf):
    _qepy.f90wrap_control_flags__set__lscf(lscf)

def get_lbfgs():
    """
    Element lbfgs ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lbfgs()

def set_lbfgs(lbfgs):
    _qepy.f90wrap_control_flags__set__lbfgs(lbfgs)

def get_lmd():
    """
    Element lmd ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lmd()

def set_lmd(lmd):
    _qepy.f90wrap_control_flags__set__lmd(lmd)

def get_lwf():
    """
    Element lwf ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lwf()

def set_lwf(lwf):
    _qepy.f90wrap_control_flags__set__lwf(lwf)

def get_lwfnscf():
    """
    Element lwfnscf ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lwfnscf()

def set_lwfnscf(lwfnscf):
    _qepy.f90wrap_control_flags__set__lwfnscf(lwfnscf)

def get_lwfpbe0nscf():
    """
    Element lwfpbe0nscf ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lwfpbe0nscf()

def set_lwfpbe0nscf(lwfpbe0nscf):
    _qepy.f90wrap_control_flags__set__lwfpbe0nscf(lwfpbe0nscf)

def get_lbands():
    """
    Element lbands ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lbands()

def set_lbands(lbands):
    _qepy.f90wrap_control_flags__set__lbands(lbands)

def get_lconstrain():
    """
    Element lconstrain ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lconstrain()

def set_lconstrain(lconstrain):
    _qepy.f90wrap_control_flags__set__lconstrain(lconstrain)

def get_llondon():
    """
    Element llondon ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__llondon()

def set_llondon(llondon):
    _qepy.f90wrap_control_flags__set__llondon(llondon)

def get_ldftd3():
    """
    Element ldftd3 ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__ldftd3()

def set_ldftd3(ldftd3):
    _qepy.f90wrap_control_flags__set__ldftd3(ldftd3)

def get_ts_vdw():
    """
    Element ts_vdw ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__ts_vdw()

def set_ts_vdw(ts_vdw):
    _qepy.f90wrap_control_flags__set__ts_vdw(ts_vdw)

def get_lxdm():
    """
    Element lxdm ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__lxdm()

def set_lxdm(lxdm):
    _qepy.f90wrap_control_flags__set__lxdm(lxdm)

def get_restart():
    """
    Element restart ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 172
    
    """
    return _qepy.f90wrap_control_flags__get__restart()

def set_restart(restart):
    _qepy.f90wrap_control_flags__set__restart(restart)

def get_ngm0():
    """
    Element ngm0 ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 180
    
    """
    return _qepy.f90wrap_control_flags__get__ngm0()

def set_ngm0(ngm0):
    _qepy.f90wrap_control_flags__set__ngm0(ngm0)

def get_niter():
    """
    Element niter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 180
    
    """
    return _qepy.f90wrap_control_flags__get__niter()

def set_niter(niter):
    _qepy.f90wrap_control_flags__set__niter(niter)

def get_nmix():
    """
    Element nmix ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 180
    
    """
    return _qepy.f90wrap_control_flags__get__nmix()

def set_nmix(nmix):
    _qepy.f90wrap_control_flags__set__nmix(nmix)

def get_imix():
    """
    Element imix ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 180
    
    """
    return _qepy.f90wrap_control_flags__get__imix()

def set_imix(imix):
    _qepy.f90wrap_control_flags__set__imix(imix)

def get_n_scf_steps():
    """
    Element n_scf_steps ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 182
    
    """
    return _qepy.f90wrap_control_flags__get__n_scf_steps()

def set_n_scf_steps(n_scf_steps):
    _qepy.f90wrap_control_flags__set__n_scf_steps(n_scf_steps)

def get_mixing_beta():
    """
    Element mixing_beta ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 186
    
    """
    return _qepy.f90wrap_control_flags__get__mixing_beta()

def set_mixing_beta(mixing_beta):
    _qepy.f90wrap_control_flags__set__mixing_beta(mixing_beta)

def get_tr2():
    """
    Element tr2 ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 186
    
    """
    return _qepy.f90wrap_control_flags__get__tr2()

def set_tr2(tr2):
    _qepy.f90wrap_control_flags__set__tr2(tr2)

def get_scf_error():
    """
    Element scf_error ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 186
    
    """
    return _qepy.f90wrap_control_flags__get__scf_error()

def set_scf_error(scf_error):
    _qepy.f90wrap_control_flags__set__scf_error(scf_error)

def get_conv_elec():
    """
    Element conv_elec ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 188
    
    """
    return _qepy.f90wrap_control_flags__get__conv_elec()

def set_conv_elec(conv_elec):
    _qepy.f90wrap_control_flags__set__conv_elec(conv_elec)

def get_adapt_thr():
    """
    Element adapt_thr ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 191
    
    """
    return _qepy.f90wrap_control_flags__get__adapt_thr()

def set_adapt_thr(adapt_thr):
    _qepy.f90wrap_control_flags__set__adapt_thr(adapt_thr)

def get_tr2_init():
    """
    Element tr2_init ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 195
    
    """
    return _qepy.f90wrap_control_flags__get__tr2_init()

def set_tr2_init(tr2_init):
    _qepy.f90wrap_control_flags__set__tr2_init(tr2_init)

def get_tr2_multi():
    """
    Element tr2_multi ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 195
    
    """
    return _qepy.f90wrap_control_flags__get__tr2_multi()

def set_tr2_multi(tr2_multi):
    _qepy.f90wrap_control_flags__set__tr2_multi(tr2_multi)

def get_scf_must_converge():
    """
    Element scf_must_converge ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 197
    
    """
    return _qepy.f90wrap_control_flags__get__scf_must_converge()

def set_scf_must_converge(scf_must_converge):
    _qepy.f90wrap_control_flags__set__scf_must_converge(scf_must_converge)

def get_ethr():
    """
    Element ethr ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 202
    
    """
    return _qepy.f90wrap_control_flags__get__ethr()

def set_ethr(ethr):
    _qepy.f90wrap_control_flags__set__ethr(ethr)

def get_isolve():
    """
    Element isolve ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 207
    
    """
    return _qepy.f90wrap_control_flags__get__isolve()

def set_isolve(isolve):
    _qepy.f90wrap_control_flags__set__isolve(isolve)

def get_david():
    """
    Element david ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 207
    
    """
    return _qepy.f90wrap_control_flags__get__david()

def set_david(david):
    _qepy.f90wrap_control_flags__set__david(david)

def get_max_cg_iter():
    """
    Element max_cg_iter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 207
    
    """
    return _qepy.f90wrap_control_flags__get__max_cg_iter()

def set_max_cg_iter(max_cg_iter):
    _qepy.f90wrap_control_flags__set__max_cg_iter(max_cg_iter)

def get_max_ppcg_iter():
    """
    Element max_ppcg_iter ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 207
    
    """
    return _qepy.f90wrap_control_flags__get__max_ppcg_iter()

def set_max_ppcg_iter(max_ppcg_iter):
    _qepy.f90wrap_control_flags__set__max_ppcg_iter(max_ppcg_iter)

def get_diago_full_acc():
    """
    Element diago_full_acc ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 209
    
    """
    return _qepy.f90wrap_control_flags__get__diago_full_acc()

def set_diago_full_acc(diago_full_acc):
    _qepy.f90wrap_control_flags__set__diago_full_acc(diago_full_acc)

def get_nstep():
    """
    Element nstep ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 216
    
    """
    return _qepy.f90wrap_control_flags__get__nstep()

def set_nstep(nstep):
    _qepy.f90wrap_control_flags__set__nstep(nstep)

def get_istep():
    """
    Element istep ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 216
    
    """
    return _qepy.f90wrap_control_flags__get__istep()

def set_istep(istep):
    _qepy.f90wrap_control_flags__set__istep(istep)

def get_conv_ions():
    """
    Element conv_ions ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 218
    
    """
    return _qepy.f90wrap_control_flags__get__conv_ions()

def set_conv_ions(conv_ions):
    _qepy.f90wrap_control_flags__set__conv_ions(conv_ions)

def get_upscale():
    """
    Element upscale ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 220
    
    """
    return _qepy.f90wrap_control_flags__get__upscale()

def set_upscale(upscale):
    _qepy.f90wrap_control_flags__set__upscale(upscale)

def get_noinv():
    """
    Element noinv ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 225
    
    """
    return _qepy.f90wrap_control_flags__get__noinv()

def set_noinv(noinv):
    _qepy.f90wrap_control_flags__set__noinv(noinv)

def get_modenum():
    """
    Element modenum ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 230
    
    """
    return _qepy.f90wrap_control_flags__get__modenum()

def set_modenum(modenum):
    _qepy.f90wrap_control_flags__set__modenum(modenum)

def get_io_level():
    """
    Element io_level ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 235
    
    """
    return _qepy.f90wrap_control_flags__get__io_level()

def set_io_level(io_level):
    _qepy.f90wrap_control_flags__set__io_level(io_level)

def get_iverbosity():
    """
    Element iverbosity ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 237
    
    """
    return _qepy.f90wrap_control_flags__get__iverbosity()

def set_iverbosity(iverbosity):
    _qepy.f90wrap_control_flags__set__iverbosity(iverbosity)

def get_use_para_diag():
    """
    Element use_para_diag ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 242
    
    """
    return _qepy.f90wrap_control_flags__get__use_para_diag()

def set_use_para_diag(use_para_diag):
    _qepy.f90wrap_control_flags__set__use_para_diag(use_para_diag)

def get_remove_rigid_rot():
    """
    Element remove_rigid_rot ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 246
    
    """
    return _qepy.f90wrap_control_flags__get__remove_rigid_rot()

def set_remove_rigid_rot(remove_rigid_rot):
    _qepy.f90wrap_control_flags__set__remove_rigid_rot(remove_rigid_rot)

def get_do_makov_payne():
    """
    Element do_makov_payne ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 249
    
    """
    return _qepy.f90wrap_control_flags__get__do_makov_payne()

def set_do_makov_payne(do_makov_payne):
    _qepy.f90wrap_control_flags__set__do_makov_payne(do_makov_payne)

def get_ortho_max():
    """
    Element ortho_max ftype=integer   pytype=int
    
    
    Defined at control_flags.fpp line 252
    
    """
    return _qepy.f90wrap_control_flags__get__ortho_max()

def set_ortho_max(ortho_max):
    _qepy.f90wrap_control_flags__set__ortho_max(ortho_max)

def get_ortho_eps():
    """
    Element ortho_eps ftype=real(dp) pytype=float
    
    
    Defined at control_flags.fpp line 253
    
    """
    return _qepy.f90wrap_control_flags__get__ortho_eps()

def set_ortho_eps(ortho_eps):
    _qepy.f90wrap_control_flags__set__ortho_eps(ortho_eps)

def get_iesr():
    """
    Element iesr ftype=integer pytype=int
    
    
    Defined at control_flags.fpp line 257
    
    """
    return _qepy.f90wrap_control_flags__get__iesr()

def set_iesr(iesr):
    _qepy.f90wrap_control_flags__set__iesr(iesr)

def get_tqr():
    """
    Element tqr ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 261
    
    """
    return _qepy.f90wrap_control_flags__get__tqr()

def set_tqr(tqr):
    _qepy.f90wrap_control_flags__set__tqr(tqr)

def get_tq_smoothing():
    """
    Element tq_smoothing ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 266
    
    """
    return _qepy.f90wrap_control_flags__get__tq_smoothing()

def set_tq_smoothing(tq_smoothing):
    _qepy.f90wrap_control_flags__set__tq_smoothing(tq_smoothing)

def get_tbeta_smoothing():
    """
    Element tbeta_smoothing ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 267
    
    """
    return _qepy.f90wrap_control_flags__get__tbeta_smoothing()

def set_tbeta_smoothing(tbeta_smoothing):
    _qepy.f90wrap_control_flags__set__tbeta_smoothing(tbeta_smoothing)

def get_textfor():
    """
    Element textfor ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 271
    
    """
    return _qepy.f90wrap_control_flags__get__textfor()

def set_textfor(textfor):
    _qepy.f90wrap_control_flags__set__textfor(textfor)

def get_treinit_gvecs():
    """
    Element treinit_gvecs ftype=logical pytype=bool
    
    
    Defined at control_flags.fpp line 272
    
    """
    return _qepy.f90wrap_control_flags__get__treinit_gvecs()

def set_treinit_gvecs(treinit_gvecs):
    _qepy.f90wrap_control_flags__set__treinit_gvecs(treinit_gvecs)


_array_initialisers = [get_array_tranp, get_array_amprp]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "control_flags".')

for func in _dt_array_initialisers:
    func()
