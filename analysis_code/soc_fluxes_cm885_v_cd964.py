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

ukesm_file = diag_dir + 'cm885a.p620140529_all_clear_clearclean_fluxes.pp'


# Load ukesm fluxes - only for converting coords of socrates cubes
ukesm_sw_up, ukesm_sw_down,\
ukesm_lw_up, ukesm_lw_down,\
ukesm_clear_sw_up, ukesm_clear_sw_down,\
ukesm_clear_lw_up, ukesm_clear_lw_down,\
ukesm_clearclean_sw_up, ukesm_clearclean_sw_down,\
ukesm_clearclean_lw_up, ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(ukesm_file)


# Load socrates flux cubes for each suite
sky_types = ['', 'clear_sky_', 'clearclean_sky_']

cd964_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '20140529', 'toa', 'szen_fix.nflx',\
                                        ukesm_sw_up)

cm885_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cm885',\
                                        '20140529', 'toa', 'szen_fix.nflx',\
                                        ukesm_sw_up)
    
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
    

# Calculate differences'
diff_net_down_sw_toa = cd964_soc_net_down_sw_toa - cm885_soc_net_down_sw_toa
diff_net_down_lw_toa = cd964_soc_net_down_lw_toa - cm885_soc_net_down_lw_toa
diff_net_down_total_toa = cd964_soc_net_down_total_toa - cm885_soc_net_down_total_toa
    

# plotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux_diff(diff_net_down_sw_toa, \
               'Socrates SU forcing TOA net down sw 20140529 all sky szen fix',\
               plot_dir + 'forcing_su_cd964-cm885_net_sw_down_toa_map_20140529_soc_szen_fix',\
               vmin = 0, vmax = 0\
               )
    
soc_flux.plot_flux_diff(diff_net_down_lw_toa, \
               'Socrates SU forcing TOA net down lw 20140529 all sky szen fix',\
               plot_dir + 'forcing_su_cd964-cm885_net_lw_down_toa_map_20140529_soc_szen_fix',\
               vmin = 0, vmax = 0\
               )

soc_flux.plot_flux_diff(diff_net_down_total_toa, \
               'Socrates SU forcing TOA net down total 20140529 all sky szen fix',\
               plot_dir + 'forcing_su_cd964-cm885_net_total_down_toa_map_20140529_soc_szen_fix',\
               vmin = 0, vmax = 0\
               )



    
