#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 11:02:14 2022

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

ukesm_file = diag_dir + 'cm885a.p620140529_all_clear_clearclean_fluxes.pp'

# Load ukesm fluxes, all, clear and clearclean
ukesm_sw_up, ukesm_sw_down,\
ukesm_lw_up, ukesm_lw_down,\
ukesm_clear_sw_up, ukesm_clear_sw_down,\
ukesm_clear_lw_up, ukesm_clear_lw_down,\
ukesm_clearclean_sw_up, ukesm_clearclean_sw_down,\
ukesm_clearclean_lw_up, ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(ukesm_file)


# Calculate net down fluxes for ukesm all, clear, clearclean fluxes
ukesm_net_down_sw, ukesm_net_down_lw, ukesm_net_down =\
   soc_flux.ukesm_net_down_fluxes(ukesm_sw_up, ukesm_sw_down, ukesm_lw_up)
ukesm_clear_net_down_sw, ukesm_clear_net_down_lw, ukesm_clear_net_down =\
    soc_flux.ukesm_net_down_fluxes(ukesm_clear_sw_up, ukesm_clear_sw_down, ukesm_clear_lw_up)
ukesm_clearclean_net_down_sw, ukesm_clearclean_net_down_lw, ukesm_clearclean_net_down =\
    soc_flux.ukesm_net_down_fluxes(ukesm_clearclean_sw_up, ukesm_clearclean_sw_down, ukesm_clearclean_lw_up)
    

# Load socrates flux cubes
sky_types = ['', 'clear_sky_', 'clearclean_sky_']
soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cm885',\
                                        '20140529', 'toa', 'szen_fix.nflx',\
                                        ukesm_sw_up)

# Extract cubes from the list
soc_net_down_sw_toa, soc_net_down_lw_toa,\
soc_clear_net_down_sw_toa, soc_clear_net_down_lw_toa,\
soc_clearclean_net_down_sw_toa, soc_clearclean_net_down_lw_toa =\
soc_cubes


# Calculate SOCRATES total (sw + lw) net down fluxes
soc_net_down_toa = soc_net_down_sw_toa + soc_net_down_lw_toa
soc_clear_net_down_toa = soc_clear_net_down_sw_toa + soc_clear_net_down_lw_toa
soc_clearclean_net_down_toa = soc_clearclean_net_down_sw_toa + \
    soc_clearclean_net_down_lw_toa
    

# Difference the SOCRATES minus UKESM fluxes
diff_net_down_sw_toa = soc_net_down_sw_toa - ukesm_net_down_sw[85]
diff_net_down_lw_toa = soc_net_down_lw_toa - ukesm_net_down_lw[85]

diff_clear_net_down_sw_toa = soc_clear_net_down_sw_toa - ukesm_clear_net_down_sw[85]
diff_clear_net_down_lw_toa = soc_clear_net_down_lw_toa - ukesm_clear_net_down_lw[85]

diff_clearclean_net_down_sw_toa = soc_clearclean_net_down_sw_toa - ukesm_clearclean_net_down_sw[85]
diff_clearclean_net_down_lw_toa = soc_clearclean_net_down_lw_toa - ukesm_clearclean_net_down_lw[85]


# Plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux_diff(diff_net_down_sw_toa, \
               'SU pert TOA net down sw flux SOC - UKESM 20140529 all sky szen fix',\
               plot_dir + 'cm885_net_sw_down_flux_toa_map_20140529_soc-ukesm_szen_fix',\
               vmin = -80, vmax = 80\
               )

soc_flux.plot_flux_diff(diff_net_down_lw_toa, \
               'SU pert TOA net down lw flux SOC - UKESM 20140529 all sky szen fix',\
               plot_dir + 'cm885_net_lw_down_flux_toa_map_20140529_soc-ukesm_szen_fix',\
               vmin = -50, vmax = 50\
               )

soc_flux.plot_flux_diff(diff_clear_net_down_sw_toa, \
               'SU pert TOA net down sw flux SOC - UKESM 20140529 clear sky szen fix',\
               plot_dir + 'cm885_net_sw_down_flux_toa_map_20140529_soc-ukesm_szen_fix_clear',\
               vmin = -5, vmax = 5\
               )

soc_flux.plot_flux_diff(diff_clear_net_down_lw_toa, \
               'SU pert TOA net down lw flux SOC - UKESM 20140529 clear sky szen fix',\
               plot_dir + 'cm885_net_lw_down_flux_toa_map_20140529_soc-ukesm_szen_fix_clear',\
               vmin = -20, vmax = 20\
               )
    
soc_flux.plot_flux_diff(diff_clearclean_net_down_sw_toa, \
               'SU pert TOA net down sw flux SOC - UKESM 20140529 clearclean sky szen fix',\
               plot_dir + 'cm885_net_sw_down_flux_toa_map_20140529_soc-ukesm_szen_fix_clearclean',\
               vmin = -1, vmax = 1\
               )

soc_flux.plot_flux_diff(diff_clearclean_net_down_lw_toa, \
               'SU pert TOA net down lw flux SOC - UKESM 20140529 clearclean sky szen fix',\
               plot_dir + 'cm885_net_lw_down_flux_toa_map_20140529_soc-ukesm_szen_fix_clearclean',\
               vmin = -10, vmax = 10\
               )
    
    
# # Extra plot to check nans presence in cm885 data - Yes is the answer!
# soc_flux.plot_flux(soc_net_down_lw_toa, \
#                'SU pert TOA net down lw flux SOC 20140529 all sky szen fix',\
#                plot_dir + 'cm885_net_lw_down_flux_toa_map_20140529_soc_szen_fix',\
#                vmin = 0, vmax = 0\
#                )