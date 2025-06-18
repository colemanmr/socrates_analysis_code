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


def calc_socrates_prp(band):
    """
    Function for performing PRP calculations with final SOCRATES flux outputs.
    Calculates PRP for 6 variables (control, aerosol, water vapour, albedo, 
    atmospheric T, and surface T) and assumes corresponding forward and
    backward cases have been calculated with SOCRATES (i.e. one input file for
    each)
    :param string band: string denoting radiative band, either 'sw' or 'lw'
    :returns: dictionaries of fwd, bwd, and two sided PRP flux difference cubes
    """
    
    # set diagnositcs directory
    diag_dir = file_loc.diag_dir + \
        'socrates_diags/bc_prp_1year_clear_sky/multiannual_mean_fluxes/'
        
    
    # load arbitrary ukesm data for extracting lat and lon coords
    file_ukesm_data = file_loc.diag_dir + \
        '/socrates_diags/cd964a.p620140130_daymn_flux.pp'
        
    ukesm_cube = iris.load_cube(file_ukesm_data,\
                               'upwelling_shortwave_flux_in_air')
        
    ukesm_lon = ukesm_cube.coord('longitude')
    ukesm_lat = ukesm_cube.coord('latitude')
    

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
    
        filename = diag_dir + 'bc_prp_1year_clear_sky_' + case + '_multiannual_mean_toa_' + band + '.nflx'
    
        # load files
        cube = iris.load_cube(filename)
        
        # make coords same as ukesm output
        cube.remove_coord('longitude')
        cube.remove_coord('latitude')
        
        cube.add_dim_coord(ukesm_lon, 2)
        cube.add_dim_coord(ukesm_lat, 1)
        
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
sw_diffs, sw_two_sided_diffs = calc_socrates_prp('sw')
lw_diffs, lw_two_sided_diffs = calc_socrates_prp('lw')


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
        # area_mean_dict[key] = area_mean_diff.data  #use if don't want rounded
        
        
sw_area_means_list = []

for key, value in area_means_sw.items():
    sw_area_means_list.append(value)
    
sw_fwd_mean = np.sum(sw_area_means_list[0:6])
sw_bwd_mean = np.sum(sw_area_means_list[6:12])

print('fwd mean is: ', sw_fwd_mean)
print('bwd mean is: ', sw_bwd_mean)
    
       

###Plotting###################################################################


# set directory for saving plots to
plot_dir = file_loc.plot_dir + \
    'socrates_plots/bc_prp_1year_clear_sky_final_flux_plots/'
    
plt.tight_layout()


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
#     # plt.title('1 year clear sky BC SW TOA forcing prp: ' + key)
#     plt.text(10, -120, 'Mean = ' + str(format(area_means[0][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
#     plt.savefig(plot_dir+'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_sw',\
#                 dpi = 300)
#     plt.show()
    

    # plt.figure()
    # mesh = iplt.pcolormesh(lw_diffs[key], cmap = 'seismic',\
    #                         vmin = -15, vmax = 15\
    #                             )
    # plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.title('1 year clear sky BC LW TOA forcing prp: ' + key)
    # plt.text(10, -120, 'Mean = ' + str(format(area_means[2][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
    # plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_lw',\
    #             dpi = 300)
    # plt.show()


    # plt.figure()
    # mesh = iplt.pcolormesh(net_diffs[key], cmap = 'seismic',\
    #                         vmin = -15, vmax = 15\
    #                             )
    # plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
    #                   orientation = 'horizontal',
    #                     #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
    #                     )
    # plt.title('1 year clear sky BC NET TOA forcing prp: ' + key)
    # plt.text(10, -120, 'Mean = ' + str(format(area_means[4][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
    # plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_net',\
    #             dpi = 300)
#     plt.show()


# plots for double sided cases for sw, lw, and net
for key, value in sw_two_sided_diffs.items():
        
    plt.figure()
    mesh = iplt.pcolormesh(sw_two_sided_diffs[key], cmap = 'seismic',\
                            vmin = -15, vmax = 15\
                                )
    plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                      orientation = 'horizontal',
                        #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                        )
    ax=plt.gca()
    ax.coastlines(linewidth=0.15)
    # plt.title('1 year clear sky BC SW TOA forcing prp: ' + key)
    plt.text(10, -120, 'Mean = ' + str(format(area_means[1][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
    plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_sw',\
                dpi = 300, bbox_inches='tight')
    plt.show()
    

    plt.figure()
    mesh = iplt.pcolormesh(lw_two_sided_diffs[key], cmap = 'seismic',\
                            vmin = -15, vmax = 15\
                                )
    plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                      orientation = 'horizontal',
                        #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                        )
    ax=plt.gca()
    ax.coastlines(linewidth=0.15)
    # plt.title('1 year clear sky BC LW TOA forcing prp: ' + key)
    plt.text(10, -120, 'Mean = ' + str(format(area_means[3][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
    plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_lw',\
                dpi = 300, bbox_inches='tight')
    plt.show()


    plt.figure()
    mesh = iplt.pcolormesh(net_two_sided_diffs[key], cmap = 'seismic',\
                            vmin = -15, vmax = 15\
                                )
    plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                      orientation = 'horizontal',
                        #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                        )
    ax=plt.gca()
    ax.coastlines(linewidth=0.15)
    # plt.title('1 year clear sky BC NET TOA forcing prp: ' + key)
    plt.text(10, -120, 'Mean = ' + str(format(area_means[5][key], '.2f')) + u' W m$^{-2}$', ha = 'center')
    plt.savefig(plot_dir + 'bc_prp_1year_clear_sky_'+key+'_toa_nflx_forcing_net',\
                dpi = 300, bbox_inches='tight')
    plt.show()


### Area mean bar chart#######################################################

font = {'size' : 12}
plt.rc('font', **font)
# plt.rcParams["text.usetex"] = True   # for alpha character

fwd_keys = ['aer_fwd_diff', 'vap_fwd_diff', 'alb_fwd_diff',\
            't_fwd_diff', 'tsurf_fwd_diff', 'fwd_residual']
    
bwd_keys = ['aer_bwd_diff', 'vap_bwd_diff', 'alb_bwd_diff',\
        't_bwd_diff', 'tsurf_bwd_diff', 'bwd_residual']


sw_fwd_area_means = []
sw_bwd_area_means = []
   
for key in fwd_keys:
    sw_fwd_area_means.append(area_means[0][key])

for key in bwd_keys:
    sw_bwd_area_means.append(area_means[0][key])
    
lw_fwd_area_means = []
lw_bwd_area_means = []
   
for key in fwd_keys:
    lw_fwd_area_means.append(area_means[2][key])

for key in bwd_keys:
    lw_bwd_area_means.append(area_means[2][key])
    

        
prp_exp_axis = np.linspace(1, 6, num = 6)
x_axis_offsets = [-0.3, -0.1, 0.1, 0.3]
prp_exp = ['A', 'q', r'$\alpha$', 'T', 'T*', 'o']

width = 0.2

# colours = ['black', 'indigo', 'red']

# fwd_labels = ['q_fwd','T_fwd','T*_fwd']
# bwd_labels = ['q_bwd','T_bwd','T*_bwd']


f, ax = plt.subplots()

ax.bar(prp_exp_axis + x_axis_offsets[0],\
        sw_fwd_area_means,\
        width = width, hatch = '///', label = 'SW fwd', edgecolor = 'black',\
        fill = False)
ax.bar(prp_exp_axis + x_axis_offsets[1],\
        sw_bwd_area_means,\
        width = width, hatch = '\\\\', label = 'SW bwd', edgecolor = 'black',\
        fill = False)
ax.bar(prp_exp_axis + x_axis_offsets[2],\
        lw_fwd_area_means,\
        width = width, hatch = '...', label = 'LW fwd', edgecolor = 'black',\
        fill = False)
ax.bar(prp_exp_axis + x_axis_offsets[3],\
        lw_bwd_area_means,\
        width = width, hatch = 'oo', label = 'LW bwd', edgecolor = 'black',\
        fill = False)

plt.legend(ncol=2)

ax.set_xticks(prp_exp_axis)
ax.set_xticklabels(prp_exp)
plt.ylim(-0.41,0.55)
plt.ylabel(u'Radiative forcing / W m$^{-2}$')
        
ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')

plt.savefig(plot_dir + 'bc_1year_clear_sky_area_mean_prps_bars',\
            dpi=300)
plt.show()