#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:21:41 2022

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



cd964_ukesm_file = diag_dir + 'cd964a.p6201403_03_30_all_sky_fluxes.pp'
cm885_ukesm_file = diag_dir + 'cm885a.p6201403_03_30_all_sky_fluxes.pp'

cd964_ukesm_cubes = iris.load(cd964_ukesm_file)
cm885_ukesm_cubes = iris.load(cm885_ukesm_file)

cd964_ukesm_lw_up_days = cd964_ukesm_cubes[2][:,85]
cd964_ukesm_sw_down_days = cd964_ukesm_cubes[1][:,85]
cd964_ukesm_sw_up_days = cd964_ukesm_cubes[3][:,85]


cd964_ukesm_lw_up,_,_ = flux_mod.time_mean_cube(cd964_ukesm_lw_up_days)
cd964_ukesm_sw_up,_,_ = flux_mod.time_mean_cube(cd964_ukesm_sw_up_days)
cd964_ukesm_sw_down,_,_ = flux_mod.time_mean_cube(cd964_ukesm_sw_down_days)

cd964_ukesm_net_down_sw, cd964_ukesm_net_down_lw, cd964_ukesm_net_down_tot =\
    soc_flux.ukesm_net_down_fluxes(cd964_ukesm_sw_up, cd964_ukesm_sw_down, cd964_ukesm_lw_up)
    

cm885_ukesm_lw_up_days = cm885_ukesm_cubes[2][:,85]
cm885_ukesm_sw_down_days = cm885_ukesm_cubes[1][:,85]
cm885_ukesm_sw_up_days = cm885_ukesm_cubes[3][:,85]


cm885_ukesm_lw_up,_,_ = flux_mod.time_mean_cube(cm885_ukesm_lw_up_days)
cm885_ukesm_sw_up,_,_ = flux_mod.time_mean_cube(cm885_ukesm_sw_up_days)
cm885_ukesm_sw_down,_,_ = flux_mod.time_mean_cube(cm885_ukesm_sw_down_days)

cm885_ukesm_net_down_sw, cm885_ukesm_net_down_lw, cm885_ukesm_net_down_tot =\
    soc_flux.ukesm_net_down_fluxes(cm885_ukesm_sw_up, cm885_ukesm_sw_down, cm885_ukesm_lw_up)
    

ukesm_diff_net_down_sw_toa = cd964_ukesm_net_down_sw - cm885_ukesm_net_down_sw
ukesm_diff_net_down_lw_toa = cd964_ukesm_net_down_lw - cm885_ukesm_net_down_lw
ukesm_diff_net_down_total_toa = cd964_ukesm_net_down_tot - cm885_ukesm_net_down_tot


    
# Load socrates flux cubes for each suite
sky_types = ['']

cd964_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '201403_03_30', 'toa', 'aer_spline_bias_fix_soc_surft_emis.nflx',\
                                        cd964_ukesm_sw_up)

cm885_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cm885',\
                                        '201403_03_30', 'toa', 'aer_spline_bias_fix_soc_surft_emis.nflx',\
                                        cd964_ukesm_sw_up)
    
# Extract cubes from the lists
cd964_soc_net_down_sw_toa, cd964_soc_net_down_lw_toa =\
cd964_soc_cubes

cm885_soc_net_down_sw_toa, cm885_soc_net_down_lw_toa =\
cm885_soc_cubes

# Calculate SOCRATES total (sw + lw) net down fluxes
cd964_soc_net_down_total_toa = cd964_soc_net_down_sw_toa + cd964_soc_net_down_lw_toa
# cd964_soc_clear_net_down_total_toa = cd964_soc_clear_net_down_sw_toa + cd964_soc_clear_net_down_lw_toa
# cd964_soc_clearclean_net_down_total_toa = cd964_soc_clearclean_net_down_sw_toa + \
#     cd964_soc_clearclean_net_down_lw_toa
    
cm885_soc_net_down_total_toa = cm885_soc_net_down_sw_toa + cm885_soc_net_down_lw_toa
# cm885_soc_clear_net_down_total_toa = cm885_soc_clear_net_down_sw_toa + cm885_soc_clear_net_down_lw_toa
# cm885_soc_clearclean_net_down_total_toa = cm885_soc_clearclean_net_down_sw_toa + \
#     cm885_soc_clearclean_net_down_lw_toa
    

# Calculate SOCRATES forcing
soc_diff_net_down_sw_toa = cd964_soc_net_down_sw_toa - cm885_soc_net_down_sw_toa
soc_diff_net_down_lw_toa = cd964_soc_net_down_lw_toa - cm885_soc_net_down_lw_toa
soc_diff_net_down_total_toa = cd964_soc_net_down_total_toa - cm885_soc_net_down_total_toa

# soc_diff_clear_net_down_sw_toa = cd964_soc_clear_net_down_sw_toa - cm885_soc_clear_net_down_sw_toa
# soc_diff_clear_net_down_lw_toa = cd964_soc_clear_net_down_lw_toa - cm885_soc_clear_net_down_lw_toa
# soc_diff_clear_net_down_total_toa = cd964_soc_clear_net_down_total_toa - cm885_soc_clear_net_down_total_toa

# soc_diff_clearclean_net_down_sw_toa = cd964_soc_clearclean_net_down_sw_toa - cm885_soc_clearclean_net_down_sw_toa
# soc_diff_clearclean_net_down_lw_toa = cd964_soc_clearclean_net_down_lw_toa - cm885_soc_clearclean_net_down_lw_toa
# soc_diff_clearclean_net_down_total_toa = cd964_soc_clearclean_net_down_total_toa - cm885_soc_clearclean_net_down_total_toa


# Dfferences the offline minus online forcing
soc_ukesm_diff_net_down_sw_toa = soc_diff_net_down_sw_toa - ukesm_diff_net_down_sw_toa
soc_ukesm_diff_net_down_lw_toa = soc_diff_net_down_lw_toa - ukesm_diff_net_down_lw_toa
soc_ukesm_diff_net_down_total_toa = soc_diff_net_down_total_toa - ukesm_diff_net_down_total_toa

# soc_ukesm_diff_clear_net_down_sw_toa = soc_diff_clear_net_down_sw_toa - ukesm_diff_clear_net_down_sw_toa
# soc_ukesm_diff_clear_net_down_lw_toa = soc_diff_clear_net_down_lw_toa - ukesm_diff_clear_net_down_lw_toa
# soc_ukesm_diff_clear_net_down_total_toa = soc_diff_clear_net_down_total_toa - ukesm_diff_clear_net_down_total_toa

# soc_ukesm_diff_clearclean_net_down_sw_toa = soc_diff_clearclean_net_down_sw_toa - ukesm_diff_clearclean_net_down_sw_toa
# soc_ukesm_diff_clearclean_net_down_lw_toa = soc_diff_clearclean_net_down_lw_toa - ukesm_diff_clearclean_net_down_lw_toa
# soc_ukesm_diff_clearclean_net_down_total_toa = soc_diff_clearclean_net_down_total_toa - ukesm_diff_clearclean_net_down_total_toa   

# plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_sw_toa, \
                'SOC - UKESM SU forcing TOA net down sw 201403_03-30 all sky final',\
                plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_201403_03_30_aer_spline_bias_fix_soc_surft_emis',\
                vmin = -30, vmax = 30\
                )
    
soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_lw_toa, \
                'SOC - UKESM SU forcing TOA net down lw 201403_03-30 all sky final',\
                plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_201403_03_30_aer_spline_bias_fix_soc_surft_emis',\
                vmin = -30, vmax = 30\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_total_toa, \
                'SOC - UKESM SU forcing TOA net down total 201403_03-30 all sky final',\
                plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_201403_03_30_aer_spline_bias_fix_soc_surft_emis',\
                vmin = -30, vmax = 30\
                )

# soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_sw_toa, \
#                 'SOC - UKESM SU forcing TOA net down sw 20140529 clear sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_20140529_clear_sky_soc_szen_fix',\
#                 vmin = -11, vmax = 11\
#                 )
    
# soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_lw_toa, \
#                 'SOC - UKESM SU forcing TOA net down lw 20140529 clear sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_20140529_clear_sky_soc_szen_fix',\
#                 vmin = -11, vmax = 11\
#                 )

# soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_total_toa, \
#                 'SOC - UKESM SU forcing TOA net down total 20140529 clear sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_20140529_clear_sky_soc_szen_fix',\
#                 vmin = -11, vmax = 11\
#                 )

# soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_sw_toa, \
#                 'SOC - UKESM SU forcing TOA net down sw 20140529 clearclean sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
#                 vmin = -0.25, vmax = 0.25\
#                 )
    
# soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_lw_toa, \
#                 'SOC - UKESM SU forcing TOA net down lw 20140529 clearclean sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
#                 vmin = -9, vmax = 9\
#                 )

# soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_total_toa, \
#                 'SOC - UKESM SU forcing TOA net down total 20140529 clearclean sky szen fix',\
#                 plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
#                 vmin = -9, vmax = 9\
#                 )


# soc_flux.plot_flux_diff(diff_net_down_sw_toa, \
#                'Socrates SU forcing TOA net down sw 20140529 all sky szen fix',\
#                plot_dir + 'forcing_su_cd964-cm885_net_sw_down_toa_map_20140529_soc_szen_fix',\
#                vmin = 0, vmax = 0\
#                )
    
# soc_flux.plot_flux_diff(diff_net_down_lw_toa, \
#                'Socrates SU forcing TOA net down lw 20140529 all sky szen fix',\
#                plot_dir + 'forcing_su_cd964-cm885_net_lw_down_toa_map_20140529_soc_szen_fix',\
#                vmin = 0, vmax = 0\
#                )

# soc_flux.plot_flux_diff(diff_net_down_total_toa, \
#                'Socrates SU forcing TOA net down total 20140529 all sky szen fix',\
#                plot_dir + 'forcing_su_cd964-cm885_net_total_down_toa_map_20140529_soc_szen_fix',\
#                vmin = 0, vmax = 0\
#                )



# Area means of diffs, dealing wth nans
area_mean_sw_diff = flux_mod.area_mean_cube_nans(soc_ukesm_diff_net_down_sw_toa)
area_mean_lw_diff = flux_mod.area_mean_cube_nans(soc_ukesm_diff_net_down_lw_toa)
area_mean_diff = flux_mod.area_mean_cube_nans(soc_ukesm_diff_net_down_total_toa)

print('area mean diff: ', area_mean_diff.data)
print('area mean sw diff: ', area_mean_sw_diff.data)
print('area mean lw diff: ', area_mean_lw_diff.data)
    
