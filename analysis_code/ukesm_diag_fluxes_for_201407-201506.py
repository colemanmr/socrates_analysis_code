#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 15:24:18 2024

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


diag_dir = file_loc.diag_dir + 'net_flux/'

cd964_clear_file = diag_dir + 'cd964_fluxes_bc_prp_1year_clear_sky.pp'
db548_clear_file = diag_dir + 'db548_fluxes_bc_prp_1year_clear_sky.pp'

cd964_clearclean_file = diag_dir + 'cd964_fluxes_bc_prp_1year_clearclean_sky.pp'
db548_clearclean_file = diag_dir + 'db548_fluxes_bc_prp_1year_clearclean_sky.pp'



cd964_sw_down, cd964_sw_up_clear, cd964_lw_up_clear = \
    iris.load(cd964_clear_file, \
    ['toa_incoming_shortwave_flux',
     'toa_outgoing_shortwave_flux_assuming_clear_sky',
     'toa_outgoing_longwave_flux_assuming_clear_sky'])
        
cd964_sw_up_clearclean, cd964_lw_up_clearclean = \
    iris.load(cd964_clearclean_file, ['m01s01i519', 'm01s02i519'])
    
cd964_sw_up_clearclean.units = 'W m-2'
cd964_lw_up_clearclean.units = 'W m-2'
        
cd964_clear_sw_net_down, cd964_clear_lw_net_down, cd964_clear_net_down =\
    flux_mod.total_down_fluxes(\
    cd964_sw_down, cd964_sw_up_clear, cd964_lw_up_clear)
    
cd964_clearclean_sw_net_down, cd964_clearclean_lw_net_down, cd964_clearclean_net_down =\
    flux_mod.total_down_fluxes(\
    cd964_sw_down, cd964_sw_up_clearclean[:,85], cd964_lw_up_clearclean[:,85])
        

    
db548_sw_down, db548_sw_up_clear, db548_lw_up_clear = \
    iris.load(db548_clear_file, \
    ['toa_incoming_shortwave_flux',
     'toa_outgoing_shortwave_flux_assuming_clear_sky',
     'toa_outgoing_longwave_flux_assuming_clear_sky'])
        
db548_sw_up_clearclean, db548_lw_up_clearclean = \
    iris.load(db548_clearclean_file, ['m01s01i519', 'm01s02i519'])
        
db548_sw_up_clearclean.units = 'W m-2'
db548_lw_up_clearclean.units = 'W m-2'

db548_clear_sw_net_down, db548_clear_lw_net_down, db548_clear_net_down =\
    flux_mod.total_down_fluxes(\
    db548_sw_down, db548_sw_up_clear, db548_lw_up_clear)
    
db548_clearclean_sw_net_down, db548_clearclean_lw_net_down, db548_clearclean_net_down =\
    flux_mod.total_down_fluxes(\
    db548_sw_down, db548_sw_up_clearclean[:,85], db548_lw_up_clearclean[:,85])



clear_sw_diff = cd964_clear_sw_net_down - db548_clear_sw_net_down
clear_lw_diff = cd964_clear_lw_net_down - db548_clear_lw_net_down
clear_diff = cd964_clear_net_down - db548_clear_net_down

clearclean_sw_diff = cd964_clearclean_sw_net_down - db548_clearclean_sw_net_down
clearclean_lw_diff = cd964_clearclean_lw_net_down - db548_clearclean_lw_net_down
clearclean_diff = cd964_clearclean_net_down - db548_clearclean_net_down

dre_sw = clear_sw_diff - clearclean_sw_diff
dre_lw = clear_lw_diff - clearclean_lw_diff
dre = clear_diff - clearclean_diff



time_mean_clear_sw_diff,_,_ = flux_mod.time_mean_cube(clear_sw_diff)
time_mean_clear_lw_diff,_,_ = flux_mod.time_mean_cube(clear_lw_diff)
time_mean_clear_diff,_,_ = flux_mod.time_mean_cube(clear_diff)

time_area_mean_clear_sw_diff = flux_mod.area_mean_cube(time_mean_clear_sw_diff)
time_area_mean_clear_lw_diff = flux_mod.area_mean_cube(time_mean_clear_lw_diff)
time_area_mean_clear_diff = flux_mod.area_mean_cube(time_mean_clear_diff)


# time_mean_clearclean_sw_diff,_,_ = flux_mod.time_mean_cube(clearclean_sw_diff)
# time_mean_clearclean_lw_diff,_,_ = flux_mod.time_mean_cube(clearclean_lw_diff)
# time_mean_clearclean_diff,_,_ = flux_mod.time_mean_cube(clearclean_diff)

# time_area_mean_clearclean_sw_diff = flux_mod.area_mean_cube(time_mean_clearclean_sw_diff)
# time_area_mean_clearclean_lw_diff = flux_mod.area_mean_cube(time_mean_clearclean_lw_diff)
# time_area_mean_clearclean_diff = flux_mod.area_mean_cube(time_mean_clearclean_diff)


time_mean_dre_sw,_,_ = flux_mod.time_mean_cube(dre_sw)
time_mean_dre_lw,_,_ = flux_mod.time_mean_cube(dre_lw)
time_mean_dre,_,_ = flux_mod.time_mean_cube(dre)

time_area_mean_dre_sw = flux_mod.area_mean_cube(time_mean_dre_sw)
time_area_mean_dre_lw = flux_mod.area_mean_cube(time_mean_dre_lw)
time_area_mean_dre = flux_mod.area_mean_cube(time_mean_dre)


### plotting #################################################################

plot_dir = file_loc.plot_dir + 'socrates_plots/ukesm_flux_diags_for_bc_prp_1year_clear_sky'



plt.figure()
mesh = iplt.pcolormesh(time_mean_clear_sw_diff, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year clear sky BC SW TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_clear_sw_diff.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_clear_sky_sw_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()


plt.figure()
mesh = iplt.pcolormesh(time_mean_clear_lw_diff, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year clear sky BC LW TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_clear_lw_diff.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_clear_sky_lw_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()


plt.figure()
mesh = iplt.pcolormesh(time_mean_clear_diff, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year clear sky BC net TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_clear_diff.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_clear_sky_net_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()



plt.figure()
mesh = iplt.pcolormesh(time_mean_dre_sw, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year dre sky BC SW TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_dre_sw.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_dre_sky_sw_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()


plt.figure()
mesh = iplt.pcolormesh(time_mean_dre_lw, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year dre sky BC LW TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_dre_lw.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_dre_sky_lw_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()


plt.figure()
mesh = iplt.pcolormesh(time_mean_dre, cmap = 'seismic',\
                        vmin = -15, vmax = 15\
                            )
plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
plt.title('1 year dre sky BC net TOA forcing - UKESM diags')
plt.text(10, -120, 'Mean = ' + str(np.round(time_area_mean_dre.data,2)) + u' W m$^{-2}$', ha = 'center')
# plt.savefig(plot_dir+'bc_prp_1year_dre_sky_net_toa_forcing_ukesm_diags,\
#             dpi = 300)
plt.show()