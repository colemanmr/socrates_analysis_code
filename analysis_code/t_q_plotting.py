#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:41:14 2024

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


cd964_t_file = 'cd964_t_1year_month_means.pp'
db548_t_file = 'db548_t_1year_month_means.pp'

cd964_q_file = 'cd964_q_1year_month_means.pp'
db548_q_file = 'db548_q_1year_month_means.pp'


cd964_t = iris.load_cube(diag_dir + cd964_t_file)
db548_t = iris.load_cube(diag_dir + db548_t_file)

cd964_q = iris.load_cube(diag_dir + cd964_q_file)
db548_q = iris.load_cube(diag_dir + db548_q_file)


cd964_t_mean,_,_ = flux_mod.time_mean_cube(cd964_t)
db548_t_mean,_,_ = flux_mod.time_mean_cube(db548_t)

cd964_q_mean,_,_ = flux_mod.time_mean_cube(cd964_q)
db548_q_mean,_,_ = flux_mod.time_mean_cube(db548_q)


t_adjust = cd964_t_mean - db548_t_mean
q_adjust = cd964_q_mean - db548_q_mean



### plotting #################################################################

# set plot directory
plot_dir = file_loc.plot_dir + 'socrates_plots/bc_prp_1year_clear_sky_adjustments/'



plt.figure()
mesh = iplt.pcolormesh(t_adjust.collapsed('longitude', iris.analysis.MEAN),\
                       cmap = 'seismic',
                        # vmin = 0.0, vmax = 1.0,
                        )
plt.colorbar(mesh, shrink = 0.9, label = 'atmospheric temperature / K', \
                  orientation = 'horizontal',
                    #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                    )
# plt.savefig(plot_dir + 'cd964_sw_albedo_control_dir_201501_band_'\
            # + str(band), dpi = 300)
# plt.title('Control SW direct surface albedo: jan mean, band ' + str(band) )
plt.show()
