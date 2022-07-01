#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the minimal label padding and label alignment functionality
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_special


def main():
    """Test of minimal padding after embedding"""
    print(__doc__)
    fig, ax = plt.subplots()
    x = np.linspace(0.1, 12.1, 300)
    y = np.sin(x)
    
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y=y_1$")
    ax2 = ax.twinx()
    ax2.set_ylabel(r"$y=y_2$")
    
    ax.plot(x, y)
    mpl_special.format_ticklabels(ax)
    mpl_special.polish(fig, ax)
    mpl_special.embed_ylabel(ax2, align="left")
    return 0  
    
if __name__ == "__main__":
    main()
