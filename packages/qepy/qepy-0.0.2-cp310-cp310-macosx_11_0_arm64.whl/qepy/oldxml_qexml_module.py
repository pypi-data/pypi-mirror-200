"""
Module oldxml_qexml_module


Defined at oldxml_qexml.fpp lines 16-4608

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def qexml_init(unit_in, unit_out=None, dir=None, dir_in=None, dir_out=None, \
    datafile=None, datafile_in=None, datafile_out=None):
    """
    qexml_init(unit_in[, unit_out, dir, dir_in, dir_out, datafile, datafile_in, \
        datafile_out])
    
    
    Defined at oldxml_qexml.fpp lines 100-161
    
    Parameters
    ----------
    unit_in : int
    unit_out : int
    dir : str
    dir_in : str
    dir_out : str
    datafile : str
    datafile_in : str
    datafile_out : str
    
    ------------------------------------------------------------------------
     just init module data
    """
    _qepy.f90wrap_qexml_init(unit_in=unit_in, unit_out=unit_out, dir=dir, \
        dir_in=dir_in, dir_out=dir_out, datafile=datafile, datafile_in=datafile_in, \
        datafile_out=datafile_out)

def qexml_openfile(filename, action, binary=None):
    """
    ierr = qexml_openfile(filename, action[, binary])
    
    
    Defined at oldxml_qexml.fpp lines 166-214
    
    Parameters
    ----------
    filename : str
    action : str
    binary : bool
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
     open data file
    """
    ierr = _qepy.f90wrap_qexml_openfile(filename=filename, action=action, \
        binary=binary)
    return ierr

def qexml_closefile(action):
    """
    ierr = qexml_closefile(action)
    
    
    Defined at oldxml_qexml.fpp lines 218-242
    
    Parameters
    ----------
    action : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
     close data file
    """
    ierr = _qepy.f90wrap_qexml_closefile(action=action)
    return ierr

def qexml_create_directory(dirname):
    """
    ierr = qexml_create_directory(dirname)
    
    
    Defined at oldxml_qexml.fpp lines 426-451
    
    Parameters
    ----------
    dirname : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_create_directory(dirname=dirname)
    return ierr

def qexml_kpoint_dirname(basedir, ik):
    """
    qexml_kpoint_dirname = qexml_kpoint_dirname(basedir, ik)
    
    
    Defined at oldxml_qexml.fpp lines 456-480
    
    Parameters
    ----------
    basedir : str
    ik : int
    
    Returns
    -------
    qexml_kpoint_dirname : str
    
    ------------------------------------------------------------------------
    """
    qexml_kpoint_dirname = _qepy.f90wrap_qexml_kpoint_dirname(basedir=basedir, \
        ik=ik)
    return qexml_kpoint_dirname

def qexml_wfc_filename(basedir, name, ik, ipol=None, tag=None, extension=None, \
    dir=None):
    """
    qexml_wfc_filename = qexml_wfc_filename(basedir, name, ik[, ipol, tag, \
        extension, dir])
    
    
    Defined at oldxml_qexml.fpp lines 485-528
    
    Parameters
    ----------
    basedir : str
    name : str
    ik : int
    ipol : int
    tag : str
    extension : str
    dir : bool
    
    Returns
    -------
    qexml_wfc_filename : str
    
    ------------------------------------------------------------------------
    """
    qexml_wfc_filename = _qepy.f90wrap_qexml_wfc_filename(basedir=basedir, \
        name=name, ik=ik, ipol=ipol, tag=tag, extension=extension, dir=dir)
    return qexml_wfc_filename

def qexml_restart_dirname(outdir, prefix, runit):
    """
    qexml_restart_dirname = qexml_restart_dirname(outdir, prefix, runit)
    
    
    Defined at oldxml_qexml.fpp lines 594-621
    
    Parameters
    ----------
    outdir : str
    prefix : str
    runit : int
    
    Returns
    -------
    qexml_restart_dirname : str
    
    ------------------------------------------------------------------------
    """
    qexml_restart_dirname = _qepy.f90wrap_qexml_restart_dirname(outdir=outdir, \
        prefix=prefix, runit=runit)
    return qexml_restart_dirname

def qexml_write_header(creator_name, creator_version):
    """
    qexml_write_header(creator_name, creator_version)
    
    
    Defined at oldxml_qexml.fpp lines 629-647
    
    Parameters
    ----------
    creator_name : str
    creator_version : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_header(creator_name=creator_name, \
        creator_version=creator_version)

def qexml_write_control(pp_check_flag=None, lkpoint_dir=None, q_real_space=None, \
    tq_smoothing=None, tbeta_smoothing=None, beta_real_space=None):
    """
    qexml_write_control([pp_check_flag, lkpoint_dir, q_real_space, tq_smoothing, \
        tbeta_smoothing, beta_real_space])
    
    
    Defined at oldxml_qexml.fpp lines 652-681
    
    Parameters
    ----------
    pp_check_flag : bool
    lkpoint_dir : bool
    q_real_space : bool
    tq_smoothing : bool
    tbeta_smoothing : bool
    beta_real_space : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_control(pp_check_flag=pp_check_flag, \
        lkpoint_dir=lkpoint_dir, q_real_space=q_real_space, \
        tq_smoothing=tq_smoothing, tbeta_smoothing=tbeta_smoothing, \
        beta_real_space=beta_real_space)

def qexml_write_status_cp(nfi, simtime, time_units, title, ekin, eht, esr, \
    eself, epseu, enl, exc, vave, enthal, energy_units):
    """
    qexml_write_status_cp(nfi, simtime, time_units, title, ekin, eht, esr, eself, \
        epseu, enl, exc, vave, enthal, energy_units)
    
    
    Defined at oldxml_qexml.fpp lines 688-716
    
    Parameters
    ----------
    nfi : int
    simtime : float
    time_units : str
    title : str
    ekin : float
    eht : float
    esr : float
    eself : float
    epseu : float
    enl : float
    exc : float
    vave : float
    enthal : float
    energy_units : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_status_cp(nfi=nfi, simtime=simtime, \
        time_units=time_units, title=title, ekin=ekin, eht=eht, esr=esr, \
        eself=eself, epseu=epseu, enl=enl, exc=exc, vave=vave, enthal=enthal, \
        energy_units=energy_units)

def qexml_write_cell(ibravais_latt, celldm, alat, a1, a2, a3, b1, b2, b3, \
    alat_units, a_units, b_units, do_mp, do_mt, do_esm, do_cutoff_2d):
    """
    qexml_write_cell(ibravais_latt, celldm, alat, a1, a2, a3, b1, b2, b3, \
        alat_units, a_units, b_units, do_mp, do_mt, do_esm, do_cutoff_2d)
    
    
    Defined at oldxml_qexml.fpp lines 722-812
    
    Parameters
    ----------
    ibravais_latt : int
    celldm : float array
    alat : float
    a1 : float array
    a2 : float array
    a3 : float array
    b1 : float array
    b2 : float array
    b3 : float array
    alat_units : str
    a_units : str
    b_units : str
    do_mp : bool
    do_mt : bool
    do_esm : bool
    do_cutoff_2d : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_cell(ibravais_latt=ibravais_latt, celldm=celldm, \
        alat=alat, a1=a1, a2=a2, a3=a3, b1=b1, b2=b2, b3=b3, alat_units=alat_units, \
        a_units=a_units, b_units=b_units, do_mp=do_mp, do_mt=do_mt, do_esm=do_esm, \
        do_cutoff_2d=do_cutoff_2d)

def qexml_write_moving_cell(lmovecell, cell_factor):
    """
    qexml_write_moving_cell(lmovecell, cell_factor)
    
    
    Defined at oldxml_qexml.fpp lines 817-826
    
    Parameters
    ----------
    lmovecell : bool
    cell_factor : float
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_moving_cell(lmovecell=lmovecell, \
        cell_factor=cell_factor)

def qexml_write_ions(nsp, nat, atm, ityp, psfile, pseudo_dir, amass, \
    amass_units, tau, tau_units, if_pos, dirname, pos_unit):
    """
    qexml_write_ions(nsp, nat, atm, ityp, psfile, pseudo_dir, amass, amass_units, \
        tau, tau_units, if_pos, dirname, pos_unit)
    
    
    Defined at oldxml_qexml.fpp lines 833-925
    
    Parameters
    ----------
    nsp : int
    nat : int
    atm : str array
    ityp : int array
    psfile : str array
    pseudo_dir : str
    amass : float array
    amass_units : str
    tau : float array
    tau_units : str
    if_pos : int array
    dirname : str
    pos_unit : float
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_ions(nsp=nsp, nat=nat, atm=atm, ityp=ityp, \
        psfile=psfile, pseudo_dir=pseudo_dir, amass=amass, amass_units=amass_units, \
        tau=tau, tau_units=tau_units, if_pos=if_pos, dirname=dirname, \
        pos_unit=pos_unit)

def qexml_write_symmetry(ibrav, nrot, nsym, invsym, noinv, time_reversal, \
    no_t_rev, ft, s, sname, s_units, irt, nat, t_rev):
    """
    qexml_write_symmetry(ibrav, nrot, nsym, invsym, noinv, time_reversal, no_t_rev, \
        ft, s, sname, s_units, irt, nat, t_rev)
    
    
    Defined at oldxml_qexml.fpp lines 932-996
    
    Parameters
    ----------
    ibrav : int
    nrot : int
    nsym : int
    invsym : bool
    noinv : bool
    time_reversal : bool
    no_t_rev : bool
    ft : float array
    s : int array
    sname : str array
    s_units : str
    irt : int array
    nat : int
    t_rev : int array
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_symmetry(ibrav=ibrav, nrot=nrot, nsym=nsym, \
        invsym=invsym, noinv=noinv, time_reversal=time_reversal, no_t_rev=no_t_rev, \
        ft=ft, s=s, sname=sname, s_units=s_units, irt=irt, nat=nat, t_rev=t_rev)

def qexml_write_efield(tefield, dipfield, edir, emaxpos, eopreg, eamp, gate, \
    zgate, relaxz, block, block_1, block_2, block_height):
    """
    qexml_write_efield(tefield, dipfield, edir, emaxpos, eopreg, eamp, gate, zgate, \
        relaxz, block, block_1, block_2, block_height)
    
    
    Defined at oldxml_qexml.fpp lines 1003-1051
    
    Parameters
    ----------
    tefield : bool
    dipfield : bool
    edir : int
    emaxpos : float
    eopreg : float
    eamp : float
    gate : bool
    zgate : float
    relaxz : bool
    block : bool
    block_1 : float
    block_2 : float
    block_height : float
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_efield(tefield=tefield, dipfield=dipfield, edir=edir, \
        emaxpos=emaxpos, eopreg=eopreg, eamp=eamp, gate=gate, zgate=zgate, \
        relaxz=relaxz, block=block, block_1=block_1, block_2=block_2, \
        block_height=block_height)

def qexml_write_planewaves(ecutwfc, ecutrho, npwx, gamma_only, nr1, nr2, nr3, \
    ngm, nr1s, nr2s, nr3s, ngms, nr1b, nr2b, nr3b, igv, lgvec, cutoff_units):
    """
    qexml_write_planewaves(ecutwfc, ecutrho, npwx, gamma_only, nr1, nr2, nr3, ngm, \
        nr1s, nr2s, nr3s, ngms, nr1b, nr2b, nr3b, igv, lgvec, cutoff_units)
    
    
    Defined at oldxml_qexml.fpp lines 1058-1124
    
    Parameters
    ----------
    ecutwfc : float
    ecutrho : float
    npwx : int
    gamma_only : bool
    nr1 : int
    nr2 : int
    nr3 : int
    ngm : int
    nr1s : int
    nr2s : int
    nr3s : int
    ngms : int
    nr1b : int
    nr2b : int
    nr3b : int
    igv : int array
    lgvec : bool
    cutoff_units : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_planewaves(ecutwfc=ecutwfc, ecutrho=ecutrho, \
        npwx=npwx, gamma_only=gamma_only, nr1=nr1, nr2=nr2, nr3=nr3, ngm=ngm, \
        nr1s=nr1s, nr2s=nr2s, nr3s=nr3s, ngms=ngms, nr1b=nr1b, nr2b=nr2b, nr3b=nr3b, \
        igv=igv, lgvec=lgvec, cutoff_units=cutoff_units)

def qexml_write_gk(ik, npwk, npwkx, gamma_only, xk, k_units, index_bn, igk):
    """
    qexml_write_gk(ik, npwk, npwkx, gamma_only, xk, k_units, index_bn, igk)
    
    
    Defined at oldxml_qexml.fpp lines 1129-1158
    
    Parameters
    ----------
    ik : int
    npwk : int
    npwkx : int
    gamma_only : bool
    xk : float array
    k_units : str
    index_bn : bool array
    igk : bool array
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_gk(ik=ik, npwk=npwk, npwkx=npwkx, \
        gamma_only=gamma_only, xk=xk, k_units=k_units, index_bn=index_bn, igk=igk)

def qexml_write_spin(lsda, noncolin, npol, lspinorb, domag):
    """
    qexml_write_spin(lsda, noncolin, npol, lspinorb, domag)
    
    
    Defined at oldxml_qexml.fpp lines 1163-1183
    
    Parameters
    ----------
    lsda : bool
    noncolin : bool
    npol : int
    lspinorb : bool
    domag : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_spin(lsda=lsda, noncolin=noncolin, npol=npol, \
        lspinorb=lspinorb, domag=domag)

def qexml_write_magnetization(starting_magnetization, angle1, angle2, nsp, \
    two_fermi_energies, i_cons, mcons, bfield, ef_up, ef_dw, nelup, neldw, \
    lambda_, energy_units):
    """
    qexml_write_magnetization(starting_magnetization, angle1, angle2, nsp, \
        two_fermi_energies, i_cons, mcons, bfield, ef_up, ef_dw, nelup, neldw, \
        lambda_, energy_units)
    
    
    Defined at oldxml_qexml.fpp lines 1190-1261
    
    Parameters
    ----------
    starting_magnetization : float array
    angle1 : float array
    angle2 : float array
    nsp : int
    two_fermi_energies : bool
    i_cons : int
    mcons : float array
    bfield : float array
    ef_up : float
    ef_dw : float
    nelup : float
    neldw : float
    lambda_ : float
    energy_units : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_magnetization(starting_magnetization=starting_magnetization, \
        angle1=angle1, angle2=angle2, nsp=nsp, \
        two_fermi_energies=two_fermi_energies, i_cons=i_cons, mcons=mcons, \
        bfield=bfield, ef_up=ef_up, ef_dw=ef_dw, nelup=nelup, neldw=neldw, \
        lambda_=lambda_, energy_units=energy_units)

def qexml_write_xc(dft, lda_plus_u, nsp=None, lda_plus_u_kind=None, \
    u_projection=None, hubbard_lmax=None, hubbard_l=None, hubbard_u=None, \
    hubbard_j=None, hubbard_j0=None, hubbard_beta=None, hubbard_alpha=None, \
    inlc=None, vdw_table_name=None, pseudo_dir=None, acfdt_in_pw=None, \
    dirname=None, llondon=None, london_s6=None, london_rcut=None, \
    london_c6=None, london_rvdw=None, lxdm=None, ts_vdw=None, \
    vdw_isolated=None):
    """
    qexml_write_xc(dft, lda_plus_u[, nsp, lda_plus_u_kind, u_projection, \
        hubbard_lmax, hubbard_l, hubbard_u, hubbard_j, hubbard_j0, hubbard_beta, \
        hubbard_alpha, inlc, vdw_table_name, pseudo_dir, acfdt_in_pw, dirname, \
        llondon, london_s6, london_rcut, london_c6, london_rvdw, lxdm, ts_vdw, \
        vdw_isolated])
    
    
    Defined at oldxml_qexml.fpp lines 1271-1403
    
    Parameters
    ----------
    dft : str
    lda_plus_u : bool
    nsp : int
    lda_plus_u_kind : int
    u_projection : str
    hubbard_lmax : int
    hubbard_l : int array
    hubbard_u : float array
    hubbard_j : float array
    hubbard_j0 : float array
    hubbard_beta : float array
    hubbard_alpha : float array
    inlc : int
    vdw_table_name : str
    pseudo_dir : str
    acfdt_in_pw : bool
    dirname : str
    llondon : bool
    london_s6 : float
    london_rcut : float
    london_c6 : float array
    london_rvdw : float array
    lxdm : bool
    ts_vdw : bool
    vdw_isolated : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_xc(dft=dft, lda_plus_u=lda_plus_u, nsp=nsp, \
        lda_plus_u_kind=lda_plus_u_kind, u_projection=u_projection, \
        hubbard_lmax=hubbard_lmax, hubbard_l=hubbard_l, hubbard_u=hubbard_u, \
        hubbard_j=hubbard_j, hubbard_j0=hubbard_j0, hubbard_beta=hubbard_beta, \
        hubbard_alpha=hubbard_alpha, inlc=inlc, vdw_table_name=vdw_table_name, \
        pseudo_dir=pseudo_dir, acfdt_in_pw=acfdt_in_pw, dirname=dirname, \
        llondon=llondon, london_s6=london_s6, london_rcut=london_rcut, \
        london_c6=london_c6, london_rvdw=london_rvdw, lxdm=lxdm, ts_vdw=ts_vdw, \
        vdw_isolated=vdw_isolated)

def qexml_write_exx(x_gamma_extrapolation, nqx1, nqx2, nqx3, exxdiv_treatment, \
    yukawa, ecutvcut, exx_fraction, gau_parameter, screening_parameter, \
    exx_is_active, ecutfock):
    """
    qexml_write_exx(x_gamma_extrapolation, nqx1, nqx2, nqx3, exxdiv_treatment, \
        yukawa, ecutvcut, exx_fraction, gau_parameter, screening_parameter, \
        exx_is_active, ecutfock)
    
    
    Defined at oldxml_qexml.fpp lines 1409-1433
    
    Parameters
    ----------
    x_gamma_extrapolation : bool
    nqx1 : int
    nqx2 : int
    nqx3 : int
    exxdiv_treatment : str
    yukawa : float
    ecutvcut : float
    exx_fraction : float
    gau_parameter : float
    screening_parameter : float
    exx_is_active : bool
    ecutfock : float
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_exx(x_gamma_extrapolation=x_gamma_extrapolation, \
        nqx1=nqx1, nqx2=nqx2, nqx3=nqx3, exxdiv_treatment=exxdiv_treatment, \
        yukawa=yukawa, ecutvcut=ecutvcut, exx_fraction=exx_fraction, \
        gau_parameter=gau_parameter, screening_parameter=screening_parameter, \
        exx_is_active=exx_is_active, ecutfock=ecutfock)

def qexml_write_esm(esm_nfit, esm_efield, esm_w, esm_a, esm_bc):
    """
    qexml_write_esm(esm_nfit, esm_efield, esm_w, esm_a, esm_bc)
    
    
    Defined at oldxml_qexml.fpp lines 1438-1452
    
    Parameters
    ----------
    esm_nfit : int
    esm_efield : float
    esm_w : float
    esm_a : float
    esm_bc : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_esm(esm_nfit=esm_nfit, esm_efield=esm_efield, \
        esm_w=esm_w, esm_a=esm_a, esm_bc=esm_bc)

def qexml_write_occ(lgauss, ltetra, tfixed_occ, lsda, ngauss=None, degauss=None, \
    degauss_units=None, tetra_type=None, ntetra=None, tetra=None, \
    nstates_up=None, nstates_dw=None, input_occ=None):
    """
    qexml_write_occ(lgauss, ltetra, tfixed_occ, lsda[, ngauss, degauss, \
        degauss_units, tetra_type, ntetra, tetra, nstates_up, nstates_dw, \
        input_occ])
    
    
    Defined at oldxml_qexml.fpp lines 1459-1525
    
    Parameters
    ----------
    lgauss : bool
    ltetra : bool
    tfixed_occ : bool
    lsda : bool
    ngauss : int
    degauss : float
    degauss_units : str
    tetra_type : int
    ntetra : int
    tetra : int array
    nstates_up : int
    nstates_dw : int
    input_occ : float array
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_occ(lgauss=lgauss, ltetra=ltetra, \
        tfixed_occ=tfixed_occ, lsda=lsda, ngauss=ngauss, degauss=degauss, \
        degauss_units=degauss_units, tetra_type=tetra_type, ntetra=ntetra, \
        tetra=tetra, nstates_up=nstates_up, nstates_dw=nstates_dw, \
        input_occ=input_occ)

def qexml_write_bz(num_k_points, xk, wk, k1, k2, k3, nk1, nk2, nk3, k_units, \
    qnorm, nks_start=None, xk_start=None, wk_start=None):
    """
    qexml_write_bz(num_k_points, xk, wk, k1, k2, k3, nk1, nk2, nk3, k_units, qnorm[, \
        nks_start, xk_start, wk_start])
    
    
    Defined at oldxml_qexml.fpp lines 1532-1593
    
    Parameters
    ----------
    num_k_points : int
    xk : float array
    wk : float array
    k1 : int
    k2 : int
    k3 : int
    nk1 : int
    nk2 : int
    nk3 : int
    k_units : str
    qnorm : float
    nks_start : int
    xk_start : float array
    wk_start : float array
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_bz(num_k_points=num_k_points, xk=xk, wk=wk, k1=k1, \
        k2=k2, k3=k3, nk1=nk1, nk2=nk2, nk3=nk3, k_units=k_units, qnorm=qnorm, \
        nks_start=nks_start, xk_start=xk_start, wk_start=wk_start)

def qexml_write_para(kunit, nproc, nproc_pool, nproc_image, ntask_groups, \
    nproc_bgrp, nproc_ortho):
    """
    qexml_write_para(kunit, nproc, nproc_pool, nproc_image, ntask_groups, \
        nproc_bgrp, nproc_ortho)
    
    
    Defined at oldxml_qexml.fpp lines 1599-1622
    
    Parameters
    ----------
    kunit : int
    nproc : int
    nproc_pool : int
    nproc_image : int
    ntask_groups : int
    nproc_bgrp : int
    nproc_ortho : int
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_para(kunit=kunit, nproc=nproc, nproc_pool=nproc_pool, \
        nproc_image=nproc_image, ntask_groups=ntask_groups, nproc_bgrp=nproc_bgrp, \
        nproc_ortho=nproc_ortho)

def qexml_write_bands_info(num_k_points, natomwfc, nbnd, nbnd_up, nbnd_down, \
    nspin, nelec, nel_up, nel_down, energy_units, k_units, ef=None, \
    two_fermi_energies=None, ef_up=None, ef_down=None, noncolin=None):
    """
    qexml_write_bands_info(num_k_points, natomwfc, nbnd, nbnd_up, nbnd_down, nspin, \
        nelec, nel_up, nel_down, energy_units, k_units[, ef, two_fermi_energies, \
        ef_up, ef_down, noncolin])
    
    
    Defined at oldxml_qexml.fpp lines 1631-1699
    
    Parameters
    ----------
    num_k_points : int
    natomwfc : int
    nbnd : int
    nbnd_up : int
    nbnd_down : int
    nspin : int
    nelec : float
    nel_up : int
    nel_down : int
    energy_units : str
    k_units : str
    ef : float
    two_fermi_energies : bool
    ef_up : float
    ef_down : float
    noncolin : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_bands_info(num_k_points=num_k_points, \
        natomwfc=natomwfc, nbnd=nbnd, nbnd_up=nbnd_up, nbnd_down=nbnd_down, \
        nspin=nspin, nelec=nelec, nel_up=nel_up, nel_down=nel_down, \
        energy_units=energy_units, k_units=k_units, ef=ef, \
        two_fermi_energies=two_fermi_energies, ef_up=ef_up, ef_down=ef_down, \
        noncolin=noncolin)

def qexml_write_bands_pw(nbnd, num_k_points, nspin, xk, wk, wg, et, \
    energy_units, lkpoint_dir, auxunit, dirname):
    """
    qexml_write_bands_pw(nbnd, num_k_points, nspin, xk, wk, wg, et, energy_units, \
        lkpoint_dir, auxunit, dirname)
    
    
    Defined at oldxml_qexml.fpp lines 1704-1863
    
    Parameters
    ----------
    nbnd : int
    num_k_points : int
    nspin : int
    xk : float array
    wk : float array
    wg : float array
    et : float array
    energy_units : str
    lkpoint_dir : bool
    auxunit : int
    dirname : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_bands_pw(nbnd=nbnd, num_k_points=num_k_points, \
        nspin=nspin, xk=xk, wk=wk, wg=wg, et=et, energy_units=energy_units, \
        lkpoint_dir=lkpoint_dir, auxunit=auxunit, dirname=dirname)

def qexml_write_bands_cp(nbnd, num_k_points, nspin, iupdwn, nupdwn, xk, wk, et, \
    tksw, occ0, occm, energy_units, k_units, auxunit, dirname):
    """
    qexml_write_bands_cp(nbnd, num_k_points, nspin, iupdwn, nupdwn, xk, wk, et, \
        tksw, occ0, occm, energy_units, k_units, auxunit, dirname)
    
    
    Defined at oldxml_qexml.fpp lines 1869-1946
    
    Parameters
    ----------
    nbnd : int
    num_k_points : int
    nspin : int
    iupdwn : int array
    nupdwn : int array
    xk : float array
    wk : float array
    et : float array
    tksw : bool
    occ0 : float array
    occm : float array
    energy_units : str
    k_units : str
    auxunit : int
    dirname : str
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_bands_cp(nbnd=nbnd, num_k_points=num_k_points, \
        nspin=nspin, iupdwn=iupdwn, nupdwn=nupdwn, xk=xk, wk=wk, et=et, tksw=tksw, \
        occ0=occ0, occm=occm, energy_units=energy_units, k_units=k_units, \
        auxunit=auxunit, dirname=dirname)

def qexml_write_eig(iuni, filename, nbnd, eig, energy_units, occ=None, ik=None, \
    ispin=None, lkpoint_dir=None):
    """
    qexml_write_eig(iuni, filename, nbnd, eig, energy_units[, occ, ik, ispin, \
        lkpoint_dir])
    
    
    Defined at oldxml_qexml.fpp lines 1952-1992
    
    Parameters
    ----------
    iuni : int
    filename : str
    nbnd : int
    eig : float array
    energy_units : str
    occ : float array
    ik : int
    ispin : int
    lkpoint_dir : bool
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_eig(iuni=iuni, filename=filename, nbnd=nbnd, eig=eig, \
        energy_units=energy_units, occ=occ, ik=ik, ispin=ispin, \
        lkpoint_dir=lkpoint_dir)

def qexml_write_wfc(nbnd, nkpts, nspin, ik, ngw, igwx, gamma_only, ispin=None, \
    ipol=None, igk=None, wf=None, wf_kindip=None, scale_factor=None):
    """
    qexml_write_wfc(nbnd, nkpts, nspin, ik, ngw, igwx, gamma_only[, ispin, ipol, \
        igk, wf, wf_kindip, scale_factor])
    
    
    Defined at oldxml_qexml.fpp lines 1998-2104
    
    Parameters
    ----------
    nbnd : int
    nkpts : int
    nspin : int
    ik : int
    ngw : int
    igwx : int
    gamma_only : bool
    ispin : int
    ipol : int
    igk : int array
    wf : complex array
    wf_kindip : complex array
    scale_factor : float
    
    ------------------------------------------------------------------------
    """
    _qepy.f90wrap_qexml_write_wfc(nbnd=nbnd, nkpts=nkpts, nspin=nspin, ik=ik, \
        ngw=ngw, igwx=igwx, gamma_only=gamma_only, ispin=ispin, ipol=ipol, igk=igk, \
        wf=wf, wf_kindip=wf_kindip, scale_factor=scale_factor)

def qexml_write_rho(nr1, nr2, nr3, rho=None, nr1x=None, nr2x=None, rhov=None, \
    binary=None):
    """
    qexml_write_rho(nr1, nr2, nr3[, rho, nr1x, nr2x, rhov, binary])
    
    
    Defined at oldxml_qexml.fpp lines 2109-2213
    
    Parameters
    ----------
    nr1 : int
    nr2 : int
    nr3 : int
    rho : float array
    nr1x : int
    nr2x : int
    rhov : float array
    binary : bool
    
    ------------------------------------------------------------------------
     Writes charge density rho, one plane at a time.
    """
    _qepy.f90wrap_qexml_write_rho(nr1=nr1, nr2=nr2, nr3=nr3, rho=rho, nr1x=nr1x, \
        nr2x=nr2x, rhov=rhov, binary=binary)

def qexml_read_header(creator_name=None, creator_version=None, format_name=None, \
    format_version=None):
    """
    ierr = qexml_read_header([creator_name, creator_version, format_name, \
        format_version])
    
    
    Defined at oldxml_qexml.fpp lines 2222-2263
    
    Parameters
    ----------
    creator_name : str
    creator_version : str
    format_name : str
    format_version : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_header(creator_name=creator_name, \
        creator_version=creator_version, format_name=format_name, \
        format_version=format_version)
    return ierr

def qexml_read_status_cp(nfi=None, simtime=None, time_units=None, title=None, \
    ekin=None, eht=None, esr=None, eself=None, epseu=None, enl=None, exc=None, \
    vave=None, enthal=None, energy_units=None):
    """
    found, ierr = qexml_read_status_cp([nfi, simtime, time_units, title, ekin, eht, \
        esr, eself, epseu, enl, exc, vave, enthal, energy_units])
    
    
    Defined at oldxml_qexml.fpp lines 2270-2349
    
    Parameters
    ----------
    nfi : int
    simtime : float
    time_units : str
    title : str
    ekin : float
    eht : float
    esr : float
    eself : float
    epseu : float
    enl : float
    exc : float
    vave : float
    enthal : float
    energy_units : str
    
    Returns
    -------
    found : bool
    ierr : int
    
    ------------------------------------------------------------------------
    """
    found, ierr = _qepy.f90wrap_qexml_read_status_cp(nfi=nfi, simtime=simtime, \
        time_units=time_units, title=title, ekin=ekin, eht=eht, esr=esr, \
        eself=eself, epseu=epseu, enl=enl, exc=exc, vave=vave, enthal=enthal, \
        energy_units=energy_units)
    return found, ierr

def qexml_read_cell(bravais_lattice=None, celldm=None, alat=None, a1=None, \
    a2=None, a3=None, b1=None, b2=None, b3=None, alat_units=None, a_units=None, \
    b_units=None, es_corr=None):
    """
    ierr = qexml_read_cell([bravais_lattice, celldm, alat, a1, a2, a3, b1, b2, b3, \
        alat_units, a_units, b_units, es_corr])
    
    
    Defined at oldxml_qexml.fpp lines 2356-2449
    
    Parameters
    ----------
    bravais_lattice : str
    celldm : float array
    alat : float
    a1 : float array
    a2 : float array
    a3 : float array
    b1 : float array
    b2 : float array
    b3 : float array
    alat_units : str
    a_units : str
    b_units : str
    es_corr : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_cell(bravais_lattice=bravais_lattice, \
        celldm=celldm, alat=alat, a1=a1, a2=a2, a3=a3, b1=b1, b2=b2, b3=b3, \
        alat_units=alat_units, a_units=a_units, b_units=b_units, es_corr=es_corr)
    return ierr

def qexml_read_moving_cell():
    """
    lmovecell, cell_factor, ierr = qexml_read_moving_cell()
    
    
    Defined at oldxml_qexml.fpp lines 2454-2472
    
    
    Returns
    -------
    lmovecell : bool
    cell_factor : float
    ierr : int
    
    ------------------------------------------------------------------------
    """
    lmovecell, cell_factor, ierr = _qepy.f90wrap_qexml_read_moving_cell()
    return lmovecell, cell_factor, ierr

def qexml_read_ions(nsp=None, nat=None, atm=None, ityp=None, psfile=None, \
    amass=None, amass_units=None, tau=None, tau_units=None, if_pos=None, \
    pseudo_dir=None):
    """
    ierr = qexml_read_ions([nsp, nat, atm, ityp, psfile, amass, amass_units, tau, \
        tau_units, if_pos, pseudo_dir])
    
    
    Defined at oldxml_qexml.fpp lines 2478-2609
    
    Parameters
    ----------
    nsp : int
    nat : int
    atm : str array
    ityp : int array
    psfile : str array
    amass : float array
    amass_units : str
    tau : float array
    tau_units : str
    if_pos : int array
    pseudo_dir : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_ions(nsp=nsp, nat=nat, atm=atm, ityp=ityp, \
        psfile=psfile, amass=amass, amass_units=amass_units, tau=tau, \
        tau_units=tau_units, if_pos=if_pos, pseudo_dir=pseudo_dir)
    return ierr

def qexml_read_magnetization(starting_magnetization=None, angle1=None, \
    angle2=None, nsp=None, two_fermi_energies=None, i_cons=None, mcons=None, \
    bfield=None, ef_up=None, ef_dw=None, nelup=None, neldw=None, lambda_=None, \
    energy_units=None, found=None):
    """
    ierr = qexml_read_magnetization([starting_magnetization, angle1, angle2, nsp, \
        two_fermi_energies, i_cons, mcons, bfield, ef_up, ef_dw, nelup, neldw, \
        lambda_, energy_units, found])
    
    
    Defined at oldxml_qexml.fpp lines 2616-2751
    
    Parameters
    ----------
    starting_magnetization : float array
    angle1 : float array
    angle2 : float array
    nsp : int
    two_fermi_energies : bool
    i_cons : int
    mcons : float array
    bfield : float array
    ef_up : float
    ef_dw : float
    nelup : float
    neldw : float
    lambda_ : float
    energy_units : str
    found : bool
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = \
        _qepy.f90wrap_qexml_read_magnetization(starting_magnetization=starting_magnetization, \
        angle1=angle1, angle2=angle2, nsp=nsp, \
        two_fermi_energies=two_fermi_energies, i_cons=i_cons, mcons=mcons, \
        bfield=bfield, ef_up=ef_up, ef_dw=ef_dw, nelup=nelup, neldw=neldw, \
        lambda_=lambda_, energy_units=energy_units, found=found)
    return ierr

def qexml_read_symmetry(nsym=None, nrot=None, invsym=None, noinv=None, \
    time_reversal=None, no_t_rev=None, trasl=None, s=None, sname=None, \
    s_units=None, t_rev=None, irt=None, nat=None):
    """
    found, ierr = qexml_read_symmetry([nsym, nrot, invsym, noinv, time_reversal, \
        no_t_rev, trasl, s, sname, s_units, t_rev, irt, nat])
    
    
    Defined at oldxml_qexml.fpp lines 2758-2896
    
    Parameters
    ----------
    nsym : int
    nrot : int
    invsym : bool
    noinv : bool
    time_reversal : bool
    no_t_rev : bool
    trasl : float array
    s : int array
    sname : str array
    s_units : str
    t_rev : int array
    irt : int array
    nat : int
    
    Returns
    -------
    found : bool
    ierr : int
    
    ------------------------------------------------------------------------
    """
    found, ierr = _qepy.f90wrap_qexml_read_symmetry(nsym=nsym, nrot=nrot, \
        invsym=invsym, noinv=noinv, time_reversal=time_reversal, no_t_rev=no_t_rev, \
        trasl=trasl, s=s, sname=sname, s_units=s_units, t_rev=t_rev, irt=irt, \
        nat=nat)
    return found, ierr

def qexml_read_efield(tefield=None, dipfield=None, edir=None, emaxpos=None, \
    eopreg=None, eamp=None, gate=None, zgate=None, relaxz=None, block=None, \
    block_1=None, block_2=None, block_height=None):
    """
    found, ierr = qexml_read_efield([tefield, dipfield, edir, emaxpos, eopreg, eamp, \
        gate, zgate, relaxz, block, block_1, block_2, block_height])
    
    
    Defined at oldxml_qexml.fpp lines 2903-2990
    
    Parameters
    ----------
    tefield : bool
    dipfield : bool
    edir : int
    emaxpos : float
    eopreg : float
    eamp : float
    gate : bool
    zgate : float
    relaxz : bool
    block : bool
    block_1 : float
    block_2 : float
    block_height : float
    
    Returns
    -------
    found : bool
    ierr : int
    
    ----------------------------------------------------------------------
    """
    found, ierr = _qepy.f90wrap_qexml_read_efield(tefield=tefield, \
        dipfield=dipfield, edir=edir, emaxpos=emaxpos, eopreg=eopreg, eamp=eamp, \
        gate=gate, zgate=zgate, relaxz=relaxz, block=block, block_1=block_1, \
        block_2=block_2, block_height=block_height)
    return found, ierr

def qexml_read_exx(x_gamma_extrapolation=None, nqx1=None, nqx2=None, nqx3=None, \
    exxdiv_treatment=None, yukawa=None, ecutvcut=None, exx_fraction=None, \
    screening_parameter=None, gau_parameter=None, exx_is_active=None, \
    ecutfock=None):
    """
    found, ierr = qexml_read_exx([x_gamma_extrapolation, nqx1, nqx2, nqx3, \
        exxdiv_treatment, yukawa, ecutvcut, exx_fraction, screening_parameter, \
        gau_parameter, exx_is_active, ecutfock])
    
    
    Defined at oldxml_qexml.fpp lines 2998-3083
    
    Parameters
    ----------
    x_gamma_extrapolation : bool
    nqx1 : int
    nqx2 : int
    nqx3 : int
    exxdiv_treatment : str
    yukawa : float
    ecutvcut : float
    exx_fraction : float
    screening_parameter : float
    gau_parameter : float
    exx_is_active : bool
    ecutfock : float
    
    Returns
    -------
    found : bool
    ierr : int
    
    ----------------------------------------------------------------------
    """
    found, ierr = \
        _qepy.f90wrap_qexml_read_exx(x_gamma_extrapolation=x_gamma_extrapolation, \
        nqx1=nqx1, nqx2=nqx2, nqx3=nqx3, exxdiv_treatment=exxdiv_treatment, \
        yukawa=yukawa, ecutvcut=ecutvcut, exx_fraction=exx_fraction, \
        screening_parameter=screening_parameter, gau_parameter=gau_parameter, \
        exx_is_active=exx_is_active, ecutfock=ecutfock)
    return found, ierr

def qexml_read_esm(esm_nfit=None, esm_efield=None, esm_w=None, esm_a=None, \
    esm_bc=None):
    """
    ierr = qexml_read_esm([esm_nfit, esm_efield, esm_w, esm_a, esm_bc])
    
    
    Defined at oldxml_qexml.fpp lines 3088-3132
    
    Parameters
    ----------
    esm_nfit : int
    esm_efield : float
    esm_w : float
    esm_a : float
    esm_bc : str
    
    Returns
    -------
    ierr : int
    
    ----------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_esm(esm_nfit=esm_nfit, esm_efield=esm_efield, \
        esm_w=esm_w, esm_a=esm_a, esm_bc=esm_bc)
    return ierr

def qexml_read_planewaves(ecutwfc=None, ecutrho=None, npwx=None, \
    gamma_only=None, nr1=None, nr2=None, nr3=None, ngm=None, nr1s=None, \
    nr2s=None, nr3s=None, ngms=None, nr1b=None, nr2b=None, nr3b=None, igv=None, \
    cutoff_units=None):
    """
    ierr = qexml_read_planewaves([ecutwfc, ecutrho, npwx, gamma_only, nr1, nr2, nr3, \
        ngm, nr1s, nr2s, nr3s, ngms, nr1b, nr2b, nr3b, igv, cutoff_units])
    
    
    Defined at oldxml_qexml.fpp lines 3139-3250
    
    Parameters
    ----------
    ecutwfc : float
    ecutrho : float
    npwx : int
    gamma_only : bool
    nr1 : int
    nr2 : int
    nr3 : int
    ngm : int
    nr1s : int
    nr2s : int
    nr3s : int
    ngms : int
    nr1b : int
    nr2b : int
    nr3b : int
    igv : int array
    cutoff_units : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_planewaves(ecutwfc=ecutwfc, ecutrho=ecutrho, \
        npwx=npwx, gamma_only=gamma_only, nr1=nr1, nr2=nr2, nr3=nr3, ngm=ngm, \
        nr1s=nr1s, nr2s=nr2s, nr3s=nr3s, ngms=ngms, nr1b=nr1b, nr2b=nr2b, nr3b=nr3b, \
        igv=igv, cutoff_units=cutoff_units)
    return ierr

def qexml_read_gk(ik, npwk=None, npwkx=None, gamma_only=None, xk=None, \
    k_units=None, index_bn=None, igk=None):
    """
    ierr = qexml_read_gk(ik[, npwk, npwkx, gamma_only, xk, k_units, index_bn, igk])
    
    
    Defined at oldxml_qexml.fpp lines 3255-3330
    
    Parameters
    ----------
    ik : int
    npwk : int
    npwkx : int
    gamma_only : bool
    xk : float array
    k_units : str
    index_bn : int array
    igk : int array
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_gk(ik=ik, npwk=npwk, npwkx=npwkx, \
        gamma_only=gamma_only, xk=xk, k_units=k_units, index_bn=index_bn, igk=igk)
    return ierr

def qexml_read_spin(lsda=None, noncolin=None, npol=None, lspinorb=None, \
    domag=None):
    """
    ierr = qexml_read_spin([lsda, noncolin, npol, lspinorb, domag])
    
    
    Defined at oldxml_qexml.fpp lines 3335-3383
    
    Parameters
    ----------
    lsda : bool
    noncolin : bool
    npol : int
    lspinorb : bool
    domag : bool
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_spin(lsda=lsda, noncolin=noncolin, npol=npol, \
        lspinorb=lspinorb, domag=domag)
    return ierr

def qexml_read_xc(dft=None, lda_plus_u=None, lda_plus_u_kind=None, \
    u_projection=None, hubbard_lmax=None, hubbard_l=None, nsp=None, \
    hubbard_u=None, hubbard_j=None, hubbard_j0=None, hubbard_alpha=None, \
    hubbard_beta=None, inlc=None, vdw_table_name=None, acfdt_in_pw=None, \
    llondon=None, london_s6=None, london_rcut=None, london_c6=None, \
    london_rvdw=None, lxdm=None, ts_vdw=None, vdw_isolated=None):
    """
    ierr = qexml_read_xc([dft, lda_plus_u, lda_plus_u_kind, u_projection, \
        hubbard_lmax, hubbard_l, nsp, hubbard_u, hubbard_j, hubbard_j0, \
        hubbard_alpha, hubbard_beta, inlc, vdw_table_name, acfdt_in_pw, llondon, \
        london_s6, london_rcut, london_c6, london_rvdw, lxdm, ts_vdw, vdw_isolated])
    
    
    Defined at oldxml_qexml.fpp lines 3393-3600
    
    Parameters
    ----------
    dft : str
    lda_plus_u : bool
    lda_plus_u_kind : int
    u_projection : str
    hubbard_lmax : int
    hubbard_l : int array
    nsp : int
    hubbard_u : float array
    hubbard_j : float array
    hubbard_j0 : float array
    hubbard_alpha : float array
    hubbard_beta : float array
    inlc : int
    vdw_table_name : str
    acfdt_in_pw : bool
    llondon : bool
    london_s6 : float
    london_rcut : float
    london_c6 : float array
    london_rvdw : float array
    lxdm : bool
    ts_vdw : bool
    vdw_isolated : bool
    
    Returns
    -------
    ierr : int
    
    ----------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_xc(dft=dft, lda_plus_u=lda_plus_u, \
        lda_plus_u_kind=lda_plus_u_kind, u_projection=u_projection, \
        hubbard_lmax=hubbard_lmax, hubbard_l=hubbard_l, nsp=nsp, \
        hubbard_u=hubbard_u, hubbard_j=hubbard_j, hubbard_j0=hubbard_j0, \
        hubbard_alpha=hubbard_alpha, hubbard_beta=hubbard_beta, inlc=inlc, \
        vdw_table_name=vdw_table_name, acfdt_in_pw=acfdt_in_pw, llondon=llondon, \
        london_s6=london_s6, london_rcut=london_rcut, london_c6=london_c6, \
        london_rvdw=london_rvdw, lxdm=lxdm, ts_vdw=ts_vdw, \
        vdw_isolated=vdw_isolated)
    return ierr

def qexml_read_occ(lgauss=None, ngauss=None, degauss=None, degauss_units=None, \
    ltetra=None, tetra_type=None, ntetra=None, tetra=None, tfixed_occ=None, \
    nstates_up=None, nstates_dw=None, input_occ=None):
    """
    ierr = qexml_read_occ([lgauss, ngauss, degauss, degauss_units, ltetra, \
        tetra_type, ntetra, tetra, tfixed_occ, nstates_up, nstates_dw, input_occ])
    
    
    Defined at oldxml_qexml.fpp lines 3607-3756
    
    Parameters
    ----------
    lgauss : bool
    ngauss : int
    degauss : float
    degauss_units : str
    ltetra : bool
    tetra_type : int
    ntetra : int
    tetra : int array
    tfixed_occ : bool
    nstates_up : int
    nstates_dw : int
    input_occ : float array
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_occ(lgauss=lgauss, ngauss=ngauss, \
        degauss=degauss, degauss_units=degauss_units, ltetra=ltetra, \
        tetra_type=tetra_type, ntetra=ntetra, tetra=tetra, tfixed_occ=tfixed_occ, \
        nstates_up=nstates_up, nstates_dw=nstates_dw, input_occ=input_occ)
    return ierr

def qexml_read_bz(num_k_points=None, xk=None, wk=None, k1=None, k2=None, \
    k3=None, nk1=None, nk2=None, nk3=None, nks_start=None, qnorm=None, \
    k_units=None):
    """
    ierr = qexml_read_bz([num_k_points, xk, wk, k1, k2, k3, nk1, nk2, nk3, \
        nks_start, qnorm, k_units])
    
    
    Defined at oldxml_qexml.fpp lines 3763-3898
    
    Parameters
    ----------
    num_k_points : int
    xk : float array
    wk : float array
    k1 : int
    k2 : int
    k3 : int
    nk1 : int
    nk2 : int
    nk3 : int
    nks_start : int
    qnorm : float
    k_units : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_bz(num_k_points=num_k_points, xk=xk, wk=wk, \
        k1=k1, k2=k2, k3=k3, nk1=nk1, nk2=nk2, nk3=nk3, nks_start=nks_start, \
        qnorm=qnorm, k_units=k_units)
    return ierr

def qexml_read_para(kunit=None, nproc=None, nproc_pool=None, nproc_image=None, \
    ntask_groups=None, nproc_bgrp=None, nproc_ortho=None):
    """
    found, ierr = qexml_read_para([kunit, nproc, nproc_pool, nproc_image, \
        ntask_groups, nproc_bgrp, nproc_ortho])
    
    
    Defined at oldxml_qexml.fpp lines 3904-3957
    
    Parameters
    ----------
    kunit : int
    nproc : int
    nproc_pool : int
    nproc_image : int
    ntask_groups : int
    nproc_bgrp : int
    nproc_ortho : int
    
    Returns
    -------
    found : bool
    ierr : int
    
    ------------------------------------------------------------------------
    """
    found, ierr = _qepy.f90wrap_qexml_read_para(kunit=kunit, nproc=nproc, \
        nproc_pool=nproc_pool, nproc_image=nproc_image, ntask_groups=ntask_groups, \
        nproc_bgrp=nproc_bgrp, nproc_ortho=nproc_ortho)
    return found, ierr

def qexml_read_phonon(modenum=None, xqq=None, q_units=None):
    """
    ierr = qexml_read_phonon([modenum, xqq, q_units])
    
    
    Defined at oldxml_qexml.fpp lines 3962-3999
    
    Parameters
    ----------
    modenum : int
    xqq : float array
    q_units : str
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_phonon(modenum=modenum, xqq=xqq, \
        q_units=q_units)
    return ierr

def qexml_read_bands_info(num_k_points=None, natomwfc=None, nbnd=None, \
    nbnd_up=None, nbnd_down=None, nspin=None, nelec=None, nel_up=None, \
    nel_down=None, ef=None, two_fermi_energies=None, ef_up=None, ef_dw=None, \
    energy_units=None, k_units=None, noncolin=None):
    """
    ierr = qexml_read_bands_info([num_k_points, natomwfc, nbnd, nbnd_up, nbnd_down, \
        nspin, nelec, nel_up, nel_down, ef, two_fermi_energies, ef_up, ef_dw, \
        energy_units, k_units, noncolin])
    
    
    Defined at oldxml_qexml.fpp lines 4009-4139
    
    Parameters
    ----------
    num_k_points : int
    natomwfc : int
    nbnd : int
    nbnd_up : int
    nbnd_down : int
    nspin : int
    nelec : float
    nel_up : int
    nel_down : int
    ef : float
    two_fermi_energies : bool
    ef_up : float
    ef_dw : float
    energy_units : str
    k_units : str
    noncolin : bool
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_bands_info(num_k_points=num_k_points, \
        natomwfc=natomwfc, nbnd=nbnd, nbnd_up=nbnd_up, nbnd_down=nbnd_down, \
        nspin=nspin, nelec=nelec, nel_up=nel_up, nel_down=nel_down, ef=ef, \
        two_fermi_energies=two_fermi_energies, ef_up=ef_up, ef_dw=ef_dw, \
        energy_units=energy_units, k_units=k_units, noncolin=noncolin)
    return ierr

def qexml_read_bands_pw(num_k_points, nbnd, nkstot, lsda, lkpoint_dir, filename, \
    isk=None, et=None, wg=None):
    """
    ierr = qexml_read_bands_pw(num_k_points, nbnd, nkstot, lsda, lkpoint_dir, \
        filename[, isk, et, wg])
    
    
    Defined at oldxml_qexml.fpp lines 4145-4260
    
    Parameters
    ----------
    num_k_points : int
    nbnd : int
    nkstot : int
    lsda : bool
    lkpoint_dir : bool
    filename : str
    isk : int array
    et : float array
    wg : float array
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_bands_pw(num_k_points=num_k_points, nbnd=nbnd, \
        nkstot=nkstot, lsda=lsda, lkpoint_dir=lkpoint_dir, filename=filename, \
        isk=isk, et=et, wg=wg)
    return ierr

def qexml_read_bands_cp(num_k_points, nbnd_tot, nudx, nspin, iupdwn, nupdwn, \
    occ0, occm):
    """
    ierr = qexml_read_bands_cp(num_k_points, nbnd_tot, nudx, nspin, iupdwn, nupdwn, \
        occ0, occm)
    
    
    Defined at oldxml_qexml.fpp lines 4266-4355
    
    Parameters
    ----------
    num_k_points : int
    nbnd_tot : int
    nudx : int
    nspin : int
    iupdwn : int array
    nupdwn : int array
    occ0 : float array
    occm : float array
    
    Returns
    -------
    ierr : int
    
    -----------------------------------------------------------------------------
    """
    ierr = _qepy.f90wrap_qexml_read_bands_cp(num_k_points=num_k_points, \
        nbnd_tot=nbnd_tot, nudx=nudx, nspin=nspin, iupdwn=iupdwn, nupdwn=nupdwn, \
        occ0=occ0, occm=occm)
    return ierr

def qexml_read_wfc(ibnds, ibnde, ik, ispin=None, ipol=None, igk=None, ngw=None, \
    igwx=None, gamma_only=None, wf=None, wf_kindip=None):
    """
    ierr = qexml_read_wfc(ibnds, ibnde, ik[, ispin, ipol, igk, ngw, igwx, \
        gamma_only, wf, wf_kindip])
    
    
    Defined at oldxml_qexml.fpp lines 4361-4508
    
    Parameters
    ----------
    ibnds : int
    ibnde : int
    ik : int
    ispin : int
    ipol : int
    igk : int array
    ngw : int
    igwx : int
    gamma_only : bool
    wf : complex array
    wf_kindip : complex array
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
     read wfc from IBNDS to IBNDE, for kpt IK and spin ISPIN
     WF is the wfc on its proper k+g grid, while WF_KINDIP is the same wfc
     but on a truncated rho grid(k-point indipendent)
    """
    ierr = _qepy.f90wrap_qexml_read_wfc(ibnds=ibnds, ibnde=ibnde, ik=ik, \
        ispin=ispin, ipol=ipol, igk=igk, ngw=ngw, igwx=igwx, gamma_only=gamma_only, \
        wf=wf, wf_kindip=wf_kindip)
    return ierr

def qexml_read_rho(nr1=None, nr2=None, nr3=None, rho=None, ip=None, rhoz=None):
    """
    ierr = qexml_read_rho([nr1, nr2, nr3, rho, ip, rhoz])
    
    
    Defined at oldxml_qexml.fpp lines 4513-4606
    
    Parameters
    ----------
    nr1 : int
    nr2 : int
    nr3 : int
    rho : float array
    ip : int
    rhoz : float array
    
    Returns
    -------
    ierr : int
    
    ------------------------------------------------------------------------
     Reads charge density rho, as a whole or one plane at a time.
     if RHO is specified, the whole charge density is read;
     if RHOZ is specified only the IP-th plane is read
    """
    ierr = _qepy.f90wrap_qexml_read_rho(nr1=nr1, nr2=nr2, nr3=nr3, rho=rho, ip=ip, \
        rhoz=rhoz)
    return ierr

def get_qexml_current_version():
    """
    Element qexml_current_version ftype=character(10) pytype=str
    
    
    Defined at oldxml_qexml.fpp line 59
    
    """
    return _qepy.f90wrap_oldxml_qexml_module__get__qexml_current_version()

def set_qexml_current_version(qexml_current_version):
    _qepy.f90wrap_oldxml_qexml_module__set__qexml_current_version(qexml_current_version)

def get_qexml_default_version():
    """
    Element qexml_default_version ftype=character(10) pytype=str
    
    
    Defined at oldxml_qexml.fpp line 60
    
    """
    return _qepy.f90wrap_oldxml_qexml_module__get__qexml_default_version()

def set_qexml_default_version(qexml_default_version):
    _qepy.f90wrap_oldxml_qexml_module__set__qexml_default_version(qexml_default_version)

def get_qexml_current_version_init():
    """
    Element qexml_current_version_init ftype=logical pytype=bool
    
    
    Defined at oldxml_qexml.fpp line 61
    
    """
    return _qepy.f90wrap_oldxml_qexml_module__get__qexml_current_version_init()

def set_qexml_current_version_init(qexml_current_version_init):
    _qepy.f90wrap_oldxml_qexml_module__set__qexml_current_version_init(qexml_current_version_init)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "oldxml_qexml_module".')

for func in _dt_array_initialisers:
    func()
