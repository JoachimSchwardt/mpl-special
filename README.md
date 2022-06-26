# mpl-special
Special plotting tools using matplotlib

# setup
- add the path to the folder containing the files to your $PYTHONPATH

# how-to
You can import the files like any other python library.
The intended use is
```python
import mpl_special


# example: simple figure with embedded labels and ticks formatted as multiples of pi
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 300)
fig, ax = plt.subplots()
ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$x(t)$")
ax.plot(t, np.sin(t) + 0.1*t, label='data')
ax.legend()
mpl_special.format_ticklabels(ax, which='x')
mpl_special.polish(fig, ax, set_captions=True)


# example: explicit call to 'setup' if you do not want latex fonts
mpl_special.setup(UseTex=False)
```

# list of features
- function to generate the correct figure size for including figures in latex documents without further rescaling
- embed x and y labels into the ticks
- enumerate subplots with captions (a, b, ... )
- plot standalone colorbars for a given heatmap
- annotate point clouds
