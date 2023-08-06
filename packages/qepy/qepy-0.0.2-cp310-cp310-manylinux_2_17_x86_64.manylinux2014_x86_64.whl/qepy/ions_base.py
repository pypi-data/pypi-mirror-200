"""
Module ions_base


Defined at ions_base.fpp lines 13-802

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def sort_tau(tausrt, isrt, tau, isp, nat, nsp):
    """
    sort_tau(tausrt, isrt, tau, isp, nat, nsp)
    
    
    Defined at ions_base.fpp lines 79-110
    
    Parameters
    ----------
    tausrt : float array
    isrt : int array
    tau : float array
    isp : int array
    nat : int
    nsp : int
    
    """
    _qepy.f90wrap_sort_tau(tausrt=tausrt, isrt=isrt, tau=tau, isp=isp, nat=nat, \
        nsp=nsp)

def unsort_tau(tau, tausrt, isrt, nat):
    """
    unsort_tau(tau, tausrt, isrt, nat)
    
    
    Defined at ions_base.fpp lines 113-124
    
    Parameters
    ----------
    tau : float array
    tausrt : float array
    isrt : int array
    nat : int
    
    """
    _qepy.f90wrap_unsort_tau(tau=tau, tausrt=tausrt, isrt=isrt, nat=nat)

def ions_base_init(nsp_, nat_, na_, ityp_, tau_, vel_, amass_, atm_, if_pos_, \
    tau_format_, alat_, at_, rcmax_, extfor_):
    """
    ions_base_init(nsp_, nat_, na_, ityp_, tau_, vel_, amass_, atm_, if_pos_, \
        tau_format_, alat_, at_, rcmax_, extfor_)
    
    
    Defined at ions_base.fpp lines 129-325
    
    Parameters
    ----------
    nsp_ : int
    nat_ : int
    na_ : int array
    ityp_ : int array
    tau_ : float array
    vel_ : float array
    amass_ : float array
    atm_ : str array
    if_pos_ : int array
    tau_format_ : str
    alat_ : float
    at_ : float array
    rcmax_ : float array
    extfor_ : float array
    
    -------------------------------------------------------------------------
    """
    _qepy.f90wrap_ions_base_init(nsp_=nsp_, nat_=nat_, na_=na_, ityp_=ityp_, \
        tau_=tau_, vel_=vel_, amass_=amass_, atm_=atm_, if_pos_=if_pos_, \
        tau_format_=tau_format_, alat_=alat_, at_=at_, rcmax_=rcmax_, \
        extfor_=extfor_)

def deallocate_ions_base():
    """
    deallocate_ions_base()
    
    
    Defined at ions_base.fpp lines 329-350
    
    
    -------------------------------------------------------------------------
    """
    _qepy.f90wrap_deallocate_ions_base()

def ions_cofmass(tau, pmass, na, nsp, cdm):
    """
    ions_cofmass(tau, pmass, na, nsp, cdm)
    
    
    Defined at ions_base.fpp lines 397-425
    
    Parameters
    ----------
    tau : float array
    pmass : float array
    na : int array
    nsp : int
    cdm : float array
    
    """
    _qepy.f90wrap_ions_cofmass(tau=tau, pmass=pmass, na=na, nsp=nsp, cdm=cdm)

def randpos(tau, na, nsp, tranp, amprp, hinv, ifor):
    """
    randpos(tau, na, nsp, tranp, amprp, hinv, ifor)
    
    
    Defined at ions_base.fpp lines 428-468
    
    Parameters
    ----------
    tau : float array
    na : int array
    nsp : int
    tranp : bool array
    amprp : float array
    hinv : float array
    ifor : int array
    
    """
    _qepy.f90wrap_randpos(tau=tau, na=na, nsp=nsp, tranp=tranp, amprp=amprp, \
        hinv=hinv, ifor=ifor)

def ions_kinene(vels, na, nsp, h, pmass):
    """
    ekinp = ions_kinene(vels, na, nsp, h, pmass)
    
    
    Defined at ions_base.fpp lines 471-494
    
    Parameters
    ----------
    vels : float array
    na : int array
    nsp : int
    h : float array
    pmass : float array
    
    Returns
    -------
    ekinp : float
    
    """
    ekinp = _qepy.f90wrap_ions_kinene(vels=vels, na=na, nsp=nsp, h=h, pmass=pmass)
    return ekinp

def ions_temp(temps, vels, na, nsp, h, pmass, ndega, nhpdim, atm2nhp, ekin2nhp):
    """
    tempp, ekinpr = ions_temp(temps, vels, na, nsp, h, pmass, ndega, nhpdim, \
        atm2nhp, ekin2nhp)
    
    
    Defined at ions_base.fpp lines 497-560
    
    Parameters
    ----------
    temps : float array
    vels : float array
    na : int array
    nsp : int
    h : float array
    pmass : float array
    ndega : int
    nhpdim : int
    atm2nhp : int array
    ekin2nhp : float array
    
    Returns
    -------
    tempp : float
    ekinpr : float
    
    """
    tempp, ekinpr = _qepy.f90wrap_ions_temp(temps=temps, vels=vels, na=na, nsp=nsp, \
        h=h, pmass=pmass, ndega=ndega, nhpdim=nhpdim, atm2nhp=atm2nhp, \
        ekin2nhp=ekin2nhp)
    return tempp, ekinpr

def ions_thermal_stress(stress, nstress, pmass, omega, h, vels, nsp, na):
    """
    ions_thermal_stress(stress, nstress, pmass, omega, h, vels, nsp, na)
    
    
    Defined at ions_base.fpp lines 563-589
    
    Parameters
    ----------
    stress : float array
    nstress : float array
    pmass : float array
    omega : float
    h : float array
    vels : float array
    nsp : int
    na : int array
    
    """
    _qepy.f90wrap_ions_thermal_stress(stress=stress, nstress=nstress, pmass=pmass, \
        omega=omega, h=h, vels=vels, nsp=nsp, na=na)

def randvel(tempw, tau0, taum, na, nsp, iforce, amass, delt):
    """
    randvel(tempw, tau0, taum, na, nsp, iforce, amass, delt)
    
    
    Defined at ions_base.fpp lines 593-634
    
    Parameters
    ----------
    tempw : float
    tau0 : float array
    taum : float array
    na : int array
    nsp : int
    iforce : int array
    amass : float array
    delt : float
    
    """
    _qepy.f90wrap_randvel(tempw=tempw, tau0=tau0, taum=taum, na=na, nsp=nsp, \
        iforce=iforce, amass=amass, delt=delt)

def ions_vrescal(tcap, tempw, tempp, taup, tau0, taum, na, nsp, fion, iforce, \
    pmass, delt):
    """
    ions_vrescal(tcap, tempw, tempp, taup, tau0, taum, na, nsp, fion, iforce, pmass, \
        delt)
    
    
    Defined at ions_base.fpp lines 638-696
    
    Parameters
    ----------
    tcap : bool
    tempw : float
    tempp : float
    taup : float array
    tau0 : float array
    taum : float array
    na : int array
    nsp : int
    fion : float array
    iforce : int array
    pmass : float array
    delt : float
    
    """
    _qepy.f90wrap_ions_vrescal(tcap=tcap, tempw=tempw, tempp=tempp, taup=taup, \
        tau0=tau0, taum=taum, na=na, nsp=nsp, fion=fion, iforce=iforce, pmass=pmass, \
        delt=delt)

def ions_shiftvar(varp, var0, varm):
    """
    ions_shiftvar(varp, var0, varm)
    
    
    Defined at ions_base.fpp lines 699-705
    
    Parameters
    ----------
    varp : float array
    var0 : float array
    varm : float array
    
    """
    _qepy.f90wrap_ions_shiftvar(varp=varp, var0=var0, varm=varm)

def ions_reference_positions(tau):
    """
    ions_reference_positions(tau)
    
    
    Defined at ions_base.fpp lines 708-719
    
    Parameters
    ----------
    tau : float array
    
    """
    _qepy.f90wrap_ions_reference_positions(tau=tau)

def ions_displacement(dis, tau):
    """
    ions_displacement(dis, tau)
    
    
    Defined at ions_base.fpp lines 722-751
    
    Parameters
    ----------
    dis : float array
    tau : float array
    
    """
    _qepy.f90wrap_ions_displacement(dis=dis, tau=tau)

def ions_cofmsub(tausp, iforce, nat, cdm, cdm0):
    """
    ions_cofmsub(tausp, iforce, nat, cdm, cdm0)
    
    
    Defined at ions_base.fpp lines 754-777
    
    Parameters
    ----------
    tausp : float array
    iforce : int array
    nat : int
    cdm : float array
    cdm0 : float array
    
    --------------------------------------------------------------------------
    """
    _qepy.f90wrap_ions_cofmsub(tausp=tausp, iforce=iforce, nat=nat, cdm=cdm, \
        cdm0=cdm0)

def compute_eextfor(tau0=None):
    """
    compute_eextfor = compute_eextfor([tau0])
    
    
    Defined at ions_base.fpp lines 779-800
    
    Parameters
    ----------
    tau0 : float array
    
    Returns
    -------
    compute_eextfor : float
    
    """
    compute_eextfor = _qepy.f90wrap_compute_eextfor(tau0=tau0)
    return compute_eextfor

def _ions_vel3(vel, taup, taum, na, nsp, dt):
    """
    _ions_vel3(vel, taup, taum, na, nsp, dt)
    
    
    Defined at ions_base.fpp lines 354-375
    
    Parameters
    ----------
    vel : float array
    taup : float array
    taum : float array
    na : int array
    nsp : int
    dt : float
    
    -------------------------------------------------------------------------
    """
    _qepy.f90wrap_ions_vel3(vel=vel, taup=taup, taum=taum, na=na, nsp=nsp, dt=dt)

def _ions_vel2(vel, taup, taum, nat, dt):
    """
    _ions_vel2(vel, taup, taum, nat, dt)
    
    
    Defined at ions_base.fpp lines 378-394
    
    Parameters
    ----------
    vel : float array
    taup : float array
    taum : float array
    nat : int
    dt : float
    
    """
    _qepy.f90wrap_ions_vel2(vel=vel, taup=taup, taum=taum, nat=nat, dt=dt)

def ions_vel(*args, **kwargs):
    """
    ions_vel(*args, **kwargs)
    
    
    Defined at ions_base.fpp lines 73-74
    
    Overloaded interface containing the following procedures:
      _ions_vel3
      _ions_vel2
    
    """
    for proc in [_ions_vel3, _ions_vel2]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def get_nsp():
    """
    Element nsp ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 24
    
    """
    return _qepy.f90wrap_ions_base__get__nsp()

def set_nsp(nsp):
    _qepy.f90wrap_ions_base__set__nsp(nsp)

def get_array_na():
    """
    Element na ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 25
    
    """
    global na
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__na(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        na = _arrays[array_handle]
    else:
        na = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__na)
        _arrays[array_handle] = na
    return na

def set_array_na(na):
    na[...] = na

def get_nax():
    """
    Element nax ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 26
    
    """
    return _qepy.f90wrap_ions_base__get__nax()

def set_nax(nax):
    _qepy.f90wrap_ions_base__set__nax(nax)

def get_nat():
    """
    Element nat ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 27
    
    """
    return _qepy.f90wrap_ions_base__get__nat()

def set_nat(nat):
    _qepy.f90wrap_ions_base__set__nat(nat)

def get_array_zv():
    """
    Element zv ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 31
    
    """
    global zv
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__zv(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        zv = _arrays[array_handle]
    else:
        zv = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__zv)
        _arrays[array_handle] = zv
    return zv

def set_array_zv(zv):
    zv[...] = zv

def get_array_amass():
    """
    Element amass ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 32
    
    """
    global amass
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__amass(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        amass = _arrays[array_handle]
    else:
        amass = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__amass)
        _arrays[array_handle] = amass
    return amass

def set_array_amass(amass):
    amass[...] = amass

def get_array_rcmax():
    """
    Element rcmax ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 33
    
    """
    global rcmax
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__rcmax(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rcmax = _arrays[array_handle]
    else:
        rcmax = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__rcmax)
        _arrays[array_handle] = rcmax
    return rcmax

def set_array_rcmax(rcmax):
    rcmax[...] = rcmax

def get_array_ityp():
    """
    Element ityp ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 37
    
    """
    global ityp
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__ityp(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ityp = _arrays[array_handle]
    else:
        ityp = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__ityp)
        _arrays[array_handle] = ityp
    return ityp

def set_array_ityp(ityp):
    ityp[...] = ityp

def get_array_tau():
    """
    Element tau ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 38
    
    """
    global tau
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__tau(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tau = _arrays[array_handle]
    else:
        tau = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__tau)
        _arrays[array_handle] = tau
    return tau

def set_array_tau(tau):
    tau[...] = tau

def get_array_vel():
    """
    Element vel ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 39
    
    """
    global vel
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__vel(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vel = _arrays[array_handle]
    else:
        vel = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__vel)
        _arrays[array_handle] = vel
    return vel

def set_array_vel(vel):
    vel[...] = vel

def get_array_tau_srt():
    """
    Element tau_srt ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 40
    
    """
    global tau_srt
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__tau_srt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        tau_srt = _arrays[array_handle]
    else:
        tau_srt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__tau_srt)
        _arrays[array_handle] = tau_srt
    return tau_srt

def set_array_tau_srt(tau_srt):
    tau_srt[...] = tau_srt

def get_array_vel_srt():
    """
    Element vel_srt ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 41
    
    """
    global vel_srt
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__vel_srt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vel_srt = _arrays[array_handle]
    else:
        vel_srt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__vel_srt)
        _arrays[array_handle] = vel_srt
    return vel_srt

def set_array_vel_srt(vel_srt):
    vel_srt[...] = vel_srt

def get_array_ind_srt():
    """
    Element ind_srt ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 42
    
    """
    global ind_srt
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__ind_srt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ind_srt = _arrays[array_handle]
    else:
        ind_srt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__ind_srt)
        _arrays[array_handle] = ind_srt
    return ind_srt

def set_array_ind_srt(ind_srt):
    ind_srt[...] = ind_srt

def get_array_ind_bck():
    """
    Element ind_bck ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 43
    
    """
    global ind_bck
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__ind_bck(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        ind_bck = _arrays[array_handle]
    else:
        ind_bck = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__ind_bck)
        _arrays[array_handle] = ind_bck
    return ind_bck

def set_array_ind_bck(ind_bck):
    ind_bck[...] = ind_bck

def get_array_atm():
    """
    Element atm ftype=character(len=3) pytype=str
    
    
    Defined at ions_base.fpp line 44
    
    """
    global atm
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__atm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        atm = _arrays[array_handle]
    else:
        atm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__atm)
        _arrays[array_handle] = atm
    return atm

def set_array_atm(atm):
    atm[...] = atm

def get_array_label_srt():
    """
    Element label_srt ftype=character(len=3) pytype=str
    
    
    Defined at ions_base.fpp line 45
    
    """
    global label_srt
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__label_srt(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        label_srt = _arrays[array_handle]
    else:
        label_srt = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__label_srt)
        _arrays[array_handle] = label_srt
    return label_srt

def set_array_label_srt(label_srt):
    label_srt[...] = label_srt

def get_tau_format():
    """
    Element tau_format ftype=character(len=80) pytype=str
    
    
    Defined at ions_base.fpp line 46
    
    """
    return _qepy.f90wrap_ions_base__get__tau_format()

def set_tau_format(tau_format):
    _qepy.f90wrap_ions_base__set__tau_format(tau_format)

def get_array_if_pos():
    """
    Element if_pos ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 49
    
    """
    global if_pos
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__if_pos(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        if_pos = _arrays[array_handle]
    else:
        if_pos = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__if_pos)
        _arrays[array_handle] = if_pos
    return if_pos

def set_array_if_pos(if_pos):
    if_pos[...] = if_pos

def get_array_iforce():
    """
    Element iforce ftype=integer pytype=int
    
    
    Defined at ions_base.fpp line 50
    
    """
    global iforce
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__iforce(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        iforce = _arrays[array_handle]
    else:
        iforce = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__iforce)
        _arrays[array_handle] = iforce
    return iforce

def set_array_iforce(iforce):
    iforce[...] = iforce

def get_fixatom():
    """
    Element fixatom ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 51
    
    """
    return _qepy.f90wrap_ions_base__get__fixatom()

def set_fixatom(fixatom):
    _qepy.f90wrap_ions_base__set__fixatom(fixatom)

def get_ndofp():
    """
    Element ndofp ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 52
    
    """
    return _qepy.f90wrap_ions_base__get__ndofp()

def set_ndofp(ndofp):
    _qepy.f90wrap_ions_base__set__ndofp(ndofp)

def get_ndfrz():
    """
    Element ndfrz ftype=integer  pytype=int
    
    
    Defined at ions_base.fpp line 53
    
    """
    return _qepy.f90wrap_ions_base__get__ndfrz()

def set_ndfrz(ndfrz):
    _qepy.f90wrap_ions_base__set__ndfrz(ndfrz)

def get_fricp():
    """
    Element fricp ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 54
    
    """
    return _qepy.f90wrap_ions_base__get__fricp()

def set_fricp(fricp):
    _qepy.f90wrap_ions_base__set__fricp(fricp)

def get_greasp():
    """
    Element greasp ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 55
    
    """
    return _qepy.f90wrap_ions_base__get__greasp()

def set_greasp(greasp):
    _qepy.f90wrap_ions_base__set__greasp(greasp)

def get_array_taui():
    """
    Element taui ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 62
    
    """
    global taui
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__taui(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        taui = _arrays[array_handle]
    else:
        taui = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__taui)
        _arrays[array_handle] = taui
    return taui

def set_array_taui(taui):
    taui[...] = taui

def get_array_cdmi():
    """
    Element cdmi ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 66
    
    """
    global cdmi
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__cdmi(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdmi = _arrays[array_handle]
    else:
        cdmi = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__cdmi)
        _arrays[array_handle] = cdmi
    return cdmi

def set_array_cdmi(cdmi):
    cdmi[...] = cdmi

def get_array_cdm():
    """
    Element cdm ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 66
    
    """
    global cdm
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__cdm(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdm = _arrays[array_handle]
    else:
        cdm = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__cdm)
        _arrays[array_handle] = cdm
    return cdm

def set_array_cdm(cdm):
    cdm[...] = cdm

def get_array_cdms():
    """
    Element cdms ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 68
    
    """
    global cdms
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__cdms(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        cdms = _arrays[array_handle]
    else:
        cdms = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__cdms)
        _arrays[array_handle] = cdms
    return cdms

def set_array_cdms(cdms):
    cdms[...] = cdms

def get_array_extfor():
    """
    Element extfor ftype=real(dp) pytype=float
    
    
    Defined at ions_base.fpp line 70
    
    """
    global extfor
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_ions_base__array__extfor(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        extfor = _arrays[array_handle]
    else:
        extfor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_ions_base__array__extfor)
        _arrays[array_handle] = extfor
    return extfor

def set_array_extfor(extfor):
    extfor[...] = extfor

def get_tions_base_init():
    """
    Element tions_base_init ftype=logical pytype=bool
    
    
    Defined at ions_base.fpp line 71
    
    """
    return _qepy.f90wrap_ions_base__get__tions_base_init()

def set_tions_base_init(tions_base_init):
    _qepy.f90wrap_ions_base__set__tions_base_init(tions_base_init)


_array_initialisers = [get_array_na, get_array_zv, get_array_amass, \
    get_array_rcmax, get_array_ityp, get_array_tau, get_array_vel, \
    get_array_tau_srt, get_array_vel_srt, get_array_ind_srt, get_array_ind_bck, \
    get_array_atm, get_array_label_srt, get_array_if_pos, get_array_iforce, \
    get_array_taui, get_array_cdmi, get_array_cdm, get_array_cdms, \
    get_array_extfor]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "ions_base".')

for func in _dt_array_initialisers:
    func()
