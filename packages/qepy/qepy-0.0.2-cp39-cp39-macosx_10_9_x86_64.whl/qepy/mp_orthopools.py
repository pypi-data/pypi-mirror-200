"""
Module mp_orthopools


Defined at mp_pools.fpp lines 60-123

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_stop_orthopools():
    """
    mp_stop_orthopools()
    
    
    Defined at mp_pools.fpp lines 88-98
    
    
    """
    _qepy.f90wrap_mp_stop_orthopools()

def mp_start_orthopools(parent_comm):
    """
    mp_start_orthopools(parent_comm)
    
    
    Defined at mp_pools.fpp lines 102-122
    
    Parameters
    ----------
    parent_comm : int
    
    ---------------------------------------------------------------------------
     ... Divide processors(of the "parent_comm" group) into "orthopools"
     ... Requires: pools being already initialized
     ...           parent_comm, typically world_comm = group of all processors
    """
    _qepy.f90wrap_mp_start_orthopools(parent_comm=parent_comm)

def get_northopool():
    """
    Element northopool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 74
    
    """
    return _qepy.f90wrap_mp_orthopools__get__northopool()

def set_northopool(northopool):
    _qepy.f90wrap_mp_orthopools__set__northopool(northopool)

def get_nproc_orthopool():
    """
    Element nproc_orthopool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 75
    
    """
    return _qepy.f90wrap_mp_orthopools__get__nproc_orthopool()

def set_nproc_orthopool(nproc_orthopool):
    _qepy.f90wrap_mp_orthopools__set__nproc_orthopool(nproc_orthopool)

def get_me_orthopool():
    """
    Element me_orthopool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 76
    
    """
    return _qepy.f90wrap_mp_orthopools__get__me_orthopool()

def set_me_orthopool(me_orthopool):
    _qepy.f90wrap_mp_orthopools__set__me_orthopool(me_orthopool)

def get_root_orthopool():
    """
    Element root_orthopool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 78
    
    """
    return _qepy.f90wrap_mp_orthopools__get__root_orthopool()

def set_root_orthopool(root_orthopool):
    _qepy.f90wrap_mp_orthopools__set__root_orthopool(root_orthopool)

def get_my_orthopool_id():
    """
    Element my_orthopool_id ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 79
    
    """
    return _qepy.f90wrap_mp_orthopools__get__my_orthopool_id()

def set_my_orthopool_id(my_orthopool_id):
    _qepy.f90wrap_mp_orthopools__set__my_orthopool_id(my_orthopool_id)

def get_inter_orthopool_comm():
    """
    Element inter_orthopool_comm ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 80
    
    """
    return _qepy.f90wrap_mp_orthopools__get__inter_orthopool_comm()

def set_inter_orthopool_comm(inter_orthopool_comm):
    _qepy.f90wrap_mp_orthopools__set__inter_orthopool_comm(inter_orthopool_comm)

def get_intra_orthopool_comm():
    """
    Element intra_orthopool_comm ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 81
    
    """
    return _qepy.f90wrap_mp_orthopools__get__intra_orthopool_comm()

def set_intra_orthopool_comm(intra_orthopool_comm):
    _qepy.f90wrap_mp_orthopools__set__intra_orthopool_comm(intra_orthopool_comm)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mp_orthopools".')

for func in _dt_array_initialisers:
    func()
