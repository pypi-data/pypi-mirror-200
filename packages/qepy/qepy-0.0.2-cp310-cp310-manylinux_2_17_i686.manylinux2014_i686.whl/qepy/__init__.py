from __future__ import print_function, absolute_import, division
# Fix
# MPI_IN_PLACE and MKL
import sys, os
from ctypes import util, CDLL, RTLD_LOCAL, RTLD_GLOBAL
if 'mpi4py' in sys.modules :
    if hasattr(util, '_findLib_ld') and hasattr(util, '_get_soname') :
        mpilib = util._get_soname(util._findLib_ld('mpi'))
    else :
        mpilib = None
    mpilib = mpilib or util.find_library('mpi') or util.find_library('mpifort')
    try:
        CDLL(mpilib, RTLD_LOCAL | RTLD_GLOBAL)
    except Exception :
        pass
try:
    if hasattr(util, '_findLib_ld'):
        mkllib = os.path.basename(util._findLib_ld('mkl_rt'))
    else :
        mkllib = util.find_library('mkl_rt')
    CDLL(mkllib, RTLD_LOCAL | RTLD_GLOBAL)
except Exception :
    pass

# control the output
import types
from .core import Logger, env
class QEpyLib :
    def __init__(self, **kwargs):
        import _qepy as qepylib
        sys.modules['_qepy'] = self
        self.qepylib =qepylib

    def __getattr__(self, attr):
        attr_value = getattr(self.qepylib, attr)
        if '__array__' not in attr :
            attr_value = Logger.stdout2file(attr_value, fileobj=env['STDOUT'])
        return attr_value
qepylib = QEpyLib()
# End fix
import _qepy
import f90wrap.runtime
import logging
import numpy
import qepy.mp_pools
import qepy.fixed_occ
import qepy.io_global
import qepy.us
import qepy.extrapolation
import qepy.uspp
import qepy.ener
import qepy.qepy_scatter_mod
import qepy.mp_orthopools
import qepy.constants
import qepy.rap_point_group
import qepy.oldxml_io_rho_xml
import qepy.read_input
import qepy.mp_bands_tddfpt
import qepy.basis
import qepy.control_flags
import qepy.wavefunctions
import qepy.scf
import qepy.mp_world
import qepy.check_stop
import qepy.force_mod
import qepy.mp_global
import qepy.oldxml_xml_io_base
import qepy.environment
import qepy.gvecs
import qepy.rap_point_group_so
import qepy.relax
import qepy.uspp_param
import qepy.klist
import qepy.funct
import qepy.pwcom
import qepy.mp_diag
import qepy.qepy_api
import qepy.ions_base
import qepy.vlocal
import qepy.oldxml_pw_restart
import qepy.oldxml_qexml_module
import qepy.cellmd
import qepy.qepy_pw_restart_new
import qepy.lsda_mod
import qepy.spin_orb
import qepy.qepy_mod
import qepy.rap_point_group_is
import qepy.qepy_common
import qepy.gvect
import qepy.cell_base
import qepy.qexsd_module
import qepy.mp_bands
import qepy.wvfct

def impose_deviatoric_strain(at_old, at):
    """
    impose_deviatoric_strain(at_old, at)
    
    
    Defined at deviatoric.fpp lines 14-35
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
         Impose a pure deviatoric(volume-conserving) deformation
         Needed to enforce volume conservation in variable-cell MD/optimization
    """
    _qepy.f90wrap_impose_deviatoric_strain(at_old=at_old, at=at)

def impose_deviatoric_strain_2d(at_old, at):
    """
    impose_deviatoric_strain_2d(at_old, at)
    
    
    Defined at deviatoric.fpp lines 39-62
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
         Modif. of impose_deviatoric_strain but for
         Area conserving deformation(2DSHAPE) added by Richard Charles Andrew
         Physics Department, University if Pretoria,
         South Africa, august 2012
    """
    _qepy.f90wrap_impose_deviatoric_strain_2d(at_old=at_old, at=at)

def impose_deviatoric_stress(sigma):
    """
    impose_deviatoric_stress(sigma)
    
    
    Defined at deviatoric.fpp lines 66-80
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
         Impose a pure deviatoric stress
    """
    _qepy.f90wrap_impose_deviatoric_stress(sigma=sigma)

def impose_deviatoric_stress_2d(sigma):
    """
    impose_deviatoric_stress_2d(sigma)
    
    
    Defined at deviatoric.fpp lines 84-99
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
         Modif. of impose_deviatoric_stress but for
         Area conserving deformation(2DSHAPE) added by Richard Charles Andrew
         Physics Department, University if Pretoria,
         South Africa, august 2012
    """
    _qepy.f90wrap_impose_deviatoric_stress_2d(sigma=sigma)

def read_file():
    """
    read_file()
    
    
    Defined at read_file_new.fpp lines 13-61
    
    
    ----------------------------------------------------------------------------
     Wrapper routine, for backwards compatibility
    """
    _qepy.f90wrap_read_file()

def read_file_new(needwf):
    """
    read_file_new(needwf)
    
    
    Defined at read_file_new.fpp lines 65-123
    
    Parameters
    ----------
    needwf : bool
    
    ----------------------------------------------------------------------------
     Reads xml data file produced by pw.x or cp.x, performs initializations
     related to the contents of the xml file
     If needwf=.t. performs wavefunction-related initialization as well
     Does not read wfcs but returns in "wfc_is_collected" info on the wfc file
    """
    _qepy.f90wrap_read_file_new(needwf=needwf)

def post_xml_init():
    """
    post_xml_init()
    
    
    Defined at read_file_new.fpp lines 126-301
    
    
    ----------------------------------------------------------------------------
     ... Various initializations needed to start a calculation:
     ... pseudopotentials, G vectors, FFT arrays, rho, potential
    """
    _qepy.f90wrap_post_xml_init()

def punch(what):
    """
    punch(what)
    
    
    Defined at punch.fpp lines 13-135
    
    Parameters
    ----------
    what : str
    
    ----------------------------------------------------------------------------
     This routine is called at the end of the run to save on a file
     the information needed for further processing(phonon etc.).
     * what = 'all' : write xml data file, charge density, wavefunctions
    (for final data);
     * what = 'config' : write xml data file and charge density; also,
                         for nks=1, wavefunctions in plain binary format
    (see why in comments below). For intermediate
                         or incomplete results;
     * what = 'config-nowf' : write xml data file iand charge density only
     * what = 'config-init' : write xml data file only excluding final results
    (for dry run, can be called at early stages).
    """
    _qepy.f90wrap_punch(what=what)

def close_files(lflag):
    """
    close_files(lflag)
    
    
    Defined at close_files.fpp lines 13-86
    
    Parameters
    ----------
    lflag : bool
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes for a new scf calculation.
    """
    _qepy.f90wrap_close_files(lflag=lflag)

def stress(sigma):
    """
    stress(sigma)
    
    
    Defined at stress.fpp lines 14-261
    
    Parameters
    ----------
    sigma : float array
    
    ----------------------------------------------------------------------
     Computes the total stress.
    """
    _qepy.f90wrap_stress(sigma=sigma)

def electrons():
    """
    electrons()
    
    
    Defined at electrons.fpp lines 18-344
    
    
    ----------------------------------------------------------------------------
     General self-consistency loop, also for hybrid functionals
     For non-hybrid functionals it just calls "electron_scf"
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%  Iterate hybrid functional  %%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    _qepy.f90wrap_electrons()

def electrons_scf(printout, exxen):
    """
    electrons_scf(printout, exxen)
    
    
    Defined at electrons.fpp lines 348-1362
    
    Parameters
    ----------
    printout : int
    exxen : float
    
    ----------------------------------------------------------------------------
     This routine is a driver of the self-consistent cycle.
     It uses the routine c_bands for computing the bands at fixed
     Hamiltonian, the routine sum_band to compute the charge density,
     the routine v_of_rho to compute the new potential and the routine
     mix_rho to mix input and output charge densities.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%          iterate
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    _qepy.f90wrap_electrons_scf(printout=printout, exxen=exxen)

def exxenergyace():
    """
    exxenergyace = exxenergyace()
    
    
    Defined at electrons.fpp lines 1366-1411
    
    
    Returns
    -------
    exxenergyace : float
    
    --------------------------------------------------------------------------
     Compute exchange energy using ACE
    """
    exxenergyace = _qepy.f90wrap_exxenergyace()
    return exxenergyace

def scale_h():
    """
    scale_h()
    
    
    Defined at scale_h.fpp lines 14-105
    
    
    -----------------------------------------------------------------------
     When variable cell calculation are performed this routine scales the
     quantities needed in the calculation of the hamiltonian using the
     new and old cell parameters.
    """
    _qepy.f90wrap_scale_h()

def pw2casino(istep):
    """
    pw2casino(istep)
    
    
    Defined at pw2casino.fpp lines 16-90
    
    Parameters
    ----------
    istep : int
    
    ----------------------------------------------------------------------------
    """
    _qepy.f90wrap_pw2casino(istep=istep)

def forces():
    """
    forces()
    
    
    Defined at forces.fpp lines 18-417
    
    
    ----------------------------------------------------------------------------
     This routine is a driver routine which computes the forces
     acting on the atoms. The complete expression of the forces
     contains four parts which are computed by different routines:
      a)  force_lc,     local contribution to the forces
      b)  force_cc,     contribution due to NLCC
      c)  force_ew,     contribution due to the electrostatic ewald term
      d)  force_us,     contribution due to the non-local potential
      e)  force_corr,   correction term for incomplete self-consistency
      f)  force_hub,    contribution due to the Hubbard term
      g)  force_london, semi-empirical correction for dispersion forces
      h)  force_d3,     Grimme-D3(DFT-D3) correction to dispersion forces
    """
    _qepy.f90wrap_forces()

def move_ions(idone, ions_status):
    """
    move_ions(idone, ions_status)
    
    
    Defined at move_ions.fpp lines 13-362
    
    Parameters
    ----------
    idone : int
    ions_status : int
    
    ----------------------------------------------------------------------------
     Perform a ionic step, according to the requested scheme:
     * lbfgs: bfgs minimizations
     * lmd: molecular dynamics( all kinds )
     Additional variables affecting the calculation:
     * lmovecell: Variable-cell calculation
     * calc: type of MD
     * lconstrain: constrained MD
     * "idone" is the counter on ionic moves, "nstep" their total number
     * "istep" contains the number of all steps including previous runs.
     Coefficients for potential and wavefunctions extrapolation are
     no longer computed here but in update_pot.
    """
    _qepy.f90wrap_move_ions(idone=idone, ions_status=ions_status)

def add_qexsd_step(i_step):
    """
    add_qexsd_step(i_step)
    
    
    Defined at add_qexsd_step.fpp lines 17-103
    
    Parameters
    ----------
    i_step : int
    
    -----------------------------------------------------------------
    ------------------------------------------------------------------------
           START_GLOBAL_VARIABLES( INTENT(IN) )
    --------------------------------------------------------------------------
    """
    _qepy.f90wrap_add_qexsd_step(i_step=i_step)

def hinit1():
    """
    hinit1()
    
    
    Defined at hinit1.fpp lines 13-86
    
    
    ----------------------------------------------------------------------------
     Atomic configuration dependent hamiltonian initialization,
     potential, wavefunctions for Hubbard U.
     Important note: it does not recompute structure factors and core charge,
     they must be computed before this routine is called.
    """
    _qepy.f90wrap_hinit1()

def run_pwscf():
    """
    exit_status = run_pwscf()
    
    
    Defined at run_pwscf.fpp lines 13-289
    
    
    Returns
    -------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Author: Paolo Giannozzi
     License: GNU
     Summary: Run an instance of the Plane Wave Self-Consistent Field code
     Run an instance of the Plane Wave Self-Consistent Field code
     MPI initialization and input data reading is performed in the
     calling code - returns in exit_status the exit code for pw.x,
     returned in the shell. Values are:
     * 0: completed successfully
     * 1: an error has occurred(value returned by the errore() routine)
     * 2-127: convergence error
        * 2: scf convergence error
        * 3: ion convergence error
     * 128-255: code exited due to specific trigger
        * 255: exit due to user request, or signal trapped,
              or time > max_seconds
    (note: in the future, check_stop_now could also return a value
         to specify the reason of exiting, and the value could be used
         to return a different value for different reasons)
     @Note
     10/01/17 Samuel Ponce: Add Ford documentation
     @endnote
    """
    exit_status = _qepy.f90wrap_run_pwscf()
    return exit_status

def reset_gvectors():
    """
    reset_gvectors()
    
    
    Defined at run_pwscf.fpp lines 294-334
    
    
    -------------------------------------------------------------
     Prepare a new scf calculation with newly recomputed grids,
     restarting from scratch, not from available data of previous
     steps(dimensions and file lengths will be different in general)
     Useful as a check of variable-cell optimization:
     once convergence is achieved, compare the final energy with the
     energy computed with G-vectors and plane waves for the final cell
    """
    _qepy.f90wrap_reset_gvectors()

def reset_exx():
    """
    reset_exx()
    
    
    Defined at run_pwscf.fpp lines 339-363
    
    
    -------------------------------------------------------------
    """
    _qepy.f90wrap_reset_exx()

def reset_magn():
    """
    reset_magn()
    
    
    Defined at run_pwscf.fpp lines 368-394
    
    
    ----------------------------------------------------------------
     LSDA optimization: a final configuration with zero
     absolute magnetization has been found and we check
     if it is really the minimum energy structure by
     performing a new scf iteration without any "electronic" history.
    """
    _qepy.f90wrap_reset_magn()

def reset_starting_magnetization():
    """
    reset_starting_magnetization()
    
    
    Defined at run_pwscf.fpp lines 399-483
    
    
    -------------------------------------------------------------------
     On input, the scf charge density is needed.
     On output, new values for starting_magnetization, angle1, angle2
     estimated from atomic magnetic moments - to be used in last step.
    """
    _qepy.f90wrap_reset_starting_magnetization()

def stop_run(exit_status):
    """
    stop_run(exit_status)
    
    
    Defined at stop_run.fpp lines 13-59
    
    Parameters
    ----------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping:
     * exit_status = 0: successfull execution, remove temporary files;
     * exit_status =-1: code stopped by user request;
     * exit_status = 1: convergence not achieved.
     Do not remove temporary files needed for restart.
    """
    _qepy.f90wrap_stop_run(exit_status=exit_status)

def do_stop(exit_status):
    """
    do_stop(exit_status)
    
    
    Defined at stop_run.fpp lines 63-93
    
    Parameters
    ----------
    exit_status : int
    
    ---------------------------------------
     Stop the run.
    """
    _qepy.f90wrap_do_stop(exit_status=exit_status)

def closefile():
    """
    closefile()
    
    
    Defined at stop_run.fpp lines 97-108
    
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping.
     Called by "sigcatch" when it receives a signal.
    """
    _qepy.f90wrap_closefile()

def sum_band():
    """
    sum_band()
    
    
    Defined at sum_band.fpp lines 14-818
    
    
    ----------------------------------------------------------------------------
     ... Calculates the symmetrized charge density and related quantities
     ... Also computes the occupations and the sum of occupied eigenvalues.
    """
    _qepy.f90wrap_sum_band()

def sum_bec(ik, current_spin, ibnd_start, ibnd_end, this_bgrp_nbnd):
    """
    sum_bec(ik, current_spin, ibnd_start, ibnd_end, this_bgrp_nbnd)
    
    
    Defined at sum_band.fpp lines 821-1053
    
    Parameters
    ----------
    ik : int
    current_spin : int
    ibnd_start : int
    ibnd_end : int
    this_bgrp_nbnd : int
    
    ----------------------------------------------------------------------------
     This routine computes the sum over bands
         \sum_i <\psi_i|\beta_l>w_i<\beta_m|\psi_i>
     for point "ik" and, for LSDA, spin "current_spin"
     Calls calbec to compute "becp"=<beta_m|psi_i>
     Output is accumulated(unsymmetrized) into "becsum", module "uspp"
     Routine used in sum_band(if okvan) and in compute_becsum, called by hinit1(if \
         okpaw)
    """
    _qepy.f90wrap_sum_bec(ik=ik, current_spin=current_spin, ibnd_start=ibnd_start, \
        ibnd_end=ibnd_end, this_bgrp_nbnd=this_bgrp_nbnd)

def add_becsum_nc(na, np, becsum_nc, becsum):
    """
    add_becsum_nc(na, np, becsum_nc, becsum)
    
    
    Defined at sum_band.fpp lines 1057-1102
    
    Parameters
    ----------
    na : int
    np : int
    becsum_nc : complex array
    becsum : float array
    
    ----------------------------------------------------------------------------
     This routine multiplies becsum_nc by the identity and the Pauli matrices,
     saves it in becsum for the calculation of augmentation charge and
     magnetization.
    """
    _qepy.f90wrap_add_becsum_nc(na=na, np=np, becsum_nc=becsum_nc, becsum=becsum)

def add_becsum_so(na, np, becsum_nc, becsum):
    """
    add_becsum_so(na, np, becsum_nc, becsum)
    
    
    Defined at sum_band.fpp lines 1106-1169
    
    Parameters
    ----------
    na : int
    np : int
    becsum_nc : complex array
    becsum : float array
    
    ----------------------------------------------------------------------------
     This routine multiplies becsum_nc by the identity and the Pauli matrices,
     rotates it as appropriate for the spin-orbit case, saves it in becsum
     for the calculation of augmentation charge and magnetization.
    """
    _qepy.f90wrap_add_becsum_so(na=na, np=np, becsum_nc=becsum_nc, becsum=becsum)

def non_scf():
    """
    non_scf()
    
    
    Defined at non_scf.fpp lines 14-114
    
    
    -----------------------------------------------------------------------
     Diagonalization of the KS hamiltonian in the non-scf case.
    """
    _qepy.f90wrap_non_scf()

def laxlib_free_ortho_group():
    """
    laxlib_free_ortho_group()
    
    
    Defined at la_helper.fpp lines 6-12
    
    
    ----------------------------------------------------------------------------
    """
    _qepy.f90wrap_laxlib_free_ortho_group()

def set_mpi_comm_4_solvers(parent_comm, intra_bgrp_comm_, inter_bgrp_comm_):
    """
    set_mpi_comm_4_solvers(parent_comm, intra_bgrp_comm_, inter_bgrp_comm_)
    
    
    Defined at set_mpi_comm_4_solvers.fpp lines 13-37
    
    Parameters
    ----------
    parent_comm : int
    intra_bgrp_comm_ : int
    inter_bgrp_comm_ : int
    
    ----------------------------------------------------------------------------
    """
    _qepy.f90wrap_set_mpi_comm_4_solvers(parent_comm=parent_comm, \
        intra_bgrp_comm_=intra_bgrp_comm_, inter_bgrp_comm_=inter_bgrp_comm_)

def oldxml_wfcinit(starting=None):
    """
    oldxml_wfcinit([starting])
    
    
    Defined at oldxml_wfcinit.fpp lines 14-178
    
    Parameters
    ----------
    starting : str
    
    ----------------------------------------------------------------------------
     ... This routine computes an estimate of the starting wavefunctions
     ... from superposition of atomic wavefunctions and/or random wavefunctions.
     ... It also open needed files or memory buffers
    """
    _qepy.f90wrap_oldxml_wfcinit(starting=starting)

def oldxml_potinit(starting=None):
    """
    oldxml_potinit([starting])
    
    
    Defined at oldxml_potinit.fpp lines 14-257
    
    Parameters
    ----------
    starting : str
    
    ----------------------------------------------------------------------------
     ... This routine initializes the self consistent potential in the array
     ... vr. There are three possible cases:
     ... a) the code is restarting from a broken run:
     ...    read rho from data stored during the previous run
     ... b) the code is performing a non-scf calculation following a scf one:
     ...    read rho from the file produced by the scf calculation
     ... c) the code starts a new calculation:
     ...    calculate rho as a sum of atomic charges
     ... In all cases the scf potential is recalculated and saved in vr
    """
    _qepy.f90wrap_oldxml_potinit(starting=starting)

def oldxml_nc_magnetization_from_lsda(nnr, nspin, rho):
    """
    oldxml_nc_magnetization_from_lsda(nnr, nspin, rho)
    
    
    Defined at oldxml_potinit.fpp lines 261-298
    
    Parameters
    ----------
    nnr : int
    nspin : int
    rho : float array
    
    -------------
    """
    _qepy.f90wrap_oldxml_nc_magnetization_from_lsda(nnr=nnr, nspin=nspin, rho=rho)

def oldxml_read_file():
    """
    oldxml_read_file()
    
    
    Defined at oldxml_read_file.fpp lines 18-187
    
    
    ----------------------------------------------------------------------------
     Wrapper routine, for compatibility
    """
    _qepy.f90wrap_oldxml_read_file()

def oldxml_read_xml_file():
    """
    oldxml_read_xml_file()
    
    
    Defined at oldxml_read_file.fpp lines 190-192
    
    
    """
    _qepy.f90wrap_oldxml_read_xml_file()

def oldxml_read_xml_file_nobs():
    """
    oldxml_read_xml_file_nobs()
    
    
    Defined at oldxml_read_file.fpp lines 194-196
    
    
    """
    _qepy.f90wrap_oldxml_read_xml_file_nobs()

def oldxml_read_xml_file_internal(withbs):
    """
    oldxml_read_xml_file_internal(withbs)
    
    
    Defined at oldxml_read_file.fpp lines 199-502
    
    Parameters
    ----------
    withbs : bool
    
    ----------------------------------------------------------------------------
     ... This routine allocates space for all quantities already computed
     ... in the pwscf program and reads them from the data file.
     ... All quantities that are initialized in subroutine "setup" when
     ... starting from scratch should be initialized here when restarting
    """
    _qepy.f90wrap_oldxml_read_xml_file_internal(withbs=withbs)

def qepy_setlocal(exttype=None):
    """
    qepy_setlocal([exttype])
    
    
    Defined at qepy_setlocal.fpp lines 18-139
    
    Parameters
    ----------
    exttype : int
    
    ----------------------------------------------------------------------
     This routine computes the local potential in real space vltot(ir).
    """
    _qepy.f90wrap_qepy_setlocal(exttype=exttype)

def qepy_v_of_rho_all(self, rho_core, rhog_core, etotefield, v, embed):
    """
    ehart, etxc, vtxc, eth, charge = qepy_v_of_rho_all(self, rho_core, rhog_core, \
        etotefield, v, embed)
    
    
    Defined at qepy_v_of_rho.fpp lines 14-101
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etotefield : float
    v : Scf_Type
    embed : Embed_Base
    
    Returns
    -------
    ehart : float
    etxc : float
    vtxc : float
    eth : float
    charge : float
    
    ----------------------------------------------------------------------------
     This routine computes the Hartree and Exchange and Correlation
     potential and energies which corresponds to a given charge density
     The XC potential is computed in real space, while the
     Hartree potential is computed in reciprocal space.
    """
    ehart, etxc, vtxc, eth, charge = \
        _qepy.f90wrap_qepy_v_of_rho_all(rho=self._handle, rho_core=rho_core, \
        rhog_core=rhog_core, etotefield=etotefield, v=v._handle, \
        embed=embed._handle)
    return ehart, etxc, vtxc, eth, charge

def qepy_v_of_rho(self, rho_core, rhog_core, etotefield, v, embed):
    """
    ehart, etxc, vtxc, eth, charge = qepy_v_of_rho(self, rho_core, rhog_core, \
        etotefield, v, embed)
    
    
    Defined at qepy_v_of_rho.fpp lines 105-212
    
    Parameters
    ----------
    rho : Scf_Type
    rho_core : float array
    rhog_core : complex array
    etotefield : float
    v : Scf_Type
    embed : Embed_Base
    
    Returns
    -------
    ehart : float
    etxc : float
    vtxc : float
    eth : float
    charge : float
    
    ----------------------------------------------------------------------------
     This routine computes the Hartree and Exchange and Correlation
     potential and energies which corresponds to a given charge density
     The XC potential is computed in real space, while the
     Hartree potential is computed in reciprocal space.
    """
    ehart, etxc, vtxc, eth, charge = _qepy.f90wrap_qepy_v_of_rho(rho=self._handle, \
        rho_core=rho_core, rhog_core=rhog_core, etotefield=etotefield, v=v._handle, \
        embed=embed._handle)
    return ehart, etxc, vtxc, eth, charge

def qepy_calc_energies(self):
    """
    qepy_calc_energies(self)
    
    
    Defined at qepy_pw2casino_write.fpp lines 298-780
    
    Parameters
    ----------
    embed : Embed_Base
    
    """
    _qepy.f90wrap_qepy_calc_energies(embed=self._handle)

def qepy_hinit1(exttype):
    """
    qepy_hinit1(exttype)
    
    
    Defined at qepy_hinit1.fpp lines 13-88
    
    Parameters
    ----------
    exttype : int
    
    ----------------------------------------------------------------------------
     Atomic configuration dependent hamiltonian initialization,
     potential, wavefunctions for Hubbard U.
     Important note: it does not recompute structure factors and core charge,
     they must be computed before this routine is called.
    """
    _qepy.f90wrap_qepy_hinit1(exttype=exttype)

def qepy_potinit(starting=None):
    """
    qepy_potinit([starting])
    
    
    Defined at qepy_potinit.fpp lines 14-252
    
    Parameters
    ----------
    starting : str
    
    ----------------------------------------------------------------------------
     ... This routine initializes the self consistent potential in the array
     ... vr. There are three possible cases:
     ... a) the code is restarting from a broken run:
     ...    read rho from data stored during the previous run
     ... b) the code is performing a non-scf calculation following a scf one:
     ...    read rho from the file produced by the scf calculation
     ... c) the code starts a new calculation:
     ...    calculate rho as a sum of atomic charges
     ... In all cases the scf potential is recalculated and saved in vr
    """
    _qepy.f90wrap_qepy_potinit(starting=starting)

def qepy_wfcinit(starting=None):
    """
    qepy_wfcinit([starting])
    
    
    Defined at qepy_wfcinit.fpp lines 14-185
    
    Parameters
    ----------
    starting : str
    
    ----------------------------------------------------------------------------
     ... This routine computes an estimate of the starting wavefunctions
     ... from superposition of atomic wavefunctions and/or random wavefunctions.
     ... It also open needed files or memory buffers
    """
    _qepy.f90wrap_qepy_wfcinit(starting=starting)

def qepy_init_run(oldxml=None):
    """
    qepy_init_run([oldxml])
    
    
    Defined at qepy_init_run.fpp lines 13-152
    
    Parameters
    ----------
    oldxml : bool
    
    ----------------------------------------------------------------------------
    """
    _qepy.f90wrap_qepy_init_run(oldxml=oldxml)

def qepy_pwscf(infile, my_world_comm=None, oldxml=None, embed=None):
    """
    qepy_pwscf(infile[, my_world_comm, oldxml, embed])
    
    
    Defined at qepy_pwscf.fpp lines 13-142
    
    Parameters
    ----------
    infile : str
    my_world_comm : int
    oldxml : bool
    embed : Embed_Base
    
    """
    _qepy.f90wrap_qepy_pwscf(infile=infile, my_world_comm=my_world_comm, \
        oldxml=oldxml, embed=None if embed is None else embed._handle)

def qepy_pwscf_finalise():
    """
    qepy_pwscf_finalise()
    
    
    Defined at qepy_pwscf.fpp lines 145-150
    
    
    """
    _qepy.f90wrap_qepy_pwscf_finalise()

def qepy_initial(self=None):
    """
    qepy_initial([self])
    
    
    Defined at qepy_pwscf.fpp lines 152-189
    
    Parameters
    ----------
    input : Input_Base
    
    """
    _qepy.f90wrap_qepy_initial(input=None if self is None else self._handle)

def qepy_finalise_end(self=None):
    """
    qepy_finalise_end([self])
    
    
    Defined at qepy_pwscf.fpp lines 191-203
    
    Parameters
    ----------
    input : Input_Base
    
    """
    _qepy.f90wrap_qepy_finalise_end(input=None if self is None else self._handle)

def qepy_run_pwscf(oldxml=None, embed=None):
    """
    exit_status = qepy_run_pwscf([oldxml, embed])
    
    
    Defined at qepy_run_pwscf.fpp lines 13-315
    
    Parameters
    ----------
    oldxml : bool
    embed : Embed_Base
    
    Returns
    -------
    exit_status : int
    
    ----------------------------------------------------------------------------
     Author: Paolo Giannozzi
     License: GNU
     Summary: Run an instance of the Plane Wave Self-Consistent Field code
     Run an instance of the Plane Wave Self-Consistent Field code
     MPI initialization and input data reading is performed in the
     calling code - returns in exit_status the exit code for pw.x,
     returned in the shell. Values are:
     * 0: completed successfully
     * 1: an error has occurred(value returned by the errore() routine)
     * 2-127: convergence error
        * 2: scf convergence error
        * 3: ion convergence error
     * 128-255: code exited due to specific trigger
        * 255: exit due to user request, or signal trapped,
              or time > max_seconds
    (note: in the future, check_stop_now could also return a value
         to specify the reason of exiting, and the value could be used
         to return a different value for different reasons)
     @Note
     10/01/17 Samuel Ponce: Add Ford documentation
     @endnote
    """
    exit_status = _qepy.f90wrap_qepy_run_pwscf(oldxml=oldxml, embed=None if embed is \
        None else embed._handle)
    return exit_status

def qepy_electrons(self):
    """
    qepy_electrons(self)
    
    
    Defined at qepy_electrons.fpp lines 18-354
    
    Parameters
    ----------
    embed : Embed_Base
    
    ----------------------------------------------------------------------------
     General self-consistency loop, also for hybrid functionals
     For non-hybrid functionals it just calls "electron_scf"
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%  Iterate hybrid functional  %%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    _qepy.f90wrap_qepy_electrons(embed=self._handle)

def qepy_electrons_scf(printout, exxen, embed):
    """
    qepy_electrons_scf(printout, exxen, embed)
    
    
    Defined at qepy_electrons.fpp lines 358-1530
    
    Parameters
    ----------
    printout : int
    exxen : float
    embed : Embed_Base
    
    ----------------------------------------------------------------------------
     This routine is a driver of the self-consistent cycle.
     It uses the routine c_bands for computing the bands at fixed
     Hamiltonian, the routine sum_band to compute the charge density,
     the routine v_of_rho to compute the new potential and the routine
     mix_rho to mix input and output charge densities.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%          iterate
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    _qepy.f90wrap_qepy_electrons_scf(printout=printout, exxen=exxen, \
        embed=embed._handle)

def qepy_delta_e(vr):
    """
    qepy_delta_e = qepy_delta_e(vr)
    
    
    Defined at qepy_electrons.fpp lines 1582-1654
    
    Parameters
    ----------
    vr : float array
    
    Returns
    -------
    qepy_delta_e : float
    
    -----------------------------------------------------------------------
     This function computes \(\textrm{delta_e}\), where:
     $$\begin{alignat*}{2} \text{delta}\_\text{e} &= - \
         \int\text{rho}\%\text{of}\_\text{r(r)}\cdot
                                                               \text{v}\%\text{of}\_\text{r(r)} && \
                              &= - \int \text{rho}\%\text{kin}\_\text{r(r)}\cdot \text{v}\%\text{kin}\_
                                                               \text{r(r)} && \text{[for Meta-GGA]} \
                              &= - \sum \text{rho}\%\text{ns}\cdot \text{v}\%\text{ns} &&
                                                                                   \text{[for LDA+U]}\
                              &= - \sum \text{becsum}\cdot \text{D1}\_\text{Hxc} && \text{[for PAW]}
                                                                                      \end{alignat*} $$
     ... delta_e =  - \int rho%of_r(r)  v%of_r(r)
                    - \int rho%kin_r(r) v%kin_r(r) [for Meta-GGA]
                    - \sum rho%ns       v%ns       [for LDA+U]
                    - \sum becsum       D1_Hxc     [for PAW]
    """
    qepy_delta_e = _qepy.f90wrap_qepy_delta_e(vr=vr)
    return qepy_delta_e

def qepy_forces(icalc=None, embed=None):
    """
    qepy_forces([icalc, embed])
    
    
    Defined at qepy_forces.fpp lines 18-457
    
    Parameters
    ----------
    icalc : int
    embed : Embed_Base
    
    ----------------------------------------------------------------------------
     This routine is a driver routine which computes the forces
     acting on the atoms. The complete expression of the forces
     contains four parts which are computed by different routines:
      a)  force_lc,     local contribution to the forces
      b)  force_cc,     contribution due to NLCC
      c)  force_ew,     contribution due to the electrostatic ewald term
      d)  force_us,     contribution due to the non-local potential
      e)  force_corr,   correction term for incomplete self-consistency
      f)  force_hub,    contribution due to the Hubbard term
      g)  force_london, semi-empirical correction for dispersion forces
      h)  force_d3,     Grimme-D3(DFT-D3) correction to dispersion forces
    """
    _qepy.f90wrap_qepy_forces(icalc=icalc, embed=None if embed is None else \
        embed._handle)

def qepy_stress(sigma, icalc=None, embed=None):
    """
    qepy_stress(sigma[, icalc, embed])
    
    
    Defined at qepy_stress.fpp lines 14-279
    
    Parameters
    ----------
    sigma : float array
    icalc : int
    embed : Embed_Base
    
    ----------------------------------------------------------------------
     Computes the total stress.
    """
    _qepy.f90wrap_qepy_stress(sigma=sigma, icalc=icalc, embed=None if embed is None \
        else embed._handle)

def qepy_stop_run(exit_status, print_flag=None, what=None, finalize=None):
    """
    qepy_stop_run(exit_status[, print_flag, what, finalize])
    
    
    Defined at qepy_stop_run.fpp lines 61-164
    
    Parameters
    ----------
    exit_status : int
    print_flag : int
    what : str
    finalize : bool
    
    ----------------------------------------------------------------------------
     Close all files and synchronize processes before stopping:
     * exit_status = 0: successfull execution, remove temporary files;
     * exit_status =-1: code stopped by user request;
     * exit_status = 1: convergence not achieved.
     Do not remove temporary files needed for restart.
    qepy -->
     Also add some from pwscf and run_pwscf
     Merge and modify the mp_global.mp_global_end
    qepy <--
    """
    _qepy.f90wrap_qepy_stop_run(exit_status=exit_status, print_flag=print_flag, \
        what=what, finalize=finalize)

def qepy_read_file():
    """
    qepy_read_file()
    
    
    Defined at qepy_read_file_new.fpp lines 13-61
    
    
    ----------------------------------------------------------------------------
     Wrapper routine, for backwards compatibility
    """
    _qepy.f90wrap_qepy_read_file()

def qepy_read_file_new(needwf):
    """
    qepy_read_file_new(needwf)
    
    
    Defined at qepy_read_file_new.fpp lines 65-123
    
    Parameters
    ----------
    needwf : bool
    
    ----------------------------------------------------------------------------
     Reads xml data file produced by pw.x or cp.x, performs initializations
     related to the contents of the xml file
     If needwf=.t. performs wavefunction-related initialization as well
     Does not read wfcs but returns in "wfc_is_collected" info on the wfc file
    """
    _qepy.f90wrap_qepy_read_file_new(needwf=needwf)

def qepy_post_xml_init():
    """
    qepy_post_xml_init()
    
    
    Defined at qepy_read_file_new.fpp lines 126-342
    
    
    ----------------------------------------------------------------------------
     ... Various initializations needed to start a calculation:
     ... pseudopotentials, G vectors, FFT arrays, rho, potential
    """
    _qepy.f90wrap_qepy_post_xml_init()

def qepy_electrons_nscf(printout, exxen, embed):
    """
    qepy_electrons_nscf(printout, exxen, embed)
    
    
    Defined at qepy_electrons_nscf.fpp lines 13-320
    
    Parameters
    ----------
    printout : int
    exxen : float
    embed : Embed_Base
    
    ----------------------------------------------------------------------------
     This routine is a driver of the self-consistent cycle.
     It uses the routine c_bands for computing the bands at fixed
     Hamiltonian, the routine sum_band to compute the charge density,
     the routine v_of_rho to compute the new potential and the routine
     mix_rho to mix input and output charge densities.
    """
    _qepy.f90wrap_qepy_electrons_nscf(printout=printout, exxen=exxen, \
        embed=embed._handle)

def qepy_sum_band(update_occupations=None):
    """
    qepy_sum_band([update_occupations])
    
    
    Defined at qepy_sum_band.fpp lines 14-828
    
    Parameters
    ----------
    update_occupations : bool
    
    ----------------------------------------------------------------------------
     ... Calculates the symmetrized charge density and related quantities
     ... Also computes the occupations and the sum of occupied eigenvalues.
    """
    _qepy.f90wrap_qepy_sum_band(update_occupations=update_occupations)

# import atexit

# def pwscf_finalise():
#     qepy_pwscf_finalise()


# atexit.register(pwscf_finalise)

import pkgutil
import operator
def qepy_clean_saved():
    mods = [name for _, name, _ in pkgutil.iter_modules(qepy.__path__)]
    for mod in mods :
        if hasattr(qepy, mod):
            for item in ['_arrays', '_objs'] :
                if hasattr(operator.attrgetter(mod)(qepy), item):
                    attr = mod + '.' + item
                    operator.attrgetter(attr)(qepy).clear()


qepy_clean_saved()
__author__ = "Pavanello Research Group"
__contact__ = "m.pavanello@rutgers.edu"
__version__ = "0.0.2"
__license__ = "GPL"
__date__ = "2023-03-28"

try:
    from importlib.metadata import version # python >= 3.8
except Exception :
    try:
        from importlib_metadata import version
    except Exception :
        pass

try:
    __version__ = version("qepy")
except Exception :
    pass
