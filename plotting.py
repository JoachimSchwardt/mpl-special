#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variants of the standard 'plot' routine
"""

import numpy as np
import matplotlib.pyplot as plt
from setup import COLORS
from matplotlib.collections import LineCollection


__all__ = ['Colors', 'plot_colorbar', 'plot_lines', 'plot_step']


class Colors():
    """
    Provides a simple periodic list of colors.
    Default:
        colors == None       ->  higher contrast color cycle
        colors == 'default'  ->  default mpl color cycle

    Use 'get_color()' to get the next color in the list.
    You may pass 'inc=0' to prevent incrementing the cycle
    """
    def __init__(self, colors=None, ctr=0):
        """Set the counter to 0 and initialize the colors (see class doc-string)"""
        self.ctr = ctr
        if colors is None:
            self.colors = COLORS
        elif colors == "default":
            self.colors = list(plt.get_cmap("tab10").colors)
        else:
            self.colors = colors
        self.clength = len(self.colors)

    def get_color(self, inc=1):
        """Return the next color in the cycle and increment by 'inc' (default 1)."""
        cval = self.colors[self.ctr % self.clength]
        self.ctr += inc
        return cval

    def prev_color(self):
        """Return the most recently used color"""
        cval = self.colors[(self.ctr - 1) % self.clength]
        return cval


def plot_colorbar(heat, cmap='viridis', orientation="horizontal", width=0.8, height=0.3,
                  figsize=None, x0=None, y0=None, alpha=1.0, label=None):
    """
    Create a standalone colorbar based on a given 'heat'-array.
    Main functionality from ::
        https://stackoverflow.com/questions/16595138/standalone-colorbar-matplotlib
    """
    if orientation == "horizontal":
        if figsize is None:
            figsize = plt.rcParams["figure.figsize"]
            figsize = (figsize[0], 0.2 * figsize[1])
        if x0 is None:
            x0 = 0.1
        if y0 is None:
            y0 = 0.5
        if height > width:
            print(f"Warning, {orientation = } but {width = } smaller than {height = }"
                  "Values will be swapped automatically...")
            width, height = height, width

    elif orientation == "vertical":
        if figsize is None:
            figsize = plt.rcParams["figure.figsize"]
            figsize = (0.15 * figsize[0], figsize[1])
        if x0 is None:
            x0 = 0.2
        if y0 is None:
            y0 = 0.1
        if width > height:
            print(f"Warning, {orientation = } but {height = } smaller than {width = }"
                  "\nValues will be swapped automatically...")
            width, height = height, width

    plt.figure(figsize=figsize)
    plt.imshow(heat, cmap=cmap, alpha=alpha)
    plt.gca().set_visible(False)
    cax = plt.axes([x0, y0, width, height])
    plt.colorbar(orientation=orientation, cax=cax, label=label)
    return cax


def plot_lines(ax, x, y, c, cmap='viridis'):
    """
    Plot lines connecting all pairs of points in the arrays 'x' and 'y'
    with colors in the corresponding array 'c' of the same size.

    https://stackoverflow.com/questions/17240694/python-how-to-plot-one-line-in-different-colors

    Example:
        x, y = (np.random.random((100, 2)) - 0.5).cumsum(axis=0).T
        fig, ax = plt.subplots()
        plot_lines(ax, x, y, c=np.linspace(0, 1, x.shape[0]))
    """

    # Convert format to 'segments = [[(x0,y0),(x1,y1)], [(x0,y0),(x1,y1)], ...]'
    # (-1, ...) --> size of first dimension determined automatically
    xy = np.array([x, y]).T.reshape((-1, 1, 2))
    segments = np.hstack([xy[:-1], xy[1:]])

    coll = LineCollection(segments, cmap=getattr(plt.cm, cmap))
    coll.set_array(c)           # set colors for each line segment

    ax.add_collection(coll)
    ax.autoscale_view()         # important rescaling


def plot_step(ax, x, y, PlotNaNs=False, **kwargs):
    """
    Plot 'y' over 'x' in axis 'ax' and draw horizontal lines for each pair.
    Effectively executes 'plot(new_x, new_y)' for the arrays
        new_x = [x[0], x[1], x[1], x[2], x[2], ...]
        new_y = [y[0], y[0], y[1], y[1], y[2], ...]
    """
    if PlotNaNs:   # handle NaN in y:
        y = np.copy(y)
        ylast = y[~np.isnan(y)][0]
        for i in range(y.shape[0]):
            if np.isnan(y[i]):
                y[i] = ylast
            else:
                ylast = y[i]

    nx = np.outer(x, np.ones(2)).flatten()[1:]
    ny = np.outer(y, np.ones(2)).flatten()[:-1]
    ax.plot(nx, ny, **kwargs)
