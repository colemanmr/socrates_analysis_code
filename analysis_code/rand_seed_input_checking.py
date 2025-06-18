#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 15:16:05 2023

@author: nn819853
"""

# from __future__ import print_function

import sys
sys.path.append('/home/users/nn819853/Documents/python_code')

import iris
import numpy as np
# import matplotlib.pyplot as plt
# import iris.quickplot as qplt
# import iris.plot as iplt
# import Documents.python_code.diagnostics.file_locations_module as file_loc
# import diagnostics.radiative_fluxes.fluxes_module as flux_mod

np.set_printoptions(precision=9)

# def print(*args):
#     __builtins__.print(*("%.2f" % a if isinstance(a, float) else a
#                          for a in args))
    

filename = '~/cd964_2014013000.ocs'

ocs_cube = iris.load_cube(filename)

seed = ocs_cube[0,:,:]


