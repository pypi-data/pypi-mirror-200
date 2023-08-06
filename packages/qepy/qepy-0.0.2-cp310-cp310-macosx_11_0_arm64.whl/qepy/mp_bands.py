"""
Module mp_bands


Defined at mp_bands.fpp lines 13-67

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_start_bands(nband_, parent_comm, ntg_=None, nyfft_=None):
    """
    mp_start_bands(nband_, parent_comm[, ntg_, nyfft_])
    
    
    Defined at mp_bands.fpp lines 48-65
    
    Parameters
    ----------
    nband_ : int
    parent_comm : int
    ntg_ : int
    nyfft_ : int
    
    ---------------------------------------------------------------------------
     ... Divide processors(of the "parent_comm" group) into nband_ pools
     ... Requires: nband_, read from command line
     ...           parent_comm, typically processors of a k-point pool
     ...           (intra_pool_comm)
    """
    _qepy.f90wrap_mp_start_bands(nband_=nband_, parent_comm=parent_comm, ntg_=ntg_, \
        nyfft_=nyfft_)

def get_nbgrp():
    """
    Element nbgrp ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 25
    
    """
    return _qepy.f90wrap_mp_bands__get__nbgrp()

def set_nbgrp(nbgrp):
    _qepy.f90wrap_mp_bands__set__nbgrp(nbgrp)

def get_nproc_bgrp():
    """
    Element nproc_bgrp ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 26
    
    """
    return _qepy.f90wrap_mp_bands__get__nproc_bgrp()

def set_nproc_bgrp(nproc_bgrp):
    _qepy.f90wrap_mp_bands__set__nproc_bgrp(nproc_bgrp)

def get_me_bgrp():
    """
    Element me_bgrp ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 27
    
    """
    return _qepy.f90wrap_mp_bands__get__me_bgrp()

def set_me_bgrp(me_bgrp):
    _qepy.f90wrap_mp_bands__set__me_bgrp(me_bgrp)

def get_root_bgrp():
    """
    Element root_bgrp ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 28
    
    """
    return _qepy.f90wrap_mp_bands__get__root_bgrp()

def set_root_bgrp(root_bgrp):
    _qepy.f90wrap_mp_bands__set__root_bgrp(root_bgrp)

def get_my_bgrp_id():
    """
    Element my_bgrp_id ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 29
    
    """
    return _qepy.f90wrap_mp_bands__get__my_bgrp_id()

def set_my_bgrp_id(my_bgrp_id):
    _qepy.f90wrap_mp_bands__set__my_bgrp_id(my_bgrp_id)

def get_root_bgrp_id():
    """
    Element root_bgrp_id ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 30
    
    """
    return _qepy.f90wrap_mp_bands__get__root_bgrp_id()

def set_root_bgrp_id(root_bgrp_id):
    _qepy.f90wrap_mp_bands__set__root_bgrp_id(root_bgrp_id)

def get_inter_bgrp_comm():
    """
    Element inter_bgrp_comm ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 31
    
    """
    return _qepy.f90wrap_mp_bands__get__inter_bgrp_comm()

def set_inter_bgrp_comm(inter_bgrp_comm):
    _qepy.f90wrap_mp_bands__set__inter_bgrp_comm(inter_bgrp_comm)

def get_intra_bgrp_comm():
    """
    Element intra_bgrp_comm ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 32
    
    """
    return _qepy.f90wrap_mp_bands__get__intra_bgrp_comm()

def set_intra_bgrp_comm(intra_bgrp_comm):
    _qepy.f90wrap_mp_bands__set__intra_bgrp_comm(intra_bgrp_comm)

def get_use_bgrp_in_hpsi():
    """
    Element use_bgrp_in_hpsi ftype=logical pytype=bool
    
    
    Defined at mp_bands.fpp line 36
    
    """
    return _qepy.f90wrap_mp_bands__get__use_bgrp_in_hpsi()

def set_use_bgrp_in_hpsi(use_bgrp_in_hpsi):
    _qepy.f90wrap_mp_bands__set__use_bgrp_in_hpsi(use_bgrp_in_hpsi)

def get_ntask_groups():
    """
    Element ntask_groups ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 40
    
    """
    return _qepy.f90wrap_mp_bands__get__ntask_groups()

def set_ntask_groups(ntask_groups):
    _qepy.f90wrap_mp_bands__set__ntask_groups(ntask_groups)

def get_nyfft():
    """
    Element nyfft ftype=integer  pytype=int
    
    
    Defined at mp_bands.fpp line 43
    
    """
    return _qepy.f90wrap_mp_bands__get__nyfft()

def set_nyfft(nyfft):
    _qepy.f90wrap_mp_bands__set__nyfft(nyfft)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_bands".')

for func in _dt_array_initialisers:
    func()
