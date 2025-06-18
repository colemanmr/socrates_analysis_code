#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:44:00 2022

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


# ukesm_file = diag_dir + 'cd964a.p6201405_05_30_all_sky_fluxes.pp' # decided not to save this file to repo 
ukesm_file = diag_dir + 'cd964a.p6201403_03_30_all_sky_fluxes.pp'

ukesm_cubes = iris.load(ukesm_file)

ukesm_lw_up_days = ukesm_cubes[2][:,85]
ukesm_sw_down_days = ukesm_cubes[1][:,85]
ukesm_sw_up_days = ukesm_cubes[3][:,85]


ukesm_lw_up,_,_ = flux_mod.time_mean_cube(ukesm_lw_up_days)
ukesm_sw_up,_,_ = flux_mod.time_mean_cube(ukesm_sw_up_days)
ukesm_sw_down,_,_ = flux_mod.time_mean_cube(ukesm_sw_down_days)

ukesm_net_down_sw, ukesm_net_down_lw, ukesm_net_down_tot =\
    soc_flux.ukesm_net_down_fluxes(ukesm_sw_up, ukesm_sw_down, ukesm_lw_up)
    

# soc_file_lw = diag_dir + 'cd964_201405_05_30_toa_lw_emis_sea_fix.nflx'
# soc_file_sw = diag_dir + 'cd964_201405_05_30_toa_sw_emis_sea_fix.nflx'
soc_file_lw = diag_dir + 'cd964_201403_03_30_toa_lw_aer_spline_bias_fix_soc_surft_emis.nflx'
soc_file_sw = diag_dir + 'cd964_201403_03_30_toa_sw_aer_spline_bias_fix_soc_surft_emis.nflx'

soc_net_down_sw = soc_flux.load_soc_single_lev_data(soc_file_sw)
soc_net_down_lw = soc_flux.load_soc_single_lev_data(soc_file_lw)


soc_net_down_sw = soc_flux.edit_soc_coords(soc_net_down_sw, ukesm_lw_up)
soc_net_down_lw = soc_flux.edit_soc_coords(soc_net_down_lw, ukesm_lw_up)

soc_net_down_tot = soc_net_down_sw + soc_net_down_lw


diff_net_down_tot = soc_net_down_tot - ukesm_net_down_tot
diff_net_down_sw = soc_net_down_sw - ukesm_net_down_sw
diff_net_down_lw = soc_net_down_lw - ukesm_net_down_lw


### plotting
plot_dir = file_loc.plot_dir + 'socrates_plots/'

soc_flux.plot_flux_diff(diff_net_down_tot,
                   #      'SOC - ukesm control TOA net down total flux 201405 05-30 mean',
                   # plot_dir + 'soc-ukesm_control_toa_net_down_total_flux_201405_05_30_mean_all_sky_emis_sea_fix',
                                           'SOC - ukesm control TOA net down total flux 201403 03-30 mean',
                   plot_dir + 'soc-ukesm_control_toa_net_down_total_flux_201403_03_30_mean_all_sky_aer_spline_bias_fix_soc_surft_emis',
                    vmin=-80, vmax=80,
                   )

# soc_flux.plot_flux_diff(diff_net_down_sw,
#                         'SOC - ukesm control TOA net down SW flux 201405 05-30 mean',
#                    plot_dir + 'soc-ukesm_control_toa_net_down_sw_flux_201405_05_30_mean_all_sky_emis_sea_fix',
#                     vmin=-80, vmax=80,
#                    )

# soc_flux.plot_flux_diff(diff_net_down_lw,
#                         'SOC - ukesm control TOA net down LW flux 201405 05-30 mean',
#                    plot_dir + 'soc-ukesm_control_toa_net_down_lw_flux_201405_05_30_mean_all_sky_emis_sea_fix',
#                     vmin=-30, vmax=30,
#                    )


# Area means of diffs, dealing wth nans
area_mean_diff = flux_mod.area_mean_cube_nans(diff_net_down_tot)
area_mean_sw_diff = flux_mod.area_mean_cube_nans(diff_net_down_sw)
area_mean_lw_diff = flux_mod.area_mean_cube_nans(diff_net_down_lw)

print('area mean diff: ', area_mean_diff.data)
print('area mean sw diff: ', area_mean_sw_diff.data)
print('area mean lw diff: ', area_mean_lw_diff.data)












