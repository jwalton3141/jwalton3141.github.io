---
layout: post
title: Plot publication-quality figures with matplotlib and LaTeX
image: https://jwalton3141.github.io/assets/publication_quality/new_style.png
mathjax: false
comments: true
---

Figures are an incredibly important aspect of effectively communicating research and ideas. Poor quality figures are difficult to read and interpret. At their worse, bad figures are simply misleading. Good quality plots, however, blend seamlessly with a document, they are readable, clear, concise and aesthetically pleasing.

So, if you care about your research (and, since you're here, I'm going to take that as a given) you should care about your figure presentation too. Producing graphics isn't the most exciting aspect of research, but it is an essential and unavoidable part of it.

This post will introduce the essential skills and ideas you'll need to produce publication-quality figures using the Python plotting package [matplotlib](https://matplotlib.org/). We'll learn how to seamlessly embed figures into [LaTeX](https://www.latex-project.org/about/) documents and [beamer presentations](https://ctan.org/pkg/beamer?lang=en). Minimum working examples will be provided to fully illustrate figure production.

It is assumed that the reader already has some familiarity with matplotlib. References and links will be provided to relevant literature and further reading.

# Colour and styling

One of the first things that a reader will notice about your figures is theicoir colour scheme and styling. Many matplotlib users are languishing behind the times with an old install of the package. More recent releases of matplotlib (>= v2.0) feature improved styling. [This excellent talk from Scipy's 2015 conference](https://www.youtube.com/watch?v=xAoljeRJ3lU]) delves into some of the theory behind the new default colourmap. If you aren't sure how to get the latest install, you can [refer to the documentation provided by matplotlib](https://matplotlib.org/users/installing.html).

[![old_style](/assets/publication_quality/old_style.png "Old default"){:class="img-responsive"}](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html)
[![new_style](/assets/publication_quality/new_style.png "New default"){:class="img-responsive"}](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html)


Matplotlib also provides [many different style sheets for you to try out](https://matplotlib.org/devdocs/gallery/style_sheets/style_sheets_reference.html). You can list the available styles with
```py
import matplotlib.pyplot as plt
plt.style.available
```

Style sheets allow the user to effortlessly swap between styles without having to alter their plotting routines. As an example, to change to the [seaborn](https://seaborn.pydata.org/) style we would use ```plt.style.use('seaborn')```.

# Seamless embedding in LaTeX

It's relatively easy to get our figures to blend nice with our LaTeX document. However, it isn't going to happen by accident. In this section we'll cover the two key ingredients for a well-embedded plot: determining our desired figure dimensions in matplotlib and using LaTeX to typeset the text in our figure.
Later in this post we shall also discuss the best file formats to save and preserve your new figures. Finally we will see how to insert these figures into LaTeX.

## Determining figure size

The key to seamlessly blending your matplotlib figures into your LaTeX document is in determining the desired dimensions of the figure *before* creation. In this way, when you insert your figure it will not need to be resized, and therefore the fontsize and aspect ratio won't be altered. The figure you produce with matplotlib will be the *exact* figure you see in your LaTeX document.

Our first step to creating appropriately sized figures is to determine the textwidth of ourLaTeX document. To do this we can make use of the ```\showthe``` command. If we wished to determine the width of a 10pt report, we could do so by compiling this dummy ```.tex``` file:
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

You may find it useful to predefine widths which you use regularly to your ```set_size``` function. Examples could be the textwidth of your thesis document, a journal you submit to, or a beamer template. Our amended function may include:
```py
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
```

## Text rendering with LaTeX

To really make our figures blend with our document we need the font to match between our figure and the body of our text. [This topic is well-covered in matplotlib's documentation](https://matplotlib.org/users/usetex.html), though I cover it here for completeness.

We shall use LaTeX to render the text in our figures by updating our [```rc settings```](http://matplotlib.org/users/customizing.html#the-matplotlibrc-file). This update can also be used to ensure that the document and figure use the same font sizes. The example below shows how to update ```rcParams``` to use LaTeX to render your text:
```py
""" A simple example of creating a figure with text rendered in LaTeX. """

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
        # Use 10pt font in plots, to match 10pt font in document
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
```

rcParams can be used to control many other aspects of your figures. Run ```mpl.rcParams``` to return a dictionary object detailing your current settings.

## Handling multiple axes

It's often easier to handle subfigures at the matplotlib level, rather than within LaTeX. To insert plots with subfigures we need to understand how to adjust figure dimensions for multiple axes.

Consider a figure containing subfigures arranged into 5 rows and 2 columns. It's easy to imagine (if you can't, try it for yourself) how using our previously defined ```set_size``` will not handle plots with multiple axes well.

Fortunately, our function is easy to adapt. Simply add the default argument ```subplot=[1, 1]``` to the function definition. Along with this, you must change the line which calculates the figure height to ```fig_height_in = fig_width_in * golden_ratio * (subplot[0] / subplot[1])```. We'd initialise a figure with 5 rows and 2 columns of axes as ```fig, ax = plt.subplots(5, 2, figsize=set_size(width, subplot=[5, 2]))```.

## Save format

Some file formats are better suited than others when saving your plots. If you are submitting to a journal it is essential that you first check which formats they will accept.

I would strongly recommend the use of a file format which can store vector images. Vector images allow the reader to zoom into a plot indefinitely, without encountering any pixelation. This is not true for raster images. Examples of raster image formats are .png and .jpeg; examples of vector graphic formats are .svg and .pdf. If, for whatever reason, you wish to continue using raster graphics - [make sure to use .png and not .jpeg.](https://www.labnol.org/software/tutorials/jpeg-vs-png-image-quality-or-bandwidth/5385/)

[![raster_v_vector](/assets/publication_quality/raster_v_vector.svg "Raster vs vector"){:class="img-responsive"}](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics#/media/File:Bitmap_VS_SVG.svg)

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

The ```graphicx``` package may then be used to insert this figure into LaTeX:

```tex
% your document class here
\documentclass[10pt]{report}
% package necessary to inset pdf as image
\usepackage{graphicx}

\begin{document}

\begin{figure}[!htbp]
	\centering
	\includegraphics{/path/to/directory/example_1.pdf}
	\caption{Our first figure.}
\end{figure}

\end{document}
```

Typically, alongside figures typeset in LaTeX you'll see ```[width=\textwidth]```. However, now that our figures are created to specification, this command becomes superfluous.

# Summary

In this post we have seen how easy it is to change the style of our plots. We have learnt that to effectively present figures in a document we must take care to create a figure of the correct dimensions. With the correct dimensions our figure avoids any unwanted scaling and change in aspect ratio. After a brief discussion of why we should save our figures in the ```.pdf``` format, we discussed how to use LaTeX to render the fonts in our figures. Putting all these things together we can now produce truly publication-quality plots, and embed them in our work.
