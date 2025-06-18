#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 15:18:51 2022

@author: nn819853
"""


import iris 
import numpy as np
import matplotlib.pyplot as plt


#'/home/users/nn819853/stoa_cosszen_20140101_example.nc'
filename = '/home/users/nn819853/cd964_diags_01142_01218_201401020100.pp'

cubes = iris.load(filename)

# cubes_save = iris.cube.CubeList([cubes[0],cubes[28]])
# iris.save(cubes_save, '/home/users/nn819853/stoa_cosszen_20140101_example.nc')

cos_szen = cubes[0].data
stoa = cubes[1][85].data


boolean_cos_szen = np.zeros_like(cos_szen)
boolean_stoa = np.zeros_like(stoa)


for i in range(144):
    for j in range(192):
        if cos_szen[i,j] > 0:
            boolean_cos_szen[i,j] = 1

for i in range(144):
    for j in range(192):
        if stoa[i,j] > 0:
            boolean_stoa[i,j] = 1       
            
            
boolean_match = np.zeros_like(stoa)

for i in range(144):
    for j in range(192):
        if boolean_cos_szen[i,j] == boolean_stoa[i,j]:
            boolean_match[i,j] = 0
        elif boolean_cos_szen[i,j] > boolean_stoa[i,j]:
            boolean_match[i,j] = 1
        else:
            boolean_match[i,j] = -1
            
            
plt.pcolormesh(boolean_match)
plt.colorbar()
plt.show()
            

