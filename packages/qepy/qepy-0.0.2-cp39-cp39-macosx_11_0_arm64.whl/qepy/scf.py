"""
Module scf


Defined at scf_mod.fpp lines 13-922

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy.scf_type")
class scf_type(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=scf_type)
    
    
    Defined at scf_mod.fpp lines 49-63
    
    """
    def __init__(self, handle=None):
        """
        self = Scf_Type()
        
        
        Defined at scf_mod.fpp lines 49-63
        
        
        Returns
        -------
        this : Scf_Type
        	Object to be constructed
        
        
        Automatically generated constructor for scf_type
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_scf_type_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Scf_Type
        
        
        Defined at scf_mod.fpp lines 49-63
        
        Parameters
        ----------
        this : Scf_Type
        	Object to be destructed
        
        
        Automatically generated destructor for scf_type
        """
        if self._alloc:
            _qepy.f90wrap_scf_type_finalise(this=self._handle)
    
    @property
    def of_r(self):
        """
        Element of_r ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 50
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__of_r(self._handle)
        if array_handle in self._arrays:
            of_r = self._arrays[array_handle]
        else:
            of_r = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__of_r)
            self._arrays[array_handle] = of_r
        return of_r
    
    @of_r.setter
    def of_r(self, of_r):
        self.of_r[...] = of_r
    
    @property
    def of_g(self):
        """
        Element of_g ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 52
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__of_g(self._handle)
        if array_handle in self._arrays:
            of_g = self._arrays[array_handle]
        else:
            of_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__of_g)
            self._arrays[array_handle] = of_g
        return of_g
    
    @of_g.setter
    def of_g(self, of_g):
        self.of_g[...] = of_g
    
    @property
    def kin_r(self):
        """
        Element kin_r ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 54
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__kin_r(self._handle)
        if array_handle in self._arrays:
            kin_r = self._arrays[array_handle]
        else:
            kin_r = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__kin_r)
            self._arrays[array_handle] = kin_r
        return kin_r
    
    @kin_r.setter
    def kin_r(self, kin_r):
        self.kin_r[...] = kin_r
    
    @property
    def kin_g(self):
        """
        Element kin_g ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 56
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__kin_g(self._handle)
        if array_handle in self._arrays:
            kin_g = self._arrays[array_handle]
        else:
            kin_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__kin_g)
            self._arrays[array_handle] = kin_g
        return kin_g
    
    @kin_g.setter
    def kin_g(self, kin_g):
        self.kin_g[...] = kin_g
    
    @property
    def ns(self):
        """
        Element ns ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 58
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__ns(self._handle)
        if array_handle in self._arrays:
            ns = self._arrays[array_handle]
        else:
            ns = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__ns)
            self._arrays[array_handle] = ns
        return ns
    
    @ns.setter
    def ns(self, ns):
        self.ns[...] = ns
    
    @property
    def ns_nc(self):
        """
        Element ns_nc ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 60
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__ns_nc(self._handle)
        if array_handle in self._arrays:
            ns_nc = self._arrays[array_handle]
        else:
            ns_nc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__ns_nc)
            self._arrays[array_handle] = ns_nc
        return ns_nc
    
    @ns_nc.setter
    def ns_nc(self, ns_nc):
        self.ns_nc[...] = ns_nc
    
    @property
    def bec(self):
        """
        Element bec ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 62
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_scf_type__array__bec(self._handle)
        if array_handle in self._arrays:
            bec = self._arrays[array_handle]
        else:
            bec = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_scf_type__array__bec)
            self._arrays[array_handle] = bec
        return bec
    
    @bec.setter
    def bec(self, bec):
        self.bec[...] = bec
    
    def __str__(self):
        ret = ['<scf_type>{\n']
        ret.append('    of_r : ')
        ret.append(repr(self.of_r))
        ret.append(',\n    of_g : ')
        ret.append(repr(self.of_g))
        ret.append(',\n    kin_r : ')
        ret.append(repr(self.kin_r))
        ret.append(',\n    kin_g : ')
        ret.append(repr(self.kin_g))
        ret.append(',\n    ns : ')
        ret.append(repr(self.ns))
        ret.append(',\n    ns_nc : ')
        ret.append(repr(self.ns_nc))
        ret.append(',\n    bec : ')
        ret.append(repr(self.bec))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy.mix_type")
class mix_type(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=mix_type)
    
    
    Defined at scf_mod.fpp lines 66-78
    
    """
    def __init__(self, handle=None):
        """
        self = Mix_Type()
        
        
        Defined at scf_mod.fpp lines 66-78
        
        
        Returns
        -------
        this : Mix_Type
        	Object to be constructed
        
        
        Automatically generated constructor for mix_type
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_mix_type_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Mix_Type
        
        
        Defined at scf_mod.fpp lines 66-78
        
        Parameters
        ----------
        this : Mix_Type
        	Object to be destructed
        
        
        Automatically generated destructor for mix_type
        """
        if self._alloc:
            _qepy.f90wrap_mix_type_finalise(this=self._handle)
    
    @property
    def of_g(self):
        """
        Element of_g ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 67
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_mix_type__array__of_g(self._handle)
        if array_handle in self._arrays:
            of_g = self._arrays[array_handle]
        else:
            of_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_mix_type__array__of_g)
            self._arrays[array_handle] = of_g
        return of_g
    
    @of_g.setter
    def of_g(self, of_g):
        self.of_g[...] = of_g
    
    @property
    def kin_g(self):
        """
        Element kin_g ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 69
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_mix_type__array__kin_g(self._handle)
        if array_handle in self._arrays:
            kin_g = self._arrays[array_handle]
        else:
            kin_g = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_mix_type__array__kin_g)
            self._arrays[array_handle] = kin_g
        return kin_g
    
    @kin_g.setter
    def kin_g(self, kin_g):
        self.kin_g[...] = kin_g
    
    @property
    def ns(self):
        """
        Element ns ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 71
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_mix_type__array__ns(self._handle)
        if array_handle in self._arrays:
            ns = self._arrays[array_handle]
        else:
            ns = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_mix_type__array__ns)
            self._arrays[array_handle] = ns
        return ns
    
    @ns.setter
    def ns(self, ns):
        self.ns[...] = ns
    
    @property
    def ns_nc(self):
        """
        Element ns_nc ftype=complex(dp) pytype=complex
        
        
        Defined at scf_mod.fpp line 73
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_mix_type__array__ns_nc(self._handle)
        if array_handle in self._arrays:
            ns_nc = self._arrays[array_handle]
        else:
            ns_nc = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_mix_type__array__ns_nc)
            self._arrays[array_handle] = ns_nc
        return ns_nc
    
    @ns_nc.setter
    def ns_nc(self, ns_nc):
        self.ns_nc[...] = ns_nc
    
    @property
    def bec(self):
        """
        Element bec ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 75
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_mix_type__array__bec(self._handle)
        if array_handle in self._arrays:
            bec = self._arrays[array_handle]
        else:
            bec = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_mix_type__array__bec)
            self._arrays[array_handle] = bec
        return bec
    
    @bec.setter
    def bec(self, bec):
        self.bec[...] = bec
    
    @property
    def el_dipole(self):
        """
        Element el_dipole ftype=real(dp) pytype=float
        
        
        Defined at scf_mod.fpp line 77
        
        """
        return _qepy.f90wrap_mix_type__get__el_dipole(self._handle)
    
    @el_dipole.setter
    def el_dipole(self, el_dipole):
        _qepy.f90wrap_mix_type__set__el_dipole(self._handle, el_dipole)
    
    def __str__(self):
        ret = ['<mix_type>{\n']
        ret.append('    of_g : ')
        ret.append(repr(self.of_g))
        ret.append(',\n    kin_g : ')
        ret.append(repr(self.kin_g))
        ret.append(',\n    ns : ')
        ret.append(repr(self.ns))
        ret.append(',\n    ns_nc : ')
        ret.append(repr(self.ns_nc))
        ret.append(',\n    bec : ')
        ret.append(repr(self.bec))
        ret.append(',\n    el_dipole : ')
        ret.append(repr(self.el_dipole))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

def create_scf_type(self, do_not_allocate_becsum=None):
    """
    create_scf_type(self[, do_not_allocate_becsum])
    
    
    Defined at scf_mod.fpp lines 113-155
    
    Parameters
    ----------
    rho : Scf_Type
    do_not_allocate_becsum : bool
    
    ----------------------------------------------------------
     Creates an scf_type object by allocating all the
     different terms.
    """
    _qepy.f90wrap_create_scf_type(rho=self._handle, \
        do_not_allocate_becsum=do_not_allocate_becsum)

def destroy_scf_type(self):
    """
    destroy_scf_type(self)
    
    
    Defined at scf_mod.fpp lines 160-178
    
    Parameters
    ----------
    rho : Scf_Type
    
    ---------------------------------------------------
     Deallocates an scf_type object
    """
    _qepy.f90wrap_destroy_scf_type(rho=self._handle)

def create_mix_type(self):
    """
    create_mix_type(self)
    
    
    Defined at scf_mod.fpp lines 183-220
    
    Parameters
    ----------
    rho : Mix_Type
    
    --------------------------------------------------
    """
    _qepy.f90wrap_create_mix_type(rho=self._handle)

def destroy_mix_type(self):
    """
    destroy_mix_type(self)
    
    
    Defined at scf_mod.fpp lines 225-239
    
    Parameters
    ----------
    rho : Mix_Type
    
    ----------------------------------------------------
    """
    _qepy.f90wrap_destroy_mix_type(rho=self._handle)

def assign_scf_to_mix_type(self, rho_m):
    """
    assign_scf_to_mix_type(self, rho_m)
    
    
    Defined at scf_mod.fpp lines 244-266
    
    Parameters
    ----------
    rho_s : Scf_Type
    rho_m : Mix_Type
    
    ----------------------------------------------------
    """
    _qepy.f90wrap_assign_scf_to_mix_type(rho_s=self._handle, rho_m=rho_m._handle)

def assign_mix_to_scf_type(self, rho_s):
    """
    assign_mix_to_scf_type(self, rho_s)
    
    
    Defined at scf_mod.fpp lines 271-316
    
    Parameters
    ----------
    rho_m : Mix_Type
    rho_s : Scf_Type
    
    ----------------------------------------------------------------
    """
    _qepy.f90wrap_assign_mix_to_scf_type(rho_m=self._handle, rho_s=rho_s._handle)

def scf_type_copy(self, y):
    """
    scf_type_copy(self, y)
    
    
    Defined at scf_mod.fpp lines 321-345
    
    Parameters
    ----------
    x : Scf_Type
    y : Scf_Type
    
    ----------------------------------------------------------------------------
     works like DCOPY for scf_type copy variables :  Y = X
    """
    _qepy.f90wrap_scf_type_copy(x=self._handle, y=y._handle)

def mix_type_axpy(a, x, y):
    """
    mix_type_axpy(a, x, y)
    
    
    Defined at scf_mod.fpp lines 350-372
    
    Parameters
    ----------
    a : float
    x : Mix_Type
    y : Mix_Type
    
    ----------------------------------------------------------------------------
     Works like daxpy for scf_type variables :  Y = A * X + Y
     NB: A is a REAL(DP) number
    """
    _qepy.f90wrap_mix_type_axpy(a=a, x=x._handle, y=y._handle)

def mix_type_copy(self, y):
    """
    mix_type_copy(self, y)
    
    
    Defined at scf_mod.fpp lines 377-397
    
    Parameters
    ----------
    x : Mix_Type
    y : Mix_Type
    
    ----------------------------------------------------------------------------
     Works like DCOPY for mix_type copy variables :  Y = X
    """
    _qepy.f90wrap_mix_type_copy(x=self._handle, y=y._handle)

def mix_type_scal(a, x):
    """
    mix_type_scal(a, x)
    
    
    Defined at scf_mod.fpp lines 402-423
    
    Parameters
    ----------
    a : float
    x : Mix_Type
    
    ----------------------------------------------------------------------------
     Works like DSCAL for mix_type copy variables :  \(X = A * X\)
     NB: A is a REAL(DP) number
    """
    _qepy.f90wrap_mix_type_scal(a=a, x=x._handle)

def high_frequency_mixing(self, input_rhout, alphamix):
    """
    high_frequency_mixing(self, input_rhout, alphamix)
    
    
    Defined at scf_mod.fpp lines 428-485
    
    Parameters
    ----------
    rhoin : Scf_Type
    input_rhout : Scf_Type
    alphamix : float
    
    -------------------------------------------------------------------
    """
    _qepy.f90wrap_high_frequency_mixing(rhoin=self._handle, \
        input_rhout=input_rhout._handle, alphamix=alphamix)

def open_mix_file(iunit, extension, exst):
    """
    open_mix_file(iunit, extension, exst)
    
    
    Defined at scf_mod.fpp lines 490-531
    
    Parameters
    ----------
    iunit : int
    extension : str
    exst : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_open_mix_file(iunit=iunit, extension=extension, exst=exst)

def close_mix_file(iunit, stat):
    """
    close_mix_file(iunit, stat)
    
    
    Defined at scf_mod.fpp lines 536-549
    
    Parameters
    ----------
    iunit : int
    stat : str
    
    ---------------------------------------------------------------------
    """
    _qepy.f90wrap_close_mix_file(iunit=iunit, stat=stat)

def davcio_mix_type(self, iunit, record, iflag):
    """
    davcio_mix_type(self, iunit, record, iflag)
    
    
    Defined at scf_mod.fpp lines 554-589
    
    Parameters
    ----------
    rho : Mix_Type
    iunit : int
    record : int
    iflag : int
    
    ----------------------------------------------------------
    """
    _qepy.f90wrap_davcio_mix_type(rho=self._handle, iunit=iunit, record=record, \
        iflag=iflag)

def rho_ddot(self, rho2, gf):
    """
    rho_ddot = rho_ddot(self, rho2, gf)
    
    
    Defined at scf_mod.fpp lines 594-666
    
    Parameters
    ----------
    rho1 : Mix_Type
    rho2 : Mix_Type
    gf : int
    
    Returns
    -------
    rho_ddot : float
    
    ----------------------------------------------------------------------------------
     Calculates \(4\pi/G^2\ \rho_1(-G)\ \rho_2(G) = V1_\text{Hartree}(-G)\ \
         \rho_2(G)\)
     used as an estimate of the self-consistency error on the energy.
    """
    rho_ddot = _qepy.f90wrap_rho_ddot(rho1=self._handle, rho2=rho2._handle, gf=gf)
    return rho_ddot

def tauk_ddot(self, rho2, gf):
    """
    tauk_ddot = tauk_ddot(self, rho2, gf)
    
    
    Defined at scf_mod.fpp lines 671-742
    
    Parameters
    ----------
    rho1 : Mix_Type
    rho2 : Mix_Type
    gf : int
    
    Returns
    -------
    tauk_ddot : float
    
    ----------------------------------------------------------------------------
     Calculates \(4\pi/G^2\ \rho_1(-G)\ \rho_2(G) = V1_\text{Hartree}(-G)\ \
         \rho_2(G)\)
     used as an estimate of the self-consistency error on the energy - kinetic \
         density
     version.
    """
    tauk_ddot = _qepy.f90wrap_tauk_ddot(rho1=self._handle, rho2=rho2._handle, gf=gf)
    return tauk_ddot

def ns_ddot(self, rho2):
    """
    ns_ddot = ns_ddot(self, rho2)
    
    
    Defined at scf_mod.fpp lines 747-791
    
    Parameters
    ----------
    rho1 : Mix_Type
    rho2 : Mix_Type
    
    Returns
    -------
    ns_ddot : float
    
    ---------------------------------------------------------------------------
     Calculates \(U/2 \sum_i \text{ns1}(i)\ \text{ns2}(i)\) used as an estimate
     of the self-consistency error on the LDA+U correction to the energy.
    """
    ns_ddot = _qepy.f90wrap_ns_ddot(rho1=self._handle, rho2=rho2._handle)
    return ns_ddot

def local_tf_ddot(rho1, rho2, ngm0):
    """
    local_tf_ddot = local_tf_ddot(rho1, rho2, ngm0)
    
    
    Defined at scf_mod.fpp lines 796-843
    
    Parameters
    ----------
    rho1 : complex array
    rho2 : complex array
    ngm0 : int
    
    Returns
    -------
    local_tf_ddot : float
    
    ----------------------------------------------------------------------------
     Calculates \(4\pi/G^2\ \rho_1(-G)\ \rho_2(G) = V1_\text{Hartree}(-G)\ \
         \rho_2(G)\)
     used as an estimate of the self-consistency error on the energy - version
     for the case with local-density dependent TF preconditioning to drho.
    """
    local_tf_ddot = _qepy.f90wrap_local_tf_ddot(rho1=rho1, rho2=rho2, ngm0=ngm0)
    return local_tf_ddot

def bcast_scf_type(self, root, comm):
    """
    bcast_scf_type(self, root, comm)
    
    
    Defined at scf_mod.fpp lines 848-869
    
    Parameters
    ----------
    rho : Scf_Type
    root : int
    comm : int
    
    ----------------------------------------------------------------------------
     Broadcast all mixed quantities from first pool to all others.
     Needed to prevent divergencies in k-point parallelization.
    """
    _qepy.f90wrap_bcast_scf_type(rho=self._handle, root=root, comm=comm)

def rhoz_or_updw(self, sp, dir):
    """
    rhoz_or_updw(self, sp, dir)
    
    
    Defined at scf_mod.fpp lines 874-920
    
    Parameters
    ----------
    rho : Scf_Type
    sp : str
    dir : str
    
    --------------------------------------------------------------------------
     Converts rho(up,dw) into rho(up+dw,up-dw) if dir='->rhoz' and
     vice versa if dir='->updw'.
    """
    _qepy.f90wrap_rhoz_or_updw(rho=self._handle, sp=sp, dir=dir)

def get_v_of_0():
    """
    Element v_of_0 ftype=real(dp) pytype=float
    
    
    Defined at scf_mod.fpp line 88
    
    """
    return _qepy.f90wrap_scf__get__v_of_0()

def set_v_of_0(v_of_0):
    _qepy.f90wrap_scf__set__v_of_0(v_of_0)

def get_array_vltot():
    """
    Element vltot ftype=real(dp) pytype=float
    
    
    Defined at scf_mod.fpp line 90
    
    """
    global vltot
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_scf__array__vltot(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vltot = _arrays[array_handle]
    else:
        vltot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_scf__array__vltot)
        _arrays[array_handle] = vltot
    return vltot

def set_array_vltot(vltot):
    vltot[...] = vltot

def get_array_vrs():
    """
    Element vrs ftype=real(dp) pytype=float
    
    
    Defined at scf_mod.fpp line 92
    
    """
    global vrs
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_scf__array__vrs(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        vrs = _arrays[array_handle]
    else:
        vrs = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_scf__array__vrs)
        _arrays[array_handle] = vrs
    return vrs

def set_array_vrs(vrs):
    vrs[...] = vrs

def get_array_rho_core():
    """
    Element rho_core ftype=real(dp) pytype=float
    
    
    Defined at scf_mod.fpp line 94
    
    """
    global rho_core
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_scf__array__rho_core(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rho_core = _arrays[array_handle]
    else:
        rho_core = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_scf__array__rho_core)
        _arrays[array_handle] = rho_core
    return rho_core

def set_array_rho_core(rho_core):
    rho_core[...] = rho_core

def get_array_kedtau():
    """
    Element kedtau ftype=real(dp) pytype=float
    
    
    Defined at scf_mod.fpp line 96
    
    """
    global kedtau
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_scf__array__kedtau(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        kedtau = _arrays[array_handle]
    else:
        kedtau = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_scf__array__kedtau)
        _arrays[array_handle] = kedtau
    return kedtau

def set_array_kedtau(kedtau):
    kedtau[...] = kedtau

def get_array_rhog_core():
    """
    Element rhog_core ftype=complex(dp) pytype=complex
    
    
    Defined at scf_mod.fpp line 98
    
    """
    global rhog_core
    array_ndim, array_type, array_shape, array_handle = \
        _qepy.f90wrap_scf__array__rhog_core(f90wrap.runtime.empty_handle)
    if array_handle in _arrays:
        rhog_core = _arrays[array_handle]
    else:
        rhog_core = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                f90wrap.runtime.empty_handle,
                                _qepy.f90wrap_scf__array__rhog_core)
        _arrays[array_handle] = rhog_core
    return rhog_core

def set_array_rhog_core(rhog_core):
    rhog_core[...] = rhog_core


_array_initialisers = [get_array_vltot, get_array_vrs, get_array_rho_core, \
    get_array_kedtau, get_array_rhog_core]
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module "scf".')

for func in _dt_array_initialisers:
    func()
