"""
Module qepy_mod


Defined at qepy_mod.fpp lines 5-554

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qepy_get_rho(rhor, gather=None):
    """
    qepy_get_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 134-152
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_rho(rhor=rhor, gather=gather)

def qepy_set_rho(rhor, gather=None):
    """
    qepy_set_rho(rhor[, gather])
    
    
    Defined at qepy_mod.fpp lines 154-174
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_rho(rhor=rhor, gather=gather)

def qepy_get_rho_core(rhoc, gather=None):
    """
    qepy_get_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 176-189
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_rho_core(rhoc, gather=None):
    """
    qepy_set_rho_core(rhoc[, gather])
    
    
    Defined at qepy_mod.fpp lines 191-204
    
    Parameters
    ----------
    rhoc : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_rho_core(rhoc=rhoc, gather=gather)

def qepy_set_extpot(self, vin, gather=None):
    """
    qepy_set_extpot(self, vin[, gather])
    
    
    Defined at qepy_mod.fpp lines 206-233
    
    Parameters
    ----------
    embed : Embed_Base
    vin : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_extpot(embed=self._handle, vin=vin, gather=gather)

def qepy_get_grid(nr=None, gather=None):
    """
    nrw = qepy_get_grid([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 235-251
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = _qepy.f90wrap_qepy_get_grid(nr=nr, gather=gather)
    return nrw

def qepy_get_grid_smooth(nr=None, gather=None):
    """
    nrw = qepy_get_grid_smooth([nr, gather])
    
    
    Defined at qepy_mod.fpp lines 273-289
    
    Parameters
    ----------
    nr : int array
    gather : bool
    
    Returns
    -------
    nrw : int array
    
    """
    nrw = _qepy.f90wrap_qepy_get_grid_smooth(nr=nr, gather=gather)
    return nrw

def qepy_set_stdout(fname=None, uni=None, append=None):
    """
    qepy_set_stdout([fname, uni, append])
    
    
    Defined at qepy_mod.fpp lines 291-317
    
    Parameters
    ----------
    fname : str
    uni : int
    append : bool
    
    """
    _qepy.f90wrap_qepy_set_stdout(fname=fname, uni=uni, append=append)

def qepy_write_stdout(fstr):
    """
    qepy_write_stdout(fstr)
    
    
    Defined at qepy_mod.fpp lines 319-325
    
    Parameters
    ----------
    fstr : str
    
    """
    _qepy.f90wrap_qepy_write_stdout(fstr=fstr)

def qepy_close_stdout(fname):
    """
    qepy_close_stdout(fname)
    
    
    Defined at qepy_mod.fpp lines 327-333
    
    Parameters
    ----------
    fname : str
    
    """
    _qepy.f90wrap_qepy_close_stdout(fname=fname)

def qepy_get_evc(ik, wfc=None):
    """
    qepy_get_evc(ik[, wfc])
    
    
    Defined at qepy_mod.fpp lines 335-349
    
    Parameters
    ----------
    ik : int
    wfc : complex array
    
    """
    _qepy.f90wrap_qepy_get_evc(ik=ik, wfc=wfc)

def qepy_get_wf(ik, ibnd, wf, gather=None):
    """
    qepy_get_wf(ik, ibnd, wf[, gather])
    
    
    Defined at qepy_mod.fpp lines 351-399
    
    Parameters
    ----------
    ik : int
    ibnd : int
    wf : complex array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_wf(ik=ik, ibnd=ibnd, wf=wf, gather=gather)

def qepy_get_vkb(ik, vk, gather=None):
    """
    qepy_get_vkb(ik, vk[, gather])
    
    
    Defined at qepy_mod.fpp lines 401-452
    
    Parameters
    ----------
    ik : int
    vk : complex array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_get_vkb(ik=ik, vk=vk, gather=gather)

def qepy_set_extforces(self, forces):
    """
    qepy_set_extforces(self, forces)
    
    
    Defined at qepy_mod.fpp lines 454-464
    
    Parameters
    ----------
    embed : Embed_Base
    forces : float array
    
    """
    _qepy.f90wrap_qepy_set_extforces(embed=self._handle, forces=forces)

def qepy_calc_effective_potential(self, potential=None, gather=None):
    """
    qepy_calc_effective_potential(self[, potential, gather])
    
    
    Defined at qepy_mod.fpp lines 466-494
    
    Parameters
    ----------
    embed : Embed_Base
    potential : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_calc_effective_potential(embed=self._handle, \
        potential=potential, gather=gather)

def qepy_set_effective_potential(self, potential, gather=None):
    """
    qepy_set_effective_potential(self, potential[, gather])
    
    
    Defined at qepy_mod.fpp lines 496-514
    
    Parameters
    ----------
    embed : Embed_Base
    potential : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_set_effective_potential(embed=self._handle, \
        potential=potential, gather=gather)

def qepy_calc_density(rhor=None, gather=None):
    """
    qepy_calc_density([rhor, gather])
    
    
    Defined at qepy_mod.fpp lines 516-534
    
    Parameters
    ----------
    rhor : float array
    gather : bool
    
    """
    _qepy.f90wrap_qepy_calc_density(rhor=rhor, gather=gather)

def qepy_diagonalize(iter=None, threshold=None):
    """
    qepy_diagonalize([iter, threshold])
    
    
    Defined at qepy_mod.fpp lines 536-554
    
    Parameters
    ----------
    iter : int
    threshold : float
    
    """
    _qepy.f90wrap_qepy_diagonalize(iter=iter, threshold=threshold)

def _mp_gather_real(fin, fout):
    """
    _mp_gather_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 27-39
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    _qepy.f90wrap_mp_gather_real(fin=fin, fout=fout)

def _mp_gather_complex(fin, fout):
    """
    _mp_gather_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 55-67
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    _qepy.f90wrap_mp_gather_complex(fin=fin, fout=fout)

def mp_gather(*args, **kwargs):
    """
    mp_gather(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 14-15
    
    Overloaded interface containing the following procedures:
      _mp_gather_real
      _mp_gather_complex
    
    """
    for proc in [_mp_gather_real, _mp_gather_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _mp_scatter_real(fin, fout):
    """
    _mp_scatter_real(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 41-53
    
    Parameters
    ----------
    fin : float array
    fout : float array
    
    """
    _qepy.f90wrap_mp_scatter_real(fin=fin, fout=fout)

def _mp_scatter_complex(fin, fout):
    """
    _mp_scatter_complex(fin, fout)
    
    
    Defined at qepy_mod.fpp lines 69-81
    
    Parameters
    ----------
    fin : complex array
    fout : complex array
    
    """
    _qepy.f90wrap_mp_scatter_complex(fin=fin, fout=fout)

def mp_scatter(*args, **kwargs):
    """
    mp_scatter(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 18-19
    
    Overloaded interface containing the following procedures:
      _mp_scatter_real
      _mp_scatter_complex
    
    """
    for proc in [_mp_scatter_real, _mp_scatter_complex]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    

def _qepy_get_value_real_1(fin, fout, gather=None, scatter=None):
    """
    _qepy_get_value_real_1(fin, fout[, gather, scatter])
    
    
    Defined at qepy_mod.fpp lines 83-110
    
    Parameters
    ----------
    fin : float array
    fout : float array
    gather : bool
    scatter : bool
    
    """
    _qepy.f90wrap_qepy_get_value_real_1(fin=fin, fout=fout, gather=gather, \
        scatter=scatter)

def _qepy_get_value_real_2(fin, fout, gather=None, scatter=None):
    """
    _qepy_get_value_real_2(fin, fout[, gather, scatter])
    
    
    Defined at qepy_mod.fpp lines 112-132
    
    Parameters
    ----------
    fin : float array
    fout : float array
    gather : bool
    scatter : bool
    
    """
    _qepy.f90wrap_qepy_get_value_real_2(fin=fin, fout=fout, gather=gather, \
        scatter=scatter)

def qepy_get_value(*args, **kwargs):
    """
    qepy_get_value(*args, **kwargs)
    
    
    Defined at qepy_mod.fpp lines 22-23
    
    Overloaded interface containing the following procedures:
      _qepy_get_value_real_1
      _qepy_get_value_real_2
    
    """
    for proc in [_qepy_get_value_real_1, _qepy_get_value_real_2]:
        try:
            return proc(*args, **kwargs)
        except TypeError:
            continue
    


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "qepy_mod".')

for func in _dt_array_initialisers:
    func()
