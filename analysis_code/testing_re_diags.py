# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt


file_loc = '/storage/silver/scenario/nn819853/diags/socrates_diags/'

old_re_weight_file = file_loc + 'old_re_weighted.nc'
re_weight_file = file_loc + 're_weighted.nc'
old_weight_file = file_loc + 'old_weight.nc'
weight_file = file_loc + 'weight.nc'

old_re_weighted = iris.load_cube(old_re_weight_file)
re_weighted = iris.load_cube(re_weight_file)
old_weight = iris.load_cube(old_weight_file)
weight = iris.load_cube(weight_file)

# old_re_weighted = old_re_weighted[0,70,:,:].data
# re_weighted = re_weighted[0,70,:,:].data
# old_weight = old_weight[0,70,:,:].data
# weight = weight[0,70,:,:].data


old_re_weighted = old_re_weighted/1000000


# old_re = np.divide(old_re_weighted, old_weight, out=np.zeros_like(old_re_weighted), where=old_weight!=0)
# re = np.divide(re_weighted, weight, out=np.zeros_like(re_weighted), where=weight!=0)
old_re = old_re_weighted / old_weight
re = re_weighted / weight


old_re.units = 'unknown'
re.units = 'unknown'


re_diff = re - old_re
weight_diff = weight - old_weight


plt.figure()
plt.pcolormesh(re_diff[0,70,:,:])
plt.show()

plt.figure()
plt.pcolormesh(weight_diff[0,70,:,:])
plt.show()