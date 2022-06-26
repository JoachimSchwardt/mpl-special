#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of some simple functionality of the label embedding
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_special


def main():
    print(__doc__)
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
    ax[0, 0].set_title(mpl_special.si_string(t[5], unit=r"\micro s", digits=2))
    ax[0, 1].set_xlim(-0.03, 0.9*np.pi)
    mpl_special.format_ticklabels(ax[0, 1], major_den=6, minor_den=24)
    ax[0, 0].axis([-0.15, 1.15, -1.78, 1.87])
    ax[1, 1].axis([0.05, 0.95, -0.95, 0.95])
    plt.subplots_adjust(left=0.07, right=0.88, top=0.98, bottom=0.08)
    mpl_special.polish(fig, ax, xva=['top', 'center', 'center', 'bottom'],
                       yha=['left', 'center', 'center', 'right'])
    return 0


if __name__ == "__main__":
    main()
