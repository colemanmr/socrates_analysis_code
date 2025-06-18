#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:19:27 2024

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


diag_dir = file_loc.diag_dir + \
    'socrates_diags/bc_prp_1year_clear_sky/multiannual_mean_fluxes/'


    
alb_bwd_file = diag_dir  + 'bc_prp_1year_clear_sky_alb_bwd_multiannual_mean_toa_sw.nflx'
t_bwd_file = diag_dir + 'bc_prp_1year_clear_sky_t_bwd_multiannual_mean_toa_sw.nflx'

alb_bwd = iris.load_cube(alb_bwd_file)[0]
t_bwd = iris.load_cube(t_bwd_file)[0]

t_bwd_diff = t_bwd - alb_bwd

area_mean_t_bwd_diff = flux_mod.area_mean_cube(t_bwd_diff)
print(area_mean_t_bwd_diff.data)


alb_fwd_file = diag_dir  + 'bc_prp_1year_clear_sky_alb_fwd_multiannual_mean_toa_sw.nflx'
t_fwd_file = diag_dir + 'bc_prp_1year_clear_sky_t_fwd_multiannual_mean_toa_sw.nflx'

alb_fwd = iris.load_cube(alb_fwd_file)[0]
t_fwd = iris.load_cube(t_fwd_file)[0]

t_fwd_diff = t_fwd - alb_fwd

area_mean_t_fwd_diff = flux_mod.area_mean_cube(t_fwd_diff)
print(area_mean_t_fwd_diff.data)





