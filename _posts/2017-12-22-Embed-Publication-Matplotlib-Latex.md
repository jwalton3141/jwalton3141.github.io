---
layout: post
title: Publication-quality plots with matplotlib and LaTex
image: https://jwalton3141.github.io/assets/new_style.png
---

Figures are an incredibly important aspect of effectively communicating research and ideas. Poor quality figures are difficult to read and interpret. At their worse, bad figures are simply misleading. Good quality plots, however, blend seamlessly with a document, they are readable, clear, concise and aesthetically pleasing.

So, if you care about your research (and, since you're here, I'm going to take that as a given) you should care about your figure presentation too. Producing graphics isn't the most exciting aspect of research, but it is an essential and unavoidable part of it.

This post will introduce the essential skills and ideas you'll need to produce publication-quality figures using the Python plotting package [matplotlib](https://matplotlib.org/). We'll learn how to seamlessly embed figures into [LaTex](https://www.latex-project.org/about/) documents and [beamer presentations](https://ctan.org/pkg/beamer?lang=en). Minimum working examples will be provided to fully illustrate figure production.

It is assumed that the reader already has some familiarity with matplotlib, however, more advanced ability is not assumed. References and links will be provided to relevant literature and further reading.

# Colour and styling

One of the first things that a reader will notice about your figures is their colour scheme and styling. Many matplotlib users are languishing behind the times with an old install of the package. More recent releases of matplotlib (>= v2.0) feature improved styling. [This excellent talk from Scipy's 2015 conference](https://www.youtube.com/watch?v=xAoljeRJ3lU]) delves into some of the theory behind the new default colourmap. If you aren't sure how to get the latest install, [refer to the documentation provided by matplotlib](https://matplotlib.org/users/installing.html).

[![old_style](/assets/old_style.png "Old default"){:class="img-responsive"}](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html)
[![new_style](/assets/new_style.png "New default"){:class="img-responsive"}](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html)


If you remain unhappy with the default styling, matplotlib provides [many different style sheets for you to try out](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html). Alternatively you could use
```py
import matplotlib.pyplot as plt
plt.style.available
```
to list our style options.

Style sheets allow the user to effortlessly swap between styles without having to alter their plotting routines. As an example, to change to the [seaborn](https://seaborn.pydata.org/) style we would use ```plt.style.use('seaborn')```.

# Seamless embedding in LaTex

Whether you wish to pen a research paper, your doctoral thesis or a report for a colleague, many will wish to embed figures from matplotlib into a [LaTex](https://www.latex-project.org/about/) document. To maintain the desired aspect ratio of your figures, to avoid unwanted scaling and to allow font size to be matched between figure and the body of your text, we must learn to set the dimensions of your figure correctly. Later in this post we shall discuss the best file formats to save and preserve your new figures. Finally we show how to insert your figures into LaTex.

## Determining figure size

The key to seamlessly blending your matplotlib figures into your LaTex document is in determining the desired dimensions of the figure *before* creation. In this way, when you insert your figure it will not need to be resized, and therefore font and aspect ratio will remain true to your specifications. The figure you produce with matplotlib will be the *exact* figure you see in your LaTex document.

Our first step to creating appropriately sized figures is to determine the width of our document. To do this we can make use of the ```\showthe``` command. If we wished to determine the width of a 10pt report, we could do so by compiling this dummy ```.tex``` file:
```tex
% your document class here
\documentclass[10pt]{report}
\begin{document}

% gives the width of the current document in pts
\showthe\textwidth

\end{document}
```
After compilation open the associated ```.log``` file. Within this output you should find your textwidth. Following our above example, within our ```.log``` file we find our document is 345pts wide:
```tex
> 345.0pt.
l.6 \showthe\textwidth
```
If you're plotting in a document typeset in columns, you may use ```\showthe\columnwidth``` in a similar manner.

To specify the dimensions of a figure in matplotlib we use the ```figsize``` argument. However, the figsize argument takes input in inches and we have the width of our document in pts. To set the figure size we can use a function to convert from pts to inches and to set an aesthetic aspect ratio:
```py
def set_size(width, fraction=1):
    """ Set aesthetic figure dimensions to avoid scaling in latex.

    Parameters
    ----------
    width: float
            Width in pts
    fraction: float
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim
```
You may wish to keep the ```set_size``` function in a module ```my_plot.py```. Using this function we may create a figure which fits the width of our document perfectly:
```py
import matplotlib.pyplot as plt
# if keeping the set_size function in my_plot module
from my_plot import set_size

width = 345
fig, ax = plt.subplots(1, 1, figsize=set_size(width))
```
If you desire to create a figure narrower than the textwidth you may use the fraction argument. For example, to create a figure half the width of your document:
```py
fig, ax = plt.subplots(1, 1, figsize=set_size(width, fraction=0.5))
```

You may find it useful to predefine widths which you use regularly to your ```set_size``` function. Examples could be the textwidth of your thesis document, a journal you submit to, or a beamer template. Your revised function may now look something like the one below.
```py
def set_size(width, fraction=1):
    """ Set aesthetic figure dimensions to avoid scaling in LaTex.

    Parameters
    ----------
    width: float or string
            Width in pts or a predefined size, 'thesis', 'beamer', 'pnas'
    fraction: float
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: list
            Dimensions of figure in inches
    """
    # If using a pre-defined width
    if width == 'thesis':
        width_pt = 426.79135
    elif width == 'beamer':
        width_pt = 307.28987
    elif width == 'pnas':
        width_pt = 246.09686
    else:
        width_pt = width
    # Width of figure
    fig_width_pt = width_pt * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = [fig_width_in, fig_height_in]

    return fig_dim
```

## Save format

When it comes to saving your now beautifully rendered figures - some file formats are better suited than others. If you are submitting to a journal it is essential that you first check which formats they will accept.

I would strongly recommend the use of a file format which can store vector images. Vector images allow the reader to zoom into a plot indefinitely, without encountering any pixelation. This is not true for raster images. Examples of raster image formats are .png and .jpeg; examples of vector graphic formats are .svg and .pdf. If, for whatever reason, you wish to continue using raster graphics - [make sure to use .png and not .jpeg.](https://www.labnol.org/software/tutorials/jpeg-vs-png-image-quality-or-bandwidth/5385/)

[![raster_v_vector](/assets/raster_v_vector.svg "Raster vs vector"){:class="img-responsive"}](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics#/media/File:Bitmap_VS_SVG.svg)

Below we create a simple figure and save it in the ```.pdf``` format. To remove excess whitespace which matplotlib pads plots with we may use ```bbox_inches='tight'```:

```py
""" A simple example of creating a figure and saving as a pdf. """
import matplotlib.pyplot as plt
from my_plot import set_size
import numpy as np

# Using seaborn's style
plt.style.use('seaborn')
width = 345

x = np.linspace(0, 2*np.pi, 100)
# Initialise figure instance
fig, ax = plt.subplots(1, 1, figsize=set_size(width))

# Plot
ax.plot(x, np.sin(x))
ax.set_xlim(0, 2*np.pi)
ax.set_xlabel(r'$\theta$')
ax.set_ylabel(r'$\sin{(\theta)}$')

# Save and remove excess whitespace
plt.savefig('/path/to/directory/example_1.pdf', format='pdf', bbox_inches='tight')
```

The ```graphicx``` package may then be used to insert this figure into LaTex:

```tex
% your document class here
\documentclass[10pt]{report}
% package necessary to inset pdf as image
\usepackage{graphicx}

\begin{document}

\begin{figure}[!htbp]
	\centering
	\includegraphics[width=\textwidth]{/path/to/directory/example_1.pdf}
	\caption{Our first figure.}
\end{figure}

\end{document}
```

## Text rendering with LaTeX

To really make our figures blend with our document we need the font to match between our figure and the body of our text. [This topic is well-covered in matplotlib's documentation](https://matplotlib.org/users/usetex.html), however I shall cover the topic here for completeness.

We shall use LaTex to render the text in our figures by updating our [```rc settings```](http://matplotlib.org/users/customizing.html#the-matplotlibrc-file). This update can also be used to ensure that the document and figure use the same font sizes. Extending our earlier example we now have:
```py
""" A simple example of creating a figure and saving as a pdf, with text rendered with LaTex. """

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from my_plot import set_size

# Using seaborn's style
plt.style.use('seaborn')
width = 345

nice_fonts = {
        # Use LaTeX to write all text
        "text.usetex": True,
        "font.family": "serif",
        # Use 10pt font in plots
        "axes.labelsize": 10,
        "font.size": 10,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
}

mpl.rcParams.update(nice_fonts)

x = np.linspace(0, 2*np.pi, 100)
# Initialise figure instance
fig, ax = plt.subplots(1, 1, figsize=set_size(width))
# Plot
ax.plot(x, np.sin(x))
ax.set_xlim(0, 2*np.pi)
ax.set_xlabel(r'$\theta$')
ax.set_ylabel(r'$\sin{(\theta)}$')

plt.savefig('/path/to/directory/example_2.pdf', format='pdf', bbox_inches='tight')
```

The figure produced looks professional and aesthetically pleasing - it will also look great when embedded into a report.

# Summary

In this post we have seen how easy it is to change the style of our plots. We have learnt that to effectively present figures in a document we must take care to create a figure of the correct dimensions. With the correct dimensions our figure avoids any unwanted scaling and change in aspect ratio. After a brief discussion of why we should save our figures in the ```.pdf``` format, we discussed how to use LaTex to render the fonts in our figures. Putting all these things together we can now produce truly publication-quality plots, and embed them in our work.
