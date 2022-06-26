#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 12:31:22 2022

@author: joachim
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from figsize import set_figsize

__all__ = ['setup']
COLORS = ['blue', (1, 0.5, 0), 'green', 'darkred', 'cyan', 'orangered', 'purple', 'lime']


def setup(UseTex=True, figsize=None, colors=None):
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
