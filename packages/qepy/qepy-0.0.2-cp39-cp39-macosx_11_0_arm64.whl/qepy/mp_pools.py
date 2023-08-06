"""
Module mp_pools


Defined at mp_pools.fpp lines 13-57

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_start_pools(npool_, parent_comm):
    """
    mp_start_pools(npool_, parent_comm)
    
    
    Defined at mp_pools.fpp lines 40-55
    
    Parameters
    ----------
    npool_ : int
    parent_comm : int
    
    ---------------------------------------------------------------------------
     ... Divide processors(of the "parent_comm" group) into "pools"
     ... Requires: npool_, read from command line
     ...           parent_comm, typically world_comm = group of all processors
    """
    _qepy.f90wrap_mp_start_pools(npool_=npool_, parent_comm=parent_comm)

def get_npool():
    """
    Element npool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 25
    
    """
    return _qepy.f90wrap_mp_pools__get__npool()

def set_npool(npool):
    _qepy.f90wrap_mp_pools__set__npool(npool)

def get_nproc_pool():
    """
    Element nproc_pool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 26
    
    """
    return _qepy.f90wrap_mp_pools__get__nproc_pool()

def set_nproc_pool(nproc_pool):
    _qepy.f90wrap_mp_pools__set__nproc_pool(nproc_pool)

def get_me_pool():
    """
    Element me_pool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 27
    
    """
    return _qepy.f90wrap_mp_pools__get__me_pool()

def set_me_pool(me_pool):
    _qepy.f90wrap_mp_pools__set__me_pool(me_pool)

def get_root_pool():
    """
    Element root_pool ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 28
    
    """
    return _qepy.f90wrap_mp_pools__get__root_pool()

def set_root_pool(root_pool):
    _qepy.f90wrap_mp_pools__set__root_pool(root_pool)

def get_my_pool_id():
    """
    Element my_pool_id ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 29
    
    """
    return _qepy.f90wrap_mp_pools__get__my_pool_id()

def set_my_pool_id(my_pool_id):
    _qepy.f90wrap_mp_pools__set__my_pool_id(my_pool_id)

def get_inter_pool_comm():
    """
    Element inter_pool_comm ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 30
    
    """
    return _qepy.f90wrap_mp_pools__get__inter_pool_comm()

def set_inter_pool_comm(inter_pool_comm):
    _qepy.f90wrap_mp_pools__set__inter_pool_comm(inter_pool_comm)

def get_intra_pool_comm():
    """
    Element intra_pool_comm ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 31
    
    """
    return _qepy.f90wrap_mp_pools__get__intra_pool_comm()

def set_intra_pool_comm(intra_pool_comm):
    _qepy.f90wrap_mp_pools__set__intra_pool_comm(intra_pool_comm)

def get_kunit():
    """
    Element kunit ftype=integer  pytype=int
    
    
    Defined at mp_pools.fpp line 33
    
    """
    return _qepy.f90wrap_mp_pools__get__kunit()

def set_kunit(kunit):
    _qepy.f90wrap_mp_pools__set__kunit(kunit)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_pools".')

for func in _dt_array_initialisers:
    func()
