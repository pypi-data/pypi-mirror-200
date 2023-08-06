"""
Module qexsd_module


Defined at qexsd.fpp lines 12-608

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qexsd_set_status(status_int):
    """
    qexsd_set_status(status_int)
    
    
    Defined at qexsd.fpp lines 82-86
    
    Parameters
    ----------
    status_int : int
    
    -------------------------------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexsd_set_status(status_int=status_int)

def qexsd_openschema(filename, ounit, prog, title):
    """
    qexsd_openschema(filename, ounit, prog, title)
    
    
    Defined at qexsd.fpp lines 96-152
    
    Parameters
    ----------
    filename : str
    ounit : int
    prog : str
    title : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexsd_openschema(filename=filename, ounit=ounit, prog=prog, \
        title=title)

def qexsd_closeschema():
    """
    qexsd_closeschema()
    
    
    Defined at qexsd.fpp lines 214-243
    
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexsd_closeschema()

def qexsd_readschema(filename):
    """
    ierr = qexsd_readschema(filename)
    
    
    Defined at qexsd.fpp lines 253-349
    
    Parameters
    ----------
    filename : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexsd_readschema(filename=filename)
    return ierr

def qexsd_step_addstep(i_step, max_steps, ntyp, atm, ityp, nat, tau, alat, a1, \
    a2, a3, etot, eband, ehart, vtxc, etxc, ewald, forces, stress, \
    scf_has_converged, n_scf_steps, scf_error, degauss=None, demet=None, \
    efieldcorr=None, potstat_contr=None, fcp_force=None, fcp_tot_charge=None, \
    gatefield_en=None):
    """
    qexsd_step_addstep(i_step, max_steps, ntyp, atm, ityp, nat, tau, alat, a1, a2, \
        a3, etot, eband, ehart, vtxc, etxc, ewald, forces, stress, \
        scf_has_converged, n_scf_steps, scf_error[, degauss, demet, efieldcorr, \
        potstat_contr, fcp_force, fcp_tot_charge, gatefield_en])
    
    
    Defined at qexsd.fpp lines 446-512
    
    Parameters
    ----------
    i_step : int
    max_steps : int
    ntyp : int
    atm : str array
    ityp : int array
    nat : int
    tau : float array
    alat : float
    a1 : float array
    a2 : float array
    a3 : float array
    etot : float
    eband : float
    ehart : float
    vtxc : float
    etxc : float
    ewald : float
    forces : float array
    stress : float array
    scf_has_converged : bool
    n_scf_steps : int
    scf_error : float
    degauss : float
    demet : float
    efieldcorr : float
    potstat_contr : float
    fcp_force : float
    fcp_tot_charge : float
    gatefield_en : float
    
    -----------------------------------------------------------------------------------------
     This routing initializes le steps array containing up to max_steps elements of \
         the step_type
     data structure. Each element contains structural and energetic info for m.d. \
         trajectories and
     structural minimization paths. All quantities must be provided directly in \
         Hartree atomic units.
     @Note updated on April 10th 2018 by Pietro Delugas
    """
    _qepy.f90wrap_qexsd_step_addstep(i_step=i_step, max_steps=max_steps, ntyp=ntyp, \
        atm=atm, ityp=ityp, nat=nat, tau=tau, alat=alat, a1=a1, a2=a2, a3=a3, \
        etot=etot, eband=eband, ehart=ehart, vtxc=vtxc, etxc=etxc, ewald=ewald, \
        forces=forces, stress=stress, scf_has_converged=scf_has_converged, \
        n_scf_steps=n_scf_steps, scf_error=scf_error, degauss=degauss, demet=demet, \
        efieldcorr=efieldcorr, potstat_contr=potstat_contr, fcp_force=fcp_force, \
        fcp_tot_charge=fcp_tot_charge, gatefield_en=gatefield_en)

def qexsd_reset_steps():
    """
    qexsd_reset_steps()
    
    
    Defined at qexsd.fpp lines 516-524
    
    
    """
    _qepy.f90wrap_qexsd_reset_steps()

def get_qexsd_current_version():
    """
    Element qexsd_current_version ftype=character(10) pytype=str
    
    
    Defined at qexsd.fpp line 56
    
    """
    return _qepy.f90wrap_qexsd_module__get__qexsd_current_version()

def set_qexsd_current_version(qexsd_current_version):
    _qepy.f90wrap_qexsd_module__set__qexsd_current_version(qexsd_current_version)

def get_qexsd_default_version():
    """
    Element qexsd_default_version ftype=character(10) pytype=str
    
    
    Defined at qexsd.fpp line 57
    
    """
    return _qepy.f90wrap_qexsd_module__get__qexsd_default_version()

def set_qexsd_default_version(qexsd_default_version):
    _qepy.f90wrap_qexsd_module__set__qexsd_default_version(qexsd_default_version)

def get_qexsd_current_version_init():
    """
    Element qexsd_current_version_init ftype=logical pytype=bool
    
    
    Defined at qexsd.fpp line 58
    
    """
    return _qepy.f90wrap_qexsd_module__get__qexsd_current_version_init()

def set_qexsd_current_version_init(qexsd_current_version_init):
    _qepy.f90wrap_qexsd_module__set__qexsd_current_version_init(qexsd_current_version_init)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qexsd_module".')

for func in _dt_array_initialisers:
    func()
