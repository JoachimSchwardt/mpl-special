#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Special tools for annotating data
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def annotate_points(ax, text, x, y, yoffset=0.03, align='center',
                    TextBelow=False, **kwargs):
    """Annotate a set of points (above or below)"""
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)

    if align == 'left':
        xpos = xmin
    elif align == 'center':
        xpos = (xmin + xmax) / 2
    elif align == 'right':
        xpos = xmax
    else:
        msg = ("Alignment should have been one of "
                + f"['left', 'center', 'right'], but was {align}!")
        raise ValueError(msg)

    if TextBelow:
        ypos = ymin - yoffset * ymax
    else:
        ypos = ymax + yoffset * ymax
    label = ax.text(xpos, ypos, text, **kwargs)

    # complicated construct to adjust axis limits to include the new text
    plt.gcf().tight_layout()
    plt.draw()
    bbox = label.get_window_extent(plt.gcf().canvas.get_renderer())
    bbox_data = bbox.transformed(ax.transData.inverted())
    ax.update_datalim(bbox_data.corners())
    ax.autoscale_view()


def draw_bbox(ax, x, y, xbuffer=0.01, ybuffer=0.05, **kwargs):
    """Draw a bounding box around a set of points"""
    if x.shape[0] == 1:
        return
    xmin, xmax = np.min(x), np.max(x)
    ymin, ymax = np.min(y), np.max(y)
    width = xmax - xmin
    height = ymax - ymin
    xleft = xbuffer
    ybottom = ybuffer

    xright = xleft
    if ax.get_xscale() == 'log':
        xleft = xbuffer * xmin
        # let x1 := xleft - eps1, x2 := xright + eps2
        # linear scaling: eps1 == eps2 (we want xleft - x1 == x2 - xright)
        # log scaling: log(x2) - log(x) == log(x) - log(x1)
        #   ... leads to: eps2 == x2*eps1 / (x1 - eps1)
        xright = xmax * xleft / (xmin - xleft)

    ytop = ybottom
    if ax.get_yscale() == 'log':
        ybottom = ybuffer * ymin
        ytop = ymax * ybottom / (ymin - ybottom)

    rect = mpl.patches.Rectangle((xmin - xleft, ymin - ybottom),
                                 width + (xleft + xright), height + (ybottom + ytop), **kwargs)
    ax.add_patch(rect)  # Add the patch to the Axes
