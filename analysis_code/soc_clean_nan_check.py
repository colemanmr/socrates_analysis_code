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

# Load files
diag_dir = file_loc.diag_dir + 'socrates_diags/'

soc_file_lw = diag_dir + 'cd964_20140530_toa_lw_clean_sky_emis_sea_fix_normal.nflx'
soc_file_sw = diag_dir + 'cd964_20140530_toa_sw_clean_sky_emis_sea_fix_normal.nflx'
ukesm_file = diag_dir + 'cd964a.p620140529_daymn_clean_sky_flux.pp' 


# Load ukesm data for differencing and as template for edit soc coords
ukesm_sw_up, ukesm_sw_down, ukesm_lw_up, ukesm_lw_down = iris.load_cubes(ukesm_file,\
                                                 ['m01s01i517', 'm01s01i518',\
                                                  'm01s02i517', 'm01s02i518'])

for cube in [ukesm_sw_up, ukesm_sw_down, ukesm_lw_up, ukesm_lw_down]:
    cube.units = 'W m-2'
    
ukesm_net_down_sw, ukesm_net_down_lw, ukesm_net_down_total = \
    soc_flux.ukesm_net_down_fluxes(ukesm_sw_up, ukesm_sw_down, ukesm_lw_up)
    
    
# Process socrates input
soc_lw = soc_flux.load_soc_single_lev_data(soc_file_lw)
soc_sw = soc_flux.load_soc_single_lev_data(soc_file_sw)
    
soc_lw = soc_flux.edit_soc_coords(soc_lw, ukesm_sw_up)
soc_sw = soc_flux.edit_soc_coords(soc_sw, ukesm_sw_up)


# Calculate diffs
sw_diff = soc_sw - ukesm_net_down_sw[85]
lw_diff = soc_lw - ukesm_net_down_lw[85]


# Plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

# Soc fluxes
soc_flux.plot_flux(soc_lw,
                   'SOC control clean TOA net down LW flux 20140530 normal',
                   plot_dir + 'soc_control_clean_toa_net_down_lw_flux_20140530_normal',
                    vmin=0, vmax=0,
                   )

soc_flux.plot_flux(soc_sw,
                   'SOC control clean TOA net down SW flux 20140530_normal',
                   plot_dir + 'soc_control_clean_toa_net_down_sw_flux_20140530_normal',
                    vmin=0, vmax=0,
                   )

# # Diffs
# soc_flux.plot_flux_diff(sw_diff,
#                    'SOC - UKESM control clean TOA net down SW flux 20140530_normal',
#                    plot_dir + 'soc-ukesm_control_clean_toa_net_down_sw_flux_20140530_normal',
#                     vmin=-100, vmax=100,
#                    )

# soc_flux.plot_flux_diff(lw_diff,
#                    'SOC - UKESM control clean TOA net down LW flux 20140530_normal',
#                    plot_dir + 'soc-ukesm_control_clean_toa_net_down_lw_flux_20140530_normal',
#                     vmin=-50, vmax=50,
#                    )