#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:10:28 2024

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


def calc_socrates_prp(band, yearmonth):
    """
    function for performing PRP calculations with final SOCRATES flux outputs
    calculates PRP for 6 variables (control, aerosol, water vapour, albedo, 
    atmospheric T, and surface T) and assumes corresponding forward and
    backward cases have been calculated with SOCRATES (i.e. one input file for
    each)
    :param string band: string denoting radiative band, either 'sw' or 'lw'
    :returns: dictionaries of fwd, bwd, and two sided PRP flux difference cubes
    """
    
    # set diagnositcs directory
    diag_dir = file_loc.diag_dir + \
        'socrates_diags/bc_prp_1year_clear_sky/month_mean_fluxes/'
        

    # set list of SOCRATES cases
    cases = [
             'cont',
             'aer_fwd',
             'vap_fwd',
             'alb_fwd',
             't_fwd',
             'tsurf_fwd',
             'pert',
             'aer_bwd',
             'vap_bwd',
             'alb_bwd',
             't_bwd',
             'tsurf_bwd'        
             ] 
    
    cubes = []
    
    for case in cases: 
    
        filename = diag_dir + 'bc_prp_1year_clear_sky_' + case + '_' + \
            yearmonth + '_toa_' + band + '.nflx'
    
        # load files
        cube = iris.load_cube(filename)
        
        cubes.append(cube)
        
    print(cubes)
        
   
    # set list of PRP differences
    diff_cases = [
             'aer_fwd_diff',
             'vap_fwd_diff',
             'alb_fwd_diff',
             't_fwd_diff',
             'tsurf_fwd_diff',
             'fwd_residual',
             'aer_bwd_diff',
             'vap_bwd_diff',
             'alb_bwd_diff',
             't_bwd_diff',
             'tsurf_bwd_diff',
             'bwd_residual'
            ]
    
    # check is the expected calculation being done (can remove)
    cubes_check = [
             'cont',
             'aer_fwd',
             'vap_fwd',
             'alb_fwd',
             't_fwd',
             'tsurf_fwd',
             'pert',
             'aer_bwd',
             'vap_bwd',
             'alb_bwd',
             't_bwd',
             'tsurf_bwd',
                   ]
    
    # create dictionary to store PRP differences
    diffs = {}
    
    # loop over differences, differencing neighbouring cases
    # extra [0] index is to remove pressure coord
    for count, diff_case in enumerate(diff_cases):
        print(count, diff_case)
        
        # because pert is PI fwd calculation is reversed
        if count < 6:
            diff = cubes[count][0] - cubes[count+1][0]
            print(cubes_check[count], ' minus ', cubes_check[count+1])
        
        # backward differences
        elif count < 11:
            diff = cubes[count+1][0] - cubes[count][0]
            print(cubes_check[count+1], ' minus ', cubes_check[count])
            
        # final backward difference (bwd_residual) needs special indexing
        elif count == 11:
            diff = cubes[0][0] - cubes[count][0]
            print(cubes_check[0], ' minus ', cubes_check[count])
        
        # enter differences into dictionary
        diffs[diff_case] = diff
        
        
    # add total difference between cont and pert to dictionary
    total_pert = cubes[0][0] - cubes[6][0]
    diffs['total'] = total_pert
    
    
    # list keys for mean of fwd and bwd diffs
    two_sided_diff_cases = [
                            'aer_diff',
                            'vap_diff',
                            'alb_diff',
                            't_diff',
                            'tsurf_diff',
                            'residual_diff'
                            ]
    
    # dictionary for two sided diffs
    two_sided_diffs = {}
    
    # calculate two sided diffs by meaning fwd and bwd and add to dictionary
    for count, diff in enumerate(two_sided_diff_cases):
        print(count, diff)
        
        two_sided_diff = (diffs[diff_cases[count]] + \
                          diffs[diff_cases[count+6]])/2
        
        two_sided_diffs[diff] = two_sided_diff
        
    
    return diffs, two_sided_diffs


# do PRP calculations
sw_diffs, sw_two_sided_diffs = calc_socrates_prp('sw', '201407')
lw_diffs, lw_two_sided_diffs = calc_socrates_prp('lw', '201407')


# # For checking where there are NaNs
# print(np.where(np.isnan((lw_diffs['aer_fwd_diff'].data))))


# calculate net of SW and LW for one and two sided differences
net_diffs = {}
net_two_sided_diffs = {}
 
for key, value in sw_diffs.items():
        
    net_diff = sw_diffs[key] + lw_diffs[key]
    net_diffs[key] = net_diff
    
for key, value in sw_two_sided_diffs.items():
    
    net_diff = sw_two_sided_diffs[key] + lw_two_sided_diffs[key]
    net_two_sided_diffs[key] = net_diff
    

# set list of dicts for looping
diff_dicts = [sw_diffs, sw_two_sided_diffs,
              lw_diffs, lw_two_sided_diffs,
              net_diffs, net_two_sided_diffs
              ]

# Set list for storing area means
area_means_sw = {}
area_means_sw_two_sided = {}
area_means_lw = {}
area_means_lw_two_sided = {}
area_means_net = {}
area_means_net_two_sided = {}

area_means = [area_means_sw, area_means_sw_two_sided,
              area_means_lw, area_means_lw_two_sided,
              area_means_net, area_means_net_two_sided
              ]

# area_mean_set_names = [sw, sw_two, lw, lw_two, net, net_two]

# take area mean of differences cubes and store in separate list of dicts
for index in range(len(diff_dicts)):
    
    diff_dict = diff_dicts[index]
    
    for key, value in diff_dict.items():
        
        cube = diff_dict[key]
        
        cube.data = np.ma.masked_invalid(cube.data)
                
        area_mean_diff = flux_mod.area_mean_cube(cube)    
        
        area_mean_dict = area_means[index]        
        area_mean_dict[key] = np.round(area_mean_diff.data, 2)
        # area_mean_dict[key] = area_mean_diff.data
    


# ##Plotting###################################################################


# # set directory for saving plots to
# plot_dir = file_loc.plot_dir + \
#     'socrates_plots/bc_prp_1year_clear_sky_final_flux_plots/'


# # plots for fwd and bwd cases for sw, lw, and net
# for key, value in sw_diffs.items():
        
#     plt.figure()
#     mesh = iplt.pcolormesh(sw_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC SW TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[0][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_sw')
    
#     plt.show()
    

#     plt.figure()
#     mesh = iplt.pcolormesh(lw_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC LW TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[2][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_lw')
#     plt.show()


#     plt.figure()
#     mesh = iplt.pcolormesh(net_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC NET TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[4][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_net')
#     plt.show()


# # plots for double sided cases for sw, lw, and net
# for key, value in sw_two_sided_diffs.items():
        
#     plt.figure()
#     mesh = iplt.pcolormesh(sw_two_sided_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC SW TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[1][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_sw')
#     plt.show()
    

#     plt.figure()
#     mesh = iplt.pcolormesh(lw_two_sided_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC LW TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[3][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_lw')
#     plt.show()


#     plt.figure()
#     mesh = iplt.pcolormesh(net_two_sided_diffs[key], cmap = 'seismic',\
#                             vmin = -15, vmax = 15\
#                                 )
#     plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
#                       orientation = 'horizontal',
#                         #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
#                         )
#     plt.title('1 year clear sky BC NET TOA forcing prp: ' + key)
#     plt.text(50, -124, 'Mean = ' + str(area_means[5][key]) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_net')
#     plt.show()


