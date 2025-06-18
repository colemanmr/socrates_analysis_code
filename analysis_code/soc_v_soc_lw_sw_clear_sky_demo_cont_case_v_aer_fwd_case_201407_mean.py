#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:45:56 2022

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


# Set different socrates cases data filenames
file_soc_toa_lw_cont = file_loc.diag_dir + '/socrates_diags/bc_prp_1year_clear_sky_cont_201407_toa_lw.nflx'
file_soc_toa_sw_cont = file_loc.diag_dir + '/socrates_diags/bc_prp_1year_clear_sky_cont_201407_toa_sw.nflx'

file_soc_toa_lw_aer_fwd = file_loc.diag_dir + '/socrates_diags/bc_prp_1year_clear_sky_aer_fwd_201407_toa_lw.nflx'
file_soc_toa_sw_aer_fwd = file_loc.diag_dir + '/socrates_diags/bc_prp_1year_clear_sky_aer_fwd_201407_toa_sw.nflx'

# Load data - zero index is to remove the redundant pressure dimension
soc_toa_lw_cont = iris.load_cube(file_soc_toa_lw_cont)[0]
soc_toa_sw_cont = iris.load_cube(file_soc_toa_sw_cont)[0]

soc_toa_lw_aer_fwd = iris.load_cube(file_soc_toa_lw_aer_fwd)[0]
soc_toa_sw_aer_fwd = iris.load_cube(file_soc_toa_sw_aer_fwd)[0]


# # add units
# soc_toa_sw.units = 'W m-2'
# soc_toa_lw.units = 'W m-2'

# load ukesm data for coordinate system altering
file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964_20140701_toa_fluxes.pp'
ukesm_data = iris.load(file_ukesm_data,['downwelling_shortwave_flux_in_air'])

# Set socrates data lat and long same as in ukesm data
# Note: adding the ukesm dimension for lon auto corrects for meridian start
ukesm_longitude = ukesm_data[0].coord('longitude')
ukesm_latitude = ukesm_data[0].coord('latitude')

# define function for changing coords to another cube's coords
def coord_change(cube, new_lon, new_lat):
    """Replaces a cube's coords with new lat and lon.
    Note replaces the  input cube's coordinates, doesn't create a new cube.
    Also must check coords have correct index, currently hardcoded."""
    
    cube.remove_coord('longitude')
    cube.remove_coord('latitude')
    
    # assumes index 1 for lon and 0 for lat
    cube.add_dim_coord(new_lon, 1)
    cube.add_dim_coord(new_lat, 0)

coord_change(soc_toa_sw_cont, ukesm_longitude, ukesm_latitude)
coord_change(soc_toa_lw_cont, ukesm_longitude, ukesm_latitude)
coord_change(soc_toa_sw_aer_fwd, ukesm_longitude, ukesm_latitude)
coord_change(soc_toa_lw_aer_fwd, ukesm_longitude, ukesm_latitude)


# Calc net soc flux
soc_toa_net_cont = soc_toa_sw_cont + soc_toa_lw_cont
soc_toa_net_aer_fwd = soc_toa_sw_aer_fwd + soc_toa_lw_aer_fwd


# Difference the two datasets
# net_diff = soc_toa_net - ukesm_net_toa
# net_diff_sw = soc_toa_sw - ukesm_net_toa_sw
# net_diff_lw = soc_toa_lw - ukesm_net_toa_lw
net_diff = soc_toa_net_cont - soc_toa_net_aer_fwd
net_diff_sw = soc_toa_sw_cont - soc_toa_sw_aer_fwd
net_diff_lw = soc_toa_lw_cont - soc_toa_lw_aer_fwd

### Plotting ###
plot_dir = file_loc.plot_dir + 'socrates_plots/'
plt.tight_layout()

# # socrates cont plot
# plt.figure()
# plt.title('SOCRATES TOA net down flux 201407 prp bc demo cont case clear')
# mesh = iplt.pcolormesh(soc_toa_net_aer_fwd, vmin = -250, vmax = 250, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_flux_toa_map_201407_soc_prp_bc_demo_cont_case_clear.png', dpi = 300)
# plt.show()

# # socrates cont plot sw
# plt.figure()
# plt.title('SOCRATES TOA sw net down flux 201407 prp bc demo cont case clear')
# mesh = iplt.pcolormesh(soc_toa_sw_aer_fwd, vmin = 0, vmax = 450, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'sw_down_flux_toa_map_201407_soc_prp_bc_demo_cont_case_clear.png', dpi = 300)
# plt.show()

# # socrates cont plot lw
# plt.figure()
# plt.title('SOCRATES TOA lw net down flux 201407 prp bc demo cont case clear')
# mesh = iplt.pcolormesh(soc_toa_lw_aer_fwd, vmin = -400, vmax = -50, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'lw_down_flux_toa_map_201407_soc_prp_bc_demo_cont_case_clear.png', dpi = 300)
# plt.show()

# # socrates aer_fwd plot
# plt.figure()
# plt.title('SOCRATES TOA net down flux 201407 prp bc demo aer fwd case clear')
# mesh = iplt.pcolormesh(soc_toa_net_aer_fwd, vmin = -250, vmax = 250, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_flux_toa_map_201407_soc_prp_bc_demo_aer_fwd_case_clear.png', dpi = 300)
# plt.show()

# # socrates  aer_fwdplot sw
# plt.figure()
# plt.title('SOCRATES TOA sw net down flux 201407 prp bc demo aer fwd case clear')
# mesh = iplt.pcolormesh(soc_toa_sw_aer_fwd, vmin = 0, vmax = 450, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'sw_down_flux_toa_map_201407_soc_prp_bc_demo_aer_fwd_case_clear.png', dpi = 300)
# plt.show()

# # socrates aer_fwd plot lw
# plt.figure()
# plt.title('SOCRATES TOA lw net down flux 201407 prp bc demo aer fwd case clear')
# mesh = iplt.pcolormesh(soc_toa_lw_aer_fwd, vmin = -400, vmax = -50, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'lw_down_flux_toa_map_201407_soc_prp_bc_demo_aer_fwd_case_clear.png', dpi = 300)
# plt.show()
    
# difference plot
plt.figure()
# plt.title('TOA net down flux 201407 Socrates prp bc demo aer fwd case - UKESM cont clear')
mesh = iplt.pcolormesh(net_diff, vmin = -50, vmax = 50, cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.savefig(plot_dir + 'net_flux_toa_map_201407_soc_prp_bc_demo_cont-aer_fwd_case.png', dpi = 300)
plt.show()

# sw difference plot
plt.figure()
# plt.title('TOA sw net down flux 201407 Socrates prp bc demo aer fwd case - UKESM cont clear')
mesh = iplt.pcolormesh(net_diff_sw, vmin = -50, vmax = 50, cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.savefig(plot_dir + 'net_sw_flux_toa_map_201407_soc_prp_bc_demo_cont-aer_fwd_case.png', dpi = 300)
plt.show()

# lw difference plot
plt.figure()
# plt.title('TOA lw net down flux 201407 Socrates prp bc demo aer fwd case - UKESM cont clear')
mesh = iplt.pcolormesh(net_diff_lw, vmin = -50, vmax = 50, cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
current_map = plt.gca()
current_map.coastlines(linewidth = 1)
plt.savefig(plot_dir + 'net_lw_flux_toa_map_201407_soc_prp_bc_demo_cont-aer_fwd_case.png', dpi = 300)
plt.show()


# # Print nans number (shape)
# print('sw nans: ', np.shape(np.where(np.isnan(net_diff_sw.data))))
# print('lw nans: ', np.shape(np.where(np.isnan(net_diff_lw.data))))


# # Area means of diffs, dealing wth nans
# area_mean_diff = flux_mod.area_mean_cube_nans(net_diff)
# area_mean_sw_diff = flux_mod.area_mean_cube_nans(net_diff_sw)
# area_mean_lw_diff = flux_mod.area_mean_cube_nans(net_diff_lw)

# print('area mean diff: ', area_mean_diff.data)
# print('area mean sw diff: ', area_mean_sw_diff.data)
# print('area mean lw diff: ', area_mean_lw_diff.data)

