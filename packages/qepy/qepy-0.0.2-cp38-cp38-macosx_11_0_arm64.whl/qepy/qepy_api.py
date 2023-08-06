"""
Module qepy_api


Defined at qepy_api.fpp lines 5-103

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qepy_update_ions(self, pos, ikind=None, lattice=None):
    """
    qepy_update_ions(self, pos[, ikind, lattice])
    
    
    Defined at qepy_api.fpp lines 13-103
    
    Parameters
    ----------
    embed : Embed_Base
    pos : float array
    ikind : int
    lattice : float array
    
    -----------------------------------------------------------------------
     This is function Combined 'run_pwscf' and 'move_ions'.
    ***********************************************************************
     pos:
       ionic positions in bohr
     ikind:
       ikind = 0  all
       ikind = 1  atomic configuration dependent information
     lattice:
       lattice parameter in bohr
    ***********************************************************************
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_qepy_update_ions(embed=self._handle, pos=pos, ikind=ikind, \
        lattice=lattice)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "qepy_api".')

for func in _dt_array_initialisers:
    func()
