"""
Module mp_diag


Defined at mp_diag.fpp lines 13-164

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def mp_start_diag(ndiag_, my_world_comm, parent_comm, \
    do_distr_diag_inside_bgrp_):
    """
    mp_start_diag(ndiag_, my_world_comm, parent_comm, do_distr_diag_inside_bgrp_)
    
    
    Defined at mp_diag.fpp lines 46-98
    
    Parameters
    ----------
    ndiag_ : int
    my_world_comm : int
    parent_comm : int
    do_distr_diag_inside_bgrp_ : bool
    
    ---------------------------------------------------------------------------
     ... Ortho/diag/linear algebra group initialization
    """
    _qepy.f90wrap_mp_start_diag(ndiag_=ndiag_, my_world_comm=my_world_comm, \
        parent_comm=parent_comm, \
        do_distr_diag_inside_bgrp_=do_distr_diag_inside_bgrp_)

def init_ortho_group(nproc_try_in, my_world_comm, comm_all, nparent_comm, \
    my_parent_id):
    """
    init_ortho_group(nproc_try_in, my_world_comm, comm_all, nparent_comm, \
        my_parent_id)
    
    
    Defined at mp_diag.fpp lines 102-114
    
    Parameters
    ----------
    nproc_try_in : int
    my_world_comm : int
    comm_all : int
    nparent_comm : int
    my_parent_id : int
    
    """
    _qepy.f90wrap_init_ortho_group(nproc_try_in=nproc_try_in, \
        my_world_comm=my_world_comm, comm_all=comm_all, nparent_comm=nparent_comm, \
        my_parent_id=my_parent_id)

def clean_ortho_group():
    """
    clean_ortho_group()
    
    
    Defined at mp_diag.fpp lines 117-126
    
    
    """
    _qepy.f90wrap_clean_ortho_group()

def laxlib_rank(comm):
    """
    laxlib_rank = laxlib_rank(comm)
    
    
    Defined at mp_diag.fpp lines 130-137
    
    Parameters
    ----------
    comm : int
    
    Returns
    -------
    laxlib_rank : int
    
    """
    laxlib_rank = _qepy.f90wrap_laxlib_rank(comm=comm)
    return laxlib_rank

def laxlib_size(comm):
    """
    laxlib_size = laxlib_size(comm)
    
    
    Defined at mp_diag.fpp lines 140-147
    
    Parameters
    ----------
    comm : int
    
    Returns
    -------
    laxlib_size : int
    
    """
    laxlib_size = _qepy.f90wrap_laxlib_size(comm=comm)
    return laxlib_size

def laxlib_comm_split(old_comm, color, key):
    """
    new_comm = laxlib_comm_split(old_comm, color, key)
    
    
    Defined at mp_diag.fpp lines 149-156
    
    Parameters
    ----------
    old_comm : int
    color : int
    key : int
    
    Returns
    -------
    new_comm : int
    
    """
    new_comm = _qepy.f90wrap_laxlib_comm_split(old_comm=old_comm, color=color, \
        key=key)
    return new_comm

def laxlib_comm_free(comm):
    """
    laxlib_comm_free(comm)
    
    
    Defined at mp_diag.fpp lines 158-163
    
    Parameters
    ----------
    comm : int
    
    """
    _qepy.f90wrap_laxlib_comm_free(comm=comm)

def get_array_np_ortho():
    """
    Element np_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 25
    
    """
    global np_ortho
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_mp_diag__array__np_ortho(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        np_ortho = _arrays[array_handle]
    else:
        np_ortho = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_mp_diag__array__np_ortho)
        _arrays[array_handle] = np_ortho
    return np_ortho

def set_array_np_ortho(np_ortho):
    np_ortho[...] = np_ortho

def get_array_me_ortho():
    """
    Element me_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 26
    
    """
    global me_ortho
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_mp_diag__array__me_ortho(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        me_ortho = _arrays[array_handle]
    else:
        me_ortho = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_mp_diag__array__me_ortho)
        _arrays[array_handle] = me_ortho
    return me_ortho

def set_array_me_ortho(me_ortho):
    me_ortho[...] = me_ortho

def get_me_ortho1():
    """
    Element me_ortho1 ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 27
    
    """
    return _qepy.f90wrap_mp_diag__get__me_ortho1()

def set_me_ortho1(me_ortho1):
    _qepy.f90wrap_mp_diag__set__me_ortho1(me_ortho1)

def get_nproc_ortho():
    """
    Element nproc_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 28
    
    """
    return _qepy.f90wrap_mp_diag__get__nproc_ortho()

def set_nproc_ortho(nproc_ortho):
    _qepy.f90wrap_mp_diag__set__nproc_ortho(nproc_ortho)

def get_leg_ortho():
    """
    Element leg_ortho ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 29
    
    """
    return _qepy.f90wrap_mp_diag__get__leg_ortho()

def set_leg_ortho(leg_ortho):
    _qepy.f90wrap_mp_diag__set__leg_ortho(leg_ortho)

def get_ortho_comm():
    """
    Element ortho_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 31
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_comm()

def set_ortho_comm(ortho_comm):
    _qepy.f90wrap_mp_diag__set__ortho_comm(ortho_comm)

def get_ortho_row_comm():
    """
    Element ortho_row_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 32
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_row_comm()

def set_ortho_row_comm(ortho_row_comm):
    _qepy.f90wrap_mp_diag__set__ortho_row_comm(ortho_row_comm)

def get_ortho_col_comm():
    """
    Element ortho_col_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 33
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_col_comm()

def set_ortho_col_comm(ortho_col_comm):
    _qepy.f90wrap_mp_diag__set__ortho_col_comm(ortho_col_comm)

def get_ortho_comm_id():
    """
    Element ortho_comm_id ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 34
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_comm_id()

def set_ortho_comm_id(ortho_comm_id):
    _qepy.f90wrap_mp_diag__set__ortho_comm_id(ortho_comm_id)

def get_ortho_parent_comm():
    """
    Element ortho_parent_comm ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 35
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_parent_comm()

def set_ortho_parent_comm(ortho_parent_comm):
    _qepy.f90wrap_mp_diag__set__ortho_parent_comm(ortho_parent_comm)

def get_world_cntx():
    """
    Element world_cntx ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 38
    
    """
    return _qepy.f90wrap_mp_diag__get__world_cntx()

def set_world_cntx(world_cntx):
    _qepy.f90wrap_mp_diag__set__world_cntx(world_cntx)

def get_ortho_cntx():
    """
    Element ortho_cntx ftype=integer  pytype=int
    
    
    Defined at mp_diag.fpp line 39
    
    """
    return _qepy.f90wrap_mp_diag__get__ortho_cntx()

def set_ortho_cntx(ortho_cntx):
    _qepy.f90wrap_mp_diag__set__ortho_cntx(ortho_cntx)

def get_do_distr_diag_inside_bgrp():
    """
    Element do_distr_diag_inside_bgrp ftype=logical pytype=bool
    
    
    Defined at mp_diag.fpp line 41
    
    """
    return _qepy.f90wrap_mp_diag__get__do_distr_diag_inside_bgrp()

def set_do_distr_diag_inside_bgrp(do_distr_diag_inside_bgrp):
    _qepy.f90wrap_mp_diag__set__do_distr_diag_inside_bgrp(do_distr_diag_inside_bgrp)


_array_initialisers = [get_array_np_ortho, get_array_me_ortho]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "mp_diag".')

for func in _dt_array_initialisers:
    func()
