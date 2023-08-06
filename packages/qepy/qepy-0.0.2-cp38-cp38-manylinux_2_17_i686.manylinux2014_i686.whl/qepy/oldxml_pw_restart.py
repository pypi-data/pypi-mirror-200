"""
Module oldxml_pw_restart


Defined at oldxml_pw_restart.fpp lines 21-2986

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def pw_writefile(what):
    """
    pw_writefile(what)
    
    
    Defined at oldxml_pw_restart.fpp lines 103-806
    
    Parameters
    ----------
    what : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_pw_writefile(what=what)

def pw_readfile(what):
    """
    ierr = pw_readfile(what)
    
    
    Defined at oldxml_pw_restart.fpp lines 810-1186
    
    Parameters
    ----------
    what : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_pw_readfile(what=what)
    return ierr

def gk_l2gmap(ngm, ig_l2g, ngk, igk, igk_l2g):
    """
    gk_l2gmap(ngm, ig_l2g, ngk, igk, igk_l2g)
    
    
    Defined at oldxml_pw_restart.fpp lines 2784-2809
    
    Parameters
    ----------
    ngm : int
    ig_l2g : int array
    ngk : int
    igk : int array
    igk_l2g : int array
    
    ----------------------------------------------------------------------------
     ... This subroutine maps local G+k index to the global G vector index
     ... the mapping is used to collect wavefunctions subsets distributed
     ... across processors.
     ... Written by Carlo Cavazzoni
    """
    _qepy.f90wrap_gk_l2gmap(ngm=ngm, ig_l2g=ig_l2g, ngk=ngk, igk=igk, \
        igk_l2g=igk_l2g)

def gk_l2gmap_kdip(npw_g, ngk_g, ngk, igk_l2g, igk_l2g_kdip=None, igwk=None):
    """
    gk_l2gmap_kdip(npw_g, ngk_g, ngk, igk_l2g[, igk_l2g_kdip, igwk])
    
    
    Defined at oldxml_pw_restart.fpp lines 2813-2896
    
    Parameters
    ----------
    npw_g : int
    ngk_g : int
    ngk : int
    igk_l2g : int array
    igk_l2g_kdip : int array
    igwk : int array
    
    -----------------------------------------------------------------------
     ... This subroutine maps local G+k index to the global G vector index
     ... the mapping is used to collect wavefunctions subsets distributed
     ... across processors.
     ... This map is used to obtained the G+k grids related to each kpt
    """
    _qepy.f90wrap_gk_l2gmap_kdip(npw_g=npw_g, ngk_g=ngk_g, ngk=ngk, igk_l2g=igk_l2g, \
        igk_l2g_kdip=igk_l2g_kdip, igwk=igwk)

def pp_check_file():
    """
    pp_check_file = pp_check_file()
    
    
    Defined at oldxml_pw_restart.fpp lines 2899-2983
    
    
    Returns
    -------
    pp_check_file : bool
    
    ------------------------------------------------------------------------
    """
    pp_check_file = _qepy.f90wrap_pp_check_file()
    return pp_check_file


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "oldxml_pw_restart".')

for func in _dt_array_initialisers:
    func()
