#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 12:49:15 2022

@author: nn819853
"""

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import Documents.python_code.diagnostics.file_locations_module as file_loc
import diagnostics.radiative_fluxes.fluxes_module as flux_mod
import soc_fluxes_module as soc_flux


diag_dir = file_loc.diag_dir + 'socrates_diags/'


ukesm_file = diag_dir + 'cd964a.p620140529_daymn_clean_sky_flux.pp'   # Just dummy file for formattign soc data 
ukesm_cubes = iris.load(ukesm_file)


# Plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'


# Suppress warnings to see nans list easier
import warnings
warnings.filterwarnings('ignore') # setting ignore as a parameter


for band in range(1,10):
    print(band)
    
    soc_file_lw = diag_dir + 'cd964_20140529_toa_lw_emis_sea_fix_band' + str(band) + '.nflx'
    
    soc_lw = soc_flux.load_soc_single_lev_data(soc_file_lw)

    soc_lw = soc_flux.edit_soc_coords(soc_lw, ukesm_cubes[0])

    soc_flux.plot_flux(soc_lw,
                   'SOC control TOA net down LW flux 20140529 band ' + str(band),
                   plot_dir + 'soc_control_toa_net_down_lw_flux_20140529 band ' + str(band),
                    vmin=0, vmax=0,
                   )
    
    print('nans in lw band ', band, np.where(np.isnan(soc_lw.data)))


for band in range(1,7):
    print(band)
    
    soc_file_sw = diag_dir + 'cd964_20140529_toa_sw_emis_sea_fix_band' + str(band) + '.nflx'
    
    soc_sw = soc_flux.load_soc_single_lev_data(soc_file_sw)

    soc_sw = soc_flux.edit_soc_coords(soc_sw, ukesm_cubes[0])

    soc_flux.plot_flux(soc_sw,
                   'SOC control TOA net down SW flux 20140529 band ' + str(band),
                   plot_dir + 'soc_control_toa_net_down_sw_flux_20140529 band ' + str(band),
                    vmin=0, vmax=0,
                   )
    
    print('nans in sw band ', band, np.where(np.isnan(soc_sw.data)))
