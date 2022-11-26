#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Simple tool for creating a figsize compatible with latex documents.
Put the command
    \showthe\textwidth
in your latex document and read out the log file to find the correct width (in pt).
Calling 'set_figsize()' with that width will generate a figure size, that allows
including plots in your latex documents without any rescaling.

This file also provides defualt values for common document types
"""
WIDTH_PT_SCR = 418.25555          # default linewidth of a scr-document in pt
WIDTH_PT_BMR = 302.0              # default linewidth of a beamer-document in pt

__all__ = ['set_figsize']

def set_figsize(width=None, fraction=1, subplots=(1, 1)):
    """
    Copied from: https://jwalton.info/Embed-Publication-Matplotlib-Latex/

    Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # put \showthe\textwidth in your latex document to find the correct width
    if width in ['thesis', None]:
        width_pt = WIDTH_PT_SCR
    elif width == 'beamer':
        width_pt = WIDTH_PT_BMR
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)

