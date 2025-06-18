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


# Set UKESM and socrates data filenames
# file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964a.p620140529_daymn_flux.pp'
file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964a.p620140130_daymn_flux.pp'

# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_emis_sea_fix.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_emis_sea_fix_latest_soc.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_emis_sea_fix_no_cloud_zeroing.nflx'
#file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_szen_fix_lwalb_10_percent.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_emis_sea_fix_zero_vapour.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_aer_interp_re_lim_fix.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_aer_spline_bias_fix.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_sw_aer_spline_bias_fix_fixed_fsd.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_sw_aer_spline_bias_fix_fixed_seed.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_aer_spline_bias_fix_fixed_fsd_and_seed.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_aer_spline_bias_fix_soc_surft_emis.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_sw_fixed_fsd_and_seed_soc_surft_emis.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_sw_fixed_seed_soc_surft_emis.nflx'
# file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_sw_fixed_fsd_and_seed_soc_surft_emis.nflx'
file_soc_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_sw_corr_qcfqcl_no_seed_fix.nflx'

# file_s1oc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_emis_sea_fix.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_emis_sea_fix_latest_soc.nflx'
# file_soc_toa_lw = file_loc.diag_dir + 'socrates_diags/cd964_20140529_toa_lw_emis_sea_fix_no_cloud_zeroing.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_emis_sea_fix_zero_vapour.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_aer_interp_re_lim_fix.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_aer_spline_bias_fix.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_lw_aer_spline_bias_fix_fixed_fsd.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_lw_aer_spline_bias_fix_fixed_seed.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_aer_spline_bias_fix_fixed_fsd_and_seed.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_aer_spline_bias_fix_soc_surft_emis.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_toa_lw_fixed_fsd_and_seed_soc_surft_emis.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_lw_fixed_seed_soc_surft_emis.nflx'
# file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_lw_fixed_fsd_and_seed_soc_surft_emis.nflx'
file_soc_toa_lw = file_loc.diag_dir + '/socrates_diags/cd964_20140130_toa_lw_corr_qcfqcl_no_seed_fix.nflx'


# Load and calculate net from UKESM data and choose TOA only
ukesm_up_sw, ukesm_down_sw, ukesm_up_lw = iris.load(\
    file_ukesm_data, \
    ['upwelling_shortwave_flux_in_air', 'downwelling_shortwave_flux_in_air',\
     'upwelling_longwave_flux_in_air']\
    )

ukesm_net_toa_sw = ukesm_down_sw[85] - ukesm_up_sw[85]
ukesm_net_toa_lw = ukesm_up_lw[85]*-1
ukesm_net_toa = ukesm_net_toa_sw + ukesm_net_toa_lw


# Load data from socrates
soc_toa_sw_raw = iris.load_cube(file_soc_toa_sw)
soc_toa_lw_raw = iris.load_cube(file_soc_toa_lw)

# Get rid of plev dimension
# soc_toa_sw = soc_toa_sw_raw[:,0,:]   # for chunked as lat dim first
# soc_toa_lw = soc_toa_lw_raw[:,0,:]
soc_toa_sw = soc_toa_sw_raw[0,:,:]   # # for non chunked
soc_toa_lw = soc_toa_lw_raw[0,:,:]

# add units to allow dfferencing to ukesm data
soc_toa_sw.units = 'W m-2'
soc_toa_lw.units = 'W m-2'

# Set socrates data lat and long same as in ukesm data
# Note: adding the ukesm dimension for lon auto corrects for meridian start
ukesm_longitude = ukesm_net_toa.coord('longitude')
ukesm_latitude = ukesm_net_toa.coord('latitude')

soc_toa_sw.remove_coord('longitude')
soc_toa_sw.remove_coord('latitude')

soc_toa_lw.remove_coord('longitude')
soc_toa_lw.remove_coord('latitude')

soc_toa_sw.add_dim_coord(ukesm_longitude, 1)
soc_toa_sw.add_dim_coord(ukesm_latitude, 0)

soc_toa_lw.add_dim_coord(ukesm_longitude, 1)
soc_toa_lw.add_dim_coord(ukesm_latitude, 0)

# Calc net soc flux
soc_toa_net = soc_toa_sw + soc_toa_lw


# Difference the two datasets
net_diff = soc_toa_net - ukesm_net_toa
net_diff_sw = soc_toa_sw - ukesm_net_toa_sw
net_diff_lw = soc_toa_lw - ukesm_net_toa_lw


### Plotting ###
plot_dir = file_loc.plot_dir + 'socrates_plots/'
plt.tight_layout()

# ukesm plot
plt.figure()
plt.title('UKESM TOA net down flux 20140130')
mesh = iplt.pcolormesh(ukesm_net_toa, vmin = -250, vmax = 250, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_20140130_ukesm.png', dpi = 300)
plt.show() 

# ukesm plot sw 
plt.figure()
plt.title('UKESM TOA sw net down flux 20140130')
mesh = iplt.pcolormesh(ukesm_net_toa_sw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_sw_flux_toa_map_20140130_ukesm.png', dpi = 300)
plt.show() 

# ukesm plot lw
plt.figure()
plt.title('UKESM TOA lw net down flux 20140130')
mesh = iplt.pcolormesh(ukesm_net_toa_lw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_lw_flux_toa_map_20140130_ukesm.png', dpi = 300)
plt.show() 

# socrates plot
plt.figure()
plt.title('SOCRATES TOA net down flux 20140130 corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(soc_toa_net, vmin = -250, vmax = 250, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_20140130_soc_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()

# socrates plot sw
plt.figure()
plt.title('SOCRATES TOA sw net down flux 20140130 corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(soc_toa_sw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_sw_down_flux_toa_map_20140130_soc_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()

# socrates plot lw
plt.figure()
plt.title('SOCRATES TOA lw net down flux 20140130 corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(soc_toa_lw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_lw_down_flux_toa_map_20140130_soc_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()
    
# difference plot
plt.figure()
plt.title('TOA net down flux 20140130 Socrates - UKESM corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(net_diff,\
                        vmin = -50, vmax = 50,\
                           cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_20140130_soc-ukesm_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()

# sw difference plot
plt.figure()
plt.title('TOA sw net down flux 20140130 Socrates - UKESM corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(net_diff_sw,\
                        vmin = -50, vmax = 50,\
                           cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_sw_flux_toa_map_20140130_soc-ukesm_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()

# lw difference plot
plt.figure()
plt.title('TOA lw net down flux 20140130 Socrates - UKESM corr qcfqcl no seed fix')
mesh = iplt.pcolormesh(net_diff_lw,\
                        vmin = -50, vmax = 50,\
                           cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_lw_flux_toa_map_20140130_soc-ukesm_corr_qcfqcl_no_seed_fix.png', dpi = 300)
plt.show()


# Print nans number (shape)
# print('sw nans: ', np.shape(np.where(np.isnan(net_diff_sw.data))))
# print('lw nans: ', np.shape(np.where(np.isnan(net_diff_lw.data))))
print('sw nans: ', np.where(np.isnan(net_diff_sw.data)))
print('lw nans: ', np.where(np.isnan(net_diff_lw.data)))


# Area means of diffs, dealing wth nans
area_mean_diff = flux_mod.area_mean_cube_nans(net_diff)
area_mean_sw_diff = flux_mod.area_mean_cube_nans(net_diff_sw)
area_mean_lw_diff = flux_mod.area_mean_cube_nans(net_diff_lw)

print('area mean diff: ', area_mean_diff.data)
print('area mean sw diff: ', area_mean_sw_diff.data)
print('area mean lw diff: ', area_mean_lw_diff.data)

