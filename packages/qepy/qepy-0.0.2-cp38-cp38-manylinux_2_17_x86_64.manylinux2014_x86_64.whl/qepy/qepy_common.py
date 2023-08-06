"""
Module qepy_common


Defined at qepy_common.fpp lines 5-249

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("qepy.input_base")
class input_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=input_base)
    
    
    Defined at qepy_common.fpp lines 12-21
    
    """
    def __init__(self, handle=None):
        """
        self = Input_Base()
        
        
        Defined at qepy_common.fpp lines 12-21
        
        
        Returns
        -------
        this : Input_Base
        	Object to be constructed
        
        
        Automatically generated constructor for input_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_input_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Input_Base
        
        
        Defined at qepy_common.fpp lines 12-21
        
        Parameters
        ----------
        this : Input_Base
        	Object to be destructed
        
        
        Automatically generated destructor for input_base
        """
        if self._alloc:
            _qepy.f90wrap_input_base_finalise(this=self._handle)
    
    @property
    def my_world_comm(self):
        """
        Element my_world_comm ftype=integer             pytype=int
        
        
        Defined at qepy_common.fpp line 13
        
        """
        return _qepy.f90wrap_input_base__get__my_world_comm(self._handle)
    
    @my_world_comm.setter
    def my_world_comm(self, my_world_comm):
        _qepy.f90wrap_input_base__set__my_world_comm(self._handle, my_world_comm)
    
    @property
    def start_images(self):
        """
        Element start_images ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 14
        
        """
        return _qepy.f90wrap_input_base__get__start_images(self._handle)
    
    @start_images.setter
    def start_images(self, start_images):
        _qepy.f90wrap_input_base__set__start_images(self._handle, start_images)
    
    @property
    def filename(self):
        """
        Element filename ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 15
        
        """
        return _qepy.f90wrap_input_base__get__filename(self._handle)
    
    @filename.setter
    def filename(self, filename):
        _qepy.f90wrap_input_base__set__filename(self._handle, filename)
    
    @property
    def code(self):
        """
        Element code ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 16
        
        """
        return _qepy.f90wrap_input_base__get__code(self._handle)
    
    @code.setter
    def code(self, code):
        _qepy.f90wrap_input_base__set__code(self._handle, code)
    
    @property
    def tmp_dir(self):
        """
        Element tmp_dir ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 17
        
        """
        return _qepy.f90wrap_input_base__get__tmp_dir(self._handle)
    
    @tmp_dir.setter
    def tmp_dir(self, tmp_dir):
        _qepy.f90wrap_input_base__set__tmp_dir(self._handle, tmp_dir)
    
    @property
    def wfc_dir(self):
        """
        Element wfc_dir ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 18
        
        """
        return _qepy.f90wrap_input_base__get__wfc_dir(self._handle)
    
    @wfc_dir.setter
    def wfc_dir(self, wfc_dir):
        _qepy.f90wrap_input_base__set__wfc_dir(self._handle, wfc_dir)
    
    @property
    def prefix(self):
        """
        Element prefix ftype=character(len=256) pytype=str
        
        
        Defined at qepy_common.fpp line 19
        
        """
        return _qepy.f90wrap_input_base__get__prefix(self._handle)
    
    @prefix.setter
    def prefix(self, prefix):
        _qepy.f90wrap_input_base__set__prefix(self._handle, prefix)
    
    @property
    def needwf(self):
        """
        Element needwf ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 21
        
        """
        return _qepy.f90wrap_input_base__get__needwf(self._handle)
    
    @needwf.setter
    def needwf(self, needwf):
        _qepy.f90wrap_input_base__set__needwf(self._handle, needwf)
    
    def __str__(self):
        ret = ['<input_base>{\n']
        ret.append('    my_world_comm : ')
        ret.append(repr(self.my_world_comm))
        ret.append(',\n    start_images : ')
        ret.append(repr(self.start_images))
        ret.append(',\n    filename : ')
        ret.append(repr(self.filename))
        ret.append(',\n    code : ')
        ret.append(repr(self.code))
        ret.append(',\n    tmp_dir : ')
        ret.append(repr(self.tmp_dir))
        ret.append(',\n    wfc_dir : ')
        ret.append(repr(self.wfc_dir))
        ret.append(',\n    prefix : ')
        ret.append(repr(self.prefix))
        ret.append(',\n    needwf : ')
        ret.append(repr(self.needwf))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy.tddft_base")
class tddft_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=tddft_base)
    
    
    Defined at qepy_common.fpp lines 24-33
    
    """
    def __init__(self, handle=None):
        """
        self = Tddft_Base()
        
        
        Defined at qepy_common.fpp lines 24-33
        
        
        Returns
        -------
        this : Tddft_Base
        	Object to be constructed
        
        
        Automatically generated constructor for tddft_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_tddft_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Tddft_Base
        
        
        Defined at qepy_common.fpp lines 24-33
        
        Parameters
        ----------
        this : Tddft_Base
        	Object to be destructed
        
        
        Automatically generated destructor for tddft_base
        """
        if self._alloc:
            _qepy.f90wrap_tddft_base_finalise(this=self._handle)
    
    @property
    def initial(self):
        """
        Element initial ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 25
        
        """
        return _qepy.f90wrap_tddft_base__get__initial(self._handle)
    
    @initial.setter
    def initial(self, initial):
        _qepy.f90wrap_tddft_base__set__initial(self._handle, initial)
    
    @property
    def finish(self):
        """
        Element finish ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 26
        
        """
        return _qepy.f90wrap_tddft_base__get__finish(self._handle)
    
    @finish.setter
    def finish(self, finish):
        _qepy.f90wrap_tddft_base__set__finish(self._handle, finish)
    
    @property
    def istep(self):
        """
        Element istep ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 27
        
        """
        return _qepy.f90wrap_tddft_base__get__istep(self._handle)
    
    @istep.setter
    def istep(self, istep):
        _qepy.f90wrap_tddft_base__set__istep(self._handle, istep)
    
    @property
    def nstep(self):
        """
        Element nstep ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 28
        
        """
        return _qepy.f90wrap_tddft_base__get__nstep(self._handle)
    
    @nstep.setter
    def nstep(self, nstep):
        _qepy.f90wrap_tddft_base__set__nstep(self._handle, nstep)
    
    @property
    def iterative(self):
        """
        Element iterative ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 29
        
        """
        return _qepy.f90wrap_tddft_base__get__iterative(self._handle)
    
    @iterative.setter
    def iterative(self, iterative):
        _qepy.f90wrap_tddft_base__set__iterative(self._handle, iterative)
    
    @property
    def dipole(self):
        """
        Element dipole ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 30
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_tddft_base__array__dipole(self._handle)
        if array_handle in self._arrays:
            dipole = self._arrays[array_handle]
        else:
            dipole = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_tddft_base__array__dipole)
            self._arrays[array_handle] = dipole
        return dipole
    
    @dipole.setter
    def dipole(self, dipole):
        self.dipole[...] = dipole
    
    def __str__(self):
        ret = ['<tddft_base>{\n']
        ret.append('    initial : ')
        ret.append(repr(self.initial))
        ret.append(',\n    finish : ')
        ret.append(repr(self.finish))
        ret.append(',\n    istep : ')
        ret.append(repr(self.istep))
        ret.append(',\n    nstep : ')
        ret.append(repr(self.nstep))
        ret.append(',\n    iterative : ')
        ret.append(repr(self.iterative))
        ret.append(',\n    dipole : ')
        ret.append(repr(self.dipole))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy.energies_base")
class energies_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=energies_base)
    
    
    Defined at qepy_common.fpp lines 36-70
    
    """
    def __init__(self, handle=None):
        """
        self = Energies_Base()
        
        
        Defined at qepy_common.fpp lines 36-70
        
        
        Returns
        -------
        this : Energies_Base
        	Object to be constructed
        
        
        Automatically generated constructor for energies_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_energies_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Energies_Base
        
        
        Defined at qepy_common.fpp lines 36-70
        
        Parameters
        ----------
        this : Energies_Base
        	Object to be destructed
        
        
        Automatically generated destructor for energies_base
        """
        if self._alloc:
            _qepy.f90wrap_energies_base_finalise(this=self._handle)
    
    @property
    def etot(self):
        """
        Element etot ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 37
        
        """
        return _qepy.f90wrap_energies_base__get__etot(self._handle)
    
    @etot.setter
    def etot(self, etot):
        _qepy.f90wrap_energies_base__set__etot(self._handle, etot)
    
    @property
    def ek(self):
        """
        Element ek ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 38
        
        """
        return _qepy.f90wrap_energies_base__get__ek(self._handle)
    
    @ek.setter
    def ek(self, ek):
        _qepy.f90wrap_energies_base__set__ek(self._handle, ek)
    
    @property
    def eloc(self):
        """
        Element eloc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 39
        
        """
        return _qepy.f90wrap_energies_base__get__eloc(self._handle)
    
    @eloc.setter
    def eloc(self, eloc):
        _qepy.f90wrap_energies_base__set__eloc(self._handle, eloc)
    
    @property
    def enl(self):
        """
        Element enl ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 40
        
        """
        return _qepy.f90wrap_energies_base__get__enl(self._handle)
    
    @enl.setter
    def enl(self, enl):
        _qepy.f90wrap_energies_base__set__enl(self._handle, enl)
    
    @property
    def ewld(self):
        """
        Element ewld ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 41
        
        """
        return _qepy.f90wrap_energies_base__get__ewld(self._handle)
    
    @ewld.setter
    def ewld(self, ewld):
        _qepy.f90wrap_energies_base__set__ewld(self._handle, ewld)
    
    @property
    def exc(self):
        """
        Element exc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 42
        
        """
        return _qepy.f90wrap_energies_base__get__exc(self._handle)
    
    @exc.setter
    def exc(self, exc):
        _qepy.f90wrap_energies_base__set__exc(self._handle, exc)
    
    @property
    def ehart(self):
        """
        Element ehart ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 43
        
        """
        return _qepy.f90wrap_energies_base__get__ehart(self._handle)
    
    @ehart.setter
    def ehart(self, ehart):
        _qepy.f90wrap_energies_base__set__ehart(self._handle, ehart)
    
    @property
    def fock2(self):
        """
        Element fock2 ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 44
        
        """
        return _qepy.f90wrap_energies_base__get__fock2(self._handle)
    
    @fock2.setter
    def fock2(self, fock2):
        _qepy.f90wrap_energies_base__set__fock2(self._handle, fock2)
    
    @property
    def demet(self):
        """
        Element demet ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 45
        
        """
        return _qepy.f90wrap_energies_base__get__demet(self._handle)
    
    @demet.setter
    def demet(self, demet):
        _qepy.f90wrap_energies_base__set__demet(self._handle, demet)
    
    @property
    def elondon(self):
        """
        Element elondon ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 46
        
        """
        return _qepy.f90wrap_energies_base__get__elondon(self._handle)
    
    @elondon.setter
    def elondon(self, elondon):
        _qepy.f90wrap_energies_base__set__elondon(self._handle, elondon)
    
    @property
    def edftd3(self):
        """
        Element edftd3 ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 47
        
        """
        return _qepy.f90wrap_energies_base__get__edftd3(self._handle)
    
    @edftd3.setter
    def edftd3(self, edftd3):
        _qepy.f90wrap_energies_base__set__edftd3(self._handle, edftd3)
    
    @property
    def exdm(self):
        """
        Element exdm ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 48
        
        """
        return _qepy.f90wrap_energies_base__get__exdm(self._handle)
    
    @exdm.setter
    def exdm(self, exdm):
        _qepy.f90wrap_energies_base__set__exdm(self._handle, exdm)
    
    @property
    def etsvdw(self):
        """
        Element etsvdw ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 49
        
        """
        return _qepy.f90wrap_energies_base__get__etsvdw(self._handle)
    
    @etsvdw.setter
    def etsvdw(self, etsvdw):
        _qepy.f90wrap_energies_base__set__etsvdw(self._handle, etsvdw)
    
    @property
    def eext(self):
        """
        Element eext ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 50
        
        """
        return _qepy.f90wrap_energies_base__get__eext(self._handle)
    
    @eext.setter
    def eext(self, eext):
        _qepy.f90wrap_energies_base__set__eext(self._handle, eext)
    
    @property
    def etotefield(self):
        """
        Element etotefield ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 51
        
        """
        return _qepy.f90wrap_energies_base__get__etotefield(self._handle)
    
    @etotefield.setter
    def etotefield(self, etotefield):
        _qepy.f90wrap_energies_base__set__etotefield(self._handle, etotefield)
    
    @property
    def etotgatefield(self):
        """
        Element etotgatefield ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 52
        
        """
        return _qepy.f90wrap_energies_base__get__etotgatefield(self._handle)
    
    @etotgatefield.setter
    def etotgatefield(self, etotgatefield):
        _qepy.f90wrap_energies_base__set__etotgatefield(self._handle, etotgatefield)
    
    @property
    def eth(self):
        """
        Element eth ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 53
        
        """
        return _qepy.f90wrap_energies_base__get__eth(self._handle)
    
    @eth.setter
    def eth(self, eth):
        _qepy.f90wrap_energies_base__set__eth(self._handle, eth)
    
    @property
    def epaw(self):
        """
        Element epaw ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 54
        
        """
        return _qepy.f90wrap_energies_base__get__epaw(self._handle)
    
    @epaw.setter
    def epaw(self, epaw):
        _qepy.f90wrap_energies_base__set__epaw(self._handle, epaw)
    
    @property
    def ept(self):
        """
        Element ept ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 55
        
        """
        return _qepy.f90wrap_energies_base__get__ept(self._handle)
    
    @ept.setter
    def ept(self, ept):
        _qepy.f90wrap_energies_base__set__ept(self._handle, ept)
    
    @property
    def extene(self):
        """
        Element extene ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 57
        
        """
        return _qepy.f90wrap_energies_base__get__extene(self._handle)
    
    @extene.setter
    def extene(self, extene):
        _qepy.f90wrap_energies_base__set__extene(self._handle, extene)
    
    @property
    def ehf(self):
        """
        Element ehf ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 58
        
        """
        return _qepy.f90wrap_energies_base__get__ehf(self._handle)
    
    @ehf.setter
    def ehf(self, ehf):
        _qepy.f90wrap_energies_base__set__ehf(self._handle, ehf)
    
    @property
    def etxc(self):
        """
        Element etxc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 60
        
        """
        return _qepy.f90wrap_energies_base__get__etxc(self._handle)
    
    @etxc.setter
    def etxc(self, etxc):
        _qepy.f90wrap_energies_base__set__etxc(self._handle, etxc)
    
    @property
    def etxcc(self):
        """
        Element etxcc ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 61
        
        """
        return _qepy.f90wrap_energies_base__get__etxcc(self._handle)
    
    @etxcc.setter
    def etxcc(self, etxcc):
        _qepy.f90wrap_energies_base__set__etxcc(self._handle, etxcc)
    
    @property
    def paw_ehart_ae(self):
        """
        Element paw_ehart_ae ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 62
        
        """
        return _qepy.f90wrap_energies_base__get__paw_ehart_ae(self._handle)
    
    @paw_ehart_ae.setter
    def paw_ehart_ae(self, paw_ehart_ae):
        _qepy.f90wrap_energies_base__set__paw_ehart_ae(self._handle, paw_ehart_ae)
    
    @property
    def paw_ehart_ps(self):
        """
        Element paw_ehart_ps ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 63
        
        """
        return _qepy.f90wrap_energies_base__get__paw_ehart_ps(self._handle)
    
    @paw_ehart_ps.setter
    def paw_ehart_ps(self, paw_ehart_ps):
        _qepy.f90wrap_energies_base__set__paw_ehart_ps(self._handle, paw_ehart_ps)
    
    @property
    def paw_exc_ae(self):
        """
        Element paw_exc_ae ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 64
        
        """
        return _qepy.f90wrap_energies_base__get__paw_exc_ae(self._handle)
    
    @paw_exc_ae.setter
    def paw_exc_ae(self, paw_exc_ae):
        _qepy.f90wrap_energies_base__set__paw_exc_ae(self._handle, paw_exc_ae)
    
    @property
    def paw_exc_ps(self):
        """
        Element paw_exc_ps ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 65
        
        """
        return _qepy.f90wrap_energies_base__get__paw_exc_ps(self._handle)
    
    @paw_exc_ps.setter
    def paw_exc_ps(self, paw_exc_ps):
        _qepy.f90wrap_energies_base__set__paw_exc_ps(self._handle, paw_exc_ps)
    
    def __str__(self):
        ret = ['<energies_base>{\n']
        ret.append('    etot : ')
        ret.append(repr(self.etot))
        ret.append(',\n    ek : ')
        ret.append(repr(self.ek))
        ret.append(',\n    eloc : ')
        ret.append(repr(self.eloc))
        ret.append(',\n    enl : ')
        ret.append(repr(self.enl))
        ret.append(',\n    ewld : ')
        ret.append(repr(self.ewld))
        ret.append(',\n    exc : ')
        ret.append(repr(self.exc))
        ret.append(',\n    ehart : ')
        ret.append(repr(self.ehart))
        ret.append(',\n    fock2 : ')
        ret.append(repr(self.fock2))
        ret.append(',\n    demet : ')
        ret.append(repr(self.demet))
        ret.append(',\n    elondon : ')
        ret.append(repr(self.elondon))
        ret.append(',\n    edftd3 : ')
        ret.append(repr(self.edftd3))
        ret.append(',\n    exdm : ')
        ret.append(repr(self.exdm))
        ret.append(',\n    etsvdw : ')
        ret.append(repr(self.etsvdw))
        ret.append(',\n    eext : ')
        ret.append(repr(self.eext))
        ret.append(',\n    etotefield : ')
        ret.append(repr(self.etotefield))
        ret.append(',\n    etotgatefield : ')
        ret.append(repr(self.etotgatefield))
        ret.append(',\n    eth : ')
        ret.append(repr(self.eth))
        ret.append(',\n    epaw : ')
        ret.append(repr(self.epaw))
        ret.append(',\n    ept : ')
        ret.append(repr(self.ept))
        ret.append(',\n    extene : ')
        ret.append(repr(self.extene))
        ret.append(',\n    ehf : ')
        ret.append(repr(self.ehf))
        ret.append(',\n    etxc : ')
        ret.append(repr(self.etxc))
        ret.append(',\n    etxcc : ')
        ret.append(repr(self.etxcc))
        ret.append(',\n    paw_ehart_ae : ')
        ret.append(repr(self.paw_ehart_ae))
        ret.append(',\n    paw_ehart_ps : ')
        ret.append(repr(self.paw_ehart_ps))
        ret.append(',\n    paw_exc_ae : ')
        ret.append(repr(self.paw_exc_ae))
        ret.append(',\n    paw_exc_ps : ')
        ret.append(repr(self.paw_exc_ps))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

@f90wrap.runtime.register_class("qepy.embed_base")
class embed_base(f90wrap.runtime.FortranDerivedType):
    """
    Type(name=embed_base)
    
    
    Defined at qepy_common.fpp lines 73-102
    
    """
    def __init__(self, handle=None):
        """
        self = Embed_Base()
        
        
        Defined at qepy_common.fpp lines 73-102
        
        
        Returns
        -------
        this : Embed_Base
        	Object to be constructed
        
        
        Automatically generated constructor for embed_base
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _qepy.f90wrap_embed_base_initialise()
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Embed_Base
        
        
        Defined at qepy_common.fpp lines 73-102
        
        Parameters
        ----------
        this : Embed_Base
        	Object to be destructed
        
        
        Automatically generated destructor for embed_base
        """
        if self._alloc:
            _qepy.f90wrap_embed_base_finalise(this=self._handle)
    
    @property
    def input(self):
        """
        Element input ftype=type(input_base) pytype=Input_Base
        
        
        Defined at qepy_common.fpp line 74
        
        """
        input_handle = _qepy.f90wrap_embed_base__get__input(self._handle)
        if tuple(input_handle) in self._objs:
            input = self._objs[tuple(input_handle)]
        else:
            input = input_base.from_handle(input_handle)
            self._objs[tuple(input_handle)] = input
        return input
    
    @input.setter
    def input(self, input):
        input = input._handle
        _qepy.f90wrap_embed_base__set__input(self._handle, input)
    
    @property
    def tddft(self):
        """
        Element tddft ftype=type(tddft_base) pytype=Tddft_Base
        
        
        Defined at qepy_common.fpp line 75
        
        """
        tddft_handle = _qepy.f90wrap_embed_base__get__tddft(self._handle)
        if tuple(tddft_handle) in self._objs:
            tddft = self._objs[tuple(tddft_handle)]
        else:
            tddft = tddft_base.from_handle(tddft_handle)
            self._objs[tuple(tddft_handle)] = tddft
        return tddft
    
    @tddft.setter
    def tddft(self, tddft):
        tddft = tddft._handle
        _qepy.f90wrap_embed_base__set__tddft(self._handle, tddft)
    
    @property
    def energies(self):
        """
        Element energies ftype=type(energies_base) pytype=Energies_Base
        
        
        Defined at qepy_common.fpp line 76
        
        """
        energies_handle = _qepy.f90wrap_embed_base__get__energies(self._handle)
        if tuple(energies_handle) in self._objs:
            energies = self._objs[tuple(energies_handle)]
        else:
            energies = energies_base.from_handle(energies_handle)
            self._objs[tuple(energies_handle)] = energies
        return energies
    
    @energies.setter
    def energies(self, energies):
        energies = energies._handle
        _qepy.f90wrap_embed_base__set__energies(self._handle, energies)
    
    @property
    def extpot(self):
        """
        Element extpot ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 77
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_embed_base__array__extpot(self._handle)
        if array_handle in self._arrays:
            extpot = self._arrays[array_handle]
        else:
            extpot = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_embed_base__array__extpot)
            self._arrays[array_handle] = extpot
        return extpot
    
    @extpot.setter
    def extpot(self, extpot):
        self.extpot[...] = extpot
    
    @property
    def extene(self):
        """
        Element extene ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 78
        
        """
        return _qepy.f90wrap_embed_base__get__extene(self._handle)
    
    @extene.setter
    def extene(self, extene):
        _qepy.f90wrap_embed_base__set__extene(self._handle, extene)
    
    @property
    def exttype(self):
        """
        Element exttype ftype=integer                          pytype=int
        
        
        Defined at qepy_common.fpp line 79
        
        """
        return _qepy.f90wrap_embed_base__get__exttype(self._handle)
    
    @exttype.setter
    def exttype(self, exttype):
        _qepy.f90wrap_embed_base__set__exttype(self._handle, exttype)
    
    @property
    def extforces(self):
        """
        Element extforces ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 80
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_embed_base__array__extforces(self._handle)
        if array_handle in self._arrays:
            extforces = self._arrays[array_handle]
        else:
            extforces = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_embed_base__array__extforces)
            self._arrays[array_handle] = extforces
        return extforces
    
    @extforces.setter
    def extforces(self, extforces):
        self.extforces[...] = extforces
    
    @property
    def extstress(self):
        """
        Element extstress ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 81
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _qepy.f90wrap_embed_base__array__extstress(self._handle)
        if array_handle in self._arrays:
            extstress = self._arrays[array_handle]
        else:
            extstress = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _qepy.f90wrap_embed_base__array__extstress)
            self._arrays[array_handle] = extstress
        return extstress
    
    @extstress.setter
    def extstress(self, extstress):
        self.extstress[...] = extstress
    
    @property
    def initial(self):
        """
        Element initial ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 82
        
        """
        return _qepy.f90wrap_embed_base__get__initial(self._handle)
    
    @initial.setter
    def initial(self, initial):
        _qepy.f90wrap_embed_base__set__initial(self._handle, initial)
    
    @property
    def mix_coef(self):
        """
        Element mix_coef ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 83
        
        """
        return _qepy.f90wrap_embed_base__get__mix_coef(self._handle)
    
    @mix_coef.setter
    def mix_coef(self, mix_coef):
        _qepy.f90wrap_embed_base__set__mix_coef(self._handle, mix_coef)
    
    @property
    def finish(self):
        """
        Element finish ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 84
        
        """
        return _qepy.f90wrap_embed_base__get__finish(self._handle)
    
    @finish.setter
    def finish(self, finish):
        _qepy.f90wrap_embed_base__set__finish(self._handle, finish)
    
    @property
    def etotal(self):
        """
        Element etotal ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 85
        
        """
        return _qepy.f90wrap_embed_base__get__etotal(self._handle)
    
    @etotal.setter
    def etotal(self, etotal):
        _qepy.f90wrap_embed_base__set__etotal(self._handle, etotal)
    
    @property
    def dnorm(self):
        """
        Element dnorm ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 86
        
        """
        return _qepy.f90wrap_embed_base__get__dnorm(self._handle)
    
    @dnorm.setter
    def dnorm(self, dnorm):
        _qepy.f90wrap_embed_base__set__dnorm(self._handle, dnorm)
    
    @property
    def lewald(self):
        """
        Element lewald ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 87
        
        """
        return _qepy.f90wrap_embed_base__get__lewald(self._handle)
    
    @lewald.setter
    def lewald(self, lewald):
        _qepy.f90wrap_embed_base__set__lewald(self._handle, lewald)
    
    @property
    def nlpp(self):
        """
        Element nlpp ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 88
        
        """
        return _qepy.f90wrap_embed_base__get__nlpp(self._handle)
    
    @nlpp.setter
    def nlpp(self, nlpp):
        _qepy.f90wrap_embed_base__set__nlpp(self._handle, nlpp)
    
    @property
    def diag_conv(self):
        """
        Element diag_conv ftype=real(kind=dp) pytype=float
        
        
        Defined at qepy_common.fpp line 89
        
        """
        return _qepy.f90wrap_embed_base__get__diag_conv(self._handle)
    
    @diag_conv.setter
    def diag_conv(self, diag_conv):
        _qepy.f90wrap_embed_base__set__diag_conv(self._handle, diag_conv)
    
    @property
    def ldescf(self):
        """
        Element ldescf ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 90
        
        """
        return _qepy.f90wrap_embed_base__get__ldescf(self._handle)
    
    @ldescf.setter
    def ldescf(self, ldescf):
        _qepy.f90wrap_embed_base__set__ldescf(self._handle, ldescf)
    
    @property
    def iterative(self):
        """
        Element iterative ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 92
        
        """
        return _qepy.f90wrap_embed_base__get__iterative(self._handle)
    
    @iterative.setter
    def iterative(self, iterative):
        _qepy.f90wrap_embed_base__set__iterative(self._handle, iterative)
    
    @property
    def lmovecell(self):
        """
        Element lmovecell ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 94
        
        """
        return _qepy.f90wrap_embed_base__get__lmovecell(self._handle)
    
    @lmovecell.setter
    def lmovecell(self, lmovecell):
        _qepy.f90wrap_embed_base__set__lmovecell(self._handle, lmovecell)
    
    @property
    def oldxml(self):
        """
        Element oldxml ftype=logical pytype=bool
        
        
        Defined at qepy_common.fpp line 96
        
        """
        return _qepy.f90wrap_embed_base__get__oldxml(self._handle)
    
    @oldxml.setter
    def oldxml(self, oldxml):
        _qepy.f90wrap_embed_base__set__oldxml(self._handle, oldxml)
    
    def __str__(self):
        ret = ['<embed_base>{\n']
        ret.append('    input : ')
        ret.append(repr(self.input))
        ret.append(',\n    tddft : ')
        ret.append(repr(self.tddft))
        ret.append(',\n    energies : ')
        ret.append(repr(self.energies))
        ret.append(',\n    extpot : ')
        ret.append(repr(self.extpot))
        ret.append(',\n    extene : ')
        ret.append(repr(self.extene))
        ret.append(',\n    exttype : ')
        ret.append(repr(self.exttype))
        ret.append(',\n    extforces : ')
        ret.append(repr(self.extforces))
        ret.append(',\n    extstress : ')
        ret.append(repr(self.extstress))
        ret.append(',\n    initial : ')
        ret.append(repr(self.initial))
        ret.append(',\n    mix_coef : ')
        ret.append(repr(self.mix_coef))
        ret.append(',\n    finish : ')
        ret.append(repr(self.finish))
        ret.append(',\n    etotal : ')
        ret.append(repr(self.etotal))
        ret.append(',\n    dnorm : ')
        ret.append(repr(self.dnorm))
        ret.append(',\n    lewald : ')
        ret.append(repr(self.lewald))
        ret.append(',\n    nlpp : ')
        ret.append(repr(self.nlpp))
        ret.append(',\n    diag_conv : ')
        ret.append(repr(self.diag_conv))
        ret.append(',\n    ldescf : ')
        ret.append(repr(self.ldescf))
        ret.append(',\n    iterative : ')
        ret.append(repr(self.iterative))
        ret.append(',\n    lmovecell : ')
        ret.append(repr(self.lmovecell))
        ret.append(',\n    oldxml : ')
        ret.append(repr(self.oldxml))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qepy_common".')

for func in _dt_array_initialisers:
    func()
