"""
Module mp_world


Defined at mp_world.fpp lines 13-80

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_world_start(my_world_comm):
    """
    mp_world_start(my_world_comm)
    
    
    Defined at mp_world.fpp lines 44-70
    
    Parameters
    ----------
    my_world_comm : int
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_mp_world_start(my_world_comm=my_world_comm)

def mp_world_end():
    """
    mp_world_end()
    
    
    Defined at mp_world.fpp lines 74-79
    
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_mp_world_end()

def get_nnode():
    """
    Element nnode ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 27
    
    """
    return _qepy.f90wrap_mp_world__get__nnode()

def set_nnode(nnode):
    _qepy.f90wrap_mp_world__set__nnode(nnode)

def get_nproc():
    """
    Element nproc ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 28
    
    """
    return _qepy.f90wrap_mp_world__get__nproc()

def set_nproc(nproc):
    _qepy.f90wrap_mp_world__set__nproc(nproc)

def get_mpime():
    """
    Element mpime ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 29
    
    """
    return _qepy.f90wrap_mp_world__get__mpime()

def set_mpime(mpime):
    _qepy.f90wrap_mp_world__set__mpime(mpime)

def get_root():
    """
    Element root ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 30
    
    """
    return _qepy.f90wrap_mp_world__get__root()

def set_root(root):
    _qepy.f90wrap_mp_world__set__root(root)

def get_world_comm():
    """
    Element world_comm ftype=integer  pytype=int
    
    
    Defined at mp_world.fpp line 31
    
    """
    return _qepy.f90wrap_mp_world__get__world_comm()

def set_world_comm(world_comm):
    _qepy.f90wrap_mp_world__set__world_comm(world_comm)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_world".')

for func in _dt_array_initialisers:
    func()
