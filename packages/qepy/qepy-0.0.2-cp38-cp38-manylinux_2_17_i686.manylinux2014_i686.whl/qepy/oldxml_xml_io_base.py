"""
Module oldxml_xml_io_base


Defined at oldxml_xml_io_base.fpp lines 13-1018

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def restart_dir(outdir, runit):
    """
    restart_dir = restart_dir(outdir, runit)
    
    
    Defined at oldxml_xml_io_base.fpp lines 53-81
    
    Parameters
    ----------
    outdir : str
    runit : int
    
    Returns
    -------
    restart_dir : str
    
    ------------------------------------------------------------------------
     KNK_nimage
     USE mp_images, ONLY:  my_image_id
    """
    restart_dir = _qepy.f90wrap_restart_dir(outdir=outdir, runit=runit)
    return restart_dir

def save_print_counter(iter, outdir, wunit):
    """
    save_print_counter(iter, outdir, wunit)
    
    
    Defined at oldxml_xml_io_base.fpp lines 118-164
    
    Parameters
    ----------
    iter : int
    outdir : str
    wunit : int
    
    ------------------------------------------------------------------------
     ... a counter indicating the last successful printout iteration is saved
    """
    _qepy.f90wrap_save_print_counter(iter=iter, outdir=outdir, wunit=wunit)

def read_print_counter(outdir, runit):
    """
    nprint_nfi = read_print_counter(outdir, runit)
    
    
    Defined at oldxml_xml_io_base.fpp lines 168-213
    
    Parameters
    ----------
    outdir : str
    runit : int
    
    Returns
    -------
    nprint_nfi : int
    
    ------------------------------------------------------------------------
     ... the counter indicating the last successful printout iteration
     ... is read here
    """
    nprint_nfi = _qepy.f90wrap_read_print_counter(outdir=outdir, runit=runit)
    return nprint_nfi

def write_rho(dirname, rho, nspin, extension=None):
    """
    write_rho(dirname, rho, nspin[, extension])
    
    
    Defined at oldxml_xml_io_base.fpp lines 346-411
    
    Parameters
    ----------
    dirname : str
    rho : float array
    nspin : int
    extension : str
    
    ------------------------------------------------------------------------
     ... this routine writes the charge-density in xml format into the
     ... $dirname directory - $dirname must exist and end with '/'
    """
    _qepy.f90wrap_write_rho(dirname=dirname, rho=rho, nspin=nspin, \
        extension=extension)

def read_rho(dirname, rho, nspin, extension=None):
    """
    read_rho(dirname, rho, nspin[, extension])
    
    
    Defined at oldxml_xml_io_base.fpp lines 415-468
    
    Parameters
    ----------
    dirname : str
    rho : float array
    nspin : int
    extension : str
    
    ------------------------------------------------------------------------
     ... this routine reads the charge-density in xml format from the
     ... files saved into the '.save' directory
    """
    _qepy.f90wrap_read_rho(dirname=dirname, rho=rho, nspin=nspin, \
        extension=extension)

def write_wfc(iuni, ik, nk, kunit, ispin, nspin, wf0, ngw, gamma_only, nbnd, \
    igl, ngwl, filename, scalef, ionode, root_in_group, intra_group_comm, \
    inter_group_comm, parent_group_comm):
    """
    write_wfc(iuni, ik, nk, kunit, ispin, nspin, wf0, ngw, gamma_only, nbnd, igl, \
        ngwl, filename, scalef, ionode, root_in_group, intra_group_comm, \
        inter_group_comm, parent_group_comm)
    
    
    Defined at oldxml_xml_io_base.fpp lines 732-859
    
    Parameters
    ----------
    iuni : int
    ik : int
    nk : int
    kunit : int
    ispin : int
    nspin : int
    wf0 : complex array
    ngw : int
    gamma_only : bool
    nbnd : int
    igl : int array
    ngwl : int
    filename : str
    scalef : float
    ionode : bool
    root_in_group : int
    intra_group_comm : int
    inter_group_comm : int
    parent_group_comm : int
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_write_wfc(iuni=iuni, ik=ik, nk=nk, kunit=kunit, ispin=ispin, \
        nspin=nspin, wf0=wf0, ngw=ngw, gamma_only=gamma_only, nbnd=nbnd, igl=igl, \
        ngwl=ngwl, filename=filename, scalef=scalef, ionode=ionode, \
        root_in_group=root_in_group, intra_group_comm=intra_group_comm, \
        inter_group_comm=inter_group_comm, parent_group_comm=parent_group_comm)

def read_wfc(iuni, ik, nk, kunit, ispin, nspin, wf, ngw, nbnd, igl, ngwl, \
    filename, ionode, root_in_group, intra_group_comm, inter_group_comm, \
    parent_group_comm, flink=None):
    """
    scalef = read_wfc(iuni, ik, nk, kunit, ispin, nspin, wf, ngw, nbnd, igl, ngwl, \
        filename, ionode, root_in_group, intra_group_comm, inter_group_comm, \
        parent_group_comm[, flink])
    
    
    Defined at oldxml_xml_io_base.fpp lines 866-1017
    
    Parameters
    ----------
    iuni : int
    ik : int
    nk : int
    kunit : int
    ispin : int
    nspin : int
    wf : complex array
    ngw : int
    nbnd : int
    igl : int array
    ngwl : int
    filename : str
    ionode : bool
    root_in_group : int
    intra_group_comm : int
    inter_group_comm : int
    parent_group_comm : int
    flink : bool
    
    Returns
    -------
    scalef : float
    
    ------------------------------------------------------------------------
    """
    scalef = _qepy.f90wrap_read_wfc(iuni=iuni, ik=ik, nk=nk, kunit=kunit, \
        ispin=ispin, nspin=nspin, wf=wf, ngw=ngw, nbnd=nbnd, igl=igl, ngwl=ngwl, \
        filename=filename, ionode=ionode, root_in_group=root_in_group, \
        intra_group_comm=intra_group_comm, inter_group_comm=inter_group_comm, \
        parent_group_comm=parent_group_comm, flink=flink)
    return scalef

def get_attr():
    """
    Element attr ftype=character(iotk_attlenx) pytype=str
    
    
    Defined at oldxml_xml_io_base.fpp line 36
    
    """
    return _qepy.f90wrap_oldxml_xml_io_base__get__attr()

def set_attr(attr):
    _qepy.f90wrap_oldxml_xml_io_base__set__attr(attr)

def get_rho_binary():
    """
    Element rho_binary ftype=logical pytype=bool
    
    
    Defined at oldxml_xml_io_base.fpp line 37
    
    """
    return _qepy.f90wrap_oldxml_xml_io_base__get__rho_binary()

def set_rho_binary(rho_binary):
    _qepy.f90wrap_oldxml_xml_io_base__set__rho_binary(rho_binary)

def get_xmlpun():
    """
    Element xmlpun ftype=character(len=13) pytype=str
    
    
    Defined at oldxml_xml_io_base.fpp line 39
    
    """
    return _qepy.f90wrap_oldxml_xml_io_base__get__xmlpun()

xmlpun = get_xmlpun()

def get_qexml_version():
    """
    Element qexml_version ftype=character(len=256) pytype=str
    
    
    Defined at oldxml_xml_io_base.fpp line 40
    
    """
    return _qepy.f90wrap_oldxml_xml_io_base__get__qexml_version()

def set_qexml_version(qexml_version):
    _qepy.f90wrap_oldxml_xml_io_base__set__qexml_version(qexml_version)

def get_qexml_version_init():
    """
    Element qexml_version_init ftype=logical pytype=bool
    
    
    Defined at oldxml_xml_io_base.fpp line 41
    
    """
    return _qepy.f90wrap_oldxml_xml_io_base__get__qexml_version_init()

def set_qexml_version_init(qexml_version_init):
    _qepy.f90wrap_oldxml_xml_io_base__set__qexml_version_init(qexml_version_init)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "oldxml_xml_io_base".')

for func in _dt_array_initialisers:
    func()
