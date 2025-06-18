#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 11:02:14 2022

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


def load_ukesm_data(file):
    """
    Load ukesm pp file of 4 sky fluxes on levels, up and down, sw and lw
    :param string: filename of ukesm .pp file to load
    :returns: separate cubes for each of sky types, up/down, sw/lw
    """
    
    # list of cube names to load
    flux_list = [
        'upwelling_shortwave_flux_in_air',\
        'downwelling_shortwave_flux_in_air',\
        'upwelling_longwave_flux_in_air',\
        'downwelling_longwave_flux_in_air',\
        'upwelling_shortwave_flux_in_air_assuming_clear_sky',\
        'downwelling_shortwave_flux_in_air_assuming_clear_sky',\
        'upwelling_longwave_flux_in_air_assuming_clear_sky',\
        'downwelling_longwave_flux_in_air_assuming_clear_sky',\
        'm01s01i519',\
        'm01s01i520',\
        'm01s02i519',\
        'm01s02i520']
    
    # load cubes
    sw_up, sw_down, lw_up, lw_down,\
    clear_sw_up, clear_sw_down, clear_lw_up, clear_lw_down,\
    clearclean_sw_up, clearclean_sw_down, clearclean_lw_up, clearclean_lw_down\
        =iris.load_cubes(file, flux_list)
        
    # clearclean (and clean if add) cubes lose units for some reason
    clearclean_cubes = [clearclean_sw_up,clearclean_sw_down,\
                   clearclean_lw_up,clearclean_lw_down]
    
    for cube in clearclean_cubes:
        cube.units = 'W m-2'
        
    return sw_up, sw_down, lw_up, lw_down,\
    clear_sw_up, clear_sw_down, clear_lw_up, clear_lw_down,\
    clearclean_sw_up, clearclean_sw_down, clearclean_lw_up, clearclean_lw_down\
        
        
def load_soc_single_lev_data(file):
    """
    Load socrates output flux .nc file on one level
    :param string: filename of socrates output .nc file to load
    :returns: one cube of the socrates output flux
    """
    
    # Load cube
    cube = iris.load_cube(file)
    
    # Remove plev dimension as not needed
    cube = cube[0,:,:]
    
    # Add units for differencing to UKESM cubes
    cube.units = 'W m-2'
    
    return cube


def edit_soc_coords(soc_cube, ukesm_cube):
    """
    Make a socrates cube have same lat/lon coords as ukesm cubes
    :param iris.cube soc_cube: socrates cube to change coords of
    :param iris.cube ukesm_cube: an example ukesm cube to use coords from 
    :returns: socrates output flux cube with ukesm coords
    """
    
    # Take lat and lon coords from ukesm cube
    ukesm_lon = ukesm_cube.coord('longitude')
    ukesm_lat = ukesm_cube.coord('latitude')

    # Remove coords from socrates cube
    soc_cube.remove_coord('longitude')
    soc_cube.remove_coord('latitude')

    # Add coords to soc cube; only works atm if has lat/lon dimensions
    soc_cube.add_dim_coord(ukesm_lon, 1)
    soc_cube.add_dim_coord(ukesm_lat, 0)    

    return soc_cube


def load_soc_flux_multi(sky_types, directory, suite, datetime, level, suffix, ukesm_cube):
    """
    Load multiple socrates flux cubes and edit coords to match ukesm
    :param list sky_types: list of strings of sky types (note all sky = '')
    :param string directory: diag_dir
    :param string suite: suite name (without the u-)
    :param string datetime: the datetime of file in form yyyymmddhh
    :param string level: toa or surf
    :param string suffix: update name and flux extension (e.g. 'szen_fix.nflx')
    :param iris.cube ukesm_cube: example ukesm cube for taking coords from
    :returns: list of socrates output flux cubes with ukesm coords
    """
    
    soc_cubes = []
    
    for sky in sky_types:
        sw_file = directory + suite + '_' + datetime + '_' + level + '_sw_'\
        + sky + suffix
        soc_cubes.append(load_soc_single_lev_data(sw_file))
    
        lw_file = directory + suite + '_' + datetime + '_' + level + '_lw_'\
        + sky + suffix
        soc_cubes.append(load_soc_single_lev_data(lw_file))
    

    # Make coords same as ukesm for each cube
    for cube in soc_cubes:
        edit_soc_coords(cube, ukesm_cube)
    
    return soc_cubes


def ukesm_net_down_fluxes(sw_up, sw_down, lw_up):
    """
    Calculate net down fluxes for sw, lw and net from up and down fluxes
    :param iris.cube sw_up: cube of sw up flux
    :param iris.cube sw_down: cube of sw down flux
    :param iris.cube lw_up: cube of lw up flux 
    :returns: cube of net down sw, net down lw and net down total fluxes
    """
    
    # Calculate net fluxes - note works for cube with levels, not just 2D
    ukesm_net_down_sw = sw_down - sw_up
    ukesm_net_down_lw = lw_up*-1
    ukesm_net_down = ukesm_net_down_sw + ukesm_net_down_lw
    
    return ukesm_net_down_sw, ukesm_net_down_lw, ukesm_net_down


def plot_flux(twod_cube, title, save_name, vmin, vmax):
    """
    Plot map of flux on a level
    :param iris.cube twod_cube: 2D cube of fluxes on a level
    :param string title: title for plot
    :param string save_name: full filepath to save plot as
    :param float vmin: min value for colour scale; if zero takes plot default
    :param float vmax: max value for colour scale; if zero takes plot default
    :returns: none - creates plot and saves
    """
    plt.figure()
    plt.title(title)
    if (vmin == 0 and vmax == 0):
        mesh = iplt.pcolormesh(twod_cube, cmap = 'viridis')
    else:
        mesh = iplt.pcolormesh(twod_cube, vmin = vmin, vmax = vmax, cmap = 'viridis')
    plt.colorbar(mesh, shrink = 0.9, label = u'Flux / W m$^{-2}$', \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
    plt.savefig(save_name, dpi = 300)
    plt.show() 
   
   #return
   

def plot_flux_diff(twod_cube, title, save_name, vmin, vmax):
    """
    Plot map of a differences of fluxes on a level
    :param iris.cube twod_cube: 2D cube of a difference of fluxes on a level
    :param string title: title for plot
    :param string save_name: full filepath to save plot as
    :param float vmin: min value for colour scale; if zero takes plot default
    :param float vmax: max value for colour scale; if zero takes plot default
    :returns: none - creates plot and saves
    """
    plt.figure()
    plt.title(title)
    if (vmin == 0 and vmax == 0):
        mesh = iplt.pcolormesh(twod_cube, cmap = 'seismic')
    else:
        mesh = iplt.pcolormesh(twod_cube, vmin = vmin, vmax = vmax,\
                               label = u'Flux diff / W m$^{-2}$',\
                               cmap = 'seismic')
    plt.colorbar(mesh, shrink = 0.9,  \
                  orientation = 'horizontal',
                   #ticks = [-0.02, -0.01, 0, 0.01, 0.02]
                  )
    plt.savefig(save_name, dpi = 300)
    plt.show() 
   
   #return
   
   
