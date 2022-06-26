# -*- coding: utf-8 -*-
"""
Special tools for easier use of matplotlib
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from figsize import set_figsize


COLORS = ['blue', (1, 0.5, 0), 'green', 'darkred', 'cyan', 'orangered', 'purple', 'lime']


def setup(UseTex=False, figsize=None, colors=None):
    """Sets special matplotlib parameters and calls the personal style-sheet.
    Modify the style-sheet for general purpose parameters
    """
    path = os.path.realpath(__file__)
    path = path.replace(os.path.basename(path), "mpl-style-sheet.mplstyle")
    mpl.style.use(path)

    if figsize is None:
        figsize = set_figsize()
    elif isinstance(figsize, (float, int)):
        figsize = set_figsize(figsize)

    plt.rcParams["figure.figsize"] = figsize
    plt.rcParams["legend.edgecolor"] = plt.rcParams["axes.facecolor"]

    if colors is None:
        colors = COLORS
    plt.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)

    # if 'False', we want to go back to normal fonts --> not inside 'if' !
    plt.rcParams["text.usetex"] = UseTex
    if UseTex:
        plt.rcParams["font.family"] = 'serif'   # 'lmodern'
        plt.rcParams["font.serif"] = 'Computer Modern'
        plt.rcParams["text.latex.preamble"] = r'\usepackage{siunitx}'


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


###############################################################################
# Routines for embedding the axis-labels into the axis-ticks
###############################################################################


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


def set_ticks_linear(ax, vmin, vmax, numticks, decimals=7, axis='x'):
    """
    Puts 'numticks' linearly spaced ticks from 'vmin' to 'vmax' along the
        'axis' of the subplot 'ax'.
    Values are rounded to the specified 'decimals'.
    """
    ticks = np.round(np.linspace(vmin, vmax, numticks), decimals)
    getattr(ax, f"set_{axis}ticks")(ticks)
    getattr(ax, f"set_{axis}ticklabels")(ticks)
    
    
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


def _embed_label(axis, which='x'):
    """Subroutine:
    Returns the ticklabels within the limits of the given axis as well as a
    list containing [axis_x0, axis_y0, axis_width, axis_height]
    """
    ax0 = axis.get_window_extent().x0
    ay0 = axis.get_window_extent().y0
    ax1 = axis.get_window_extent().x1
    ay1 = axis.get_window_extent().y1
    width = ax1 - ax0
    height = ay1 - ay0

    indx = ticks_in_limits(axis, which=which)
    ticklabels = np.array(getattr(axis, f"get_{which}ticklabels")())[indx]
    if len(ticklabels) <= 1:
        raise IndexError("Length of ticklabels below 2!")
        
    return ticklabels, [ax0, ay0, width, height]


def embed_xlabel(axis, align='top', caption=None):
    """Embed the xlabel of the given axis into the ticklabels.
    Alignment can be ::
        'top' -> midpoint of ticklabel height
        'center' -> lower edge of ticklabels
        'bottom' -> lower edge minus half the label height
    """
    ticklabels, [ax0, ay0, width, height] = _embed_label(axis, which='x')

    last_tick_we = ticklabels[-1].get_window_extent()
    xpos = (last_tick_we.x0 + ticklabels[-2].get_window_extent().x1) / 2
    # ypos = (last_tick_we.y0 + last_tick_we.y1) / 2
    tick_height = last_tick_we.y1 - last_tick_we.y0

    if align == 'bottom':
        ypos = last_tick_we.y0 - tick_height / 2
    elif align == 'center':
        ypos = last_tick_we.y0
    elif align == 'top':
        ypos = last_tick_we.y0 + tick_height / 2
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
        ypos = (last_tick_we.y0 - tick_height - ay0) / height
        axis.text(0.5, ypos, caption, ha='center', va='center',
                  transform=axis.transAxes)


def embed_ylabel(axis, align='right'):
    """Embed the ylabel of the given axis into the ticklabels.
    Alignment can be ::
        'right' -> midpoint of ticklabel width
        'center' -> left edge of ticklabels
        'left' -> left edge minus half the label width
    """
    ticklabels, [ax0, ay0, width, height] = _embed_label(axis, which='y')

    last_tick_we = ticklabels[-1].get_window_extent()
    ypos = (last_tick_we.y0 + ticklabels[-2].get_window_extent().y1) / 2
    # xpos = (last_tick_we.x1 + last_tick_we.x0) / 2
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
    if xpos < 0.5:           # y-label on left axis
        min_padding = last_tick_we.x1 - ax0
        if axis.yaxis.get_label().get_window_extent().x1 + min_padding > ax0:
            axis.set_ylabel(label, rotation=0, ha='right', va='center')
            axis.yaxis.set_label_coords(min_padding / width, ypos)

    elif xpos > 0.5:         # y-label on right axis
        min_padding = last_tick_we.x0 - (ax0 + width)
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
    embed_labels(axes, set_captions=set_captions,
                  embed_xlabels=embed_xlabels, embed_ylabels=embed_ylabels,
                  xva=xva, yha=yha)
    fig.canvas.draw()
    fig.tight_layout()
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


def format_ticklabels(ax, axis='x', major_den=2, minor_den=0,
                      number=np.pi, latex=r'\pi'):
    """Format the ticklabels on the axis 'axis' of the (sub)plot 'ax'. """
    if axis in ['x', 'xaxis']:
        axis = 'xaxis'
    if axis in ['y', 'yaxis']:
        axis = 'yaxis'

    subaxis = getattr(ax, axis)
    subaxis.set_major_locator(plt.MultipleLocator(number / major_den))
    if minor_den > 0:
        subaxis.set_minor_locator(plt.MultipleLocator(number / minor_den))

    formatter = multiple_formatter(denominator=major_den,
                                   number=number, latex=latex)
    subaxis.set_major_formatter(plt.FuncFormatter(formatter))



###############################################################################
# Variants of the standard 'plot' routine
###############################################################################


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


def si_string(value, unit=r"ms", digits=3):
    r"""Returns the string generated by siunitx's command \SI{value}{unit}.
    The result is rounded to the specified number of digits.
    """
    if not plt.rcParams["text.usetex"]:
        print(r"Warning special/si_string: \SI only possible in Latex-mode!")
        return fr"${value:.{digits}e}\,$" + unit
    return fr"\SI{{{value:.{digits}e}}}{{{unit}}}"


def main():
    print(__doc__)

    setup(UseTex=True)
    t = np.linspace(-0.05, 1.05, 200)
    # colors = Colors()
    fig, ax = plt.subplots(2, 2)
    for axis in ax.flat:
        axis.set_xlabel("x")
        axis.set_ylabel("y")
        # axis.plot(t, np.sin(2*np.pi*t), c=colors.get_color())
        axis.plot(t, np.sin(2*np.pi*t))
    ax[1, 1].plot(t, np.cos(2*np.pi*t))


    # or use "\u00B5" for a text-mu within normal strings
    ax[0, 1].set_title(r"$\SI{}{\micro s}\si{\micro}$")
    # ax[0, 0].set_title(fr"$\SI{{{t[5]:.2f}}}{{\micro s}}\si{{\micro}}$")
    ax[0, 0].set_title(si_string(t[5], unit=r"\micro s", digits=2))
    ax[0, 1].set_xlim(-0.03, 0.9*np.pi)
    format_ticklabels(ax[0, 1], major_den=6, minor_den=24)
    ax[0, 0].axis([-0.15, 1.15, -1.78, 1.87])
    ax[1, 1].axis([0.05, 0.95, -0.95, 0.95])
    plt.subplots_adjust(left=0.07, right=0.88, top=0.98, bottom=0.08)
    polish(fig, ax, xva=['top', 'center', 'center', 'bottom'],
           yha=['left', 'center', 'center', 'right'])
    return 0

if __name__ == "__main__":
    main()
