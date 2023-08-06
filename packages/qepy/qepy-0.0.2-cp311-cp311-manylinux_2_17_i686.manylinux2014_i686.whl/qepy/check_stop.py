"""
Module check_stop


Defined at check_stop.fpp lines 27-176

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def check_stop_init(max_seconds_=None):
    """
    check_stop_init([max_seconds_])
    
    
    Defined at check_stop.fpp lines 50-80
    
    Parameters
    ----------
    max_seconds_ : float
    
    -----------------------------------------------------------------------
    """
    _qepy.f90wrap_check_stop_init(max_seconds_=max_seconds_)

def check_stop_now(inunit=None):
    """
    check_stop_now = check_stop_now([inunit])
    
    
    Defined at check_stop.fpp lines 84-175
    
    Parameters
    ----------
    inunit : int
    
    Returns
    -------
    check_stop_now : bool
    
    -----------------------------------------------------------------------
    """
    check_stop_now = _qepy.f90wrap_check_stop_now(inunit=inunit)
    return check_stop_now

def get_max_seconds():
    """
    Element max_seconds ftype=real(dp) pytype=float
    
    
    Defined at check_stop.fpp line 37
    
    """
    return _qepy.f90wrap_check_stop__get__max_seconds()

def set_max_seconds(max_seconds):
    _qepy.f90wrap_check_stop__set__max_seconds(max_seconds)

def get_stopped_by_user():
    """
    Element stopped_by_user ftype=logical pytype=bool
    
    
    Defined at check_stop.fpp line 39
    
    """
    return _qepy.f90wrap_check_stop__get__stopped_by_user()

def set_stopped_by_user(stopped_by_user):
    _qepy.f90wrap_check_stop__set__stopped_by_user(stopped_by_user)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "check_stop".')

for func in _dt_array_initialisers:
    func()
