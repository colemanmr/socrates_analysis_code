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

cd964_ukesm_file = diag_dir + 'cd964a.p620140529_all_clear_clearclean_fluxes.pp'
cm885_ukesm_file = diag_dir + 'cm885a.p620140529_all_clear_clearclean_fluxes.pp'


# Load ukesm fluxes
cd964_ukesm_sw_up, cd964_ukesm_sw_down,\
cd964_ukesm_lw_up, cd964_ukesm_lw_down,\
cd964_ukesm_clear_sw_up, cd964_ukesm_clear_sw_down,\
cd964_ukesm_clear_lw_up, cd964_ukesm_clear_lw_down,\
cd964_ukesm_clearclean_sw_up, cd964_ukesm_clearclean_sw_down,\
cd964_ukesm_clearclean_lw_up, cd964_ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(cd964_ukesm_file)

cm885_ukesm_sw_up, cm885_ukesm_sw_down,\
cm885_ukesm_lw_up, cm885_ukesm_lw_down,\
cm885_ukesm_clear_sw_up, cm885_ukesm_clear_sw_down,\
cm885_ukesm_clear_lw_up, cm885_ukesm_clear_lw_down,\
cm885_ukesm_clearclean_sw_up, cm885_ukesm_clearclean_sw_down,\
cm885_ukesm_clearclean_lw_up, cm885_ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(cm885_ukesm_file)


# Calculate UKESM net down fluxes
cd964_ukesm_net_down_sw, cd964_ukesm_net_down_lw, cd964_ukesm_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cd964_ukesm_sw_up, cd964_ukesm_sw_down, cd964_ukesm_lw_up)
cd964_ukesm_clear_net_down_sw, cd964_ukesm_clear_net_down_lw, cd964_ukesm_clear_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cd964_ukesm_clear_sw_up, cd964_ukesm_clear_sw_down, cd964_ukesm_clear_lw_up)
cd964_ukesm_clearclean_net_down_sw, cd964_ukesm_clearclean_net_down_lw, cd964_ukesm_clearclean_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cd964_ukesm_clearclean_sw_up, cd964_ukesm_clearclean_sw_down, cd964_ukesm_clearclean_lw_up)

cm885_ukesm_net_down_sw, cm885_ukesm_net_down_lw, cm885_ukesm_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cm885_ukesm_sw_up, cm885_ukesm_sw_down, cm885_ukesm_lw_up)
cm885_ukesm_clear_net_down_sw, cm885_ukesm_clear_net_down_lw, cm885_ukesm_clear_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cm885_ukesm_clear_sw_up, cm885_ukesm_clear_sw_down, cm885_ukesm_clear_lw_up)
cm885_ukesm_clearclean_net_down_sw, cm885_ukesm_clearclean_net_down_lw, cm885_ukesm_clearclean_net_down_total =\
soc_flux.ukesm_net_down_fluxes(cm885_ukesm_clearclean_sw_up, cm885_ukesm_clearclean_sw_down, cm885_ukesm_clearclean_lw_up)


ukesm_diff_net_down_sw_toa = cd964_ukesm_net_down_sw[85] - cm885_ukesm_net_down_sw[85]
ukesm_diff_net_down_lw_toa = cd964_ukesm_net_down_lw[85] - cm885_ukesm_net_down_lw[85]
ukesm_diff_net_down_total_toa = cd964_ukesm_net_down_total[85] - cm885_ukesm_net_down_total[85]

ukesm_diff_clear_net_down_sw_toa = cd964_ukesm_clear_net_down_sw[85] - cm885_ukesm_clear_net_down_sw[85]
ukesm_diff_clear_net_down_lw_toa = cd964_ukesm_clear_net_down_lw[85] - cm885_ukesm_clear_net_down_lw[85]
ukesm_diff_clear_net_down_total_toa = cd964_ukesm_clear_net_down_total[85] - cm885_ukesm_clear_net_down_total[85]

ukesm_diff_clearclean_net_down_sw_toa = cd964_ukesm_clearclean_net_down_sw[85] - cm885_ukesm_clearclean_net_down_sw[85]
ukesm_diff_clearclean_net_down_lw_toa = cd964_ukesm_clearclean_net_down_lw[85] - cm885_ukesm_clearclean_net_down_lw[85]
ukesm_diff_clearclean_net_down_total_toa = cd964_ukesm_clearclean_net_down_total[85] - cm885_ukesm_clearclean_net_down_total[85]


# Load socrates flux cubes for each suite
sky_types = ['', 'clear_sky_', 'clearclean_sky_']

cd964_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '20140529', 'toa', 'szen_fix.nflx',\
                                        cd964_ukesm_sw_up)

cm885_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cm885',\
                                        '20140529', 'toa', 'szen_fix.nflx',\
                                        cd964_ukesm_sw_up)
    
# Extract cubes from the lists
cd964_soc_net_down_sw_toa, cd964_soc_net_down_lw_toa,\
cd964_soc_clear_net_down_sw_toa, cd964_soc_clear_net_down_lw_toa,\
cd964_soc_clearclean_net_down_sw_toa, cd964_soc_clearclean_net_down_lw_toa =\
cd964_soc_cubes

cm885_soc_net_down_sw_toa, cm885_soc_net_down_lw_toa,\
cm885_soc_clear_net_down_sw_toa, cm885_soc_clear_net_down_lw_toa,\
cm885_soc_clearclean_net_down_sw_toa, cm885_soc_clearclean_net_down_lw_toa =\
cm885_soc_cubes

# Calculate SOCRATES total (sw + lw) net down fluxes
cd964_soc_net_down_total_toa = cd964_soc_net_down_sw_toa + cd964_soc_net_down_lw_toa
cd964_soc_clear_net_down_total_toa = cd964_soc_clear_net_down_sw_toa + cd964_soc_clear_net_down_lw_toa
cd964_soc_clearclean_net_down_total_toa = cd964_soc_clearclean_net_down_sw_toa + \
    cd964_soc_clearclean_net_down_lw_toa
    
cm885_soc_net_down_total_toa = cm885_soc_net_down_sw_toa + cm885_soc_net_down_lw_toa
cm885_soc_clear_net_down_total_toa = cm885_soc_clear_net_down_sw_toa + cm885_soc_clear_net_down_lw_toa
cm885_soc_clearclean_net_down_total_toa = cm885_soc_clearclean_net_down_sw_toa + \
    cm885_soc_clearclean_net_down_lw_toa
    

# Calculate SOCRATES forcing
soc_diff_net_down_sw_toa = cd964_soc_net_down_sw_toa - cm885_soc_net_down_sw_toa
soc_diff_net_down_lw_toa = cd964_soc_net_down_lw_toa - cm885_soc_net_down_lw_toa
soc_diff_net_down_total_toa = cd964_soc_net_down_total_toa - cm885_soc_net_down_total_toa

soc_diff_clear_net_down_sw_toa = cd964_soc_clear_net_down_sw_toa - cm885_soc_clear_net_down_sw_toa
soc_diff_clear_net_down_lw_toa = cd964_soc_clear_net_down_lw_toa - cm885_soc_clear_net_down_lw_toa
soc_diff_clear_net_down_total_toa = cd964_soc_clear_net_down_total_toa - cm885_soc_clear_net_down_total_toa

soc_diff_clearclean_net_down_sw_toa = cd964_soc_clearclean_net_down_sw_toa - cm885_soc_clearclean_net_down_sw_toa
soc_diff_clearclean_net_down_lw_toa = cd964_soc_clearclean_net_down_lw_toa - cm885_soc_clearclean_net_down_lw_toa
soc_diff_clearclean_net_down_total_toa = cd964_soc_clearclean_net_down_total_toa - cm885_soc_clearclean_net_down_total_toa


# Dfferences the offline minus online forcing
soc_ukesm_diff_net_down_sw_toa = soc_diff_net_down_sw_toa - ukesm_diff_net_down_sw_toa
soc_ukesm_diff_net_down_lw_toa = soc_diff_net_down_lw_toa - ukesm_diff_net_down_lw_toa
soc_ukesm_diff_net_down_total_toa = soc_diff_net_down_total_toa - ukesm_diff_net_down_total_toa

soc_ukesm_diff_clear_net_down_sw_toa = soc_diff_clear_net_down_sw_toa - ukesm_diff_clear_net_down_sw_toa
soc_ukesm_diff_clear_net_down_lw_toa = soc_diff_clear_net_down_lw_toa - ukesm_diff_clear_net_down_lw_toa
soc_ukesm_diff_clear_net_down_total_toa = soc_diff_clear_net_down_total_toa - ukesm_diff_clear_net_down_total_toa

soc_ukesm_diff_clearclean_net_down_sw_toa = soc_diff_clearclean_net_down_sw_toa - ukesm_diff_clearclean_net_down_sw_toa
soc_ukesm_diff_clearclean_net_down_lw_toa = soc_diff_clearclean_net_down_lw_toa - ukesm_diff_clearclean_net_down_lw_toa
soc_ukesm_diff_clearclean_net_down_total_toa = soc_diff_clearclean_net_down_total_toa - ukesm_diff_clearclean_net_down_total_toa   

# plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_sw_toa, \
                'SOC - UKESM SU forcing TOA net down sw 20140529 all sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_20140529_all_sky_soc_szen_fix',\
                vmin = -125, vmax = 125\
                )
    
soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_lw_toa, \
                'SOC - UKESM SU forcing TOA net down lw 20140529 all sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_20140529_all_sky_soc_szen_fix',\
                vmin = -125, vmax = 125\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_net_down_total_toa, \
                'SOC - UKESM SU forcing TOA net down total 20140529 all sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_20140529_all_sky_soc_szen_fix',\
                vmin = -125, vmax = 125\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_sw_toa, \
                'SOC - UKESM SU forcing TOA net down sw 20140529 clear sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_20140529_clear_sky_soc_szen_fix',\
                vmin = -11, vmax = 11\
                )
    
soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_lw_toa, \
                'SOC - UKESM SU forcing TOA net down lw 20140529 clear sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_20140529_clear_sky_soc_szen_fix',\
                vmin = -11, vmax = 11\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_clear_net_down_total_toa, \
                'SOC - UKESM SU forcing TOA net down total 20140529 clear sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_20140529_clear_sky_soc_szen_fix',\
                vmin = -11, vmax = 11\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_sw_toa, \
                'SOC - UKESM SU forcing TOA net down sw 20140529 clearclean sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_sw_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
                vmin = -0.25, vmax = 0.25\
                )
    
soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_lw_toa, \
                'SOC - UKESM SU forcing TOA net down lw 20140529 clearclean sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_lw_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
                vmin = -9, vmax = 9\
                )

soc_flux.plot_flux_diff(soc_ukesm_diff_clearclean_net_down_total_toa, \
                'SOC - UKESM SU forcing TOA net down total 20140529 clearclean sky szen fix',\
                plot_dir + 'forcing_soc-ukesm_su_net_total_down_toa_map_20140529_clearclean_sky_soc_szen_fix',\
                vmin = -9, vmax = 9\
                )


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



    
