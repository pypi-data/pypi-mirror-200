"""
Module qepy_scatter_mod


Defined at qepy_scatter_mod.fpp lines 20-361

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qepy_scatter_mod".')

for func in _dt_array_initialisers:
    func()
