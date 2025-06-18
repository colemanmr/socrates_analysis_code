#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:01:23 2022

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


file_ukesm_in_toa_sw = file_loc.diag_dir + '/socrates_diags/cd964_20140529_hourly_incoming_sw.pp'

file_soc_in_toa_sw_raw = file_loc.diag_dir + '/socrates_diags/cd964_2014052900_toa.sflx'


ukesm_in_sw = iris.load_cube(file_ukesm_in_toa_sw)
ukesm_in_toa_sw = ukesm_in_sw[0,85,:,:]
soc_in_toa_sw_raw = iris.load_cube(file_soc_in_toa_sw_raw)
soc_in_toa_sw = soc_in_toa_sw_raw[0,:,:]

# add units to allow dfferencing to ukesm data
soc_in_toa_sw.units = 'W m-2'

ukesm_longitude = ukesm_in_sw.coord('longitude')
ukesm_latitude = ukesm_in_sw.coord('latitude')

soc_in_toa_sw.remove_coord('longitude')
soc_in_toa_sw.remove_coord('latitude')

soc_in_toa_sw.add_dim_coord(ukesm_longitude, 1)
soc_in_toa_sw.add_dim_coord(ukesm_latitude, 0)


diff = soc_in_toa_sw - ukesm_in_toa_sw


plot_dir = file_loc.plot_dir + 'socrates_plots/'

# ukesm plot
plt.figure()
plt.title('UKESM TOA sw incoming 2014052900')
mesh = iplt.pcolormesh(ukesm_in_toa_sw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'ukesm_toa_sw_in_2014052900.png', dpi = 300)
plt.show() 

# soc plot
plt.figure()
plt.title('Soc TOA sw incoming 2014052900')
mesh = iplt.pcolormesh(soc_in_toa_sw, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'soc_toa_sw_in_2014052900.png', dpi = 300)
plt.show() 

# Diff plot soc-ukesm
plt.figure()
plt.title('Soc-UKESM TOA sw incoming 2014052900')
mesh = iplt.pcolormesh(diff, cmap = 'viridis')
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
plt.savefig(plot_dir + 'soc-ukesm_toa_sw_in_2014052900.png', dpi = 300)
plt.show() 

