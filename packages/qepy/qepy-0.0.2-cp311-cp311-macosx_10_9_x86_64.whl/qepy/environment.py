"""
Module environment


Defined at environment.fpp lines 17-183

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def environment_start(code):
    """
    environment_start(code)
    
    
    Defined at environment.fpp lines 42-90
    
    Parameters
    ----------
    code : str
    
    """
    _qepy.f90wrap_environment_start(code=code)

def environment_end(code):
    """
    environment_end(code)
    
    
    Defined at environment.fpp lines 93-105
    
    Parameters
    ----------
    code : str
    
    """
    _qepy.f90wrap_environment_end(code=code)

def opening_message(code_version):
    """
    opening_message(code_version)
    
    
    Defined at environment.fpp lines 108-126
    
    Parameters
    ----------
    code_version : str
    
    """
    _qepy.f90wrap_opening_message(code_version=code_version)

def parallel_info(code):
    """
    parallel_info(code)
    
    
    Defined at environment.fpp lines 144-167
    
    Parameters
    ----------
    code : str
    
    """
    _qepy.f90wrap_parallel_info(code=code)

def compilation_info():
    """
    compilation_info()
    
    
    Defined at environment.fpp lines 177-181
    
    
    """
    _qepy.f90wrap_compilation_info()


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "environment".')

for func in _dt_array_initialisers:
    func()
