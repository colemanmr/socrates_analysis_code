#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:54:35 2024

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


diag_dir = file_loc.diag_dir + 'socrates_diags/bc_prp_1year_clear_sky/other_diags/'

# cd964_alb_file = 'sw_albedo_cd964_one_year_hourly.pp'

# cd964_alb_file = 'sw_albedo_cd964_jul2014_jan2015.pp'
# db548_alb_file = 'sw_albedo_db548_jul2014_jan2015.pp'


# cd964_alb_dir, cd964_alb_dif = iris.load(diag_dir + cd964_alb_file, \
#                       ['surface_direct_beam_albedo_assuming_no_snow', \
#                        'surface_diffuse_albedo_assuming_no_snow'])
# db548_alb_dir, db548_alb_dif = iris.load(diag_dir + db548_alb_file, \
#                       ['surface_direct_beam_albedo_assuming_no_snow', \
#                        'surface_diffuse_albedo_assuming_no_snow'])


# cd964_alb_dir_jul,_,_ = flux_mod.time_mean_cube(cd964_alb_dir[:,:720])
# cd964_alb_dir_jan,_,_ = flux_mod.time_mean_cube(cd964_alb_dir[:,720:])

# db548_alb_dir_jul,_,_ = flux_mod.time_mean_cube(db548_alb_dir[:,:720])
# db548_alb_dir_jan,_,_ = flux_mod.time_mean_cube(db548_alb_dir[:,720:])

# cd964_alb_dif_jul,_,_ = flux_mod.time_mean_cube(cd964_alb_dif[:,:720])
# cd964_alb_dif_jan,_,_ = flux_mod.time_mean_cube(cd964_alb_dif[:,720:])

# db548_alb_dif_jul,_,_ = flux_mod.time_mean_cube(db548_alb_dif[:,:720])
# db548_alb_dif_jan,_,_ = flux_mod.time_mean_cube(db548_alb_dif[:,720:])


# target = ['sw_alb_dir_cd964_jul2014.nc', 'sw_alb_dir_cd964_jan2015.nc',
#           'sw_alb_dir_db548_jul2014.nc', 'sw_alb_dir_db548_jan2015.nc',
#           'sw_alb_dif_cd964_jul2014.nc', 'sw_alb_dif_cd964_jan2015.nc',
#           'sw_alb_dif_db548_jul2014.nc', 'sw_alb_dif_db548_jan2015.nc',]

# mon_mean_cubes = [cd964_alb_dir_jul, cd964_alb_dir_jan, 
#                   db548_alb_dir_jul, db548_alb_dir_jan,
#                   cd964_alb_dif_jul, cd964_alb_dif_jan, 
#                   db548_alb_dif_jul, db548_alb_dif_jan]

# for count, cube in enumerate(mon_mean_cubes):
#     print(cube)
#     print(count)
    
#     iris.save(cube, diag_dir + target[count])
    
 
cd964_alb_dir_jul = iris.load_cube(diag_dir + 'sw_alb_dir_cd964_jul2014.nc')
cd964_alb_dir_jan = iris.load_cube(diag_dir + 'sw_alb_dir_cd964_jan2015.nc')

db548_alb_dir_jul = iris.load_cube(diag_dir + 'sw_alb_dir_db548_jul2014.nc')
db548_alb_dir_jan = iris.load_cube(diag_dir + 'sw_alb_dir_db548_jan2015.nc')

cd964_alb_dif_jul = iris.load_cube(diag_dir + 'sw_alb_dif_cd964_jul2014.nc')
cd964_alb_dif_jan = iris.load_cube(diag_dir + 'sw_alb_dif_cd964_jan2015.nc')

db548_alb_dif_jul = iris.load_cube(diag_dir + 'sw_alb_dif_db548_jul2014.nc')
db548_alb_dif_jan = iris.load_cube(diag_dir + 'sw_alb_dif_db548_jan2015.nc')



diff_alb_dir_jul = cd964_alb_dir_jul - db548_alb_dir_jul
diff_alb_dir_jan = cd964_alb_dir_jan - db548_alb_dir_jan

diff_alb_dif_jul = cd964_alb_dif_jul - db548_alb_dif_jul
diff_alb_dif_jan = cd964_alb_dif_jan - db548_alb_dif_jan



### plotting #################################################################

# set plot directory
plot_dir = file_loc.plot_dir + 'socrates_plots/bc_prp_1year_clear_sky_adjustments/'


# plot for each radiation band
for band in range(1,7):
    
    # # plot for control values
    # # control direct albedo january 2015
    # plt.figure()
    # mesh = iplt.pcolormesh(cd964_alb_dir_jan[band-1], cmap = 'viridis',
    #                         vmin = 0.0, vmax = 1.0,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.savefig(plot_dir + 'cd964_sw_albedo_control_dir_201501_band_'\
    #             + str(band), dpi = 300)
    # plt.title('Control SW direct surface albedo: jan mean, band ' + str(band) )
    # plt.show()
    
    # # control direct albedo july 2014   
    # plt.figure()
    # mesh = iplt.pcolormesh(cd964_alb_dir_jul[band-1], cmap = 'viridis',
    #                         vmin = 0.0, vmax = 1.0,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.savefig(plot_dir + 'cd964_sw_albedo_control_dir_201407_band_'\
    #             + str(band), dpi = 300)
    # plt.title('Control SW direct surface albedo: jul mean, band ' + str(band) )
    # plt.show()   
    
    # control diffuse albedo january 2015
    plt.figure()
    mesh = iplt.pcolormesh(cd964_alb_dif_jan[band-1], cmap = 'viridis',
                            vmin = 0.0, vmax = 1.0,
                            )
    plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
                      orientation = 'horizontal',
                        #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                        )
    plt.savefig(plot_dir + 'cd964_sw_albedo_control_dif_201501_band_'\
                + str(band), dpi = 300)
    plt.title('Control SW diffuse surface albedo: jan mean, band ' + str(band) )
    plt.show()
    
    # control diffuse albedo july 2014
    plt.figure()
    mesh = iplt.pcolormesh(cd964_alb_dif_jul[band-1], cmap = 'viridis',
                            vmin = 0.0, vmax = 1.0,
                            )
    plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
                      orientation = 'horizontal',
                        #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                        )
    plt.savefig(plot_dir + 'cd964_sw_albedo_control_dif_201407_band_'\
                + str(band), dpi = 300)
    plt.title('Control SW diffuse surface albedo: jul mean, band ' + str(band) )
    plt.show()   
    
    
    # # plot albedo adjustments
    # # direct albedo january 2015 adjustment
    # plt.figure()
    # mesh = iplt.pcolormesh(diff_alb_dir_jan[band-1], cmap = 'seismic',
    #                         vmin = -0.8, vmax = 0.8,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.savefig(plot_dir + 'bc_prp_clear_sky_sw_albedo_adjustment_dir_201501_band_'\
    #             + str(band), dpi = 300)
    # plt.title('SW direct surface albedo adjustment: jan mean, band ' + str(band) )
    # plt.show()
    
    # # direct albedo july 2014 adjustment    
    # plt.figure()
    # mesh = iplt.pcolormesh(diff_alb_dir_jul[band-1], cmap = 'seismic',
    #                         vmin = -0.8, vmax = 0.8,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.savefig(plot_dir + 'bc_prp_clear_sky_sw_albedo_adjustment_dir_201407_band_'\
    #             + str(band), dpi = 300)
    # plt.title('SW direct surface albedo adjustment: jul mean, band ' + str(band) )
    # plt.show()  
    
    # # diffuse albedo january 2015 adjustment
    # plt.figure()
    # mesh = iplt.pcolormesh(diff_alb_dif_jan[band-1], cmap = 'seismic',
    #                         vmin = -0.8, vmax = 0.8,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.savefig(plot_dir + 'bc_prp_clear_sky_sw_albedo_adjustment_dif_201501_band_'\
    #         + str(band), dpi = 300)
    # plt.title('SW diffuse surface albedo adjustment: jan mean, band ' + str(band) )
    # plt.show()
    
    # # diffuse albedo july 2014 adjustment   
    # plt.figure()
    # mesh = iplt.pcolormesh(diff_alb_dif_jul[band-1], cmap = 'seismic',
    #                         vmin = -0.8, vmax = 0.8,
    #                         )
    # plt.colorbar(mesh, shrink = 0.9, label = 'albedo', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )    
    # plt.savefig(plot_dir + 'bc_prp_clear_sky_sw_albedo_adjustment_dif_201407_band_'\
    #             + str(band), dpi = 300)
    # plt.title('SW diffuse surface albedo adjustment: jul mean, band ' + str(band) )
    # plt.show()  
