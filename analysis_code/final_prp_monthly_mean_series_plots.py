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

import datetime as dt


def calc_socrates_prp(band):
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
    
    # month means in 1year bc prp clear sky run
    yearmonths = ['201407', '201408', '201409', '201410', '201411', '201412',\
                  '201501', '201502', '201503', '201504', '201505', '201506']
    years = [2014, 2014, 2014, 2014, 2014, 2014,\
            2015, 2015, 2015, 2015, 2015, 2015]
    months = [7,8,9,10,11,12,1,2,3,4,5,6]
    
    for case in cases: 
        
        month_cubes = []
        
        for count, yearmonth in enumerate(yearmonths):
            
            filename = diag_dir + 'bc_prp_1year_clear_sky_' + case + '_' + \
                yearmonth + '_toa_' + band + '.nflx'
                
            cube = iris.load_cube(filename)
            
            del cube.attributes['history']
            
            # new_coord = iris.coords.AuxCoord(\
            #             1,\
            #             long_name='month', units='no_unit')
            # cube.add_aux_coord(new_coord)
            
            # new_coord = iris.coords.DimCoord(\
            #             dt.date(year=years[count], month=months[count],
            #                     day=15), long_name='time', units='no_unit')
            # cube.add_dim_coord(new_coord,0)
            
            new_coord = iris.coords.AuxCoord(count, long_name='height', units='m')
            cube.add_aux_coord(new_coord)
            
            month_cubes.append(cube[0])
            
        monthly_means_cubelist = iris.cube.CubeList(month_cubes)  
        monthly_means = monthly_means_cubelist.merge_cube()
        
        
        cubes.append(monthly_means)
        
    print(cubes)
    print(cubes[0])
        
   
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
            diff = cubes[count] - cubes[count+1]
            print(cubes_check[count], ' minus ', cubes_check[count+1])
        
        # backward differences
        elif count < 11:
            diff = cubes[count+1] - cubes[count]
            print(cubes_check[count+1], ' minus ', cubes_check[count])
            
        # final backward difference (bwd_residual) needs special indexing
        elif count == 11:
            diff = cubes[0] - cubes[count]
            print(cubes_check[0], ' minus ', cubes_check[count])
        
        # enter differences into dictionary
        diffs[diff_case] = diff
        
        
    # add total difference between cont and pert to dictionary
    total_pert = cubes[0] - cubes[6]
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
        # area_mean_dict[key] = np.round(area_mean_diff.data, 2)
        area_mean_dict[key] = area_mean_diff.data
    


###Plotting###################################################################


# set directory for saving plots to
plot_dir = file_loc.plot_dir + \
    'socrates_plots/bc_prp_1year_clear_sky_final_flux_plots/'
    
###Line plot##################################################################

# # array for months
# months_axis = np.linspace(1,12,num=12)


# # fwd_keys = ['aer_fwd_diff', 'vap_fwd_diff', 'alb_fwd_diff',\
# #             't_fwd_diff', 'tsurf_fwd_diff', 'fwd_residual']
    
# # bwd_keys = ['aer_bwd_diff', 'vap_bwd_diff', 'alb_bwd_diff',\
# #         't_bwd_diff', 'tsurf_bwd_diff', 'bwd_residual']
    
# # two_sided_keys = ['aer_diff', 'vap_diff', 'alb_diff',\
# #         't_diff', 'tsurf_diff', 'residual_diff']

# # line_colours = ['b', 'g', 'r', 'y', 'm', 'c']


# fwd_keys = ['vap_fwd_diff', 't_fwd_diff', 'tsurf_fwd_diff']
# bwd_keys = ['vap_bwd_diff', 't_bwd_diff', 'tsurf_bwd_diff']
# two_sided_keys = ['vap_diff', 't_diff', 'tsurf_diff']

# labels=['q','T','T*']
    
# line_colours = ['black', 'indigo', 'red']

# xticks = [2,4,6,8,10,12]
# xtick_labels = ['Aug', 'Oct', 'Dec', 'Feb', 'Apr', 'Jun']

# ### if time would be better as a bar chart
# f, ax = plt.subplots()
# plt.plot(months_axis, area_means_lw['vap_fwd_diff'].data, label = 'fwd', linestyle='--', color='k')
# plt.plot(months_axis, area_means_lw['vap_bwd_diff'].data, label = 'bwd', linestyle='-.', color='k')
# plt.plot(months_axis, area_means_lw_two_sided['vap_diff'].data, label = 'mean', linestyle='-', color='k')
# # plt.plot(months_axis, area_means_lw_two_sided['aer_diff'].data, label = 'I', linestyle='-', color='w')
# for count, key in enumerate(fwd_keys):
#     plt.plot(months_axis, area_means_lw[key].data, linestyle='--', color=line_colours[count])
# for count, key in enumerate(bwd_keys):
#     plt.plot(months_axis, area_means_lw[key].data, linestyle='-.', color=line_colours[count])
# for count, key in enumerate(two_sided_keys):
#     plt.plot(months_axis, area_means_lw_two_sided[key].data, label = labels[count], linestyle='-', color=line_colours[count])
# plt.ylim(-1.2,1)
# plt.ylabel(u'Radiative forcing / W m$^{-2}$')
# plt.xlabel('Month')
# ax.set_xticks(xticks)
# ax.set_xticklabels(xtick_labels)
# plt.legend(ncol = 2, labelcolor=['black','black','black','white','black','black','black','black'])
# plt.savefig(plot_dir + 'bc_1year_clear_sky_lw_monthly_area_mean_prps', dpi=300)
# plt.show()


###Bar chart##################################################################

font = {'size' : 12}
plt.rc('font', **font)
plt.tight_layout()

fwd_keys = ['vap_fwd_diff', 't_fwd_diff', 'tsurf_fwd_diff']
bwd_keys = ['vap_bwd_diff', 't_bwd_diff', 'tsurf_bwd_diff']
two_sided_keys = ['vap_diff', 't_diff', 'tsurf_diff']

mid_season_month_axis = np.linspace(1, 4, num = 4)
x_axis_offsets = [-0.25, 0, 0.25]
mid_season_months = ['Jul', 'Oct', 'Jan', 'Apr']

width = 0.25

colours = ['dimgray', 'indigo', 'red']

# fwd_labels = ['q_fwd','T_fwd','T*_fwd']
# bwd_labels = ['q_bwd','T_bwd','T*_bwd']
var_labels = ['q','T','T*']


f, ax = plt.subplots()

# add duplicates of some for legend
ax.bar(mid_season_month_axis + x_axis_offsets[0],\
        area_means_lw_two_sided['vap_diff'][[0,3,6,9]].data,\
        width=width, label = 'mean', color = 'black', alpha = 0.5)
plt.plot(mid_season_month_axis + x_axis_offsets[0],\
        area_means_lw['vap_fwd_diff'][[0,3,6,9]].data,\
        label = 'fwd', color = 'black', linestyle='', marker='x')
plt.plot(mid_season_month_axis + x_axis_offsets[0],\
        area_means_lw['vap_bwd_diff'][[0,3,6,9]].data,\
        label = 'bwd', color = 'black', linestyle='', marker='o')

for count, key in enumerate(two_sided_keys):
    ax.bar(mid_season_month_axis + x_axis_offsets[count],\
           area_means_lw_two_sided[key][[0,3,6,9]].data,\
           width=width, label = var_labels[count], color = colours[count],\
           alpha = 0.5)
for count, key in enumerate(fwd_keys):
    plt.plot(mid_season_month_axis + x_axis_offsets[count],\
           area_means_lw[key][[0,3,6,9]].data,\
           color = colours[count],\
           linestyle = '', marker = 'x')
for count, key in enumerate(bwd_keys):
    plt.plot(mid_season_month_axis + x_axis_offsets[count],\
           area_means_lw[key][[0,3,6,9]].data,\
           color = colours[count],\
           linestyle = '', marker = 'o')

plt.legend(ncol=2)

ax.set_xticks([1,2,3,4])
ax.set_xticklabels(mid_season_months)

ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
plt.ylim(-1,1)
plt.ylabel(u'Radiative adjustment forcing / W m$^{-2}$', labelpad = 0)
        
ax.axhline(y=0, xmin = 0, xmax = 1, color = 'darkgrey', linestyle = ':')

plt.savefig(plot_dir + 'bc_1year_clear_sky_lw_monthly_area_mean_prps_bars',\
            dpi=300)
plt.show()
    


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


