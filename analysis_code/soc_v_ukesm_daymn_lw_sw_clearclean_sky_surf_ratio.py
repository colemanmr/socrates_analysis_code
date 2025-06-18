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
file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964a.p620140529_daymn_clearclean_sky_flux.pp'

file_soc_surf_sw_up = file_loc.diag_dir + '/socrates_diags/cd964_20140529_surf_sw_clearclean_sky_szen_fix.uflx'
file_soc_surf_lw_up = file_loc.diag_dir + '/socrates_diags/cd964_20140529_surf_lw_clearclean_sky_szen_fix.uflx'
file_soc_surf_sw_down = file_loc.diag_dir + '/socrates_diags/cd964_20140529_surf_sw_clearclean_sky_szen_fix.vflx'
file_soc_surf_lw_down = file_loc.diag_dir + '/socrates_diags/cd964_20140529_surf_lw_clearclean_sky_szen_fix.dflx'


# Load and calculate net from UKESM data and choose surf only
ukesm_up_sw, ukesm_down_sw, ukesm_up_lw, ukesm_down_lw = iris.load(\
    file_ukesm_data, \
    ['m01s01i519',\
     'm01s01i520',\
     'm01s02i519',\
     'm01s02i520']\
    )

# Add units for clearclean diags as missing
ukesm_up_sw.units = 'W m-2'
ukesm_down_sw.units = 'W m-2'
ukesm_up_lw.units = 'W m-2'
ukesm_down_lw.units = 'W m-2'
    
# ukesm_net_surf_sw = ukesm_down_sw[0] - ukesm_up_sw[0]
# ukesm_net_surf_lw = ukesm_up_lw[0]*-1
# ukesm_net_surf = ukesm_net_surf_sw + ukesm_net_surf_lw


# Load data from socrates
soc_surf_sw_up_raw = iris.load_cube(file_soc_surf_sw_up)
soc_surf_lw_up_raw = iris.load_cube(file_soc_surf_lw_up)
soc_surf_sw_down_raw = iris.load_cube(file_soc_surf_sw_down)
soc_surf_lw_down_raw = iris.load_cube(file_soc_surf_lw_down)

# Get rid of plev dimension
# soc_surf_sw = soc_surf_sw_raw[:,0,:]   # for chunked as lat dim first
# soc_surf_lw = soc_surf_lw_raw[:,0,:]
soc_surf_sw_up = soc_surf_sw_up_raw[0,:,:]   # # for non chunked
soc_surf_lw_up = soc_surf_lw_up_raw[0,:,:]
soc_surf_sw_down = soc_surf_sw_down_raw[0,:,:]   # # for non chunked
soc_surf_lw_down = soc_surf_lw_down_raw[0,:,:]

# add units to allow dfferencing to ukesm data
soc_surf_sw_up.units = 'W m-2'
soc_surf_lw_up.units = 'W m-2'
soc_surf_sw_down.units = 'W m-2'
soc_surf_lw_down.units = 'W m-2'

# Set socrates data lat and long same as in ukesm data
# Note: adding the ukesm dimension for lon auto corrects for meridian start
ukesm_longitude = ukesm_up_sw.coord('longitude')
ukesm_latitude = ukesm_up_sw.coord('latitude')

soc_surf_sw_up.remove_coord('longitude')
soc_surf_sw_up.remove_coord('latitude')

soc_surf_lw_up.remove_coord('longitude')
soc_surf_lw_up.remove_coord('latitude')

soc_surf_sw_up.add_dim_coord(ukesm_longitude, 1)
soc_surf_sw_up.add_dim_coord(ukesm_latitude, 0)

soc_surf_lw_up.add_dim_coord(ukesm_longitude, 1)
soc_surf_lw_up.add_dim_coord(ukesm_latitude, 0)

soc_surf_sw_down.remove_coord('longitude')
soc_surf_sw_down.remove_coord('latitude')

soc_surf_lw_down.remove_coord('longitude')
soc_surf_lw_down.remove_coord('latitude')

soc_surf_sw_down.add_dim_coord(ukesm_longitude, 1)
soc_surf_sw_down.add_dim_coord(ukesm_latitude, 0)

soc_surf_lw_down.add_dim_coord(ukesm_longitude, 1)
soc_surf_lw_down.add_dim_coord(ukesm_latitude, 0)

# # Calc net soc flux
# soc_surf_net = soc_surf_sw + soc_surf_lw




### one above surf repeat ###
file_soc_surf_plus_one_sw_up = file_loc.diag_dir + '/socrates_diags/cd964_20140529_1-above-surf_sw_clearclean_sky_szen_fix.uflx'
file_soc_surf_plus_one_lw_up = file_loc.diag_dir + '/socrates_diags/cd964_20140529_1-above-surf_lw_clearclean_sky_szen_fix.uflx'
file_soc_surf_plus_one_sw_down = file_loc.diag_dir + '/socrates_diags/cd964_20140529_1-above-surf_sw_clearclean_sky_szen_fix.vflx'
file_soc_surf_plus_one_lw_down = file_loc.diag_dir + '/socrates_diags/cd964_20140529_1-above-surf_lw_clearclean_sky_szen_fix.dflx'

# Load data from socrates
soc_surf_plus_one_sw_up_raw = iris.load_cube(file_soc_surf_plus_one_sw_up)
soc_surf_plus_one_lw_up_raw = iris.load_cube(file_soc_surf_plus_one_lw_up)
soc_surf_plus_one_sw_down_raw = iris.load_cube(file_soc_surf_plus_one_sw_down)
soc_surf_plus_one_lw_down_raw = iris.load_cube(file_soc_surf_plus_one_lw_down)

# Get rid of plev dimension
# soc_surf_sw = soc_surf_sw_raw[:,0,:]   # for chunked as lat dim first
# soc_surf_lw = soc_surf_lw_raw[:,0,:]
soc_surf_plus_one_sw_up = soc_surf_plus_one_sw_up_raw[0,:,:]   # # for non chunked
soc_surf_plus_one_lw_up = soc_surf_plus_one_lw_up_raw[0,:,:]
soc_surf_plus_one_sw_down = soc_surf_plus_one_sw_down_raw[0,:,:]   # # for non chunked
soc_surf_plus_one_lw_down = soc_surf_plus_one_lw_down_raw[0,:,:]

# add units to allow dfferencing to ukesm data
soc_surf_plus_one_sw_up.units = 'W m-2'
soc_surf_plus_one_lw_up.units = 'W m-2'
soc_surf_plus_one_sw_down.units = 'W m-2'
soc_surf_plus_one_lw_down.units = 'W m-2'

# Set socrates data lat and long same as in ukesm data
# Note: adding the ukesm dimension for lon auto corrects for meridian start
soc_surf_plus_one_sw_up.remove_coord('longitude')
soc_surf_plus_one_sw_up.remove_coord('latitude')

soc_surf_plus_one_lw_up.remove_coord('longitude')
soc_surf_plus_one_lw_up.remove_coord('latitude')

soc_surf_plus_one_sw_up.add_dim_coord(ukesm_longitude, 1)
soc_surf_plus_one_sw_up.add_dim_coord(ukesm_latitude, 0)

soc_surf_plus_one_lw_up.add_dim_coord(ukesm_longitude, 1)
soc_surf_plus_one_lw_up.add_dim_coord(ukesm_latitude, 0)

soc_surf_plus_one_sw_down.remove_coord('longitude')
soc_surf_plus_one_sw_down.remove_coord('latitude')

soc_surf_plus_one_lw_down.remove_coord('longitude')
soc_surf_plus_one_lw_down.remove_coord('latitude')

soc_surf_plus_one_sw_down.add_dim_coord(ukesm_longitude, 1)
soc_surf_plus_one_sw_down.add_dim_coord(ukesm_latitude, 0)

soc_surf_plus_one_lw_down.add_dim_coord(ukesm_longitude, 1)
soc_surf_plus_one_lw_down.add_dim_coord(ukesm_latitude, 0)


# Difference the down and up fluxes
surf_plus_one_down_diff_sw = soc_surf_plus_one_sw_down - ukesm_down_sw[1]
surf_plus_one_up_diff_sw = soc_surf_plus_one_sw_up - ukesm_up_sw[1]

surf_plus_one_down_diff_lw = soc_surf_plus_one_lw_down - ukesm_down_lw[1]
surf_plus_one_up_diff_lw = soc_surf_plus_one_lw_up - ukesm_up_lw[1]

##########################





# # Difference the flux ratios as proxy to investigate
# net_diff = soc_surf_net - ukesm_net_surf
# net_diff_sw = soc_surf_sw - ukesm_net_surf_sw
# net_diff_lw = soc_surf_lw - ukesm_net_surf_lw

alb_sw_soc = soc_surf_sw_up/soc_surf_sw_down
alb_lw_soc = soc_surf_lw_up/soc_surf_lw_down
alb_sw_ukesm = ukesm_up_sw[0]/ukesm_down_sw[0]
alb_lw_ukesm = ukesm_up_lw[0]/ukesm_down_lw[0]

alb_diff_sw = alb_sw_soc - alb_sw_ukesm
# wgtd_alb_diff_sw = alb_sw_soc/soc_surf_sw_down - alb_sw_ukesm/soc_surf_sw_down
alb_diff_lw = alb_lw_soc - alb_lw_ukesm


# Difference the down and up fluxes
surf_down_diff_sw = soc_surf_sw_down - ukesm_down_sw[0]
surf_up_diff_sw = soc_surf_sw_up - ukesm_up_sw[0]

surf_down_diff_lw = soc_surf_lw_down - ukesm_down_lw[0]
surf_up_diff_lw = soc_surf_lw_up - ukesm_up_lw[0]



### Plotting ###
plot_dir = file_loc.plot_dir + 'socrates_plots/'


# sw albedo proxy difference plot
plt.figure()
plt.title('sw albedo proxy 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(alb_diff_sw,\
                         vmin = -0.0005, vmax = 0.0005,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = 'Flux ratio', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'sw_surf_albedo_proxy_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# lw albedo proxy difference plot
plt.figure()
plt.title('lw albedo proxy 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(alb_diff_lw,\
                        vmin = -0.07, vmax = 0.07,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = 'Flux ratio', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'lw_surf_albedo_proxy_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# sw down diff plot
plt.figure()
plt.title('sw 1-above-surf down flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_plus_one_down_diff_sw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'sw_flux_1-above-surf_down_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# sw up diff plot
plt.figure()
plt.title('sw 1-above-surf up flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_plus_one_up_diff_sw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'sw_flux_1-above-surf_up_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# lw down diff plot
plt.figure()
plt.title('lw 1-above-surf down flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_plus_one_down_diff_lw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'lw_flux_1-above-surf_down_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# lw up diff plot
plt.figure()
plt.title('lw 1-above-surf up flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_plus_one_up_diff_lw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'lw_flux_1-above-surf_up_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# sw down diff plot
plt.figure()
plt.title('sw surf down flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_down_diff_sw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'sw_flux_surf_down_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# sw up diff plot
plt.figure()
plt.title('sw surf up flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_up_diff_sw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'sw_flux_surf_up_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# lw down diff plot
plt.figure()
plt.title('lw surf down flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_down_diff_lw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'lw_flux_surf_down_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()


# lw up diff plot
plt.figure()
plt.title('lw surf up flux 20140529 Socrates - UKESM szen fix clearclean')
mesh = iplt.pcolormesh(surf_up_diff_lw,\
                          vmin = -1, vmax = 1,\
                       cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'lw_flux_surf_up_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
plt.show()










# # ukesm plot
# plt.figure()
# plt.title('UKESM surf net down flux 20140529 clearclean')
# mesh = iplt.pcolormesh(ukesm_net_surf, vmin = -250, vmax = 250, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_flux_surf_map_20140529_ukesm_clearclean.png', dpi = 300)
# plt.show() 

# # ukesm plot sw 
# plt.figure()
# plt.title('UKESM surf sw net down flux 20140529 clearclean')
# mesh = iplt.pcolormesh(ukesm_net_surf_sw, vmin = -0, vmax = 450, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_sw_flux_surf_map_20140529_ukesm_clearclean.png', dpi = 300)
# plt.show() 

# # ukesm plot lw
# plt.figure()
# plt.title('UKESM surf lw net down flux 20140529 clearclean')
# mesh = iplt.pcolormesh(ukesm_net_surf_lw, vmin = -400, vmax = -50, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_lw_flux_surf_map_20140529_ukesm_clearclean.png', dpi = 300)
# plt.show() 

# # socrates plot
# plt.figure()
# plt.title('SOCRATES surf net down flux 20140529 szen fix clearclean')
# mesh = iplt.pcolormesh(soc_surf_net, vmin = -250, vmax = 250, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_flux_surf_map_20140529_soc_szen_fix_clearclean.png', dpi = 300)
# plt.show()

# # socrates plot sw
# plt.figure()
# plt.title('SOCRATES surf sw net down flux 20140529 szen fix clearclean')
# mesh = iplt.pcolormesh(soc_surf_sw, vmin = -0, vmax = 450, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'sw_down_flux_surf_map_20140529_soc_szen_fix_clearclean.png', dpi = 300)
# plt.show()

# # socrates plot lw
# plt.figure()
# plt.title('SOCRATES surf lw net down flux 20140529 szen fix clearclean')
# mesh = iplt.pcolormesh(soc_surf_lw, vmin = -400, vmax = -50, cmap = 'viridis')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'lw_down_flux_surf_map_20140529_soc_szen_fix_clearclean.png', dpi = 300)
# plt.show()
    
# # difference plot
# plt.figure()
# plt.title('surf net down flux 20140529 Socrates - UKESM szen fix clearclean')
# mesh = iplt.pcolormesh(net_diff, vmin = -20, vmax = 20, cmap = 'seismic')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_flux_surf_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
# plt.show()

# # sw difference plot
# plt.figure()
# plt.title('surf sw net down flux 20140529 Socrates - UKESM szen fix clearclean')
# mesh = iplt.pcolormesh(net_diff_sw, vmin = -0.6, vmax = 0.6, cmap = 'seismic')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_sw_flux_surf_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
# plt.show()

# # lw difference plot
# plt.figure()
# plt.title('surf lw net down flux 20140529 Socrates - UKESM szen fix clearclean')
# mesh = iplt.pcolormesh(net_diff_lw, vmin = -2, vmax = 2, cmap = 'seismic')
# plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                   orientation = 'horizontal',
#                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                   )
# plt.savefig(plot_dir + 'net_lw_flux_surf_map_20140529_soc-ukesm_szen_fix_clearclean.png', dpi = 300)
# plt.show()


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