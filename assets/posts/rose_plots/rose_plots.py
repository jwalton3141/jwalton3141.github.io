#!/usr/bin/env python3.5

import numpy as np
import matplotlib.pyplot as plt

def rose_plot1(ax, angles, bins=16, density=None, xticks=True, **param_dict):
    """ Plots polar histogram of angles. ax must have been created with using kwarg 
    subplot_kw=dict(projection='polar').
    """
    # To be safe, make a coppy of angles before transforming
    data = angles.copy()
    # Transform angles to range [0, 2pi)
    data %= 2*np.pi
    
    # Remove distracting grid
    ax.grid(False)
    
    # Bin data in and record count
    count, bin = np.histogram(data, bins=np.linspace(0, 2*np.pi, num=bins+1))
    
    # By default plot density instead of frequency (frequency potentially misleading)
    if density is None or density is True:
        # Area to assign each bin
        area = count / data.size
        # Calculate corresponding bin radius
        radius = (area / np.pi)**.5
    else:
        radius = count
    
    # Plot data on ax
    ax.bar(bin[:-1] + np.pi/bins, radius, width=2*np.pi/bins, zorder=1, edgecolor='C0', fill=False,
           linewidth=1, **param_dict)
    
    	# Remove ylabels, they are obstructive and not informative
    ax.set_yticks([])
    
    if xticks:
        # Label angles according to convention
        angle_pos = [0, np.pi/2, np.pi, 3*np.pi/2]
        angle_label = ['$0$', r'$\pi/2$', r'$-\pi, \pi$', r'-$\pi/2$']
        ax.set_xticks(angle_pos)
        ax.set_xticklabels(angle_label)
    else:
        ax.set_xticks([])


def rose_plot2(ax, angles, bins=16, density=None, xticks=True, **param_dict):
    """ Plots polar histogram of angles. ax must have been created with using kwarg 
    subplot_kw=dict(projection='polar').
    """
    # To be safe, make a coppy of angles before transforming
    data = angles.copy()
    # Transform angles to range [0, 2pi)
    data %= 2*np.pi
    
    # Remove distracting grid
    ax.grid(False)
    
    # Bin data in and record count
    count, bin = np.histogram(data, bins=np.linspace(0, 2*np.pi, num=bins+1))
    
    # By default plot density instead of frequency (frequency potentially misleading)
    if density is None or density is True:
        # Area to assign each bin
        area = count / data.size
        # Calculate corresponding bin radius
        radius = (area / np.pi)**.5
    else:
        radius = count
    
    # Plot data on ax
    ax.bar(bin[:-1] + np.pi/bins + np.pi/2, radius, width=2*np.pi/bins, zorder=1, edgecolor='C0', fill=False,
           linewidth=1, **param_dict)
    
    	# Remove ylabels, they are obstructive and not informative
    ax.set_yticks([])
    
    if xticks:
        # Label angles according to convention
        angle_pos = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) + np.pi/2
        angle_label = [r'$0^\circ$', r'$90^\circ$', r'$180^\circ$', r'$270^\circ$']
        ax.set_xticks(angle_pos)
        ax.set_xticklabels(angle_label)
    else:
        ax.set_xticks([])

from plot.pretty import set_size

# Generate random directions
angles0 = np.random.normal(loc=0, scale=1, size=10000)
angles1 = np.random.uniform(-np.pi, np.pi, size=100)

# Visualise with polar histogram
fig, ax = plt.subplots(1, 2, figsize=set_size(subplot=[1, 2]), subplot_kw=dict(projection='polar'))
rose_plot1(ax[0], angles0)
rose_plot1(ax[1], angles1)
fig.savefig('polar_radians.png', format='png', bbox_inches='tight', dpi=1200)

# Visualise with polar histogram
fig, ax = plt.subplots(1, 2, figsize=set_size(subplot=[1, 2]), subplot_kw=dict(projection='polar'))
rose_plot2(ax[0], angles0)
rose_plot2(ax[1], angles1)
fig.savefig('polar_degrees.png', format='png', bbox_inches='tight', dpi=1200)
