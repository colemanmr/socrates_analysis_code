#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 16:23:34 2022

@author: nn819853
"""

import iris
import numpy as np
import matplotlib.pyplot as plt
import Documents.python_code.diagnostics.file_locations_module as file_loc


diag_dir = file_loc.diag_dir + 'socrates_diags/'
filename = diag_dir + 'cd964a.p620140526_dust_tot_aod.pp'


cubes = iris.load(filename)

dust = cubes[0] 
tot_layers = cubes[1] 


tot = tot_layers.collapsed('level', iris.analysis.SUM)


plot_dir = file_loc.plot_dir + 'socrates_plots/'

for size in range(6):
    

    plt.figure()
    iplt.pcolormesh(dust[size])
    plt.show()
    
    plt.figure()
    iplt.pcolormesh(tot[size])
    plt.show()
