---
layout: post
title: Visualising circular data in matplotlib
image: https://jwalton3141.github.io/assets/rose_plots/polar_radians.png
mathjax: true
comments: true
---

Circular data arises very naturally in many different situations. Meterologists regularly encounter directional data when considering wind directions, ecologists may come across angular data when looking at the directions of motion of animals, and we all come into contact with at least one type of circular data every day: the time.

## Visualisation

In possession of a dataset, one of the first instincts of the scientist or researcher is to visualise their data. The researcher is undoubtedly familiar with a large number of graph types. Yet choosing the most suitable graph to display a given dataset is crucial in making an informative plot.

Traditional histograms are not very good for visualising directional data, they are not an intuitive way to visualise circular data. However, polar histograms (sometimes known as [rose plots](https://en.wikipedia.org/wiki/Wind_rose)) make the visualisation of such data easier. Instead of using bars, as the histogram does, the rose plot bins data into sectors of a circle. The area of each sector is proportional to the frequency of data points in the corresponding bin.

The polar histograms below visualise two randomly generated datasets, where the *area* of each sector is proportional to the number of observations in that bin. The helper function I used to create these plots is given below.

<img width="708" height="328" src="/assets/rose_plots/polar_radians.png" style="display: block; margin-left: auto; margin-right: auto; height: auto">

## Python implementation

In visualising circular data as part of my research, I came across existing angular plotting routines in python (see [1](https://matplotlib.org/examples/pie_and_polar_charts/polar_bar_demo.html), [2](https://stackoverflow.com/a/22568292) and [3](https://plot.ly/python/wind-rose-charts/)). I was, however, unsatisfied with these implementations --- all of which I found unsightly, cluttered, and not fit for purpose. Fortunately, it was a relatively quick job to construct an improved matplotlib implementation, as is included below:

```py
import numpy as np
import matplotlib.pyplot as plt

def rose_plot(ax, angles, bins=16, density=None, xticks=True, **param_dict):
    """ Plots polar histogram of angles. ax must have been created with using kwarg 
    subplot_kw=dict(projection='polar').
    """
    # To be safe, make a coppy of angles before wrapping
    data = angles.copy()
    # Wrap angles to range [0, 2pi)
    data %= 2*np.pi
    
    # Remove distracting grid
    ax.grid(False)
    
    # Bin data and record counts
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
```

With this function we can go ahead and construct our plots.


```py
plt.style.use('seaborn')

# Generate random directions
angles0 = np.random.normal(loc=0, scale=1, size=10000)
angles1 = np.random.uniform(-np.pi, np.pi, size=100)

# Visualise with polar histogram
fig, ax = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))
rose_plot(ax[0], angles0)
rose_plot(ax[1], angles1)
fig.savefig('polar.png', format='png', bbox_inches='tight', dpi=1200)
```

## A note on convention

Directions can be represented as rotations with respect to some zero–direction, or origin. The practitioner is free to chose the zero–direction as they feel appropriate. In a similar way, the practitioner may choose whether a clockwise or anti–clockwise rotation is taken as the positive direction.

Here I take the zero angle as the direction from \\((0, 0)\\) and along the positive \\(x\\)–axis, and take anti-clockwise rotations as the positive direction. Angles are chosen to be measured in radians and restricted to the domain \\((-\pi, \pi)\\). I define angles this way to be consistent with the definition of the [atan2 function](https://en.wikipedia.org/wiki/Atan2).

The helper function above is hard-coded to plot using this convention. However, it is easy to adapt the function to whatever angle convention you use. For example, consider that you define your 0 angle as the direction from \\((0, 0\\)) and along the positive \\(y\\)-direction (pointing North). To correct for this add a rotation of \\(\pi/2\\) to the call to ```ax.bar``` so that you now have.
```py
# Add rotation
ax.bar(bin[:-1] + np.pi/bins + np.pi/2, radius, width=2*np.pi/bins, zorder=1, edgecolor='C0',
		fill=False, linewidth=1, **param_dict)
```
The labels of the plot now also need rotating. It is also easy to alter the labels to measure in units of degrees instead of radians. The lines below make these alterations.
```py
# Add rotation
angle_pos = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) + np.pi/2
# Label in degrees
angle_label = [r'$0^\circ$', r'$90^\circ$', r'$180^\circ$', r'$270^\circ$']
```
Putting this altogether we plot the same randomly generated dataset as before, but measuring in degrees and with the 0 direction taken to point North.

<img width="708" height="328" src="/assets/rose_plots/polar_degrees.png" style="display: block; margin-left: auto; margin-right: auto; height: auto">
