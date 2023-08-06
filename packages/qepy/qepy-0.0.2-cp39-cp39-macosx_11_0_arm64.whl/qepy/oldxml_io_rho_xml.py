"""
Module oldxml_io_rho_xml


Defined at oldxml_io_rho_xml.fpp lines 14-204

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def write_scf(self, nspin):
    """
    write_scf(self, nspin)
    
    
    Defined at oldxml_io_rho_xml.fpp lines 27-106
    
    Parameters
    ----------
    rho : Scf_Type
    nspin : int
    
    """
    _qepy.f90wrap_write_scf(rho=self._handle, nspin=nspin)

def read_scf(self, nspin, gamma_only=None):
    """
    read_scf(self, nspin[, gamma_only])
    
    
    Defined at oldxml_io_rho_xml.fpp lines 108-203
    
    Parameters
    ----------
    rho : Scf_Type
    nspin : int
    gamma_only : bool
    
    """
    _qepy.f90wrap_read_scf(rho=self._handle, nspin=nspin, gamma_only=gamma_only)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "oldxml_io_rho_xml".')

for func in _dt_array_initialisers:
    func()
