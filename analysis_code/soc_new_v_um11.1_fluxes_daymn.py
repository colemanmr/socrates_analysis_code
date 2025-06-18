#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:13:05 2022

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

# Load ukesm cube to use for offline SOC cube loading
cd964_ukesm_file = diag_dir + 'cd964a.p620140529_all_clear_clearclean_fluxes.pp'

cd964_ukesm_sw_up, cd964_ukesm_sw_down,\
cd964_ukesm_lw_up, cd964_ukesm_lw_down,\
cd964_ukesm_clear_sw_up, cd964_ukesm_clear_sw_down,\
cd964_ukesm_clear_lw_up, cd964_ukesm_clear_lw_down,\
cd964_ukesm_clearclean_sw_up, cd964_ukesm_clearclean_sw_down,\
cd964_ukesm_clearclean_lw_up, cd964_ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(cd964_ukesm_file)


# Load socrates flux cubes
sky_types = ['',\
             'clear_sky_', 'clearclean_sky_'\
                 ]

new_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '20140529', 'toa',\
                                        'emis_sea_fix_latest_soc.nflx',\
                                        cd964_ukesm_sw_up)
old_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '20140529', 'toa',\
                                        'emis_sea_fix.nflx',\
                                        cd964_ukesm_sw_up)
    
# Extract cubes from the lists
new_soc_net_down_sw_toa, new_soc_net_down_lw_toa,\
new_soc_clear_net_down_sw_toa, new_soc_clear_net_down_lw_toa,\
new_soc_clearclean_net_down_sw_toa, new_soc_clearclean_net_down_lw_toa =\
new_soc_cubes

old_soc_net_down_sw_toa, old_soc_net_down_lw_toa,\
old_soc_clear_net_down_sw_toa, old_soc_clear_net_down_lw_toa,\
old_soc_clearclean_net_down_sw_toa, old_soc_clearclean_net_down_lw_toa =\
old_soc_cubes

# Calculate SOCRATES total (sw + lw) net down fluxes
new_soc_net_down_total_toa = new_soc_net_down_sw_toa + new_soc_net_down_lw_toa
new_soc_clear_net_down_total_toa = new_soc_clear_net_down_sw_toa + new_soc_clear_net_down_lw_toa
new_soc_clearclean_net_down_total_toa = new_soc_clearclean_net_down_sw_toa + \
    new_soc_clearclean_net_down_lw_toa
    
old_soc_net_down_total_toa = old_soc_net_down_sw_toa + old_soc_net_down_lw_toa
old_soc_clear_net_down_total_toa = old_soc_clear_net_down_sw_toa + old_soc_clear_net_down_lw_toa
old_soc_clearclean_net_down_total_toa = old_soc_clearclean_net_down_sw_toa + \
    old_soc_clearclean_net_down_lw_toa
    

# Calculate differences
total_diff = new_soc_net_down_total_toa - old_soc_net_down_total_toa
sw_diff = new_soc_net_down_sw_toa - old_soc_net_down_sw_toa
lw_diff = new_soc_net_down_lw_toa - old_soc_net_down_lw_toa
total_diff_clear = new_soc_clear_net_down_total_toa - old_soc_clear_net_down_total_toa
sw_diff_clear = new_soc_clear_net_down_sw_toa - old_soc_clear_net_down_sw_toa
lw_diff_clear = new_soc_clear_net_down_lw_toa - old_soc_clear_net_down_lw_toa
total_diff_clearclean = new_soc_clearclean_net_down_total_toa - old_soc_clearclean_net_down_total_toa
sw_diff_clearclean = new_soc_clearclean_net_down_sw_toa - old_soc_clearclean_net_down_sw_toa
lw_diff_clearclean = new_soc_clearclean_net_down_lw_toa - old_soc_clearclean_net_down_lw_toa


# PLotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux_diff(total_diff,\
                        'SOC new (r1255) minus old control net down total flux 20140529 all sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_total_flux_20140529_all_sky_emis_sea_fix',
                        vmin = -60, vmax = 60,
                        )
soc_flux.plot_flux_diff(sw_diff,\
                        'SOC new (r1255) minus old control net down sw flux 20140529 all sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_sw_flux_20140529_all_sky_emis_sea_fix',
                        vmin =-60, vmax = 60,
                        )
soc_flux.plot_flux_diff(lw_diff,\
                        'SOC new (r1255) minus old control net down lw flux 20140529 all sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_lw_flux_20140529_all_sky_emis_sea_fix',
                        vmin =-6, vmax = 6,
                        )
soc_flux.plot_flux_diff(total_diff_clear,\
                        'SOC new (r1255) minus old control net down total flux 20140529 clear sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_total_flux_20140529_clear_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )
soc_flux.plot_flux_diff(sw_diff_clear,\
                        'SOC new (r1255) minus old control net down sw flux 20140529 clear sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_sw_flux_20140529_clear_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )
soc_flux.plot_flux_diff(lw_diff_clear,\
                        'SOC new (r1255) minus old control net down lw flux 20140529 clear sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_lw_flux_20140529_clear_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )
soc_flux.plot_flux_diff(total_diff_clearclean,\
                        'SOC new (r1255) minus old control net down total flux 20140529 clearclean sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_total_flux_20140529_clearclean_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )
soc_flux.plot_flux_diff(sw_diff_clearclean,\
                        'SOC new (r1255) minus old control net down sw flux 20140529 clearclean sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_sw_flux_20140529_clearclean_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )
soc_flux.plot_flux_diff(lw_diff_clearclean,\
                        'SOC new (r1255) minus old control net down lw flux 20140529 clearclean sky emis sea fix',\
                        plot_dir + 'flux_diff_r1255-r469_soc_cont_net_down_lw_flux_20140529_clearclean_sky_emis_sea_fix',
                        vmin =-0.1, vmax = 0.1,
                        )