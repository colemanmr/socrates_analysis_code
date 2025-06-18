#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:45:56 2022

@author: nn819853
"""

import iris
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
import Documents.python_code.diagnostics.file_locations_module as file_loc


# Set UKESM and socrates data filenames
#file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964a.pm2015jan_full.pp'
file_ukesm_data = file_loc.diag_dir + '/socrates_diags/cd964a.p52015jan_sw_fluxes_levels.pp'

file_soc_toa_nflx = file_loc.diag_dir + '/socrates_diags/cd964_201501_toa.nflx'


# Load and calculate net from UKESM data and choose TOA only
ukesm_up, ukesm_down = iris.load(\
    file_ukesm_data, \
    ['upwelling_shortwave_flux_in_air', 'downwelling_shortwave_flux_in_air']\
    )

ukesm_net_toa = ukesm_down[85] - ukesm_up[85]


# Load data from socrates
soc_net_toa = iris.load_cube(file_soc_toa_nflx)

# add units to allow dfferencing to ukesm data
soc_net_toa.units = 'W m-2'

# Change to have -180 degrees as first latitude, to be same as ukesm data
soc_net_toa_1st_half_lon = soc_net_toa[:,0,0:96]
soc_net_toa_2nd_half_lon = soc_net_toa[:,0,96:192]
cubes = iris.cube.CubeList([soc_net_toa_2nd_half_lon,soc_net_toa_1st_half_lon])
soc_net_toa = cubes.concatenate()[0]

# Set socrates data lat and long metadata same as in ukesm data
ukesm_longitude = ukesm_net_toa.coord('longitude')
ukesm_latitude = ukesm_net_toa.coord('latitude')

soc_net_toa.remove_coord('longitude')
soc_net_toa.remove_coord('latitude')

soc_net_toa.add_dim_coord(ukesm_longitude, 1)
soc_net_toa.add_dim_coord(ukesm_latitude, 0)


# Difference the two datasets
diff = soc_net_toa - ukesm_net_toa


### Plotting ###
plot_dir = file_loc.plot_dir + 'socrates_plots/'

# ukesm plot
plt.figure()
plt.title('UKESM TOA net down flux 201501')
mesh = iplt.pcolormesh(ukesm_net_toa, vmin = 0, vmax = 500, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_201501_ukesm.png', dpi = 300)
plt.show() 

# socrates plot
plt.figure()
plt.title('SOCRATES TOA net down flux 201501')
mesh = iplt.pcolormesh(soc_net_toa, vmin = 0, vmax = 500, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_201501_soc.png', dpi = 300)
plt.show()
    
# difference plot
plt.figure()
plt.title('TOA net down flux 201501 Socrates - UKESM')
mesh = iplt.pcolormesh(diff, vmin = -150, vmax = 150, cmap = 'seismic')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'net_flux_toa_map_201501_soc-ukesm.png', dpi = 300)
plt.show()


# 'toa_incoming_shortwave_flux', \
#                       'toa_outgoing_shortwave_flux', \