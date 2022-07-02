#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools for formatting ticklabels, labels and captions
"""

import numpy as np
import matplotlib.pyplot as plt


__all__ = ['AlphabeticalLabels',
           'set_ticks_linear', 'ticks_in_limits', 'ticklabels_in_limits',
           'embed_xlabel', 'embed_ylabel', 'embed_labels', 'polish',
           'multiple_formatter', 'format_ticklabels', 'si_string']


class AlphabeticalLabels():
    """Simple cycle for labels.
    By default the cycle contains the letters 'a' through 'l'.
    """
    def __init__(self, abc_labels=None, ctr=0):
        if abc_labels is None:
            self.abc_labels = [r"(a)", r"(b)", r"(c)", r"(d)",
                               r"(e)", r"(f)", r"(g)", r"(h)",
                               r"(i)", r"(j)", r"(k)", r"(l)", ]
        else:
            self.abc_labels = abc_labels
        self.ctr = ctr
        self.length = len(self.abc_labels)

    def get_label(self):
        """Return the next label in the cycle"""
        next_label = self.abc_labels[self.ctr % self.length]
        self.ctr += 1
        return next_label


def set_ticks_linear(axis, vmin, vmax, numticks, decimals=7, which='x'):
    """
    Puts 'numticks' linearly spaced ticks from 'vmin' to 'vmax' along the
        'axis' of the subplot 'ax'.
    Values are rounded to the specified 'decimals'.
    """
    ticks = np.round(np.linspace(vmin, vmax, numticks), decimals)
    getattr(axis, f"set_{which}ticks")(ticks)
    getattr(axis, f"set_{which}ticklabels")(ticks)


def ticks_in_limits(axis, which='x'):
    """Return the indices of ticks within the limits of a given axis"""
    lim = getattr(axis, f"get_{which}lim")()
    ticks = getattr(axis, f"get_{which}ticks")()
    return (lim[0] <= ticks) & (ticks <= lim[1])


def ticklabels_in_limits(ticklabels, limits, which='x'):
    """Subroutine for 'embed_labels'. Returns subset of ticks inside limits"""
    new_ticklabels = []
    for ticklabel in ticklabels:
        tick_we = ticklabel.get_window_extent()
        if which == 'x':
            TickInAxis = ((tick_we.x1 > limits[0]) and (tick_we.x0 < limits[1]))
        elif which == 'y':
            TickInAxis = limits[1] > (tick_we.y1 + tick_we.y0) / 2 > limits[0]
        else:
            msg = f"Wrong parameter '{which=}', should be 'x' or 'y'."
            raise AttributeError(msg)

        if TickInAxis:
            new_ticklabels.append(ticklabel)

    return new_ticklabels


def _get_largest_ticklabel(ticklabels, which='x'):
    """Return the ticklabel with the largest size along the given axis."""
    return max(ticklabels,
               key=lambda tick: (getattr(tick.get_window_extent(), f"{which}1")
                                 - getattr(tick.get_window_extent(), f"{which}0"))
               )


def _points_to_pixels(points):
    """Convert points to pixels (see mpl: backends/backend_agg.py)"""
    return points * plt.rcParams["figure.dpi"] / 72


def __assert_existing_renderer(axis):
    """Check if 'fig.canvas.draw()' or similar were already called
    Otherwise there may not exist a renderer for the window extents, leading to
    a RuntimeError in the label embedding routines or similar.
    """
    if axis.get_renderer_cache() is None:
        plt.gcf().canvas.draw()


def _embed_label(axis, which='x'):
    """Subroutine:
    Returns the ticklabels within the limits of the given axis as well as a
    list containing [axis_x0, axis_y0, axis_width, axis_height]
    """
    __assert_existing_renderer(axis)
    ax0 = axis.get_window_extent().x0
    ay0 = axis.get_window_extent().y0
    ax1 = axis.get_window_extent().x1
    ay1 = axis.get_window_extent().y1
    width = ax1 - ax0
    height = ay1 - ay0

    indx = ticks_in_limits(axis, which=which)
    ticklabels = np.array(getattr(axis, f"get_{which}ticklabels")())
    if len(ticklabels) == len(indx):
        ticklabels = ticklabels[indx]
        
    if len(ticklabels) < 2:
        if getattr(axis, f"get_{which}label")():    # if we had a label --> actual error
            raise IndexError("Length of ticklabels below 2, can not embed label!")

    return ticklabels, [ax0, ay0, width, height]


def embed_xlabel(axis, align='top', caption=None):
    """Embed the xlabel of the given axis into the ticklabels.
    Alignment can be ::
        'top' -> midpoint of ticklabel height
        'center' -> lower edge of ticklabels
        'bottom' -> lower edge minus half the label height
    """
    ticklabels, [ax0, ay0, width, height] = _embed_label(axis, which='x')
    if len(ticklabels) < 2:     # no tick labels, and no label --> skip this (sub)plot
        return

    last_tick_we = ticklabels[-1].get_window_extent()
    xpos = (last_tick_we.x0 + ticklabels[-2].get_window_extent().x1) / 2

    max_tick_we = _get_largest_ticklabel(ticklabels, which='y').get_window_extent()

    # instead of 'max_tick_we.y1' we use the 'ay0 - major_padding' here
    tick_height = ay0 - _points_to_pixels(plt.rcParams["xtick.major.pad"]) - max_tick_we.y0

    if align == 'bottom':
        ypos = max_tick_we.y0 - tick_height / 2
    elif align == 'center':
        ypos = max_tick_we.y0
    elif align == 'top':
        ypos = max_tick_we.y0 + tick_height / 2
    else:
        msg = ("Vertical x-alignment should have been one of "
                + f"['top', 'center', 'bottom'], but was {align}!")
        raise ValueError(msg)

    # shift and transform to relative units
    xpos = (xpos - ax0) / width
    ypos = (ypos - ay0) / height
    label = axis.get_xlabel()
    axis.set_xlabel(label, rotation=0, va='center', ha='center')
    axis.xaxis.set_label_coords(xpos, ypos)

    if caption is not None:
        ypos = (max_tick_we.y0 - tick_height - ay0) / height
        axis.text(0.5, ypos, caption, va='center', ha='center',
                  transform=axis.transAxes)


def embed_ylabel(axis, align='right'):
    """Embed the ylabel of the given axis into the ticklabels.
    Alignment can be ::
        'right' -> midpoint of ticklabel width
        'center' -> left edge of ticklabels
        'left' -> left edge minus half the label width
    """
    ticklabels, [ax0, ay0, width, height] = _embed_label(axis, which='y')
    if len(ticklabels) < 2:     # no tick labels, and no label --> skip this (sub)plot
        return

    last_tick_we = ticklabels[-1].get_window_extent()
    ypos = (last_tick_we.y0 + ticklabels[-2].get_window_extent().y1) / 2
    tick_width = last_tick_we.x1 - last_tick_we.x0

    if align == 'left':
        xpos = last_tick_we.x0 - tick_width / 2
    elif align == 'center':
        xpos = last_tick_we.x0
    elif align == 'right':
        xpos = last_tick_we.x0 + tick_width / 2
    else:
        msg = ("Horizontal y-alignment should have been one of "
                + f"['left', 'center', 'right'], but was {align}!")
        raise ValueError(msg)

    # shift and transform to relative units
    xpos = (xpos - ax0) / width
    ypos = (ypos - ay0) / height
    label = axis.get_ylabel()
    axis.set_ylabel(label, rotation=0, ha='center', va='center')
    axis.yaxis.set_label_coords(xpos, ypos)

    # ensure that the y-label has a minimal padding to the y-axis
    min_padding = _points_to_pixels(plt.rcParams["ytick.major.pad"])
    if xpos < 0.5:           # y-label on left axis
        if axis.yaxis.get_label().get_window_extent().x1 + min_padding > ax0:
            axis.set_ylabel(label, rotation=0, ha='right', va='center')
            axis.yaxis.set_label_coords(-min_padding / width, ypos)

    elif xpos > 0.5:         # y-label on right axis
        if axis.yaxis.get_label().get_window_extent().x0 - min_padding < (ax0 + width):
            axis.set_ylabel(label, rotation=0, ha='left', va='center')
            axis.yaxis.set_label_coords(1 + min_padding / width, ypos)


def embed_labels(axes, set_captions=False,
                 embed_xlabels=True, embed_ylabels=True, xva=None, yha=None):
    """
    axes == single axis or list of axes on which to embed the labels

    set_captions == refers to enumerating the given 'axes' with (a), (b), ...

    xva == x-vertical alignment array with values 'top', 'center' or 'bottom'
        refers to the vertical alignment of the xlabel relative to the ticks

    yha == y-vertical alignment array with values 'right', 'center' or 'left'
        refers to the vertical alignment of the ylabel relative to the ticks
    """
    axes = np.array([axes])
    if axes.ndim > 1:
        axes = axes.flatten()
    length = axes.size

    if xva is None:
        xva = np.array(['top'] * length, dtype=str)
    else:
        xva = np.array([xva], dtype=str)
        if xva.shape[0] == 1:
            xva = np.full(length, xva)
    assert xva.shape[0] == length

    if yha is None:
        yha = np.array(['right'] * length, dtype=str)
    else:
        yha = np.array([yha], dtype=str)
        if yha.shape[0] == 1:
            yha = np.full(length, yha)
    assert yha.shape[0] == length

    if isinstance(set_captions, bool):
        set_captions = [set_captions] * length
    else:
        assert len(set_captions) == length

    if isinstance(embed_xlabels, bool):
        embed_xlabels = [embed_xlabels] * length
    else:
        assert len(embed_xlabels) == length

    if isinstance(embed_ylabels, bool):
        embed_ylabels = [embed_ylabels] * length
    else:
        assert len(embed_ylabels) == length

    captions = AlphabeticalLabels()
    for i, axis in enumerate(axes):
        if set_captions[i]:
            caption = captions.get_label()
        else:
            caption = None

        embed_xlabel(axis, xva[i], caption)
        embed_ylabel(axis, yha[i])


def polish(fig, axes, set_captions=False,
           embed_xlabels=True, embed_ylabels=True, xva=None, yha=None):
    """
    fig == the figure containing the relevant axes

    axes == single axis or list of axes on which to embed the labels

    xva == x-vertical alignment array with values 'top', 'center' or 'bottom'
        refers to the vertical alignment of the xlabel relative to the ticks

    yha == y-vertical alignment array with values 'right', 'center' or 'left'
        refers to the vertical alignment of the ylabel relative to the ticks
    """
    fig.canvas.draw()
    fig.tight_layout()
    fig.canvas.draw()
    embed_labels(axes, set_captions=set_captions,
                 embed_xlabels=embed_xlabels, embed_ylabels=embed_ylabels,
                 xva=xva, yha=yha)
    fig.canvas.draw()
    fig.tight_layout()
    plt.show()


###############################################################################
# Provides tools for easier ticklabel manipulation
###############################################################################


def multiple_formatter(denominator=2, number=np.pi, latex=r'\pi'):
    """
    den = 2
    ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / den))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / (6 * den)))
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(multiple_formatter(denominator=den)))
    https://stackoverflow.com/questions/40642061/how-to-set-axis-ticks-in
    -multiples-of-pi-python-matplotlib
    """
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _multiple_formatter(x, _):
        den = denominator
        num = int(np.rint(den * x / number))
        com = gcd(num,den)
        (num, den) = (int(num / com), int(den / com))
        if den==1:
            if num == 0:
                string = r'$0$'
            elif num == 1:
                string = r'$%s$'%latex
            elif num == -1:
                string = r'$-%s$'%latex
            else:
                string = r'$%s%s$'%(num, latex)
        else:
            if num == 1:
                string = r'$\frac{%s}{%s}$'%(latex, den)
            elif num == -1:
                string = r'$-\frac{%s}{%s}$'%(latex, den)
            else:
                if num > 0:
                    string = r'$\frac{%s%s}{%s}$'%(num, latex, den)
                else:
                    string = r'$-\frac{%s%s}{%s}$'%(abs(num), latex, den)
        return string

    return _multiple_formatter


def format_ticklabels(axis, which='x', major_den=2, minor_den=0,
                      number=np.pi, latex=r'\pi'):
    """Format the ticklabels on the axis 'axis' of the (sub)plot 'ax'. """
    if which in ['x', 'xaxis']:
        which = 'xaxis'
    if which in ['y', 'yaxis']:
        which = 'yaxis'

    subaxis = getattr(axis, which)
    subaxis.set_major_locator(plt.MultipleLocator(number / major_den))
    if minor_den > 0:
        subaxis.set_minor_locator(plt.MultipleLocator(number / minor_den))

    formatter = multiple_formatter(denominator=major_den,
                                   number=number, latex=latex)
    subaxis.set_major_formatter(plt.FuncFormatter(formatter))


def si_string(value, unit=r"ms", digits=3):
    r"""Returns the string generated by siunitx's command \SI{value}{unit}.
    The result is rounded to the specified number of digits.
    """
    if not plt.rcParams["text.usetex"]:
        print(r"Warning si_string: \SI only possible in Latex-mode!")
        return fr"${value:.{digits}e}\,$" + unit
    return fr"\SI{{{value:.{digits}e}}}{{{unit}}}"
