"""
Module extrapolation


Defined at update_pot.fpp lines 14-933

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def update_file():
    """
    update_file()
    
    
    Defined at update_pot.fpp lines 35-88
    
    
    ----------------------------------------------------------------------------
     ... Reads, updates and rewrites the file containing atomic positions at
     ... two previous steps, used by potential and wavefunction extrapolation
     ... Requires: number of atoms nat, current atomic positions tau
     ... Produces: length of history and tau at current and two previous steps
     ...           written to file $prefix.update
    """
    _qepy.f90wrap_update_file()

def update_neb():
    """
    update_neb()
    
    
    Defined at update_pot.fpp lines 92-189
    
    
    ----------------------------------------------------------------------------
     ... Potential and wavefunction extrapolation for NEB
     ... Prepares file with previous steps for usage by update_pot
     ... Must be merged soon with update_file for MD in PWscf
    """
    _qepy.f90wrap_update_neb()

def update_pot():
    """
    update_pot()
    
    
    Defined at update_pot.fpp lines 192-378
    
    
    ----------------------------------------------------------------------------
     ... update the potential extrapolating the charge density and extrapolates
     ... the wave-functions
     ... charge density extrapolation :
     ... pot_order = 0   copy the old potential(nothing is done)
     ... pot_order = 1   subtract old atomic charge density and sum the new
     ...                 if dynamics is done the routine extrapolates also
     ...                 the difference between the the scf charge and the
     ...                 atomic one,
     ... pot_order = 2   first order extrapolation :
     ...                   rho(t+dt) = 2*rho(t) - rho(t-dt)
     ... pot_order = 3   second order extrapolation :
     ...                   rho(t+dt) = rho(t) +
     ...                               + alpha0*( rho(t) - rho(t-dt) )
     ...                               + beta0* ( rho(t-dt) - rho(t-2*dt) )
     ... wave-functions extrapolation :
     ... wfc_order = 0   nothing is done
     ... wfc_order = 2   first order extrapolation :
     ...                   |psi(t+dt)> = 2*|psi(t)> - |psi(t-dt)>
     ... wfc_order = 3   second order extrapolation :
     ...                   |psi(t+dt)> = |psi(t)> +
     ...                               + alpha0*( |psi(t)> - |psi(t-dt)> )
     ...                               + beta0* ( |psi(t-dt)> - |psi(t-2*dt)> )
     ...  alpha0 and beta0 are calculated in "find_alpha_and_beta()" so that
     ...  |tau'-tau(t+dt)| is minimum;
     ...  tau' and tau(t+dt) are respectively the atomic positions at time
     ...  t+dt and the extrapolated one:
     ...  tau(t+dt) = tau(t) + alpha0*( tau(t) - tau(t-dt) )
     ...                     + beta0*( tau(t-dt) -tau(t-2*dt) )
    """
    _qepy.f90wrap_update_pot()

def extrapolate_charge(dirname, rho_extr):
    """
    extrapolate_charge(dirname, rho_extr)
    
    
    Defined at update_pot.fpp lines 382-606
    
    Parameters
    ----------
    dirname : str
    rho_extr : int
    
    ----------------------------------------------------------------------------
    """
    _qepy.f90wrap_extrapolate_charge(dirname=dirname, rho_extr=rho_extr)

def get_pot_order():
    """
    Element pot_order ftype=integer  pytype=int
    
    
    Defined at update_pot.fpp line 26
    
    """
    return _qepy.f90wrap_extrapolation__get__pot_order()

def set_pot_order(pot_order):
    _qepy.f90wrap_extrapolation__set__pot_order(pot_order)

def get_wfc_order():
    """
    Element wfc_order ftype=integer  pytype=int
    
    
    Defined at update_pot.fpp line 26
    
    """
    return _qepy.f90wrap_extrapolation__get__wfc_order()

def set_wfc_order(wfc_order):
    _qepy.f90wrap_extrapolation__set__wfc_order(wfc_order)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "extrapolation".')

for func in _dt_array_initialisers:
    func()
