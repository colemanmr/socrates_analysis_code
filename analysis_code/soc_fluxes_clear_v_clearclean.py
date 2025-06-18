#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 13:18:43 2022

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


# Load ukesm fluxes to use as template for socrates function
cd964_ukesm_sw_up, cd964_ukesm_sw_down,\
cd964_ukesm_lw_up, cd964_ukesm_lw_down,\
cd964_ukesm_clear_sw_up, cd964_ukesm_clear_sw_down,\
cd964_ukesm_clear_lw_up, cd964_ukesm_clear_lw_down,\
cd964_ukesm_clearclean_sw_up, cd964_ukesm_clearclean_sw_down,\
cd964_ukesm_clearclean_lw_up, cd964_ukesm_clearclean_lw_down=\
soc_flux.load_ukesm_data(cd964_ukesm_file)


# Load socrates flux cubes
sky_types = ['',\
             'clear_sky_',\
                 'clearclean_sky_'\
                 ]

cd964_soc_cubes = soc_flux.load_soc_flux_multi(sky_types, diag_dir, 'cd964',\
                                        '20140529', 'toa',\
                                        'emis_sea_fix.nflx',\
                                        cd964_ukesm_sw_up)

# Extract cubes from the lists
cd964_soc_net_down_sw_toa, cd964_soc_net_down_lw_toa,\
cd964_soc_clear_net_down_sw_toa, cd964_soc_clear_net_down_lw_toa,\
cd964_soc_clearclean_net_down_sw_toa, cd964_soc_clearclean_net_down_lw_toa =\
cd964_soc_cubes


# Calculate SOCRATES total (sw + lw) net down fluxes
cd964_soc_net_down_total_toa = cd964_soc_net_down_sw_toa + cd964_soc_net_down_lw_toa
cd964_soc_clear_net_down_total_toa = cd964_soc_clear_net_down_sw_toa + cd964_soc_clear_net_down_lw_toa
cd964_soc_clearclean_net_down_total_toa = cd964_soc_clearclean_net_down_sw_toa + \
    cd964_soc_clearclean_net_down_lw_toa


# Calculate difference clear - clearclean
diff_sw = cd964_soc_clear_net_down_sw_toa - cd964_soc_clearclean_net_down_sw_toa
diff_lw = cd964_soc_clear_net_down_lw_toa - cd964_soc_clearclean_net_down_lw_toa



# PLotting
plot_dir = file_loc.plot_dir  + 'socrates_plots/'

soc_flux.plot_flux(diff_sw,
                   'SOC control clear minus clearclean TOA net down SW flux 20140529',
                   plot_dir + 'soc_cont_clear-clearclean_toa_net_down_sw_flux_20140529',
                   vmin=-60, vmax=60,
                   )

soc_flux.plot_flux(diff_lw,
                   'SOC control clear minus clearclean TOA net down LW flux 20140529',
                   plot_dir + 'soc_cont_clear-clearclean_toa_net_down_lw_flux_20140529',
                   vmin=-25, vmax=25,
                   )




























